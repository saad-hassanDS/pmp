#!/usr/bin/env python3
"""
Comprehensive Test Suite for PMP Exam Practice Simulator
"""

import sqlite3
import pandas as pd
import os
import sys
import uuid
from datetime import datetime, timedelta

def test_database_initialization():
    """Test database creation and schema"""
    print("🔍 Testing Database Initialization...")

    # Remove existing database for clean test
    if os.path.exists('pmp_simulator.db'):
        os.remove('pmp_simulator.db')

    # Import and run database initialization
    sys.path.append('.')
    from app import init_db, get_db_connection

    init_db()

    # Verify tables exist
    conn = get_db_connection()
    cursor = conn.cursor()

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [table[0] for table in tables]

    expected_tables = ['users', 'questions', 'exam_templates', 'exam_attempts', 'exam_answers']

    for table in expected_tables:
        if table in table_names:
            print(f"  ✅ Table '{table}' created successfully")
        else:
            print(f"  ❌ Table '{table}' missing")
            return False

    # Verify default admin user
    admin = conn.execute('SELECT * FROM users WHERE is_admin = 1').fetchone()
    if admin:
        print(f"  ✅ Default admin user created: {admin['email']}")
    else:
        print(f"  ❌ Default admin user missing")
        return False

    # Verify default exam templates
    templates = conn.execute('SELECT COUNT(*) FROM exam_templates').fetchone()[0]
    if templates >= 4:
        print(f"  ✅ Default exam templates created: {templates} templates")
    else:
        print(f"  ❌ Missing exam templates: only {templates} found")
        return False

    conn.close()
    print("✅ Database initialization test PASSED\n")
    return True

def test_question_import():
    """Test question import functionality"""
    print("🔍 Testing Question Import...")

    # Check if question files exist
    if not os.path.exists('converted_questions.xlsx'):
        print("  ❌ converted_questions.xlsx not found")
        return False

    # Load Excel file
    try:
        df = pd.read_excel('converted_questions.xlsx')
        print(f"  ✅ Excel file loaded successfully: {len(df)} questions")
    except Exception as e:
        print(f"  ❌ Excel file loading failed: {e}")
        return False

    # Verify required columns
    required_columns = ['Question', 'Option A', 'Option B', 'Option C', 'Option D',
                       'Correct Answer', 'Explanation', 'Domain', 'Task', 'Difficulty']

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"  ❌ Missing columns: {missing_columns}")
        return False
    else:
        print("  ✅ All required columns present")

    # Test database import
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
            print(f"  ⚠️ Error importing question: {e}")

    conn.commit()

    # Verify import
    total_questions = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]
    conn.close()

    if imported_count > 0:
        print(f"  ✅ Questions imported successfully: {imported_count} questions")
        print(f"  ✅ Total questions in database: {total_questions}")
    else:
        print(f"  ❌ No questions imported")
        return False

    print("✅ Question import test PASSED\n")
    return True

def test_student_management():
    """Test student management functionality"""
    print("🔍 Testing Student Management...")

    conn = get_db_connection()

    # Test adding student
    test_email = "test.student@example.com"
    access_expiry = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    token = str(uuid.uuid4())

    try:
        conn.execute('''
            INSERT INTO users (email, access_token, access_expiry, is_admin)
            VALUES (?, ?, ?, ?)
        ''', (test_email, token, access_expiry, False))
        conn.commit()
        print(f"  ✅ Student added successfully: {test_email}")
    except Exception as e:
        print(f"  ❌ Failed to add student: {e}")
        conn.close()
        return False

    # Test student retrieval
    student = conn.execute('SELECT * FROM users WHERE email = ?', (test_email,)).fetchone()
    if student:
        print(f"  ✅ Student retrieved successfully")
        print(f"    - Email: {student['email']}")
        print(f"    - Access expires: {student['access_expiry']}")
        print(f"    - Token length: {len(student['access_token'])}")
    else:
        print(f"  ❌ Student retrieval failed")
        conn.close()
        return False

    # Test access validation
    from app import validate_access_token
    user = validate_access_token(token)
    if user:
        print(f"  ✅ Access token validation successful")
    else:
        print(f"  ❌ Access token validation failed")
        conn.close()
        return False

    conn.close()
    print("✅ Student management test PASSED\n")
    return True

