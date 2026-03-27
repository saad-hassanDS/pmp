import streamlit as st
import sqlite3
import pandas as pd
import uuid
import hashlib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import random

# Configure page
st.set_page_config(
    page_title="PMP Exam Practice Simulator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection
def get_db_connection():
    conn = sqlite3.connect('pmp_simulator.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database
def init_db():
    conn = get_db_connection()

    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            access_token TEXT UNIQUE,
            access_expiry DATE,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            attempts_reset_count INTEGER DEFAULT 0
        )
    ''')

    # Questions table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            domain TEXT NOT NULL,
            task TEXT,
            difficulty TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Exam templates table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS exam_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            num_questions INTEGER NOT NULL,
            domains TEXT,
            timer_minutes INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Exam attempts table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS exam_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            exam_template_id INTEGER,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            total_questions INTEGER,
            correct_answers INTEGER,
            score_percentage REAL,
            time_used_minutes INTEGER,
            completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (exam_template_id) REFERENCES exam_templates (id)
        )
    ''')

    # Exam answers table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS exam_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER,
            question_id INTEGER,
            selected_answer TEXT,
            is_correct BOOLEAN,
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts (id),
            FOREIGN KEY (question_id) REFERENCES questions (id)
        )
    ''')

    # Create default admin user
    admin_token = str(uuid.uuid4())
    try:
        conn.execute('''
            INSERT OR IGNORE INTO users (email, access_token, access_expiry, is_admin)
            VALUES (?, ?, ?, ?)
        ''', ('admin@pmp.com', admin_token, '2025-12-31', True))
    except sqlite3.IntegrityError:
        pass

    # Create default exam templates
    default_templates = [
        ('People Mini Quiz', 'Focus on People domain questions', 30, 'People', 40),
        ('Process Mini Quiz', 'Focus on Process domain questions', 30, 'Process', 40),
        ('Business Environment Mini Quiz', 'Focus on Business Environment domain questions', 30, 'Business Environment', 40),
        ('Full PMP Simulation', 'Complete PMP simulation exam', 180, 'People,Process,Business Environment', 230)
    ]

    for template in default_templates:
        try:
            conn.execute('''
                INSERT OR IGNORE INTO exam_templates (name, description, num_questions, domains, timer_minutes)
                VALUES (?, ?, ?, ?, ?)
            ''', template)
        except sqlite3.IntegrityError:
            pass

    conn.commit()
    conn.close()

# Authentication functions
def generate_magic_link(email):
    token = str(uuid.uuid4())
    return token

def validate_access_token(token):
    conn = get_db_connection()
    user = conn.execute('''
        SELECT * FROM users WHERE access_token = ? AND access_expiry >= date('now')
    ''', (token,)).fetchone()
    conn.close()
    return dict(user) if user else None

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_exam' not in st.session_state:
    st.session_state.current_exam = None

def main():
    init_db()

    # Handle authentication
    query_params = st.query_params

    if 'token' in query_params and not st.session_state.authenticated:
        token = query_params['token']
        user = validate_access_token(token)
        if user:
            st.session_state.authenticated = True
            st.session_state.user = user
            st.rerun()

    if not st.session_state.authenticated:
        show_login_page()
    else:
        if st.session_state.user['is_admin']:
            show_admin_dashboard()
        else:
            show_student_dashboard()

def show_login_page():
    st.title("🎓 PMP Exam Practice Simulator")
    st.markdown("### Welcome to the PMP Certification Practice Platform")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("#### Access Your Practice Exams")
        st.info("📧 Enter your registered email to receive a magic login link")

        email = st.text_input("Email Address", placeholder="your-email@example.com")

        if st.button("Send Magic Link", type="primary", width='stretch'):
            if email:
                # Check if user exists
                conn = get_db_connection()
                user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
                conn.close()

                if user:
                    # Generate and send magic link (simulation)
                    token = generate_magic_link(email)

                    # Update user token
                    conn = get_db_connection()
                    conn.execute('UPDATE users SET access_token = ? WHERE email = ?', (token, email))
                    conn.commit()
                    conn.close()

                    magic_link = f"http://localhost:8501?token={token}"

                    st.success("✅ Magic link sent!")
                    st.info(f"🔗 **Development Mode**: Use this link to login: {magic_link}")
                    st.caption("In production, this link would be sent via email.")
                else:
                    st.error("❌ Email not found. Contact your administrator for access.")
            else:
                st.error("Please enter your email address")

        st.markdown("---")
        st.markdown("##### 👨‍💼 Administrator Access")
        if st.button("Admin Login", width='stretch'):
            # For demo purposes, direct admin login
            conn = get_db_connection()
            admin = conn.execute('SELECT * FROM users WHERE is_admin = 1 LIMIT 1').fetchone()
            conn.close()

            if admin:
                st.session_state.authenticated = True
                st.session_state.user = dict(admin)
                st.rerun()

def show_admin_dashboard():
    st.title("🛠️ Admin Dashboard")

    # Initialize admin page in session state if not set
    if 'admin_page' not in st.session_state:
        st.session_state.admin_page = "Dashboard"

    # Sidebar navigation
    st.sidebar.title("Navigation")

    # Use session state for selectbox, but also listen for selectbox changes
    selectbox_value = st.sidebar.selectbox(
        "Select Page",
        ["Dashboard", "Question Bank", "Import Questions", "Exam Templates", "Students", "Analytics", "Settings"],
        index=["Dashboard", "Question Bank", "Import Questions", "Exam Templates", "Students", "Analytics", "Settings"].index(st.session_state.admin_page)
    )

    # Update session state if selectbox changed
    if selectbox_value != st.session_state.admin_page:
        st.session_state.admin_page = selectbox_value

    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        if 'admin_page' in st.session_state:
            del st.session_state.admin_page
        st.rerun()

    # Use session state to determine which page to show
    page = st.session_state.admin_page

    if page == "Dashboard":
        show_admin_dashboard_summary()
    elif page == "Question Bank":
        show_question_bank_management()
    elif page == "Import Questions":
        show_import_questions()
    elif page == "Exam Templates":
        show_exam_templates()
    elif page == "Students":
        show_student_management()
    elif page == "Analytics":
        show_admin_analytics()
    elif page == "Settings":
        show_admin_settings()

def show_admin_dashboard_summary():
    st.markdown("### Dashboard Summary")

    conn = get_db_connection()

    # Get stats
    total_questions = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    total_students = conn.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0').fetchone()[0]
    active_students = conn.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0 AND access_expiry >= date("now")').fetchone()[0]
    total_attempts = conn.execute('SELECT COUNT(*) FROM exam_attempts WHERE completed = 1').fetchone()[0]

    conn.close()

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Questions", total_questions)
    with col2:
        st.metric("Total Students", total_students)
    with col3:
        st.metric("Active Students", active_students)
    with col4:
        st.metric("Total Exams Attempted", total_attempts)

    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Add New Questions", width='stretch'):
            st.session_state.admin_page = "Import Questions"
            st.rerun()

    with col2:
        if st.button("👥 Manage Students", width='stretch'):
            st.session_state.admin_page = "Students"
            st.rerun()

    with col3:
        if st.button("📊 View Analytics", width='stretch'):
            st.session_state.admin_page = "Analytics"
            st.rerun()

def show_question_bank_management():
    st.markdown("### Question Bank Management")

    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("🔍 Search questions", placeholder="Enter keywords...")
    with col2:
        domain_filter = st.selectbox("Filter by Domain", ["All", "People", "Process", "Business Environment"])
    with col3:
        difficulty_filter = st.selectbox("Filter by Difficulty", ["All", "Easy", "Medium", "Hard"])

    # Get questions from database
    conn = get_db_connection()
    query = "SELECT * FROM questions WHERE 1=1"
    params = []

    if search_term:
        query += " AND question_text LIKE ?"
        params.append(f"%{search_term}%")
    if domain_filter != "All":
        query += " AND domain = ?"
        params.append(domain_filter)
    if difficulty_filter != "All":
        query += " AND difficulty = ?"
        params.append(difficulty_filter)

    questions = conn.execute(query + " ORDER BY created_at DESC", params).fetchall()
    conn.close()

    if questions:
        st.markdown(f"**Found {len(questions)} questions**")

        # Display questions in a table format
        for i, question in enumerate(questions):
            with st.expander(f"Question {question['id']} - {question['domain']} ({question['difficulty']})"):
                st.markdown(f"**Question:** {question['question_text']}")

                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**A.** {question['option_a']}")
                    st.write(f"**B.** {question['option_b']}")
                with col2:
                    st.write(f"**C.** {question['option_c']}")
                    st.write(f"**D.** {question['option_d']}")

                st.success(f"**Correct Answer:** {question['correct_answer']}")
                if question['explanation']:
                    st.info(f"**Explanation:** {question['explanation']}")

                st.caption(f"Domain: {question['domain']} | Task: {question['task']} | Difficulty: {question['difficulty']}")

                # Action buttons
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{question['id']}"):
                        st.info("Edit functionality would be implemented here")
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{question['id']}"):
                        # Delete question
                        conn = get_db_connection()
                        conn.execute("DELETE FROM questions WHERE id = ?", (question['id'],))
                        conn.commit()
                        conn.close()
                        st.success("Question deleted!")
                        st.rerun()
    else:
        st.info("No questions found matching your criteria.")

def show_import_questions():
    st.markdown("### Import Questions")

    # File upload
    st.markdown("#### Upload Excel File")
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=['xlsx', 'xls'],
        help="Upload an Excel file with questions following the template format"
    )

    # Show template format
    st.markdown("#### Required Excel Format")
    template_data = {
        'Question': ['What is the primary role of a project manager?', 'Which process group includes the Close Project or Phase process?'],
        'Option A': ['Manage resources', 'Initiating'],
        'Option B': ['Lead the team', 'Planning'],
        'Option C': ['Control scope', 'Executing'],
        'Option D': ['All of the above', 'Closing'],
        'Correct Answer': ['D', 'D'],
        'Explanation': ['Project managers are responsible for all aspects...', 'The Close Project or Phase process is part of...'],
        'Domain': ['People', 'Process'],
        'Task': ['Team Management', 'Project Closure'],
        'Difficulty': ['Medium', 'Easy']
    }

    template_df = pd.DataFrame(template_data)
    st.dataframe(template_df, width='stretch')

    # Download template
    @st.cache_data
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Questions')
        return output.getvalue()

    excel_data = convert_df_to_excel(template_df)
    st.download_button(
        label="📥 Download Template",
        data=excel_data,
        file_name="question_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # Process uploaded file
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)

            st.markdown("#### Preview Uploaded Data")
            st.dataframe(df.head(), width='stretch')

            # Validate columns
            required_columns = ['Question', 'Option A', 'Option B', 'Option C', 'Option D',
                              'Correct Answer', 'Explanation', 'Domain', 'Task', 'Difficulty']

            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"Missing columns: {', '.join(missing_columns)}")
            else:
                st.success("✅ All required columns found!")

                if st.button("Import Questions", type="primary"):
                    conn = get_db_connection()
                    imported_count = 0

                    for _, row in df.iterrows():
                        try:
                            conn.execute('''
                                INSERT INTO questions
                                (question_text, option_a, option_b, option_c, option_d,
                                 correct_answer, explanation, domain, task, difficulty)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                row['Question'], row['Option A'], row['Option B'],
                                row['Option C'], row['Option D'], row['Correct Answer'],
                                row['Explanation'], row['Domain'], row['Task'], row['Difficulty']
                            ))
                            imported_count += 1
                        except Exception as e:
                            st.error(f"Error importing row: {e}")

                    conn.commit()
                    conn.close()

                    st.success(f"Successfully imported {imported_count} questions!")

        except Exception as e:
            st.error(f"Error reading file: {e}")

