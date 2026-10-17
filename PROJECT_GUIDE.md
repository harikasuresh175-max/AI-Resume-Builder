# Project explanation and demo guide

## Title
AI Resume Builder and Career Guidance System

## Objective
To build a simple web app that helps students prepare a resume draft and explore entry-level job roles based on their skills.

## Modules
1. Resume input form
2. Resume preview and download
3. Skill-based career suggestions
4. Project information

## Algorithm: career role matching
1. Convert the user's comma-separated skills into a set of lowercase words.
2. Store example skills required for each job role.
3. Find the intersection between the user's skills and each role's required skills.
4. Calculate the percentage of role skills matched.
5. Display the top matching roles, matching skills, and skills to explore.

Formula:
Skill overlap (%) = (Number of matched example skills / Number of example skills for the role) × 100

This score is only a simple comparison measure, not the probability of getting hired.

## Test cases
- Enter all required resume fields: the resume should be generated.
- Leave name empty: the app should show a validation message.
- Enter Python and SQL: relevant roles should appear in Career Guidance.
- Enter no career skills: the app should ask the user to enter at least one skill.

## Viva questions and short answers
1. What is Python? A high-level programming language used for general-purpose development.
2. What is Streamlit? A Python framework used to build interactive web apps.
3. What is the purpose of this project? To help students draft resumes and explore career options.
4. Is this a fully trained AI model? No. The first version uses transparent rule-based skill matching.
5. What is a future enhancement? Add PDF templates, a database, more job roles, and machine-learning-based recommendations.
