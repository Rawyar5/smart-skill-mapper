import streamlit as st
import pandas as pd

# === Tiny sample datasets ===
courses = pd.DataFrame([
    {"course_name": "Python for Beginners", 
     "skills": "python, programming, basics",
     "link": "https://www.coursera.org/learn/python"},
    {"course_name": "Intro to Digital Marketing",
     "skills": "marketing, social media",
     "link": "https://www.coursera.org/learn/digital-marketing"},
    {"course_name": "Excel Basics",
     "skills": "excel, spreadsheets, data",
     "link": "https://www.udemy.com/course/excel-for-beginners/"},
    {"course_name": "HTML & CSS Fundamentals",
     "skills": "html, css, web",
     "link": "https://www.codecademy.com/learn/learn-html"}
])

jobs = pd.DataFrame([
    {"job_title": "Junior Web Developer",
     "skills": "html, css, javascript",
     "link": "https://www.naukri.com"},
    {"job_title": "Data Entry Clerk",
     "skills": "excel, typing",
     "link": "https://www.naukri.com"},
    {"job_title": "Marketing Assistant",
     "skills": "marketing, social media",
     "link": "https://www.naukri.com"},
    {"job_title": "Python Intern",
     "skills": "python, programming",
     "link": "https://www.naukri.com"}
])

# === Utility functions ===
def extract_user_skills(user_input, all_skills):
    return [skill for skill in all_skills if skill.lower() in user_input.lower()]

def score_item(user_skills, item_skills_str):
    item_skills = [s.strip() for s in item_skills_str.split(',')]
    return len(set(user_skills) & set(item_skills))

# === Streamlit UI ===
st.title("Smart Job–Skill Mapper")

user_input = st.text_area("Enter your skills, hobbies, or marks:", 
                          "I know python, excel and social media marketing")

if st.button("Find Matches"):
    # Build combined skill list
    all_skills = set()
    for s in courses['skills']:
        all_skills.update([skill.strip() for skill in s.split(',')])
    for s in jobs['skills']:
        all_skills.update([skill.strip() for skill in s.split(',')])

    user_skills = extract_user_skills(user_input, all_skills)

    st.subheader("Detected Skills")
    st.write(user_skills)

    # Score courses
    courses['match_score'] = courses['skills'].apply(lambda s: score_item(user_skills, s))
    recommended_courses = courses.sort_values(by='match_score', ascending=False)

    # Score jobs
    jobs['match_score'] = jobs['skills'].apply(lambda s: score_item(user_skills, s))
    recommended_jobs = jobs.sort_values(by='match_score', ascending=False)

    st.subheader("Recommended Courses")
    for _, row in recommended_courses.iterrows():
        if row['match_score'] > 0:
            st.markdown(f"- [{row['course_name']}]({row['link']}) (score: {row['match_score']})")

    st.subheader("Recommended Jobs")
    for _, row in recommended_jobs.iterrows():
        if row['match_score'] > 0:
            st.markdown(f"- [{row['job_title']}]({row['link']}) (score: {row['match_score']})")
