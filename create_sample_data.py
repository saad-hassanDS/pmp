import pandas as pd

# Sample PMP questions data
questions_data = [
    {
        'Question': 'What is the primary responsibility of a project manager?',
        'Option A': 'To write code',
        'Option B': 'To manage project constraints',
        'Option C': 'To design architecture',
        'Option D': 'To test software',
        'Correct Answer': 'B',
        'Explanation': 'Project managers are responsible for managing project constraints including scope, time, cost, and quality.',
        'Domain': 'People',
        'Task': 'Project Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which process group includes the Close Project or Phase process?',
        'Option A': 'Initiating',
        'Option B': 'Planning',
        'Option C': 'Executing',
        'Option D': 'Closing',
        'Correct Answer': 'D',
        'Explanation': 'The Close Project or Phase process is part of the Closing process group.',
        'Domain': 'Process',
        'Task': 'Project Closure',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'What is the purpose of a stakeholder register?',
        'Option A': 'To track project costs',
        'Option B': 'To identify and document stakeholder information',
        'Option C': 'To schedule meetings',
        'Option D': 'To allocate resources',
        'Correct Answer': 'B',
        'Explanation': 'A stakeholder register identifies and documents relevant information regarding project stakeholders.',
        'Domain': 'People',
        'Task': 'Stakeholder Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which document defines the detailed project scope?',
        'Option A': 'Project charter',
        'Option B': 'Scope management plan',
        'Option C': 'Work breakdown structure',
        'Option D': 'Project scope statement',
        'Correct Answer': 'D',
        'Explanation': 'The project scope statement document defines the detailed project scope.',
        'Domain': 'Process',
        'Task': 'Scope Management',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'What is servant leadership in project management?',
        'Option A': 'Leading by authority',
        'Option B': 'Leading by serving the team',
        'Option C': 'Leading by control',
        'Option D': 'Leading by delegation',
        'Correct Answer': 'B',
        'Explanation': 'Servant leadership focuses on serving the team and helping them succeed.',
        'Domain': 'People',
        'Task': 'Leadership',
        'Difficulty': 'Hard'
    },
    {
        'Question': 'Which technique is used for schedule compression?',
        'Option A': 'Resource leveling',
        'Option B': 'Fast tracking',
        'Option C': 'Quality control',
        'Option D': 'Risk assessment',
        'Correct Answer': 'B',
        'Explanation': 'Fast tracking is a schedule compression technique that performs activities in parallel.',
        'Domain': 'Process',
        'Task': 'Schedule Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What does RACI matrix stand for?',
        'Option A': 'Resource Allocation Chart Index',
        'Option B': 'Responsible, Accountable, Consulted, Informed',
        'Option C': 'Risk Assessment Control Index',
        'Option D': 'Requirements Analysis Control Items',
        'Correct Answer': 'B',
        'Explanation': 'RACI stands for Responsible, Accountable, Consulted, Informed.',
        'Domain': 'People',
        'Task': 'Team Management',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'Which is a characteristic of adaptive project life cycle?',
        'Option A': 'Fixed requirements',
        'Option B': 'Iterative approach',
        'Option C': 'Predictive planning',
        'Option D': 'Sequential phases',
        'Correct Answer': 'B',
        'Explanation': 'Adaptive project life cycles are characterized by iterative and incremental approaches.',
        'Domain': 'Process',
        'Task': 'Project Life Cycle',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the purpose of lessons learned register?',
        'Option A': 'To track project costs',
        'Option B': 'To document knowledge gained',
        'Option C': 'To schedule activities',
        'Option D': 'To manage risks',
        'Correct Answer': 'B',
        'Explanation': 'The lessons learned register documents knowledge gained throughout the project.',
        'Domain': 'Process',
        'Task': 'Knowledge Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which environmental factor affects project management?',
        'Option A': 'Team skills only',
        'Option B': 'Organizational culture',
        'Option C': 'Project charter',
        'Option D': 'Work breakdown structure',
        'Correct Answer': 'B',
        'Explanation': 'Organizational culture is an enterprise environmental factor that affects project management.',
        'Domain': 'Business Environment',
        'Task': 'Organizational Factors',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the difference between lead and lag in scheduling?',
        'Option A': 'Lead accelerates successor, lag delays successor',
        'Option B': 'Lead delays successor, lag accelerates successor',
        'Option C': 'They are the same',
        'Option D': 'Neither affects scheduling',
        'Correct Answer': 'A',
        'Explanation': 'Lead time accelerates the successor activity while lag time delays it.',
        'Domain': 'Process',
        'Task': 'Schedule Management',
        'Difficulty': 'Hard'
    },
    {
        'Question': 'Which conflict resolution technique provides temporary solution?',
        'Option A': 'Confronting',
        'Option B': 'Smoothing',
        'Option C': 'Forcing',
        'Option D': 'Collaborating',
        'Correct Answer': 'C',
        'Explanation': 'Forcing provides a temporary solution by pushing one viewpoint at the expense of others.',
        'Domain': 'People',
        'Task': 'Conflict Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the purpose of quality metrics?',
        'Option A': 'To measure project performance',
        'Option B': 'To define quality standards',
        'Option C': 'To control scope',
        'Option D': 'To manage stakeholders',
        'Correct Answer': 'A',
        'Explanation': 'Quality metrics are used to measure and track project performance against quality objectives.',
        'Domain': 'Process',
        'Task': 'Quality Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which is an example of organizational process asset?',
        'Option A': 'Company policies',
        'Option B': 'Market conditions',
        'Option C': 'Government regulations',
        'Option D': 'Competitor analysis',
        'Correct Answer': 'A',
        'Explanation': 'Company policies, procedures, and guidelines are organizational process assets.',
        'Domain': 'Business Environment',
        'Task': 'Organizational Assets',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'What is the primary focus of risk management?',
        'Option A': 'Eliminating all risks',
        'Option B': 'Maximizing opportunities and minimizing threats',
        'Option C': 'Avoiding project execution',
        'Option D': 'Increasing project scope',
        'Correct Answer': 'B',
        'Explanation': 'Risk management focuses on maximizing opportunities and minimizing the impact of threats.',
        'Domain': 'Process',
        'Task': 'Risk Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the purpose of a project charter?',
        'Option A': 'To define detailed requirements',
        'Option B': 'To formally authorize the project',
        'Option C': 'To create work breakdown structure',
        'Option D': 'To manage project risks',
        'Correct Answer': 'B',
        'Explanation': 'A project charter formally authorizes the existence of a project.',
        'Domain': 'Process',
        'Task': 'Project Authorization',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'Which communication method is most effective for complex information?',
        'Option A': 'Email',
        'Option B': 'Face-to-face meeting',
        'Option C': 'Text message',
        'Option D': 'Phone call',
        'Correct Answer': 'B',
        'Explanation': 'Face-to-face meetings are most effective for complex information due to immediate feedback.',
        'Domain': 'People',
        'Task': 'Communication Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the triple constraint in project management?',
        'Option A': 'Time, cost, quality',
        'Option B': 'Scope, time, cost',
        'Option C': 'Risk, quality, scope',
        'Option D': 'Team, budget, schedule',
        'Correct Answer': 'B',
        'Explanation': 'The triple constraint consists of scope, time, and cost.',
        'Domain': 'Process',
        'Task': 'Project Constraints',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'Which is a characteristic of a functional organization?',
        'Option A': 'Project manager has full authority',
        'Option B': 'Team members report to functional managers',
        'Option C': 'Matrix structure is used',
        'Option D': 'Project-focused structure',
        'Correct Answer': 'B',
        'Explanation': 'In functional organizations, team members report to functional managers.',
        'Domain': 'Business Environment',
        'Task': 'Organizational Structure',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the purpose of earned value management?',
        'Option A': 'To track team performance',
        'Option B': 'To measure project progress and performance',
        'Option C': 'To manage stakeholder expectations',
        'Option D': 'To control project risks',
        'Correct Answer': 'B',
        'Explanation': 'Earned value management measures project progress and performance against the baseline.',
        'Domain': 'Process',
        'Task': 'Performance Measurement',
        'Difficulty': 'Hard'
    }
]

# Create DataFrame and save to Excel
df = pd.DataFrame(questions_data)
df.to_excel('sample_questions.xlsx', index=False)
print(f"Created sample_questions.xlsx with {len(questions_data)} questions")