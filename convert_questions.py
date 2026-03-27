import pandas as pd

# Read the sample question file
df = pd.read_csv('questions_extracted_easyocr.csv')

# Convert to our expected format
converted_questions = []

for _, row in df.iterrows():
    # Handle the case where there might be Option E or not
    question_data = {
        'Question': row['Question Statement'],
        'Option A': row['Option A'],
        'Option B': row['Option B'],
        'Option C': row['Option C'],
        'Option D': row['Option D'],
        'Correct Answer': row['Correct Option'],
        'Explanation': row['Rationale'],
        'Domain': 'Process',  # We'll assign domains based on content
        'Task': 'Risk Management',  # Based on the question content
        'Difficulty': 'Hard'  # Based on complexity
    }
    converted_questions.append(question_data)

# Add more PMP questions to expand the database
additional_questions = [
    {
        'Question': 'What is the primary responsibility of a project manager?',
        'Option A': 'To write detailed technical specifications',
        'Option B': 'To manage project constraints and deliver value',
        'Option C': 'To design system architecture',
        'Option D': 'To perform quality assurance testing',
        'Correct Answer': 'B',
        'Explanation': 'Project managers are responsible for managing project constraints (scope, time, cost, quality, resources, and risk) and ensuring the project delivers value to stakeholders.',
        'Domain': 'People',
        'Task': 'Project Leadership',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which process group includes the Close Project or Phase process?',
        'Option A': 'Initiating Process Group',
        'Option B': 'Planning Process Group',
        'Option C': 'Executing Process Group',
        'Option D': 'Closing Process Group',
        'Correct Answer': 'D',
        'Explanation': 'The Close Project or Phase process is part of the Closing Process Group and involves finalizing all activities across all process groups.',
        'Domain': 'Process',
        'Task': 'Project Integration Management',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'What is the purpose of a stakeholder register?',
        'Option A': 'To track project budget and expenses',
        'Option B': 'To identify and document stakeholder information and engagement strategies',
        'Option C': 'To schedule team meetings and workshops',
        'Option D': 'To allocate human resources to tasks',
        'Correct Answer': 'B',
        'Explanation': 'The stakeholder register identifies and documents relevant information about project stakeholders, including their interests, involvement levels, and engagement strategies.',
        'Domain': 'People',
        'Task': 'Stakeholder Engagement',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which document formally authorizes a project?',
        'Option A': 'Project Management Plan',
        'Option B': 'Statement of Work',
        'Option C': 'Project Charter',
        'Option D': 'Business Case',
        'Correct Answer': 'C',
        'Explanation': 'The project charter is the document that formally authorizes the existence of a project and provides the project manager with the authority to apply organizational resources.',
        'Domain': 'Process',
        'Task': 'Project Authorization',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'What is servant leadership in the context of project management?',
        'Option A': 'Leading through authority and control',
        'Option B': 'Leading by serving the team and removing obstacles',
        'Option C': 'Leading through detailed micromanagement',
        'Option D': 'Leading by delegating all responsibilities',
        'Correct Answer': 'B',
        'Explanation': 'Servant leadership focuses on serving the team members by removing obstacles, facilitating their work, and helping them achieve their potential.',
        'Domain': 'People',
        'Task': 'Team Leadership',
        'Difficulty': 'Hard'
    },
    {
        'Question': 'Which technique is used for schedule compression?',
        'Option A': 'Resource smoothing',
        'Option B': 'Fast tracking and crashing',
        'Option C': 'Quality gate reviews',
        'Option D': 'Risk register updates',
        'Correct Answer': 'B',
        'Explanation': 'Fast tracking (performing activities in parallel) and crashing (adding resources) are the two main schedule compression techniques.',
        'Domain': 'Process',
        'Task': 'Schedule Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What does RACI matrix stand for?',
        'Option A': 'Resource Allocation and Control Index',
        'Option B': 'Responsible, Accountable, Consulted, Informed',
        'Option C': 'Risk Assessment and Communication Interface',
        'Option D': 'Requirements Analysis and Change Integration',
        'Correct Answer': 'B',
        'Explanation': 'RACI matrix stands for Responsible (who does the work), Accountable (who signs off), Consulted (who provides input), and Informed (who is kept updated).',
        'Domain': 'People',
        'Task': 'Team Management',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'Which organizational structure gives the project manager the most authority?',
        'Option A': 'Functional Organization',
        'Option B': 'Weak Matrix Organization',
        'Option C': 'Projectized Organization',
        'Option D': 'Strong Matrix Organization',
        'Correct Answer': 'C',
        'Explanation': 'In a projectized organization, the project manager has full authority over the project team and resources.',
        'Domain': 'Business Environment',
        'Task': 'Organizational Structures',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the purpose of the lessons learned register?',
        'Option A': 'To track project costs and budget variances',
        'Option B': 'To document knowledge gained during the project for future use',
        'Option C': 'To schedule recurring team meetings',
        'Option D': 'To manage project scope changes',
        'Correct Answer': 'B',
        'Explanation': 'The lessons learned register documents knowledge gained throughout the project that can be used to improve future project performance.',
        'Domain': 'Process',
        'Task': 'Knowledge Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which is an example of an enterprise environmental factor?',
        'Option A': 'Project charter',
        'Option B': 'Work breakdown structure',
        'Option C': 'Organizational culture and government regulations',
        'Option D': 'Project management plan',
        'Correct Answer': 'C',
        'Explanation': 'Enterprise environmental factors include organizational culture, government regulations, market conditions, and other external factors that influence the project.',
        'Domain': 'Business Environment',
        'Task': 'Environmental Factors',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the difference between leads and lags in project scheduling?',
        'Option A': 'Leads accelerate successor activities, lags delay them',
        'Option B': 'Leads delay successor activities, lags accelerate them',
        'Option C': 'Both leads and lags delay activities',
        'Option D': 'There is no difference between leads and lags',
        'Correct Answer': 'A',
        'Explanation': 'A lead allows a successor activity to begin before its predecessor is complete, while a lag requires a delay between activities.',
        'Domain': 'Process',
        'Task': 'Schedule Development',
        'Difficulty': 'Hard'
    },
    {
        'Question': 'Which conflict resolution technique provides a temporary solution?',
        'Option A': 'Confronting/Problem-solving',
        'Option B': 'Compromising',
        'Option C': 'Forcing/Directing',
        'Option D': 'Collaborating',
        'Correct Answer': 'C',
        'Explanation': 'Forcing provides a temporary solution by pushing one viewpoint at the expense of others, often creating win-lose situations.',
        'Domain': 'People',
        'Task': 'Conflict Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What is the purpose of quality metrics in project management?',
        'Option A': 'To measure and track project performance against quality objectives',
        'Option B': 'To define the project scope boundaries',
        'Option C': 'To control project schedule deviations',
        'Option D': 'To manage stakeholder communications',
        'Correct Answer': 'A',
        'Explanation': 'Quality metrics are operational definitions that describe project or product attributes and how the control quality process will measure them.',
        'Domain': 'Process',
        'Task': 'Quality Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which is an example of an organizational process asset?',
        'Option A': 'Market conditions and competitive landscape',
        'Option B': 'Government regulations and industry standards',
        'Option C': 'Company policies, procedures, and historical information',
        'Option D': 'Economic conditions and geographic factors',
        'Correct Answer': 'C',
        'Explanation': 'Organizational process assets include company policies, procedures, templates, historical information, and lessons learned from previous projects.',
        'Domain': 'Business Environment',
        'Task': 'Organizational Assets',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'What is the primary focus of project risk management?',
        'Option A': 'Eliminating all project risks completely',
        'Option B': 'Maximizing positive risks (opportunities) and minimizing negative risks (threats)',
        'Option C': 'Avoiding project execution altogether',
        'Option D': 'Increasing project scope to accommodate risks',
        'Correct Answer': 'B',
        'Explanation': 'Risk management aims to maximize the probability and impact of positive events (opportunities) and minimize the probability and impact of negative events (threats).',
        'Domain': 'Process',
        'Task': 'Risk Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'Which communication method is most effective for conveying complex information?',
        'Option A': 'Email with attachments',
        'Option B': 'Interactive face-to-face communication',
        'Option C': 'Text messaging',
        'Option D': 'Voice mail messages',
        'Correct Answer': 'B',
        'Explanation': 'Interactive face-to-face communication is most effective for complex information because it allows for immediate feedback, clarification, and non-verbal communication.',
        'Domain': 'People',
        'Task': 'Communication Management',
        'Difficulty': 'Medium'
    },
    {
        'Question': 'What are the three components of the triple constraint (traditional)?',
        'Option A': 'Time, cost, and quality',
        'Option B': 'Scope, time, and cost',
        'Option C': 'Risk, quality, and scope',
        'Option D': 'Resources, budget, and schedule',
        'Correct Answer': 'B',
        'Explanation': 'The traditional triple constraint consists of scope (what work will be done), time (when the work will be completed), and cost (how much the work will cost).',
        'Domain': 'Process',
        'Task': 'Project Constraints',
        'Difficulty': 'Easy'
    },
    {
        'Question': 'What is the purpose of Earned Value Management (EVM)?',
        'Option A': 'To track team member performance ratings',
        'Option B': 'To measure project performance by comparing planned work, completed work, and costs',
        'Option C': 'To manage stakeholder expectations only',
        'Option D': 'To control project risks and issues',
        'Correct Answer': 'B',
        'Explanation': 'EVM integrates scope, schedule, and cost measures to assess project performance by comparing the amount of work planned with what is actually accomplished.',
        'Domain': 'Process',
        'Task': 'Performance Measurement',
        'Difficulty': 'Hard'
    },
    {
        'Question': 'Which tool is used to identify the critical path in a project schedule?',
        'Option A': 'Gantt Chart',
        'Option B': 'Network Diagram with CPM (Critical Path Method)',
        'Option C': 'Resource Histogram',
        'Option D': 'Responsibility Assignment Matrix',
        'Correct Answer': 'B',
        'Explanation': 'The Critical Path Method (CPM) using network diagrams calculates the longest path through the project, which determines the minimum project duration.',
        'Domain': 'Process',
        'Task': 'Schedule Development',
        'Difficulty': 'Hard'
    },
    {
        'Question': 'What is the main purpose of a project kickoff meeting?',
        'Option A': 'To close the project and document lessons learned',
        'Option B': 'To align team members and stakeholders on project objectives, roles, and expectations',
        'Option C': 'To conduct detailed risk assessments',
        'Option D': 'To finalize the project budget allocation',
        'Correct Answer': 'B',
        'Explanation': 'The kickoff meeting aligns all team members and stakeholders on project objectives, success criteria, roles, responsibilities, and expectations for the project.',
        'Domain': 'People',
        'Task': 'Team Development',
        'Difficulty': 'Easy'
    }
]

# Combine original and additional questions
all_questions = converted_questions + additional_questions

# Create DataFrame and save to Excel
df_final = pd.DataFrame(all_questions)
df_final.to_excel('converted_questions.xlsx', index=False)

print(f"Converted and created {len(all_questions)} questions")
print("File saved as: converted_questions.xlsx")