import streamlit as st
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("output/ranked_candidates.csv")

# Convert score to percentage
max_score = df["score"].max()

df["score_percent"] = (
    df["score"] / max_score * 100
).round(1)

# ---------------------------
# STATUS FUNCTION
# ---------------------------
def get_status(score):

    if score >= 80:
        return "🟢 Excellent Match"

    elif score >= 60:
        return "🟡 Good Match"

    else:
        return "🔴 Low Match"

df["status"] = df["score_percent"].apply(get_status)

# Ranking
df = df.sort_values(
    "score_percent",
    ascending=False
)

df["Rank"] = range(1, len(df) + 1)

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.title("⚙️ Controls")

job_description = st.sidebar.text_area(
    "Paste Job Description",
    height=200
)

candidate_id = st.sidebar.selectbox(
    "Select Candidate",
    df.index
)

candidate = df.loc[candidate_id]

# ---------------------------
# HEADER
# ---------------------------
st.title("📄 AI Resume Screening Dashboard")

st.markdown("---")

# ---------------------------
# METRICS
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Resumes",
        len(df)
    )

with col2:
    st.metric(
        "Highest Match",
        f"{df['score_percent'].max()}%"
    )

with col3:
    st.metric(
        "Average Match",
        f"{round(df['score_percent'].mean(),1)}%"
    )

st.markdown("---")

# ---------------------------
# CANDIDATE REPORT
# ---------------------------
st.header("🎯 Candidate Report")

st.success(
    f"Match Score: {candidate['score_percent']}%"
)

st.info(
    f"Status: {candidate['status']}"
)

st.progress(
    int(candidate['score_percent'])
)

# ---------------------------
# HIRING RECOMMENDATION
# ---------------------------
if candidate['score_percent'] >= 80:
    recommendation = "✅ Shortlist for Interview"

elif candidate['score_percent'] >= 60:
    recommendation = "⚠️ Consider Candidate"

else:
    recommendation = "❌ Not Recommended"

st.subheader("📌 Hiring Recommendation")
st.success(recommendation)

# ---------------------------
# SKILLS SECTION
# ---------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("✅ Skills Found")

    skills = candidate['skills']

    if isinstance(skills, str):
        skills = eval(skills)

    for skill in skills:
        st.write(f"✔ {skill}")

with col2:

    st.subheader("❌ Missing Skills")

    missing = candidate['missing_skills']

    if isinstance(missing, str):
        missing = eval(missing)

    for skill in missing:
        st.write(f"❌ {skill}")

# ---------------------------
# EVALUATION BUTTON
# ---------------------------
if st.button("Evaluate Candidate"):

    st.success("Evaluation Completed Successfully ✅")

    st.write(
        f"Candidate Match Score: {candidate['score_percent']}%"
    )

# ---------------------------
# TOP CANDIDATES
# ---------------------------
st.markdown("---")

st.subheader("🏆 Top Ranked Candidates")

st.dataframe(
    df[
        [
            "Rank",
            "score_percent",
            "status"
        ]
    ],
    use_container_width=True
)

# ---------------------------
# CHART
# ---------------------------
st.markdown("---")

st.subheader("📊 Candidate Comparison")

chart_df = df.head(10)

st.bar_chart(
    chart_df.set_index("Rank")["score_percent"]
)