def show_exam_templates():
    st.markdown("### Exam Templates")

    # Get existing templates
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM exam_templates ORDER BY created_at DESC').fetchall()
    conn.close()

    # Display templates
    if templates:
        for template in templates:
            with st.expander(f"{template['name']} - {template['num_questions']} questions"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Questions:** {template['num_questions']}")
                    st.write(f"**Timer:** {template['timer_minutes']} minutes")
                with col2:
                    st.write(f"**Domains:** {template['domains']}")
                with col3:
                    if st.button(f"🗑️ Delete", key=f"del_template_{template['id']}"):
                        conn = get_db_connection()
                        conn.execute("DELETE FROM exam_templates WHERE id = ?", (template['id'],))
                        conn.commit()
                        conn.close()
                        st.success("Template deleted!")
                        st.rerun()

    # Add new template
    st.markdown("#### Create New Exam Template")
    with st.form("new_template"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Exam Name")
            num_questions = st.number_input("Number of Questions", min_value=1, value=30)
        with col2:
            timer_minutes = st.number_input("Timer (minutes)", min_value=1, value=40)
            domains = st.multiselect("Domains", ["People", "Process", "Business Environment"])

        description = st.text_area("Description")

        if st.form_submit_button("Create Template"):
            if name and domains:
                conn = get_db_connection()
                conn.execute('''
                    INSERT INTO exam_templates (name, description, num_questions, domains, timer_minutes)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, description, num_questions, ','.join(domains), timer_minutes))
                conn.commit()
                conn.close()
                st.success("Template created!")
                st.rerun()

def show_student_management():
    st.markdown("### Student Management")

    # Add new student
    st.markdown("#### Add New Student")
    with st.form("add_student"):
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Student Email")
        with col2:
            access_months = st.number_input("Access Duration (months)", min_value=1, max_value=12, value=3)

        if st.form_submit_button("Add Student"):
            if email:
                access_expiry = (datetime.datetime.now() + datetime.timedelta(days=access_months*30)).strftime('%Y-%m-%d')
                token = str(uuid.uuid4())

                try:
                    conn = get_db_connection()
                    conn.execute('''
                        INSERT INTO users (email, access_token, access_expiry, is_admin)
                        VALUES (?, ?, ?, ?)
                    ''', (email, token, access_expiry, False))
                    conn.commit()
                    conn.close()

                    magic_link = f"http://localhost:8501?token={token}"
                    st.success(f"Student added! Magic link: {magic_link}")
                except sqlite3.IntegrityError:
                    st.error("Email already exists!")

    # List students
    st.markdown("#### Current Students")
    conn = get_db_connection()
    students = conn.execute('''
        SELECT u.*, COUNT(ea.id) as attempt_count
        FROM users u
        LEFT JOIN exam_attempts ea ON u.id = ea.user_id
        WHERE u.is_admin = 0
        GROUP BY u.id
        ORDER BY u.created_at DESC
    ''').fetchall()
    conn.close()

    if students:
        for student in students:
            with st.expander(f"{student['email']} - {student['attempt_count']} attempts"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Email:** {student['email']}")
                    st.write(f"**Attempts:** {student['attempt_count']}")
                with col2:
                    status = "Active" if student['access_expiry'] >= datetime.date.today().strftime('%Y-%m-%d') else "Expired"
                    st.write(f"**Status:** {status}")
                    st.write(f"**Expires:** {student['access_expiry']}")
                with col3:
                    if st.button(f"🔄 Reset Attempts", key=f"reset_{student['id']}"):
                        conn = get_db_connection()
                        conn.execute("DELETE FROM exam_attempts WHERE user_id = ?", (student['id'],))
                        conn.execute("DELETE FROM exam_answers WHERE attempt_id IN (SELECT id FROM exam_attempts WHERE user_id = ?)", (student['id'],))
                        conn.commit()
                        conn.close()
                        st.success("Attempts reset!")
                        st.rerun()

                    if st.button(f"🗑️ Remove", key=f"remove_{student['id']}"):
                        conn = get_db_connection()
                        conn.execute("DELETE FROM users WHERE id = ?", (student['id'],))
                        conn.commit()
                        conn.close()
                        st.success("Student removed!")
                        st.rerun()

def show_admin_analytics():
    st.markdown("### Analytics Dashboard")

    conn = get_db_connection()

    # Overall statistics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_attempts = conn.execute('SELECT COUNT(*) FROM exam_attempts WHERE completed = 1').fetchone()[0]
        st.metric("Total Completed Exams", total_attempts)

    with col2:
        avg_score = conn.execute('SELECT AVG(score_percentage) FROM exam_attempts WHERE completed = 1').fetchone()[0]
        st.metric("Average Score", f"{avg_score:.1f}%" if avg_score else "0%")

    with col3:
        total_students = conn.execute('SELECT COUNT(DISTINCT user_id) FROM exam_attempts').fetchone()[0]
        st.metric("Active Students", total_students)

    with col4:
        avg_time = conn.execute('SELECT AVG(time_used_minutes) FROM exam_attempts WHERE completed = 1').fetchone()[0]
        st.metric("Avg Time Used", f"{avg_time:.0f} min" if avg_time else "0 min")

    # Performance by domain
    domain_stats = conn.execute('''
        SELECT q.domain, AVG(CASE WHEN ea.is_correct THEN 100.0 ELSE 0.0 END) as avg_score
        FROM exam_answers ea
        JOIN questions q ON ea.question_id = q.id
        GROUP BY q.domain
    ''').fetchall()

    if domain_stats:
        st.markdown("#### Performance by Domain")
        domains = [stat['domain'] for stat in domain_stats]
        scores = [stat['avg_score'] for stat in domain_stats]

        fig = px.bar(x=domains, y=scores, title="Average Score by Domain")
        fig.update_layout(xaxis_title="Domain", yaxis_title="Average Score (%)")
        st.plotly_chart(fig, width='stretch')

    conn.close()

def show_admin_settings():
    st.markdown("### Settings")
    st.info("Settings panel - Additional configurations can be added here")

def show_student_dashboard():
    st.title("🎓 PMP Exam Practice Simulator")
    st.markdown(f"Welcome back, **{st.session_state.user['email']}**!")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Option", ["Exam Selection", "Previous Results", "Profile"])

    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.current_exam = None
        st.rerun()

    # Check if currently in an exam
    if st.session_state.current_exam:
        show_exam_interface()
    elif page == "Exam Selection":
        show_exam_selection()
    elif page == "Previous Results":
        show_previous_results()
    elif page == "Profile":
        show_student_profile()

def show_exam_selection():
    st.markdown("### Available Practice Exams")

    # Get available exam templates
    conn = get_db_connection()
    templates = conn.execute('SELECT * FROM exam_templates ORDER BY name').fetchall()
    conn.close()

    if not templates:
        st.warning("No exam templates available. Contact your administrator.")
        return

    # Display exam options
    for template in templates:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"#### {template['name']}")
                st.write(template['description'] if template['description'] else "No description available")
                st.caption(f"Domains: {template['domains']} | Questions: {template['num_questions']} | Time: {template['timer_minutes']} minutes")

            with col2:
                st.metric("Questions", template['num_questions'])
                st.metric("Time Limit", f"{template['timer_minutes']} min")

            with col3:
                if st.button(f"Start Exam", key=f"start_{template['id']}", type="primary"):
                    start_exam(template['id'])

            st.divider()

def start_exam(template_id):
    conn = get_db_connection()

    # Get template details
    template = conn.execute('SELECT * FROM exam_templates WHERE id = ?', (template_id,)).fetchone()

    # Get questions based on template criteria
    domains = template['domains'].split(',')
    domain_placeholders = ','.join('?' for _ in domains)

    # Get available questions
    all_questions = conn.execute(f'''
        SELECT * FROM questions
        WHERE domain IN ({domain_placeholders})
    ''', domains).fetchall()

    # Randomly select questions
    selected_questions = random.sample(list(all_questions), min(template['num_questions'], len(all_questions)))

    # Create exam attempt
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO exam_attempts (user_id, exam_template_id, total_questions)
        VALUES (?, ?, ?)
    ''', (st.session_state.user['id'], template_id, len(selected_questions)))

    attempt_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Shuffle answer options for each question
    exam_questions = []
    for question in selected_questions:
        options = ['A', 'B', 'C', 'D']
        option_texts = [question['option_a'], question['option_b'], question['option_c'], question['option_d']]

        # Create shuffled options mapping
        shuffled_mapping = list(zip(options, option_texts))
        random.shuffle(shuffled_mapping)

        # Find new position of correct answer
        correct_option_text = question[f'option_{question["correct_answer"].lower()}']
        new_correct_answer = next(opt for opt, text in shuffled_mapping if text == correct_option_text)

        exam_questions.append({
            'id': question['id'],
            'question_text': question['question_text'],
            'options': shuffled_mapping,
            'correct_answer': new_correct_answer,
            'original_correct': question['correct_answer'],
            'explanation': question['explanation'],
            'domain': question['domain'],
            'difficulty': question['difficulty']
        })

    # Store exam data in session state
    st.session_state.current_exam = {
        'attempt_id': attempt_id,
        'template': dict(template),
        'questions': exam_questions,
        'current_question': 0,
        'answers': {},
        'start_time': datetime.datetime.now(),
        'flagged_questions': set()
    }

    st.rerun()

def show_exam_interface():
    exam_data = st.session_state.current_exam
    template = exam_data['template']
    questions = exam_data['questions']
    current_q_idx = exam_data['current_question']

    # Calculate time remaining
    elapsed_time = datetime.datetime.now() - exam_data['start_time']
    total_seconds = template['timer_minutes'] * 60
    elapsed_seconds = elapsed_time.total_seconds()
    remaining_seconds = max(0, total_seconds - elapsed_seconds)

    # Auto-submit if time is up
    if remaining_seconds <= 0:
        submit_exam()
        return

    # Header with timer and question info
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"### {template['name']}")
        st.markdown(f"**Question {current_q_idx + 1} of {len(questions)}**")

    with col2:
        minutes = int(remaining_seconds // 60)
        seconds = int(remaining_seconds % 60)
        timer_color = "red" if remaining_seconds < 300 else "blue"  # Red if less than 5 minutes
        st.markdown(f"### <span style='color: {timer_color}'>⏱️ {minutes:02d}:{seconds:02d}</span>", unsafe_allow_html=True)

    with col3:
        if st.button("🏁 Submit Exam", type="primary"):
            submit_exam()
            return

    st.divider()

    # Question navigation panel
    st.markdown("#### Question Navigator")
    nav_cols = st.columns(10)

    for i in range(len(questions)):
        col_idx = i % 10
        with nav_cols[col_idx]:
            if i == current_q_idx:
                button_type = "primary"
                emoji = "📍"
            elif i in exam_data['answers']:
                button_type = "secondary"
                emoji = "✅"
            else:
                button_type = "secondary"
                emoji = "⭕"

            if i in exam_data['flagged_questions']:
                emoji += "🚩"

            if st.button(f"{emoji} {i+1}", key=f"nav_{i}", help=f"Go to question {i+1}"):
                exam_data['current_question'] = i
                st.rerun()

    st.divider()

    # Current question display
    current_question = questions[current_q_idx]

    st.markdown(f"#### Question {current_q_idx + 1}")
    st.markdown(current_question['question_text'])

    # Answer options
    current_answer = exam_data['answers'].get(current_q_idx, None)

    for option_letter, option_text in current_question['options']:
        selected = st.radio(
            "Select your answer:",
            options=[opt[0] for opt in current_question['options']],
            format_func=lambda x: f"{x}. {next(text for letter, text in current_question['options'] if letter == x)}",
            key=f"question_{current_q_idx}",
            index=[opt[0] for opt in current_question['options']].index(current_answer) if current_answer else None
        )
        break  # Only need to create one radio group

    # Update answer
    if selected:
        exam_data['answers'][current_q_idx] = selected

    # Navigation and flag buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button("⬅️ Previous", disabled=(current_q_idx == 0)):
            exam_data['current_question'] = max(0, current_q_idx - 1)
            st.rerun()

    with col2:
        flag_text = "🚩 Unflag" if current_q_idx in exam_data['flagged_questions'] else "🏳️ Flag for Review"
        if st.button(flag_text):
            if current_q_idx in exam_data['flagged_questions']:
                exam_data['flagged_questions'].remove(current_q_idx)
            else:
                exam_data['flagged_questions'].add(current_q_idx)
            st.rerun()

    with col3:
        if st.button("➡️ Next", disabled=(current_q_idx == len(questions) - 1)):
            exam_data['current_question'] = min(len(questions) - 1, current_q_idx + 1)
            st.rerun()

    with col4:
        if st.button("🏁 Submit Exam", key="submit_bottom"):
            submit_exam()

def submit_exam():
    exam_data = st.session_state.current_exam

    # Calculate results
    correct_count = 0
    total_questions = len(exam_data['questions'])

    # Save answers and calculate score
    conn = get_db_connection()

    for i, question in enumerate(exam_data['questions']):
        user_answer = exam_data['answers'].get(i, None)
        is_correct = user_answer == question['correct_answer'] if user_answer else False

        if is_correct:
            correct_count += 1

        # Save answer to database
        conn.execute('''
            INSERT INTO exam_answers (attempt_id, question_id, selected_answer, is_correct)
            VALUES (?, ?, ?, ?)
        ''', (exam_data['attempt_id'], question['id'], user_answer, is_correct))

    # Update exam attempt
    end_time = datetime.datetime.now()
    time_used = (end_time - exam_data['start_time']).total_seconds() / 60
    score_percentage = (correct_count / total_questions) * 100

    conn.execute('''
        UPDATE exam_attempts
        SET end_time = ?, correct_answers = ?, score_percentage = ?, time_used_minutes = ?, completed = 1
        WHERE id = ?
    ''', (end_time, correct_count, score_percentage, time_used, exam_data['attempt_id']))

    conn.commit()
    conn.close()

    # Store results for display
    st.session_state.exam_results = {
        'attempt_id': exam_data['attempt_id'],
        'score_percentage': score_percentage,
        'correct_answers': correct_count,
        'total_questions': total_questions,
        'time_used': time_used,
        'questions': exam_data['questions'],
        'answers': exam_data['answers']
    }

    # Clear current exam
    st.session_state.current_exam = None

    show_exam_results()

def show_exam_results():
    if 'exam_results' not in st.session_state:
        st.error("No exam results found.")
        return

    results = st.session_state.exam_results

    st.title("🎯 Exam Results")

    # Overall results
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Score", f"{results['score_percentage']:.1f}%")
    with col2:
        st.metric("Correct Answers", f"{results['correct_answers']}/{results['total_questions']}")
    with col3:
        st.metric("Incorrect Answers", results['total_questions'] - results['correct_answers'])
    with col4:
        st.metric("Time Used", f"{results['time_used']:.0f} min")

    # Performance analysis
    conn = get_db_connection()

    # Domain performance
    domain_performance = conn.execute('''
        SELECT q.domain,
               COUNT(*) as total,
               SUM(CASE WHEN ea.is_correct THEN 1 ELSE 0 END) as correct
        FROM exam_answers ea
        JOIN questions q ON ea.question_id = q.id
        WHERE ea.attempt_id = ?
        GROUP BY q.domain
    ''', (results['attempt_id'],)).fetchall()

    if domain_performance:
        st.markdown("#### 📊 Domain Performance")

        domains = [d['domain'] for d in domain_performance]
        scores = [(d['correct']/d['total'])*100 for d in domain_performance]

        fig = px.bar(x=domains, y=scores, title="Performance by Domain")
        fig.update_layout(xaxis_title="Domain", yaxis_title="Score (%)")
        st.plotly_chart(fig, width='stretch')

    # Difficulty performance
    difficulty_performance = conn.execute('''
        SELECT q.difficulty,
               COUNT(*) as total,
               SUM(CASE WHEN ea.is_correct THEN 1 ELSE 0 END) as correct
        FROM exam_answers ea
        JOIN questions q ON ea.question_id = q.id
        WHERE ea.attempt_id = ?
        GROUP BY q.difficulty
    ''', (results['attempt_id'],)).fetchall()

    if difficulty_performance:
        st.markdown("#### 📈 Difficulty Performance")

        difficulties = [d['difficulty'] for d in difficulty_performance]
        scores = [(d['correct']/d['total'])*100 for d in difficulty_performance]

        fig = px.bar(x=difficulties, y=scores, title="Performance by Difficulty")
        fig.update_layout(xaxis_title="Difficulty", yaxis_title="Score (%)")
        st.plotly_chart(fig, width='stretch')

    # Question review
    st.markdown("#### 📋 Question Review")

    questions_with_answers = conn.execute('''
        SELECT q.*, ea.selected_answer, ea.is_correct
        FROM questions q
        JOIN exam_answers ea ON q.id = ea.question_id
        WHERE ea.attempt_id = ?
    ''', (results['attempt_id'],)).fetchall()

    conn.close()

    # Filter options
    filter_option = st.selectbox("Filter questions", ["All", "Correct", "Incorrect"])

    for i, qa in enumerate(questions_with_answers):
        if filter_option == "Correct" and not qa['is_correct']:
            continue
        if filter_option == "Incorrect" and qa['is_correct']:
            continue

        status_color = "green" if qa['is_correct'] else "red"
        status_icon = "✅" if qa['is_correct'] else "❌"

        with st.expander(f"{status_icon} Question {i+1} - {qa['domain']} ({qa['difficulty']})"):
            st.markdown(f"**Question:** {qa['question_text']}")

            # Show options
            st.markdown("**Options:**")
            options = ['A', 'B', 'C', 'D']
            for opt in options:
                option_text = qa[f'option_{opt.lower()}']
                if opt == qa['selected_answer']:
                    if qa['is_correct']:
                        st.success(f"**{opt}.** {option_text} ✅ (Your answer - Correct)")
                    else:
                        st.error(f"**{opt}.** {option_text} ❌ (Your answer - Incorrect)")
                elif opt == qa['correct_answer']:
                    st.success(f"**{opt}.** {option_text} ✅ (Correct answer)")
                else:
                    st.write(f"**{opt}.** {option_text}")

            if qa['explanation']:
                st.info(f"**Explanation:** {qa['explanation']}")

    # Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Take Another Exam", type="primary"):
            if 'exam_results' in st.session_state:
                del st.session_state['exam_results']
            st.rerun()
    with col2:
        if st.button("📊 View All Results"):
            if 'exam_results' in st.session_state:
                del st.session_state['exam_results']
            st.rerun()

def show_previous_results():
    st.markdown("### 📊 Previous Exam Results")

    conn = get_db_connection()
    attempts = conn.execute('''
        SELECT ea.*, et.name as exam_name
        FROM exam_attempts ea
        JOIN exam_templates et ON ea.exam_template_id = et.id
        WHERE ea.user_id = ? AND ea.completed = 1
        ORDER BY ea.start_time DESC
    ''', (st.session_state.user['id'],)).fetchall()
    conn.close()

    if not attempts:
        st.info("No completed exams found. Take your first exam to see results here!")
        return

    # Summary statistics
    if attempts:
        scores = [attempt['score_percentage'] for attempt in attempts]
        avg_score = sum(scores) / len(scores)
        best_score = max(scores)
        total_attempts = len(attempts)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Attempts", total_attempts)
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}%")
        with col3:
            st.metric("Best Score", f"{best_score:.1f}%")

    # Progress chart
    if len(attempts) > 1:
        st.markdown("#### 📈 Score Progress")

        attempt_dates = [attempt['start_time'][:10] for attempt in reversed(attempts)]  # Get date part
        attempt_scores = [attempt['score_percentage'] for attempt in reversed(attempts)]

        fig = px.line(x=attempt_dates, y=attempt_scores, title="Score Progression Over Time")
        fig.update_layout(xaxis_title="Date", yaxis_title="Score (%)")
        st.plotly_chart(fig, width='stretch')

    # Detailed results
    st.markdown("#### 📋 Detailed Results")

    for attempt in attempts:
        with st.expander(f"{attempt['exam_name']} - {attempt['start_time'][:16]} - {attempt['score_percentage']:.1f}%"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"**Score:** {attempt['score_percentage']:.1f}%")
                st.write(f"**Correct:** {attempt['correct_answers']}/{attempt['total_questions']}")
            with col2:
                st.write(f"**Time Used:** {attempt['time_used_minutes']:.0f} minutes")
                st.write(f"**Date:** {attempt['start_time'][:16]}")
            with col3:
                if st.button(f"📝 Review Details", key=f"review_{attempt['id']}"):
                    # Set up results for detailed review
                    st.session_state.review_attempt_id = attempt['id']
                    show_attempt_details(attempt['id'])

def show_attempt_details(attempt_id):
    st.markdown(f"### 📋 Detailed Review - Attempt #{attempt_id}")

    conn = get_db_connection()

    # Get attempt details
    attempt = conn.execute('''
        SELECT ea.*, et.name as exam_name
        FROM exam_attempts ea
        JOIN exam_templates et ON ea.exam_template_id = et.id
        WHERE ea.id = ?
    ''', (attempt_id,)).fetchone()

    if not attempt:
        st.error("Attempt not found.")
        return

    # Get questions and answers for this attempt
    questions_with_answers = conn.execute('''
        SELECT q.*, ea.selected_answer, ea.is_correct
        FROM questions q
        JOIN exam_answers ea ON q.id = ea.question_id
        WHERE ea.attempt_id = ?
        ORDER BY ea.id
    ''', (attempt_id,)).fetchall()

    conn.close()

    # Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Score", f"{attempt['score_percentage']:.1f}%")
    with col2:
        st.metric("Correct", f"{attempt['correct_answers']}/{attempt['total_questions']}")
    with col3:
        st.metric("Time Used", f"{attempt['time_used_minutes']:.0f} min")
    with col4:
        st.metric("Date", attempt['start_time'][:10])

    # Questions review
    st.markdown("#### Question Review")

    for i, qa in enumerate(questions_with_answers):
        status_icon = "✅" if qa['is_correct'] else "❌"

        with st.expander(f"{status_icon} Question {i+1} - {qa['domain']} ({qa['difficulty']})"):
            st.markdown(f"**Question:** {qa['question_text']}")

            # Show all options
            options = ['A', 'B', 'C', 'D']
            for opt in options:
                option_text = qa[f'option_{opt.lower()}']
                if opt == qa['selected_answer']:
                    if qa['is_correct']:
                        st.success(f"**{opt}.** {option_text} ✅ (Your correct answer)")
                    else:
                        st.error(f"**{opt}.** {option_text} ❌ (Your incorrect answer)")
                elif opt == qa['correct_answer']:
                    st.success(f"**{opt}.** {option_text} ✅ (Correct answer)")
                else:
                    st.write(f"**{opt}.** {option_text}")

            if qa['explanation']:
                st.info(f"**Explanation:** {qa['explanation']}")

    if st.button("⬅️ Back to Results"):
        if 'review_attempt_id' in st.session_state:
            del st.session_state['review_attempt_id']
        st.rerun()

def show_student_profile():
    st.markdown("### 👤 Student Profile")

    user = st.session_state.user

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Account Information")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Access Expires:** {user['access_expiry']}")

        # Check access status
        expiry_date = datetime.datetime.strptime(user['access_expiry'], '%Y-%m-%d').date()
        today = datetime.date.today()
        days_remaining = (expiry_date - today).days

        if days_remaining > 0:
            st.success(f"✅ Access active - {days_remaining} days remaining")
        else:
            st.error("❌ Access expired - Contact administrator")

    with col2:
        st.markdown("#### Quick Stats")

        conn = get_db_connection()
        stats = conn.execute('''
            SELECT
                COUNT(*) as total_attempts,
                AVG(score_percentage) as avg_score,
                MAX(score_percentage) as best_score
            FROM exam_attempts
            WHERE user_id = ? AND completed = 1
        ''', (user['id'],)).fetchone()
        conn.close()

        st.metric("Total Attempts", stats['total_attempts'] if stats['total_attempts'] else 0)
        if stats['avg_score']:
            st.metric("Average Score", f"{stats['avg_score']:.1f}%")
            st.metric("Best Score", f"{stats['best_score']:.1f}%")
        else:
            st.metric("Average Score", "No attempts yet")
            st.metric("Best Score", "No attempts yet")

if __name__ == "__main__":
    main()