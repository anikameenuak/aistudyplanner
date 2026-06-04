import pandas as pd
import numpy as np
import random

# Number of rows
n = 10000

subjects = [
    "Math", "Physics", "Chemistry", "Biology", "English",
    "History", "Geography", "Computer Science", "Economics",
    "Statistics", "Programming", "AI", "Machine Learning"
]

study_types = ["Theory", "Conceptual", "Practical"]

data = []

for _ in range(n):
    subject = random.choice(subjects)
    
    difficulty = random.randint(1, 5)
    hours_available = random.randint(1, 8)
    deadline_days = random.randint(1, 15)
    importance = random.randint(1, 5)
    study_type = random.choice(study_types)
    previous_score = random.randint(40, 95)

    # Logic to generate realistic target
    base = (difficulty * importance) / max(deadline_days, 1)
    
    score_factor = (100 - previous_score) / 50  # lower score → more hours
    
    type_factor = {
        "Theory": 0.8,
        "Conceptual": 1.2,
        "Practical": 1.5
    }[study_type]

    actual_hours_needed = round(
        (base * 2 + score_factor * 2) * type_factor,
        2
    )

    data.append([
        subject, difficulty, hours_available,
        deadline_days, importance, study_type,
        previous_score, actual_hours_needed
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "subject",
    "difficulty",
    "hours_available",
    "deadline_days",
    "importance",
    "study_type",
    "previous_score",
    "actual_hours_needed"
])

# Save CSV
df.to_csv("study_planner_10k.csv", index=False)

print("✅ Dataset generated: study_planner_10k.csv")