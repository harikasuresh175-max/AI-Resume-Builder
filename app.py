import streamlit as st
from datetime import date
from io import BytesIO

st.set_page_config(
    page_title="AI Resume Builder & Career Guide",
    page_icon="📄",
    layout="wide",
)

# This beginner-friendly prototype uses transparent skill matching.
# It does not make hiring decisions or guarantee employment.
ROLE_SKILLS = {
    "Python Developer": {"python", "programming", "sql", "git", "problem solving"},
    "Web Developer": {"html", "css", "javascript", "python", "web development"},
    "Data Analyst Intern": {"python", "sql", "excel", "statistics", "data analysis"},
    "Software Tester": {"testing", "manual testing", "sql", "communication", "attention to detail"},
    "Machine Learning Intern": {"python", "statistics", "machine learning", "pandas", "data analysis"},
    "Technical Support Associate": {"communication", "troubleshooting", "networking", "problem solving"},
    "UI/UX Design Intern": {"figma", "ui design", "ux design", "creativity", "communication"},
}

LEARNING_TIPS = {
    "Python Developer": ["Practise Python functions and object-oriented programming.", "Build a small project and learn Git basics."],
    "Web Developer": ["Create a responsive page using HTML and CSS.", "Practise JavaScript and basic web accessibility."],
    "Data Analyst Intern": ["Practise Excel, SQL queries, and basic statistics.", "Try a small data-cleaning project with pandas."],
    "Software Tester": ["Learn test cases, bug reports, and software testing basics.", "Practise testing a sample website."],
    "Machine Learning Intern": ["Learn Python, pandas, and basic statistics.", "Build a small classification project and explain its results."],
    "Technical Support Associate": ["Practise troubleshooting steps and basic networking.", "Improve clear written and spoken communication."],
    "UI/UX Design Intern": ["Create simple wireframes and practise Figma.", "Learn usability basics and collect feedback."],
}

def clean(value):
    return value.strip() if value and value.strip() else "Not provided"

def parse_skills(raw):
    return {item.strip().lower() for item in raw.replace("\n", ",").split(",") if item.strip()}

def make_resume(profile):
    lines = [
        profile["name"].upper(),
        profile["email"] + (" | " + profile["phone"] if profile["phone"] else ""),
        "",
        "CAREER OBJECTIVE",
        profile["objective"] or "Motivated student seeking an opportunity to learn, contribute, and develop professional skills.",
        "",
        "EDUCATION",
        profile["education"],
        "",
        "SKILLS",
        profile["skills"] or "Not provided",
        "",
        "PROJECTS",
        profile["projects"] or "Not provided",
        "",
        "CERTIFICATIONS",
        profile["certifications"] or "Not provided",
        "",
        "EXPERIENCE",
        profile["experience"] or "Fresher",
    ]
    if profile["linkedin"]:
        lines += ["", "LINKEDIN", profile["linkedin"]]
    return "\n".join(lines)

def make_pdf(profile):
    # PDF generation uses reportlab when installed. If unavailable, the app still works.
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import mm
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm)
        styles = getSampleStyleSheet()
        name_style = ParagraphStyle("Name", parent=styles["Title"], alignment=TA_CENTER, textColor=colors.HexColor("#174A70"), fontSize=18, leading=22)
        section_style = ParagraphStyle("Section", parent=styles["Heading2"], textColor=colors.HexColor("#174A70"), spaceBefore=10, spaceAfter=4)
        body = styles["BodyText"]
        story = [Paragraph(profile["name"].replace("&", "&amp;"), name_style), Spacer(1, 5)]
        contact = " | ".join([x for x in [profile["email"], profile["phone"], profile["linkedin"]] if x])
        if contact:
            story.append(Paragraph(contact.replace("&", "&amp;"), body))
        sections = [
            ("CAREER OBJECTIVE", profile["objective"] or "Motivated student seeking an opportunity to learn, contribute, and develop professional skills."),
            ("EDUCATION", profile["education"]),
            ("SKILLS", profile["skills"] or "Not provided"),
            ("PROJECTS", profile["projects"] or "Not provided"),
            ("CERTIFICATIONS", profile["certifications"] or "Not provided"),
            ("EXPERIENCE", profile["experience"] or "Fresher"),
        ]
        for heading, content in sections:
            story.append(Paragraph(heading, section_style))
            safe = (content or "Not provided").replace("&", "&amp;").replace("\n", "<br/>")
            story.append(Paragraph(safe, body))
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except ImportError:
        return None

st.title("📄 AI Resume Builder & Career Guidance")
st.write("Create a clear resume draft and explore entry-level career options based on your skills.")
st.info("Academic prototype: career suggestions are based on simple skill matching. They are guidance only, not a hiring decision or a guarantee of employment.")

tab_resume, tab_career, tab_about = st.tabs(["📝 Build my resume", "🧭 Career guidance", "ℹ️ About the project"])

