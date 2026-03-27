# PMP Exam Practice Simulator

A comprehensive web-based application for PMP certification exam practice, built with Streamlit.

## Features

### For Students
- **Magic Link Authentication** - Secure email-based login
- **Multiple Exam Types** - Practice different PMP domains
- **Timer-based Exams** - Realistic exam simulation
- **Detailed Analytics** - Performance tracking by domain and difficulty
- **Question Review** - Review answers with explanations
- **Progress Tracking** - Track improvement over time

### For Administrators
- **Student Management** - Add/remove students, manage access
- **Question Bank Management** - Upload, edit, and organize questions
- **Excel Import** - Bulk import questions from Excel files
- **Exam Template Configuration** - Create custom exam types
- **Analytics Dashboard** - Monitor student performance
- **Access Control** - Time-limited student access

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bhati_work
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   - Open your browser to `http://localhost:8501`
   - For admin access, click "Admin Login" on the main page
   - For student access, request a magic link with a registered email

### Initial Setup

1. **Admin Access**: Use the "Admin Login" button for initial setup
2. **Import Questions**: Upload the provided `converted_questions.xlsx` file
3. **Add Students**: Use the Student Management section to add student emails
4. **Configure Exams**: Exam templates are pre-configured but can be modified

## Question Import Format

The application expects Excel files with the following columns:

| Column | Description |
|--------|-------------|
| Question | The question text |
| Option A | First answer option |
| Option B | Second answer option |
| Option C | Third answer option |
| Option D | Fourth answer option |
| Correct Answer | The correct option (A, B, C, or D) |
| Explanation | Detailed explanation of the answer |
| Domain | PMP domain (People, Process, Business Environment) |
| Task | Specific PMP task/topic |
| Difficulty | Question difficulty (Easy, Medium, Hard) |

## Deployment

### Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial PMP Exam Simulator"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the `app.py` file as the main file
   - Deploy

### Other Platforms

The application can be deployed on:
- **Heroku** (with Procfile)
- **Railway**
- **Render**
- **DigitalOcean App Platform**

## Architecture

### Database Schema
- **Users** - Student and admin accounts with access control
- **Questions** - Question bank with metadata
- **Exam Templates** - Predefined exam configurations
- **Exam Attempts** - Student attempt records
- **Exam Answers** - Individual question responses

### Key Components
- **Authentication System** - Magic link email authentication
- **Exam Engine** - Randomized question selection and shuffling
- **Timer System** - Configurable countdown timers
- **Analytics Engine** - Performance tracking and reporting
- **Import System** - Excel file processing

## Security Features

- Email-based authentication (no passwords)
- Access expiry enforcement
- Admin-only editing rights
- Server-side question storage
- Session management

## Configuration

### Environment Variables
- `SMTP_SERVER` - Email server for magic links (optional)
- `SMTP_PORT` - Email server port (optional)
- `SMTP_USERNAME` - Email username (optional)
- `SMTP_PASSWORD` - Email password (optional)

### Default Settings
- **Admin Email**: admin@pmp.com
- **Default Access**: 3 months
- **Database**: SQLite (pmp_simulator.db)

## Support

For technical support or feature requests, please contact the development team.

## License

This project is proprietary software for PMP certification training purposes.