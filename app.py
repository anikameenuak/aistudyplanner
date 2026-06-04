import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="AI Study Planner", layout="wide")

# 🎨 Custom Background + Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #667eea, #764ba2);
        color: white;
    }
    h1, h2, h3 {
        color: #ffffff;
        text-align: center;
    }
    .stButton>button {
        background-color: #ff7eb3;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 AI Study Planner ")

st.write("Plan smarter. Study better. 🚀")

# 🔢 Allow up to 15 subjects
num_subjects = st.slider("Select Number of Subjects", 1, 15)

subjects_data = []

st.subheader("📥 Enter Subject Details")

for i in range(num_subjects):
    with st.expander(f"Subject {i+1} Details"):
        col1, col2 = st.columns(2)

        with col1:
            subject = st.text_input(f"Subject Name {i}", key=f"name{i}")
            difficulty = st.slider(f"Difficulty {i}", 1, 5, key=f"diff{i}")
            importance = st.slider(f"Importance {i}", 1, 5, key=f"imp{i}")

        with col2:
            hours_available = st.number_input(f"Hours Available {i}", 1.0, 12.0, step=0.25, key=f"hrs{i}")
            deadline_days = st.number_input(f"Deadline Days {i}", 1, 30, key=f"dead{i}")
            previous_score = st.slider(f"Previous Score {i}", 0, 100, key=f"score{i}")

        study_type = st.selectbox(
            f"Study Type {i}",
            ["Theory", "Conceptual", "Practical"],
            key=f"type{i}"
        )

        subjects_data.append({
            "subject": subject,
            "difficulty": difficulty,
            "hours_available": hours_available,
            "deadline_days": deadline_days,
            "importance": importance,
            "study_type": study_type,
            "previous_score": previous_score
        })

# Encode
def encode_type(val):
    return {"Theory":1, "Conceptual":2, "Practical":3}[val]

if st.button("🚀 Generate Smart Study Plan"):

    results = []
    total_priority = 0

    for sub in subjects_data:
        study_type_val = encode_type(sub["study_type"])
        priority_score = (sub["difficulty"] * sub["importance"]) / sub["deadline_days"]

        data = pd.DataFrame([[sub["difficulty"], sub["hours_available"],
                              sub["deadline_days"], sub["importance"],
                              study_type_val, sub["previous_score"], priority_score]],
                            columns=['difficulty','hours_available','deadline_days',
                                     'importance','study_type','previous_score','priority_score'])

        predicted_hours = float(model.predict(data)[0])

        results.append({
            "subject": sub["subject"],
            "hours": round(predicted_hours, 2),
            "priority": priority_score,
            "deadline": sub["deadline_days"]
        })

        total_priority += priority_score

    st.subheader("📊 AI Time Allocation")

    for res in results:
        res["allocated_time"] = round((res["priority"] / total_priority) * 10, 2)

    df = pd.DataFrame(results)

    st.dataframe(df.style.highlight_max(axis=0))

    # 📈 Chart
    st.subheader("📈 Study Time Distribution")
    st.bar_chart(df.set_index("subject")["allocated_time"])

    # 📅 Daily Plan
    st.subheader("📅 Daily Study Plan")

    max_days = int(max(df["deadline"]))

    for day in range(1, max_days + 1):
        st.markdown(f"### Day {day}")
        for _, row in df.iterrows():
            if day <= row["deadline"]:
                st.write(f"📘 {row['subject']} → {row['allocated_time']:.2f} hrs")

    # 🧠 Suggestions
    st.subheader("🧠 AI Suggestions")

    for sub in subjects_data:
        if sub["previous_score"] < 60:
            st.warning(f"{sub['subject']}: Improve basics")

        if sub["difficulty"] >= 4:
            st.info(f"{sub['subject']}: Break into smaller topics")

        if sub["deadline_days"] < 3:
            st.error(f"{sub['subject']}: High urgency!")

    # 💾 Save history
    df.to_csv("study_history.csv", mode='a', header=False, index=False)

    st.success("✅ Plan generated successfully!")