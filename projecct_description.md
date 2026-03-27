Product Requirements Document (PRD)
PMP Exam Practice Simulator (Web Application)
1. Product Overview
The PMP Exam Practice Simulator is a web-based application designed to help PMP candidates practice exam-style questions in a simulated environment.
The system will allow a trainer/admin to upload and manage questions, grant temporary access to students via email, and provide analytics after each quiz attempt to help candidates identify strengths and weaknesses across PMP domains.
The system will initially support ~300 questions but must be scalable to thousands of questions without structural changes.
Primary goals:
    • Allow candidates to practice PMP questions with a timer-based quiz interface
    • Provide domain-wise performance analytics
    • Allow trainers to easily upload questions via Excel
    • Provide temporary email-based access control
    • Randomize questions and answer order for each attempt
The application will be developed as a web application and hosted on a cloud environment (e.g., Streamlit Cloud or similar platform).

1.1 Wireframes

Student Exam Interface Wireframe

Admin Panel Wireframe

Exam Analytics Dashboard (Student)

2. User Roles
2.1 Admin (Trainer)
The Admin will have full control of the system including:
    • Creating user access
    • Uploading questions
    • Editing question bank
    • Setting quiz configurations
    • Resetting user attempts
    • Viewing student analytics
Example user: Trainer (Muhammad Abubakar)

2.2 Student (Candidate)
Students can:
    • Access the system using an email magic login link
    • Attempt quizzes
    • View results and analytics
    • Retake quizzes multiple times
Students cannot edit questions or see the question bank.

3. Authentication & Access System
3.1 Login Method
Authentication will use Magic Link Email Login.
Process:
    1. Admin adds user email in system
    2. System generates login link
    3. Link is sent to email
    4. User clicks link to access simulator
No password required.

3.2 Access Validity
Each user account will have an expiry date.
Example:
Access Duration: 3 months
After expiry:
    • User cannot access quizzes
    • Admin can extend access

3.3 Access Control
Admin Panel features:
    • Add user email
    • Set access duration
    • Disable user
    • Extend access
    • Reset attempts

4. Question Bank Structure
Each question will contain the following attributes.
Core Fields
Field	Description
Question ID	Unique identifier
Question Text	The main question
Option A	Answer option
Option B	Answer option
Option C	Answer option
Option D	Answer option
Correct Answer	Correct option
Explanation	Detailed explanation
Domain	People / Process / Business Environment
Task/Topic	Specific PMP task
Difficulty	Easy / Medium / Hard

Domain Categories
Based on PMP ECO:
    1. People
    2. Process
    3. Business Environment

5. Question Import System
Admin must be able to upload questions via Excel file.
Excel Format
Columns:
Column	Field
Question	Question Text
Option A	Answer
Option B	Answer
Option C	Answer
Option D	Answer
Correct Answer	A/B/C/D
Explanation	Explanation text
Domain	People/Process/Business
Task	Topic
Difficulty	Easy/Medium/Hard
Admin should also be able to:
    • Edit questions
    • Delete questions
    • Search questions

6. Quiz Engine (Revised)
6.1 Predefined Exam Types
Students will not be able to generate custom quizzes.
All quiz types will be predefined and configured by the Admin.
The Admin will create exam templates that students can select from.
Example predefined quizzes:
Exam Type	Questions	Domains	Timer
People Mini Quiz	30	People only	40 minutes
Process Mini Quiz	30	Process only	40 minutes
Business Environment Mini Quiz	30	Business Environment only	40 minutes
Full PMP Simulation	180	All domains	230 minutes
Admin must be able to configure:
    • Quiz name
    • Number of questions
    • Domain scope
    • Timer duration
Students will only see available quizzes and can choose which one to attempt.

6.2 Question Selection Logic
When a quiz begins, the system will:
    1. Identify the selected exam template
    2. Randomly select questions from the question bank matching the template criteria
    3. Ensure questions are randomly selected for every attempt
    4. Shuffle the answer options for each question
Example:
If a student selects People Mini Quiz:
    • System randomly selects 30 questions tagged as "People" domain
    • Questions appear in random order
    • Options (A, B, C, D) are shuffled
This ensures every attempt is unique even if the quiz type is the same.

6.3 Attempt Policy
Students will be allowed unlimited quiz attempts during their access period.
For each attempt:
    • A new randomized question set is generated
    • Previous attempt results remain stored for analytics
Admin capabilities:
    • Reset student attempts
    • View attempt history

7. Timer System (Updated)
Each quiz will include a countdown timer predefined by the Admin.
Behavior:
    • Timer starts when the quiz begins
    • Timer counts backward
    • When the timer reaches zero:
        ◦ The exam automatically submits
Timer values are configured in the Exam Template Settings.
Example:
Exam Type	Timer
Mini Quiz	40 minutes
Full Exam	230 minutes
Students cannot modify the timer.


8. Quiz Interface (Student UI)
The student interface should include:
Main Features
    • Question navigation panel
    • Timer countdown
    • Question display
    • Multiple choice options
    • Next / Previous navigation
    • Submit exam button

Navigation Panel
Should show:
    • Question numbers
    • Answered questions
    • Unanswered questions
    • Current question
Example:
1 2 3 4 5 6 7 8 9 10

9. Result & Analytics
After each attempt, the system will display:
Overall Metrics
Metric	Description
Total Score	Percentage
Correct Answers	Number
Incorrect Answers	Number
Time Used	Total time

Domain Analytics
Performance by PMP domain:
Domain	Correct	Incorrect	Score
People			
Process			
Business Environment			

Difficulty Analytics
Difficulty	Score
Easy	
Medium	
Hard	

Question Review
Students can review:
    • Their selected answer
    • Correct answer
    • Explanation

10. Admin Dashboard
Admin panel should include:
User Management
    • Add student email
    • Set access duration
    • Disable account
    • Reset attempts

Question Management
    • Upload Excel
    • Edit question
    • Delete question
    • Search questions
    • Filter by domain/difficulty

Quiz Settings
Admin should be able to set:
    • Default timer
    • Default quiz length

Analytics
Admin can view:
    • Student performance
    • Number of attempts
    • Domain-wise performance

11. Scalability Requirements
The system must support:
    • Expansion from 300 → 5000+ questions
    • Multiple students simultaneously
    • Fast query performance
Recommended approach:
    • Structured database (PostgreSQL or SQLite initially)

12. Technology Recommendation (Developer Guidance)
Suggested stack for fast development:
Backend
Python
Framework options:
    • Streamlit (fastest MVP)
    • FastAPI + React (scalable)

Database
Options:
    • SQLite (initial)
    • PostgreSQL (scalable)

Hosting
Cloud options:
    • Streamlit Cloud
    • Render
    • AWS
    • DigitalOcean

13. Security Requirements
    • Email-based authentication
    • Access expiry enforcement
    • Admin-only editing rights
    • Server-side question storage

14. Future Features (Version 2)
The architecture should allow adding later:
    • Additional question types:
        ◦ Multiple response
        ◦ Matching
        ◦ Drag and drop
    • Full PMP exam simulation (180 questions)
    • Weak topic identification
    • Paid subscription system
    • Mobile optimization

15. Success Criteria
The application will be successful if it allows:
    • Trainer to upload questions in minutes
    • Students to practice unlimited quizzes
    • Students to receive clear domain analytics
    • Trainer to manage access via email
