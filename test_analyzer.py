
from analyzer import analyze_resume
import json

sample_resume = """
Python Developer Intern
Skills: Python, Flask, SQL, Git, HTML, CSS.
Projects: Built an expense tracker using Python and CSV files.
Education: B.Tech Computer Science, currently pursuing.
"""

sample_job_description = """
Looking for a Python developer intern with Python, Flask, SQL,
REST APIs, Git, debugging, and problem-solving skills.
"""

try:
    result = analyze_resume(sample_resume, sample_job_description)

    print("\nAnalysis successful!\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"\nAnalysis failed: {e}")