def test_exam_templates():
    """Test exam template functionality"""
    print("🔍 Testing Exam Templates...")

    conn = get_db_connection()

    # Test retrieving templates
    templates = conn.execute('SELECT * FROM exam_templates').fetchall()

    if len(templates) < 4:
        print(f"  ❌ Insufficient exam templates: {len(templates)} found, expected 4+")
        conn.close()
        return False

    print(f"  ✅ Found {len(templates)} exam templates:")

    for template in templates:
        print(f"    - {template['name']}: {template['num_questions']} questions, {template['timer_minutes']} minutes")
        print(f"      Domains: {template['domains']}")

    # Test creating new template
    new_template = {
        'name': 'Test Quiz',
        'description': 'Test quiz for validation',
        'num_questions': 10,
        'domains': 'Process',
        'timer_minutes': 15
    }

    try:
        conn.execute('''
            INSERT INTO exam_templates (name, description, num_questions, domains, timer_minutes)
            VALUES (?, ?, ?, ?, ?)
        ''', (new_template['name'], new_template['description'], new_template['num_questions'],
              new_template['domains'], new_template['timer_minutes']))
        conn.commit()
        print(f"  ✅ New template created successfully: {new_template['name']}")
    except Exception as e:
        print(f"  ❌ Failed to create new template: {e}")
        conn.close()
        return False

    conn.close()
    print("✅ Exam templates test PASSED\n")
    return True

