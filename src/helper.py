import re
import pdfplumber

SKILLS_DB = [
    # Programming
    "Python","Java","JavaScript","TypeScript","C++","C#","C","Go","Rust","Ruby","PHP","Swift","Kotlin","R","Scala","MATLAB",
    # Web
    "React","Angular","Vue","Node.js","Django","Flask","FastAPI","Spring","HTML","CSS","REST API","GraphQL","Next.js","Express",
    # Data & ML
    "Machine Learning","Deep Learning","NLP","TensorFlow","PyTorch","Keras","Scikit-learn","Pandas","NumPy","Data Analysis",
    "Computer Vision","OpenCV","Hugging Face","BERT","LLM","Data Science","Statistics","Power BI","Tableau","Excel",
    # Cloud & DevOps
    "AWS","Azure","GCP","Docker","Kubernetes","CI/CD","Git","GitHub","Linux","Jenkins","Terraform","Ansible",
    # Databases
    "SQL","MySQL","PostgreSQL","MongoDB","Redis","Firebase","SQLite","Oracle","Cassandra","DynamoDB","Elasticsearch",
    # Tools & Others
    "Agile","Scrum","Jira","Figma","Postman","Selenium","Spark","Hadoop","Kafka","Airflow","Unity","Android","iOS",
    "Machine Learning","Leadership","Communication","Project Management","Problem Solving",
]

EDUCATION_KEYWORDS = ["b.tech","m.tech","btech","mtech","b.e","m.e","bca","mca","b.sc","m.sc","mba","phd",
                       "bachelor","master","degree","engineering","computer science","information technology",
                       "b.com","b.a","diploma","12th","10th","hsc","ssc","pgdm"]

ROLE_KEYWORDS = {
    "Data Scientist": ["machine learning","deep learning","nlp","tensorflow","pytorch","pandas","data science","statistics"],
    "ML Engineer": ["machine learning","tensorflow","pytorch","keras","mlops","model","computer vision","llm"],
    "Full Stack Developer": ["react","node.js","django","flask","fastapi","mongodb","express","full stack"],
    "Software Engineer": ["java","c++","python","golang","c#","software engineering","data structures"],
    "Python Developer": ["python","django","flask","fastapi","celery"],
    "Frontend Developer": ["react","angular","vue","html","css","javascript","typescript","frontend"],
    "DevOps Engineer": ["aws","azure","gcp","docker","kubernetes","ci/cd","terraform","ansible","jenkins"],
    "Data Analyst": ["sql","excel","tableau","power bi","data analysis","statistics"],
    "Backend Developer": ["java","python","node.js","go","sql","mongodb","redis","kafka","backend","rest api"],
    "Android Developer": ["android","kotlin","java","android studio","jetpack compose"],
    "iOS Developer": ["ios","swift","objective-c","xcode"],
    "UI UX Designer": ["figma","adobe xd","sketch","ui/ux","user interface","wireframe"],
    "Product Manager": ["product management","agile","scrum","jira","roadmap"],
    "Cloud Engineer": ["aws","azure","gcp","cloud","terraform","docker","kubernetes"],
    "Cybersecurity Engineer": ["security","penetration testing","kalilinux","firewall","cybersecurity","network"],
    "QA Engineer": ["selenium","appium","testing","qa","quality assurance","test automation"],
}

def extract_text_from_pdf(uploaded_file) -> str:
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages).strip()
    except Exception as e:
        return f"Error reading PDF: {e}"


def analyze_resume(text: str) -> dict:
    lower = text.lower()
    lines = text.split("\n")

    # Name — first non-empty line that looks like a name
    name = ""
    for line in lines[:8]:
        line = line.strip()
        if 2 < len(line) < 50 and not any(c.isdigit() for c in line) and "@" not in line:
            name = line
            break

    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    email = email_match.group() if email_match else ""

    # Phone
    phone_match = re.search(r'(\+91[\s-]?)?[6-9]\d{9}', text)
    phone = phone_match.group() if phone_match else ""

    # Skills
    found_skills = []
    for skill in SKILLS_DB:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            if skill not in found_skills:
                found_skills.append(skill)

    # Years of experience
    exp_patterns = [
        r'(\d+)\+?\s*years?\s*of\s*(experience|exp)',
        r'(\d+)\+?\s*years?\s*experience',
        r'experience\s*of\s*(\d+)\+?\s*years?',
    ]
    years = 0
    for pat in exp_patterns:
        m = re.search(pat, lower)
        if m:
            years = int(m.group(1))
            break

    # Education
    education = ""
    for line in lines:
        ll = line.lower()
        for kw in EDUCATION_KEYWORDS:
            if kw in ll:
                education = line.strip()[:60]
                break
    # Predict role based on max matching skills
    predicted_role = "Software Engineer"
    max_matches = 0
    skills_lower = [s.lower() for s in found_skills]
    for role, kw in ROLE_KEYWORDS.items():
        matches = sum(1 for k in kw if k in lower or k in skills_lower)
        if matches > max_matches:
            max_matches = matches
            predicted_role = role

    return {
        "name": name or "Candidate",
        "email": email,
        "phone": phone,
        "skills": found_skills,
        "years_experience": years if years else "N/A",
        "education": education or "Not detected",
        "predicted_role": predicted_role,
    }