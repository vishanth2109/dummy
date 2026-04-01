import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from analyzer import calculate_similarity, analyze_resume, get_skill_gap
from resume_utils import extract_text_from_pdf
from report_generator import generate_pdf
from auth import create_users_table, register_user, login_user

create_users_table()

st.set_page_config(page_title="AI Resume Analyzer")

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- LOGIN / REGISTER PAGE ----------
if not st.session_state.logged_in:

    st.title("🔐 AI Resume Analyzer Login")

    menu = ["Login", "Register"]
    choice = st.selectbox("Select Option", menu)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    else:
        if st.button("Register"):
            if register_user(username, password):
                st.success("Account Created Successfully")
            else:
                st.error("Username already exists")

# ---------- MAIN APP (ONLY IF LOGGED IN) ----------
else:

    st.sidebar.success(f"Welcome {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🚀 AI Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_desc = st.text_area("Paste Job Description")
    analyze = st.button("Analyze Resume")

    if analyze:

        if uploaded_file is None or job_desc.strip() == "":
            st.error("Upload resume and paste job description.")
        else:

            resume_text = extract_text_from_pdf(uploaded_file)

            # ATS Score
            score = calculate_similarity(resume_text, job_desc)
            st.subheader("📊 ATS Score")
            st.progress(int(score))
            st.write(f"Score: {score}%")

            # AI Analysis
            with st.spinner("Analyzing with AI..."):
                ai_result = analyze_resume(resume_text, job_desc)

            st.subheader("🧠 AI Analysis")
            st.write(ai_result)

            # Radar Chart
            st.subheader("🕸 Radar Skill Analysis")

            job_skills, resume_skills, missing_skills = get_skill_gap(resume_text, job_desc)

            if len(job_skills) > 0:

                labels = job_skills.copy()
                values = [1 if skill in resume_skills else 0 for skill in labels]

                labels.append(labels[0])
                values.append(values[0])

                angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=True)

                fig = plt.figure()
                ax = fig.add_subplot(111, polar=True)
                ax.plot(angles, values)
                ax.fill(angles, values, alpha=0.25)

                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(job_skills)

                ax.set_yticks([0, 1])
                ax.set_yticklabels(["Missing", "Matched"])

                st.pyplot(fig)

            # PDF Download
            st.subheader("📥 Download Report")

            pdf_file = generate_pdf(
                score,
                ai_result,
                resume_skills,
                missing_skills
            )

            st.download_button(
                "Download PDF",
                pdf_file,
                "resume_analysis_report.pdf",
                "application/pdf"
            )