def test_exam_simulation():
    """Test exam taking simulation"""
    print("🔍 Testing Exam Simulation...")

    conn = get_db_connection()

    # Get a student and template for testing
    student = conn.execute('SELECT * FROM users WHERE is_admin = 0 LIMIT 1').fetchone()
    template = conn.execute('SELECT * FROM exam_templates LIMIT 1').fetchone()
    questions = conn.execute('SELECT * FROM questions LIMIT 5').fetchall()  # Get 5 questions for test

    if not student:
        print("  ❌ No test student found")
        conn.close()
        return False

    if not template:
        print("  ❌ No exam template found")
        conn.close()
        return False

    if len(questions) < 5:
        print(f"  ❌ Insufficient questions: {len(questions)} found, need 5+")
        conn.close()
        return False

    # Create exam attempt
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO exam_attempts (user_id, exam_template_id, total_questions)
            VALUES (?, ?, ?)
        ''', (student['id'], template['id'], len(questions)))
        attempt_id = cursor.lastrowid
        conn.commit()
        print(f"  ✅ Exam attempt created: ID {attempt_id}")
    except Exception as e:
        print(f"  ❌ Failed to create exam attempt: {e}")
        conn.close()
        return False

    # Simulate answering questions
    correct_count = 0
    for i, question in enumerate(questions):
        # Simulate random answer (50% correct for testing)
        is_correct = i % 2 == 0  # Every other answer is correct
        user_answer = question['correct_answer'] if is_correct else 'A'

        if is_correct:
            correct_count += 1

        try:
            conn.execute('''
                INSERT INTO exam_answers (attempt_id, question_id, selected_answer, is_correct)
                VALUES (?, ?, ?, ?)
            ''', (attempt_id, question['id'], user_answer, is_correct))
        except Exception as e:
            print(f"  ❌ Failed to save answer for question {i+1}: {e}")
            conn.close()
            return False

    # Complete the exam
    try:
        end_time = datetime.now()
        time_used = 25  # Simulate 25 minutes
        score_percentage = (correct_count / len(questions)) * 100

        conn.execute('''
            UPDATE exam_attempts
            SET end_time = ?, correct_answers = ?, score_percentage = ?, time_used_minutes = ?, completed = 1
            WHERE id = ?
        ''', (end_time, correct_count, score_percentage, time_used, attempt_id))
        conn.commit()

        print(f"  ✅ Exam completed successfully:")
        print(f"    - Score: {score_percentage:.1f}%")
        print(f"    - Correct answers: {correct_count}/{len(questions)}")
        print(f"    - Time used: {time_used} minutes")

    except Exception as e:
        print(f"  ❌ Failed to complete exam: {e}")
        conn.close()
        return False

    conn.close()
    print("✅ Exam simulation test PASSED\n")
    return True

def test_analytics():
    """Test analytics functionality"""
    print("🔍 Testing Analytics...")

    conn = get_db_connection()

    # Test overall statistics
    try:
        total_attempts = conn.execute('SELECT COUNT(*) FROM exam_attempts WHERE completed = 1').fetchone()[0]
        total_students = conn.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0').fetchone()[0]
        total_questions = conn.execute('SELECT COUNT(*) FROM questions').fetchone()[0]

        print(f"  ✅ Overall statistics retrieved:")
        print(f"    - Total completed attempts: {total_attempts}")
        print(f"    - Total students: {total_students}")
        print(f"    - Total questions: {total_questions}")

    except Exception as e:
        print(f"  ❌ Failed to retrieve overall statistics: {e}")
        conn.close()
        return False

    # Test domain performance
    try:
        domain_stats = conn.execute('''
            SELECT q.domain,
                   COUNT(*) as total,
                   SUM(CASE WHEN ea.is_correct THEN 1 ELSE 0 END) as correct
            FROM exam_answers ea
            JOIN questions q ON ea.question_id = q.id
            GROUP BY q.domain
        ''').fetchall()

        if domain_stats:
            print(f"  ✅ Domain performance statistics:")
            for stat in domain_stats:
                score = (stat['correct'] / stat['total']) * 100 if stat['total'] > 0 else 0
                print(f"    - {stat['domain']}: {score:.1f}% ({stat['correct']}/{stat['total']})")
        else:
            print(f"  ⚠️ No domain performance data (expected for new installation)")

    except Exception as e:
        print(f"  ❌ Failed to retrieve domain statistics: {e}")
        conn.close()
        return False

    # Test student performance tracking
    try:
        student_performance = conn.execute('''
            SELECT u.email,
                   COUNT(ea.id) as attempts,
                   AVG(ea.score_percentage) as avg_score
            FROM users u
            LEFT JOIN exam_attempts ea ON u.id = ea.user_id AND ea.completed = 1
            WHERE u.is_admin = 0
            GROUP BY u.id, u.email
        ''').fetchall()

        if student_performance:
            print(f"  ✅ Student performance tracking:")
            for performance in student_performance:
                avg_score = performance['avg_score'] if performance['avg_score'] else 0
                print(f"    - {performance['email']}: {performance['attempts']} attempts, {avg_score:.1f}% avg score")

    except Exception as e:
        print(f"  ❌ Failed to retrieve student performance: {e}")
        conn.close()
        return False

    conn.close()
    print("✅ Analytics test PASSED\n")
    return True

def test_data_validation():
    """Test data validation and edge cases"""
    print("🔍 Testing Data Validation...")

    conn = get_db_connection()

    # Test duplicate email handling
    try:
        test_email = "duplicate@test.com"

        # Add first user
        conn.execute('''
            INSERT INTO users (email, access_token, access_expiry, is_admin)
            VALUES (?, ?, ?, ?)
        ''', (test_email, str(uuid.uuid4()), '2025-12-31', False))
        conn.commit()

        # Try to add duplicate
        try:
            conn.execute('''
                INSERT INTO users (email, access_token, access_expiry, is_admin)
                VALUES (?, ?, ?, ?)
            ''', (test_email, str(uuid.uuid4()), '2025-12-31', False))
            conn.commit()
            print(f"  ❌ Duplicate email not prevented")
            conn.close()
            return False
        except sqlite3.IntegrityError:
            print(f"  ✅ Duplicate email properly prevented")

    except Exception as e:
        print(f"  ❌ Email validation test failed: {e}")
        conn.close()
        return False

    # Test expired access token
    try:
        expired_email = "expired@test.com"
        expired_token = str(uuid.uuid4())
        expired_date = "2020-01-01"  # Past date

        conn.execute('''
            INSERT INTO users (email, access_token, access_expiry, is_admin)
            VALUES (?, ?, ?, ?)
        ''', (expired_email, expired_token, expired_date, False))
        conn.commit()

        from app import validate_access_token
        user = validate_access_token(expired_token)

        if user is None:
            print(f"  ✅ Expired access token properly rejected")
        else:
            print(f"  ❌ Expired access token not rejected")
            conn.close()
            return False

    except Exception as e:
        print(f"  ❌ Expired token test failed: {e}")
        conn.close()
        return False

    # Test question data integrity
    try:
        questions = conn.execute('SELECT * FROM questions').fetchall()

        validation_errors = []
        for question in questions:
            # Check required fields
            if not question['question_text'] or len(question['question_text'].strip()) == 0:
                validation_errors.append(f"Empty question text for ID {question['id']}")

            # Check answer options
            for option in ['option_a', 'option_b', 'option_c', 'option_d']:
                if not question[option] or len(question[option].strip()) == 0:
                    validation_errors.append(f"Empty option {option} for question ID {question['id']}")

            # Check correct answer
            if question['correct_answer'] not in ['A', 'B', 'C', 'D']:
                validation_errors.append(f"Invalid correct answer '{question['correct_answer']}' for question ID {question['id']}")

            # Check domain
            if question['domain'] not in ['People', 'Process', 'Business Environment']:
                validation_errors.append(f"Invalid domain '{question['domain']}' for question ID {question['id']}")

            # Check difficulty
            if question['difficulty'] not in ['Easy', 'Medium', 'Hard']:
                validation_errors.append(f"Invalid difficulty '{question['difficulty']}' for question ID {question['id']}")

        if validation_errors:
            print(f"  ❌ Question data validation errors:")
            for error in validation_errors[:5]:  # Show first 5 errors
                print(f"    - {error}")
            if len(validation_errors) > 5:
                print(f"    - ... and {len(validation_errors) - 5} more errors")
            conn.close()
            return False
        else:
            print(f"  ✅ Question data validation passed for {len(questions)} questions")

    except Exception as e:
        print(f"  ❌ Question validation test failed: {e}")
        conn.close()
        return False

    conn.close()
    print("✅ Data validation test PASSED\n")
    return True

def run_all_tests():
    """Run all tests"""
    print("🎯 PMP Exam Simulator - Comprehensive Test Suite")
    print("=" * 50)

    tests = [
        ("Database Initialization", test_database_initialization),
        ("Question Import", test_question_import),
        ("Student Management", test_student_management),
        ("Exam Templates", test_exam_templates),
        ("Exam Simulation", test_exam_simulation),
        ("Analytics", test_analytics),
        ("Data Validation", test_data_validation),
    ]

    passed = 0
    failed = 0

    for test_name, test_function in tests:
        try:
            if test_function():
                passed += 1
            else:
                failed += 1
                print(f"❌ {test_name} FAILED\n")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} FAILED with exception: {e}\n")

    print("=" * 50)
    print(f"🎯 TEST SUMMARY")
    print(f"✅ Tests Passed: {passed}")
    print(f"❌ Tests Failed: {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed)*100):.1f}%")

    if failed == 0:
        print("🎉 ALL TESTS PASSED! Application is ready for deployment.")
    else:
        print("⚠️ Some tests failed. Please review and fix issues before deployment.")

    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)