with tab_resume:
    st.subheader("Enter your details")
    with st.form("resume_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full name *", placeholder="e.g., Priya Kumar")
            email = st.text_input("Email address", placeholder="name@example.com")
            phone = st.text_input("Phone number (optional)")
            linkedin = st.text_input("LinkedIn URL (optional)")
        with col2:
            education = st.text_area("Education *", placeholder="BCA, 5th Semester\nCollege name | Expected graduation year")
            skills = st.text_area("Skills (separate with commas) *", placeholder="Python, HTML, CSS, SQL, communication")
            certifications = st.text_area("Certifications", placeholder="Python Programming — Cisco Networking Academy")
        projects = st.text_area("Projects", placeholder="Project title — one or two lines describing what you built")
        objective = st.text_area("Career objective (optional)", placeholder="A short statement about your career goal")
        experience = st.text_area("Experience / internship (optional)", placeholder="Fresher, or describe your experience")
        submitted = st.form_submit_button("Generate resume", type="primary")

    if submitted:
        if not name.strip() or not education.strip() or not skills.strip():
            st.error("Please complete the required fields: Full name, Education, and Skills.")
        else:
            profile = {
                "name": clean(name), "email": clean(email), "phone": phone.strip(),
                "linkedin": linkedin.strip(), "education": clean(education),
                "skills": clean(skills), "certifications": certifications.strip(),
                "projects": projects.strip(), "objective": objective.strip(),
                "experience": experience.strip(),
            }
            st.session_state["profile"] = profile
            st.session_state["resume_text"] = make_resume(profile)
            st.success("Your resume draft is ready. Review it carefully before applying for a job.")

    if "profile" in st.session_state:
        profile = st.session_state["profile"]
        st.markdown("---")
        st.subheader("Resume preview")
        st.markdown(f"## {profile['name']}")
        contact = " | ".join([x for x in [profile["email"], profile["phone"], profile["linkedin"]] if x])
        if contact:
            st.caption(contact)
        for heading, key in [
            ("Career Objective", "objective"), ("Education", "education"),
            ("Skills", "skills"), ("Projects", "projects"),
            ("Certifications", "certifications"), ("Experience", "experience")
        ]:
            st.markdown(f"**{heading}**")
            st.write(profile[key] or ("Fresher" if key == "experience" else "Not provided"))
        st.download_button(
            "⬇️ Download resume as TXT",
            data=st.session_state["resume_text"],
            file_name="my_resume.txt",
            mime="text/plain",
        )
        pdf_bytes = make_pdf(profile)
        if pdf_bytes:
            st.download_button("⬇️ Download resume as PDF", data=pdf_bytes, file_name="my_resume.pdf", mime="application/pdf")
        else:
            st.caption("PDF download needs reportlab. Install project requirements if the PDF button is not available.")

with tab_career:
    st.subheader("Find career roles to explore")
    st.write("Enter skills separated by commas. The app compares your skills with a small set of example role requirements.")
    raw_skills = st.text_input("Your skills", placeholder="Python, SQL, HTML, communication")
    if st.button("Suggest job roles", type="primary"):
        user_skills = parse_skills(raw_skills)
        if not user_skills:
            st.warning("Enter at least one skill to receive suggestions.")
        else:
            results = []
            for role, required in ROLE_SKILLS.items():
                matched = user_skills & required
                score = round(len(matched) / len(required) * 100)
                results.append((score, role, matched, required - user_skills))
            results.sort(key=lambda item: (item[0], item[1]), reverse=True)
            for score, role, matched, missing in results[:5]:
                with st.container(border=True):
                    st.markdown(f"### {role}")
                    st.progress(score / 100, text=f"Skill overlap: {score}%")
                    st.write("**Matching skills:** " + (", ".join(sorted(matched)) if matched else "No direct match found yet"))
                    if missing:
                        st.write("**Skills you could explore:** " + ", ".join(sorted(missing)))
                    st.write("**Next steps:**")
                    for tip in LEARNING_TIPS[role]:
                        st.write("• " + tip)
            st.caption("The percentage is only the share of example skills matched. It is not a probability of getting a job.")
    st.markdown("#### Example skills to try")
    st.code("Python, SQL, HTML, CSS, communication, problem solving", language="text")

with tab_about:
    st.subheader("Project summary")
    st.write("This project helps students create a structured resume draft and discover possible entry-level career roles.")
    st.markdown("**Technologies**")
    st.write("- Python")
    st.write("- Streamlit for the web interface")
    st.write("- Basic text processing and skill matching")
    st.write("- ReportLab for PDF export")
    st.markdown("**How it works**")
    st.write("1. Enter profile details.")
    st.write("2. Generate and review the resume.")
    st.write("3. Download the resume as a text file or PDF.")
    st.write("4. Enter skills in the Career Guidance tab to explore matching roles.")
    st.markdown("**Privacy tip:** This demo does not save information to a database. Avoid entering sensitive personal information when testing.")

st.markdown("---")
st.caption("Developed as a BCA-level learning project. Always proofread your resume and verify job requirements independently.")
