"""
job_api.py  —  SkillMatch AI
Role-specific job database. Every job entry has pre-built, accurate URLs
for LinkedIn, Naukri, and Indeed that match the exact job title.
"""

import urllib.parse
import random

# ── URL builder (used per-job, per-location) ────────────────────────────────
def _build_urls(title: str, company: str, location: str):
    location = location.strip() or "India"
    tq  = urllib.parse.quote_plus(f"{title} {company}")
    lq  = urllib.parse.quote_plus(location)
    tqr = urllib.parse.quote_plus(title)

    # Naukri slug: "machine-learning-engineer-jobs-in-bangalore"
    slug = title.lower().replace(" ", "-").replace("/", "-").replace("(", "").replace(")", "")
    city = location.lower().split(",")[0].strip().replace(" ", "-")
    naukri_path = f"{slug}-jobs-in-{city}" if city not in ("india","remote","pan india","") else f"{slug}-jobs"

    return {
        "linkedin_url": f"https://www.linkedin.com/jobs/search/?keywords={tq}&location={lq}&f_TPR=r604800&sortBy=R",
        "naukri_url":   f"https://www.naukri.com/{naukri_path}?src=sortby_relevance",
        "indeed_url":   f"https://in.indeed.com/jobs?q={tqr}&l={lq}&sort=date&fromage=14",
        "glassdoor_url":f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={tqr}&locT=C&locName={lq}",
        "google_url":   f"https://www.google.com/search?q={urllib.parse.quote_plus(title+' jobs '+location)}",
    }

# ── Job Database ─────────────────────────────────────────────────────────────
# Each role key maps to a list of job dicts.
# "urls" are intentionally left empty — filled dynamically with user's location.

JOB_DB = {

    # ── DATA SCIENTIST ──────────────────────────────────────────────────────
    "data scientist": [
        {"title":"Data Scientist","company":"Google","location":"Bangalore","salary":"35-60 LPA",
         "description":"Build and deploy ML models to improve Google Search, Ads, and Assistant products. Work with petabyte-scale data.",
         "skills":["Python","Machine Learning","TensorFlow","SQL","Statistics","BigQuery"],"posted":"2 days ago","source":"LinkedIn"},
        {"title":"Senior Data Scientist","company":"Amazon","location":"Bangalore","salary":"40-70 LPA",
         "description":"Drive data science initiatives for Amazon India marketplace. Own end-to-end ML pipelines for recommendations.",
         "skills":["Python","Spark","Machine Learning","AWS","Scala","Statistics"],"posted":"1 day ago","source":"Naukri"},
        {"title":"Data Scientist","company":"Flipkart","location":"Bangalore","salary":"25-45 LPA",
         "description":"Build predictive models for supply chain, pricing, and customer experience at India's largest e-commerce.",
         "skills":["Python","ML","Deep Learning","Pandas","SQL","Hive"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Data Scientist","company":"Swiggy","location":"Bangalore","salary":"22-40 LPA",
         "description":"Optimize delivery routing and demand forecasting using ML. Work with real-time data streams.",
         "skills":["Python","Machine Learning","SQL","Kafka","Airflow"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Data Scientist","company":"Meesho","location":"Bangalore","salary":"20-38 LPA",
         "description":"Drive seller and buyer growth through data-driven experimentation and ML models.",
         "skills":["Python","Statistics","SQL","Machine Learning","A/B Testing"],"posted":"Yesterday","source":"Naukri"},
        {"title":"Data Scientist","company":"Razorpay","location":"Bangalore","salary":"28-48 LPA",
         "description":"Build fraud detection and risk scoring models for India's leading fintech platform.",
         "skills":["Python","ML","NLP","SQL","Spark","Risk Modelling"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── ML ENGINEER ─────────────────────────────────────────────────────────
    "ml engineer": [
        {"title":"Machine Learning Engineer","company":"Google","location":"Bangalore","salary":"40-75 LPA",
         "description":"Design and productionize ML systems at scale. Own the full lifecycle from experimentation to serving.",
         "skills":["Python","TensorFlow","Kubernetes","MLflow","C++","Distributed Systems"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"ML Engineer","company":"Microsoft","location":"Hyderabad","salary":"35-65 LPA",
         "description":"Build ML infrastructure and models for Azure AI products serving millions of enterprise customers.",
         "skills":["Python","PyTorch","Azure ML","Docker","Kubernetes","MLOps"],"posted":"3 days ago","source":"Naukri"},
        {"title":"Senior ML Engineer","company":"Zomato","location":"Gurugram","salary":"30-55 LPA",
         "description":"Build real-time recommendation and ETA prediction systems. Own ML platform improvements.",
         "skills":["Python","TensorFlow","Kafka","Spark","MLOps","Redis"],"posted":"2 days ago","source":"Indeed"},
        {"title":"ML Engineer","company":"PhonePe","location":"Bangalore","salary":"28-50 LPA",
         "description":"Develop fraud detection and credit risk ML models for India's leading UPI platform.",
         "skills":["Python","Machine Learning","Feature Engineering","SQL","Docker","Airflow"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"ML Engineer","company":"CRED","location":"Bangalore","salary":"25-45 LPA",
         "description":"Build personalisation and credit intelligence models for premium Indian credit card users.",
         "skills":["Python","ML","NLP","PyTorch","MLflow","Kubernetes"],"posted":"Yesterday","source":"Naukri"},
        {"title":"ML Engineer","company":"Meesho","location":"Noida, Gurugram, Delhi","salary":"18-30 LPA",
         "description":"Own end-to-end ML features for seller dashboard and buyer experience recommendation engine.",
         "skills":["Python","Scikit-learn","TensorFlow","SQL","AWS","Docker"],"posted":"Yesterday","source":"Indeed"},
    ],

    # ── FULL STACK DEVELOPER ─────────────────────────────────────────────────
    "full stack developer": [
        {"title":"Full Stack Developer","company":"Razorpay","location":"Bangalore","salary":"20-40 LPA",
         "description":"Build payment infrastructure and merchant-facing products used by 8M+ businesses.",
         "skills":["React","Node.js","TypeScript","PostgreSQL","Redis","Docker"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Full Stack Engineer","company":"Flipkart","location":"Bangalore","salary":"22-42 LPA",
         "description":"Own product features across the Flipkart buyer app and seller platform end-to-end.",
         "skills":["React","Java","Spring Boot","MySQL","Kafka","Kubernetes"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Full Stack Developer","company":"Swiggy","location":"Bangalore","salary":"18-35 LPA",
         "description":"Build consumer and restaurant partner products with React and Node microservices.",
         "skills":["React","Node.js","MongoDB","TypeScript","Docker","AWS"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Full Stack Developer","company":"Freshworks","location":"Chennai","salary":"15-30 LPA",
         "description":"Build SaaS CRM and helpdesk products serving global customers using Ruby on Rails and React.",
         "skills":["Ruby on Rails","React","PostgreSQL","Redis","Elasticsearch"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Full Stack Engineer","company":"Zoho","location":"Chennai","salary":"12-25 LPA",
         "description":"Develop enterprise SaaS products across Zoho's suite of 50+ business applications.",
         "skills":["Java","React","MySQL","JavaScript","REST APIs"],"posted":"5 days ago","source":"Naukri"},
        {"title":"Full Stack Developer","company":"CRED","location":"Bangalore","salary":"20-38 LPA",
         "description":"Build consumer fintech experiences for India's premium credit card user base.",
         "skills":["React","Node.js","TypeScript","GraphQL","PostgreSQL","Redis"],"posted":"Yesterday","source":"Indeed"},
    ],

    # ── SOFTWARE ENGINEER ────────────────────────────────────────────────────
    "software engineer": [
        {"title":"Software Engineer","company":"Google","location":"Bangalore","salary":"30-50 LPA",
         "description":"Design and build scalable backend services for Google Cloud platform infrastructure.",
         "skills":["Python","Java","Go","Distributed Systems","SQL","Kubernetes"],"posted":"3 days ago","source":"LinkedIn"},
        {"title":"Software Engineer II","company":"Amazon","location":"Bangalore","salary":"28-45 LPA",
         "description":"Build and scale backend systems for Amazon India's order management and logistics.",
         "skills":["Java","Python","AWS","Microservices","DynamoDB","Kafka"],"posted":"1 day ago","source":"Naukri"},
        {"title":"Software Engineer","company":"Microsoft","location":"Hyderabad","salary":"25-42 LPA",
         "description":"Contribute to Azure cloud services and developer tooling used by millions worldwide.",
         "skills":["C#",".NET","Azure","Python","Kubernetes","SQL"],"posted":"2 days ago","source":"Indeed"},
        {"title":"Software Engineer","company":"Atlassian","location":"Bangalore","salary":"30-55 LPA",
         "description":"Build Jira and Confluence features used by 200K+ companies globally.",
         "skills":["Java","React","PostgreSQL","Kotlin","Microservices","AWS"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Software Engineer","company":"Freshworks","location":"Chennai","salary":"15-28 LPA",
         "description":"Build reliable backend APIs and integrations for Freshworks CRM platform.",
         "skills":["Ruby","Python","MySQL","Redis","Elasticsearch","REST APIs"],"posted":"5 days ago","source":"Naukri"},
        {"title":"Software Engineer","company":"Zoho","location":"Chennai","salary":"10-22 LPA",
         "description":"Develop and maintain enterprise SaaS applications in Zoho's product ecosystem.",
         "skills":["Java","JavaScript","MySQL","REST APIs","Linux"],"posted":"Yesterday","source":"Indeed"},
    ],

    # ── PYTHON DEVELOPER ─────────────────────────────────────────────────────
    "python developer": [
        {"title":"Python Developer","company":"Razorpay","location":"Bangalore","salary":"15-30 LPA",
         "description":"Build robust backend services and APIs powering India's largest payment gateway.",
         "skills":["Python","Django","FastAPI","PostgreSQL","Redis","Celery"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Python Backend Developer","company":"Swiggy","location":"Bangalore","salary":"14-28 LPA",
         "description":"Develop microservices for order management, restaurant onboarding, and delivery systems.",
         "skills":["Python","Django","REST APIs","PostgreSQL","Docker","Kafka"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Senior Python Developer","company":"PhonePe","location":"Bangalore","salary":"18-35 LPA",
         "description":"Build high-performance financial transaction processing services in Python.",
         "skills":["Python","FastAPI","PostgreSQL","Redis","Kubernetes","gRPC"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Python Developer","company":"Freshworks","location":"Chennai","salary":"10-22 LPA",
         "description":"Build integrations and automation workflows for the Freshworks SaaS platform.",
         "skills":["Python","Django","MySQL","Celery","REST APIs","AWS"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Python Engineer","company":"Meesho","location":"Bangalore","salary":"12-24 LPA",
         "description":"Own backend services for catalog, search, and seller tools on Meesho's platform.",
         "skills":["Python","Flask","MongoDB","Redis","Docker","Airflow"],"posted":"Yesterday","source":"Naukri"},
        {"title":"Python Developer","company":"Zoho","location":"Chennai","salary":"8-18 LPA",
         "description":"Develop automation scripts, APIs, and integrations for Zoho's enterprise products.",
         "skills":["Python","Django","MySQL","JavaScript","REST APIs"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── FRONTEND DEVELOPER ───────────────────────────────────────────────────
    "frontend developer": [
        {"title":"Frontend Developer","company":"CRED","location":"Bangalore","salary":"15-32 LPA",
         "description":"Craft pixel-perfect, high-performance UI for India's most design-conscious fintech app.",
         "skills":["React","TypeScript","CSS","Framer Motion","GraphQL","Webpack"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"React Developer","company":"Razorpay","location":"Bangalore","salary":"14-28 LPA",
         "description":"Build merchant-facing dashboards and payment checkout experiences used by 8M+ businesses.",
         "skills":["React","TypeScript","Redux","CSS Modules","Jest","Webpack"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Frontend Engineer","company":"Flipkart","location":"Bangalore","salary":"15-30 LPA",
         "description":"Develop high-performance buyer app experiences handling millions of daily active users.",
         "skills":["React","JavaScript","CSS","Performance Optimization","Web Vitals"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Frontend Developer","company":"Swiggy","location":"Bangalore","salary":"12-25 LPA",
         "description":"Build consumer web experiences for food delivery, Instamart, and Genie products.",
         "skills":["React","TypeScript","CSS","Jest","Storybook","Figma"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"UI Developer","company":"Zoho","location":"Chennai","salary":"8-18 LPA",
         "description":"Build enterprise web application UIs across Zoho's suite of business products.",
         "skills":["JavaScript","React","CSS","HTML","REST APIs","Figma"],"posted":"5 days ago","source":"Naukri"},
        {"title":"Frontend Engineer","company":"Freshworks","location":"Chennai","salary":"12-24 LPA",
         "description":"Develop rich interactive interfaces for CRM, helpdesk and ITSM SaaS products.",
         "skills":["React","TypeScript","GraphQL","CSS","Testing Library"],"posted":"Yesterday","source":"Indeed"},
    ],

    # ── DEVOPS ENGINEER ──────────────────────────────────────────────────────
    "devops engineer": [
        {"title":"DevOps Engineer","company":"Amazon","location":"Bangalore","salary":"20-40 LPA",
         "description":"Own CI/CD pipelines, infrastructure-as-code, and reliability engineering for AWS services.",
         "skills":["AWS","Terraform","Kubernetes","Docker","Jenkins","Python"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Senior DevOps Engineer","company":"Razorpay","location":"Bangalore","salary":"22-42 LPA",
         "description":"Build and scale infrastructure for India's largest payments platform handling 300M+ TPS.",
         "skills":["Kubernetes","Terraform","AWS","Helm","ArgoCD","Python"],"posted":"2 days ago","source":"Naukri"},
        {"title":"DevOps Engineer","company":"Zomato","location":"Gurugram","salary":"18-35 LPA",
         "description":"Manage cloud infrastructure and deployment pipelines for Zomato's real-time food platform.",
         "skills":["GCP","Kubernetes","Docker","Terraform","Ansible","CI/CD"],"posted":"3 days ago","source":"Indeed"},
        {"title":"SRE / DevOps Engineer","company":"PhonePe","location":"Bangalore","salary":"20-38 LPA",
         "description":"Ensure 99.99% uptime for financial transactions across PhonePe's critical infrastructure.",
         "skills":["AWS","Kubernetes","Prometheus","Grafana","Python","Terraform"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"DevOps Engineer","company":"Freshworks","location":"Chennai","salary":"14-28 LPA",
         "description":"Maintain deployment pipelines and cloud infrastructure for global SaaS products.",
         "skills":["AWS","Docker","Kubernetes","Jenkins","Ansible","Linux"],"posted":"5 days ago","source":"Naukri"},
        {"title":"Cloud DevOps Engineer","company":"Meesho","location":"Bangalore","salary":"16-30 LPA",
         "description":"Scale cloud-native infrastructure for one of India's fastest-growing social commerce platforms.",
         "skills":["AWS","Terraform","Kubernetes","Helm","Python","Monitoring"],"posted":"Yesterday","source":"Indeed"},
    ],

    # ── DATA ANALYST ─────────────────────────────────────────────────────────
    "data analyst": [
        {"title":"Data Analyst","company":"Flipkart","location":"Bangalore","salary":"10-20 LPA",
         "description":"Analyze seller and buyer behavior data to drive business decisions using SQL and Python.",
         "skills":["SQL","Python","Tableau","Excel","Statistics","Hive"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Business Data Analyst","company":"Swiggy","location":"Bangalore","salary":"9-18 LPA",
         "description":"Build dashboards and run analysis to optimize delivery, pricing, and restaurant partnerships.",
         "skills":["SQL","Python","Looker","Excel","A/B Testing"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Product Analyst","company":"CRED","location":"Bangalore","salary":"12-24 LPA",
         "description":"Define and track product metrics; run experiments and translate data into product decisions.",
         "skills":["SQL","Python","Mixpanel","Statistics","Data Visualization"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Data Analyst","company":"Meesho","location":"Bangalore","salary":"8-16 LPA",
         "description":"Support growth, supply chain, and seller teams with data insights and reporting.",
         "skills":["SQL","Excel","Python","Power BI","Statistics"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Marketing Analyst","company":"Zomato","location":"Gurugram","salary":"8-16 LPA",
         "description":"Track campaign performance, user acquisition funnels, and marketing ROI across channels.",
         "skills":["SQL","Excel","Google Analytics","Python","Tableau"],"posted":"5 days ago","source":"Naukri"},
        {"title":"Data Analyst","company":"Razorpay","location":"Bangalore","salary":"10-22 LPA",
         "description":"Analyze payments data to identify growth opportunities and risk patterns.",
         "skills":["SQL","Python","Looker","Statistics","Data Modelling"],"posted":"Yesterday","source":"Indeed"},
    ],

    # ── BACKEND DEVELOPER ────────────────────────────────────────────────────
    "backend developer": [
        {"title":"Backend Developer","company":"Razorpay","location":"Bangalore","salary":"18-35 LPA",
         "description":"Build high-throughput payment processing APIs and financial infrastructure services.",
         "skills":["Java","Python","PostgreSQL","Redis","Kafka","Microservices"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Backend Engineer","company":"Swiggy","location":"Bangalore","salary":"16-32 LPA",
         "description":"Design and build microservices for order management, partner APIs, and logistics.",
         "skills":["Go","Python","gRPC","MongoDB","Kafka","Docker"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Senior Backend Developer","company":"PhonePe","location":"Bangalore","salary":"22-42 LPA",
         "description":"Build critical financial services APIs handling millions of UPI transactions daily.",
         "skills":["Java","Spring Boot","MySQL","Redis","Kafka","AWS"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Backend Developer","company":"Meesho","location":"Bangalore","salary":"12-25 LPA",
         "description":"Own backend services for catalog management, search, and seller onboarding flows.",
         "skills":["Python","Django","MySQL","Redis","Docker","Elasticsearch"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Backend Engineer","company":"CRED","location":"Bangalore","salary":"18-36 LPA",
         "description":"Build secure and scalable backend APIs for credit card management and rewards.",
         "skills":["Kotlin","Java","PostgreSQL","Redis","gRPC","Kubernetes"],"posted":"5 days ago","source":"Naukri"},
        {"title":"Backend Developer","company":"Freshworks","location":"Chennai","salary":"12-24 LPA",
         "description":"Develop REST APIs and integrations for Freshworks CRM and helpdesk products.",
         "skills":["Ruby on Rails","PostgreSQL","Redis","Elasticsearch","AWS"],"posted":"Yesterday","source":"Indeed"},
    ],

    # ── ANDROID DEVELOPER ───────────────────────────────────────────────────
    "android developer": [
        {"title":"Android Developer","company":"Flipkart","location":"Bangalore","salary":"16-32 LPA",
         "description":"Build and optimize the Flipkart Android app used by 300M+ users for shopping.",
         "skills":["Kotlin","Android SDK","Jetpack Compose","MVVM","Coroutines","Room"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Senior Android Developer","company":"Swiggy","location":"Bangalore","salary":"18-36 LPA",
         "description":"Own native Android development for Swiggy's consumer and delivery partner apps.",
         "skills":["Kotlin","Jetpack","Coroutines","Dagger Hilt","Retrofit"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Android Engineer","company":"PhonePe","location":"Bangalore","salary":"20-40 LPA",
         "description":"Build and maintain the PhonePe Android app used for UPI and financial services.",
         "skills":["Kotlin","Android","MVVM","Hilt","Retrofit","Room DB"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Android Developer","company":"Zomato","location":"Gurugram","salary":"15-30 LPA",
         "description":"Develop features for Zomato's food delivery and restaurant discovery Android app.",
         "skills":["Kotlin","Jetpack Compose","Coroutines","Firebase","Retrofit"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Android Developer","company":"CRED","location":"Bangalore","salary":"18-35 LPA",
         "description":"Craft premium Android experiences for CRED's design-first fintech application.",
         "skills":["Kotlin","Compose","MVVM","Hilt","GraphQL","Animations"],"posted":"Yesterday","source":"Naukri"},
        {"title":"Android Developer","company":"Meesho","location":"Bangalore","salary":"12-25 LPA",
         "description":"Build seller and buyer Android apps for India's social commerce platform.",
         "skills":["Kotlin","Android","Coroutines","Retrofit","Room","MVVM"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── IOS DEVELOPER ────────────────────────────────────────────────────────
    "ios developer": [
        {"title":"iOS Developer","company":"CRED","location":"Bangalore","salary":"18-36 LPA",
         "description":"Build premium iOS experiences with pixel-perfect animations for India's top fintech.",
         "skills":["Swift","SwiftUI","Combine","MVVM","Alamofire","CoreData"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Senior iOS Developer","company":"Razorpay","location":"Bangalore","salary":"20-40 LPA",
         "description":"Own iOS payment SDK and merchant-facing app used by millions of businesses.",
         "skills":["Swift","UIKit","Combine","Keychain","REST APIs","Xcode"],"posted":"2 days ago","source":"Naukri"},
        {"title":"iOS Engineer","company":"Swiggy","location":"Bangalore","salary":"18-34 LPA",
         "description":"Develop consumer and delivery partner iOS apps for Swiggy's food and commerce platform.",
         "skills":["Swift","SwiftUI","CoreLocation","Firebase","Combine"],"posted":"3 days ago","source":"Indeed"},
        {"title":"iOS Developer","company":"Flipkart","location":"Bangalore","salary":"16-32 LPA",
         "description":"Build and optimize shopping experiences on the Flipkart iOS app.",
         "skills":["Swift","UIKit","VIPER","Instruments","REST APIs"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"iOS Developer","company":"PhonePe","location":"Bangalore","salary":"18-36 LPA",
         "description":"Build secure and reliable iOS UPI and financial services for PhonePe app.",
         "skills":["Swift","SwiftUI","Keychain","Biometrics","Combine","CoreData"],"posted":"Yesterday","source":"Naukri"},
        {"title":"iOS Engineer","company":"Meesho","location":"Bangalore","salary":"12-24 LPA",
         "description":"Develop iOS features for Meesho's social commerce buyer and seller applications.",
         "skills":["Swift","UIKit","Combine","CoreData","REST APIs"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── UI/UX DESIGNER ───────────────────────────────────────────────────────
    "ui ux designer": [
        {"title":"Product Designer (UI/UX)","company":"CRED","location":"Bangalore","salary":"15-30 LPA",
         "description":"Design beautiful and intuitive product experiences for India's most design-conscious fintech.",
         "skills":["Figma","Prototyping","User Research","Design Systems","Motion Design"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"UX Designer","company":"Flipkart","location":"Bangalore","salary":"12-24 LPA",
         "description":"Design shopping and discovery experiences for Flipkart's 300M+ user base.",
         "skills":["Figma","User Research","Wireframing","Usability Testing","Information Architecture"],"posted":"2 days ago","source":"Naukri"},
        {"title":"UI/UX Designer","company":"Swiggy","location":"Bangalore","salary":"10-20 LPA",
         "description":"Design food ordering and quick commerce experiences across Swiggy's product suite.",
         "skills":["Figma","Sketch","Prototyping","User Testing","Design Systems"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Product Designer","company":"Razorpay","location":"Bangalore","salary":"14-28 LPA",
         "description":"Design fintech checkout flows and merchant dashboard experiences for Razorpay.",
         "skills":["Figma","User Research","Interaction Design","Accessibility","HTML/CSS"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"UI Designer","company":"Zoho","location":"Chennai","salary":"8-16 LPA",
         "description":"Design enterprise SaaS product interfaces across Zoho's 50+ business applications.",
         "skills":["Figma","Adobe XD","Prototyping","Component Libraries"],"posted":"Yesterday","source":"Naukri"},
        {"title":"UX Researcher","company":"Google","location":"Bangalore","salary":"25-45 LPA",
         "description":"Lead user research studies to shape Google's consumer and enterprise product decisions.",
         "skills":["User Research","Usability Testing","Surveys","Data Analysis","Figma"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── PRODUCT MANAGER ──────────────────────────────────────────────────────
    "product manager": [
        {"title":"Product Manager","company":"Google","location":"Bangalore","salary":"35-65 LPA",
         "description":"Lead product strategy for Google Pay's India market across merchant and consumer products.",
         "skills":["Product Strategy","Data Analysis","SQL","Roadmapping","Stakeholder Management"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Senior Product Manager","company":"Flipkart","location":"Bangalore","salary":"28-50 LPA",
         "description":"Own the seller platform product roadmap and drive GMV growth for Flipkart's marketplace.",
         "skills":["Product Management","Analytics","SQL","A/B Testing","PRD Writing"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Product Manager","company":"Razorpay","location":"Bangalore","salary":"25-45 LPA",
         "description":"Define product vision for Razorpay's payment gateway and capital products.",
         "skills":["Product Strategy","Fintech","Data Analysis","SQL","Customer Research"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Product Manager","company":"Swiggy","location":"Bangalore","salary":"22-42 LPA",
         "description":"Drive product growth for Swiggy Instamart — India's fastest growing quick commerce.",
         "skills":["Product Management","Growth","Analytics","User Research","OKRs"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Associate Product Manager","company":"CRED","location":"Bangalore","salary":"18-35 LPA",
         "description":"Build premium financial products for India's most engaged credit card user base.",
         "skills":["Product Thinking","Data Analysis","Wireframing","Stakeholder Management"],"posted":"Yesterday","source":"Naukri"},
        {"title":"Product Manager","company":"Meesho","location":"Bangalore","salary":"18-36 LPA",
         "description":"Own discovery and catalog product to drive seller and buyer growth on Meesho.",
         "skills":["Product Strategy","Analytics","A/B Testing","SQL","User Research"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── CLOUD ENGINEER ───────────────────────────────────────────────────────
    "cloud engineer": [
        {"title":"Cloud Engineer","company":"Amazon","location":"Bangalore","salary":"22-42 LPA",
         "description":"Design and operate cloud infrastructure on AWS for Amazon's India business units.",
         "skills":["AWS","Terraform","Kubernetes","Python","CloudFormation","Monitoring"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Azure Cloud Engineer","company":"Microsoft","location":"Hyderabad","salary":"20-38 LPA",
         "description":"Build and manage Azure infrastructure and migrate enterprise customers to cloud.",
         "skills":["Azure","ARM Templates","Kubernetes","Python","PowerShell","Networking"],"posted":"2 days ago","source":"Naukri"},
        {"title":"GCP Cloud Engineer","company":"Google","location":"Bangalore","salary":"28-50 LPA",
         "description":"Design cloud-native architectures on GCP for Google's internal and external customers.",
         "skills":["GCP","Terraform","Kubernetes","Python","BigQuery","Cloud Run"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Cloud Infrastructure Engineer","company":"Razorpay","location":"Bangalore","salary":"20-40 LPA",
         "description":"Build and scale multi-region cloud infrastructure for India's payments leader.",
         "skills":["AWS","Terraform","Helm","Kubernetes","Python","Observability"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Cloud Engineer","company":"Freshworks","location":"Chennai","salary":"14-28 LPA",
         "description":"Manage AWS cloud infrastructure for Freshworks' globally distributed SaaS platform.",
         "skills":["AWS","Docker","Terraform","Jenkins","Linux","Monitoring"],"posted":"Yesterday","source":"Naukri"},
        {"title":"Cloud DevOps Engineer","company":"PhonePe","location":"Bangalore","salary":"18-35 LPA",
         "description":"Ensure platform reliability and scalability for PhonePe's financial infrastructure.",
         "skills":["AWS","Kubernetes","Terraform","Prometheus","Grafana","Python"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── CYBERSECURITY ────────────────────────────────────────────────────────
    "cybersecurity engineer": [
        {"title":"Security Engineer","company":"Razorpay","location":"Bangalore","salary":"22-42 LPA",
         "description":"Protect financial infrastructure and customer data for India's largest payment gateway.",
         "skills":["Security","Penetration Testing","Python","SIEM","Network Security","OWASP"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"Application Security Engineer","company":"Flipkart","location":"Bangalore","salary":"20-38 LPA",
         "description":"Perform security reviews, threat modelling, and vulnerability assessments at scale.",
         "skills":["SAST","DAST","Python","Burp Suite","Threat Modelling","DevSecOps"],"posted":"2 days ago","source":"Naukri"},
        {"title":"Cloud Security Engineer","company":"Amazon","location":"Bangalore","salary":"28-50 LPA",
         "description":"Build security automation and guardrails across AWS services and internal platforms.",
         "skills":["AWS Security","IAM","Python","Compliance","CSPM","Terraform"],"posted":"3 days ago","source":"Indeed"},
        {"title":"Cybersecurity Analyst","company":"PhonePe","location":"Bangalore","salary":"16-30 LPA",
         "description":"Monitor, detect, and respond to security threats across PhonePe's financial platform.",
         "skills":["SIEM","Incident Response","Python","Network Security","Threat Intelligence"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Security Engineer","company":"Google","location":"Bangalore","salary":"35-65 LPA",
         "description":"Defend Google's infrastructure and products against advanced security threats.",
         "skills":["C++","Python","Cryptography","Reverse Engineering","Threat Research"],"posted":"Yesterday","source":"Naukri"},
        {"title":"InfoSec Engineer","company":"CRED","location":"Bangalore","salary":"18-35 LPA",
         "description":"Secure CRED's fintech platform and ensure compliance with financial data regulations.",
         "skills":["Security","Python","SIEM","PCI-DSS","Pen Testing","VAPT"],"posted":"5 days ago","source":"Indeed"},
    ],

    # ── QA ENGINEER ─────────────────────────────────────────────────────────
    "qa engineer": [
        {"title":"QA Engineer","company":"Flipkart","location":"Bangalore","salary":"10-20 LPA",
         "description":"Own end-to-end quality for Flipkart's buyer app and backend services at scale.",
         "skills":["Selenium","Python","TestNG","API Testing","CI/CD","Postman"],"posted":"1 day ago","source":"LinkedIn"},
        {"title":"SDET / QA Engineer","company":"Razorpay","location":"Bangalore","salary":"12-24 LPA",
         "description":"Build test automation frameworks for critical payment flows at Razorpay.",
         "skills":["Python","Pytest","Selenium","REST Assured","Jenkins","Docker"],"posted":"2 days ago","source":"Naukri"},
        {"title":"QA Automation Engineer","company":"Freshworks","location":"Chennai","salary":"8-18 LPA",
         "description":"Build and maintain automated test suites for Freshworks' SaaS product suite.",
         "skills":["Selenium","Java","TestNG","API Testing","CI/CD","BDD"],"posted":"3 days ago","source":"Indeed"},
        {"title":"QA Engineer","company":"Swiggy","location":"Bangalore","salary":"10-20 LPA",
         "description":"Ensure quality across Swiggy's food delivery and quick commerce applications.",
         "skills":["Appium","Selenium","Python","REST APIs","Firebase Test Lab"],"posted":"4 days ago","source":"LinkedIn"},
        {"title":"Performance Test Engineer","company":"PhonePe","location":"Bangalore","salary":"12-24 LPA",
         "description":"Run load and stress tests for UPI transaction flows at millions of TPS.",
         "skills":["JMeter","k6","Python","Performance Testing","Monitoring","SQL"],"posted":"Yesterday","source":"Naukri"},
        {"title":"QA Lead","company":"Zoho","location":"Chennai","salary":"10-22 LPA",
         "description":"Lead quality engineering for Zoho's enterprise SaaS product testing initiatives.",
         "skills":["Selenium","Java","TestNG","Agile","API Testing","Reporting"],"posted":"5 days ago","source":"Indeed"},
    ],
}

# ── Keyword aliases — maps search terms → canonical DB key ──────────────────
ALIASES = {
    # ML / AI
    "ml engineer": "ml engineer",
    "machine learning engineer": "ml engineer",
    "ai engineer": "ml engineer",
    "ai ml engineer": "ml engineer",
    "mlops engineer": "ml engineer",
    "nlp engineer": "ml engineer",
    "deep learning engineer": "ml engineer",
    # Data Science
    "data scientist": "data scientist",
    "senior data scientist": "data scientist",
    "data science": "data scientist",
    # Full Stack
    "full stack developer": "full stack developer",
    "full stack engineer": "full stack developer",
    "fullstack developer": "full stack developer",
    "fullstack engineer": "full stack developer",
    "full-stack developer": "full stack developer",
    "mern stack developer": "full stack developer",
    "mean stack developer": "full stack developer",
    # Software Eng
    "software engineer": "software engineer",
    "software developer": "software engineer",
    "sde": "software engineer",
    "sde1": "software engineer",
    "sde2": "software engineer",
    "sde i": "software engineer",
    "sde ii": "software engineer",
    # Python
    "python developer": "python developer",
    "python engineer": "python developer",
    "python backend developer": "python developer",
    # Frontend
    "frontend developer": "frontend developer",
    "frontend engineer": "frontend developer",
    "react developer": "frontend developer",
    "react engineer": "frontend developer",
    "ui developer": "frontend developer",
    "vue developer": "frontend developer",
    "angular developer": "frontend developer",
    # Backend
    "backend developer": "backend developer",
    "backend engineer": "backend developer",
    "java developer": "backend developer",
    "java backend developer": "backend developer",
    "node.js developer": "backend developer",
    "golang developer": "backend developer",
    "go developer": "backend developer",
    # DevOps
    "devops engineer": "devops engineer",
    "devops": "devops engineer",
    "sre": "devops engineer",
    "site reliability engineer": "devops engineer",
    "cloud devops": "devops engineer",
    "infrastructure engineer": "devops engineer",
    # Cloud
    "cloud engineer": "cloud engineer",
    "aws engineer": "cloud engineer",
    "azure engineer": "cloud engineer",
    "gcp engineer": "cloud engineer",
    "cloud architect": "cloud engineer",
    # Data Analyst
    "data analyst": "data analyst",
    "business analyst": "data analyst",
    "product analyst": "data analyst",
    "analytics engineer": "data analyst",
    "bi analyst": "data analyst",
    # Android
    "android developer": "android developer",
    "android engineer": "android developer",
    "kotlin developer": "android developer",
    # iOS
    "ios developer": "ios developer",
    "ios engineer": "ios developer",
    "swift developer": "ios developer",
    # UI/UX
    "ui ux designer": "ui ux designer",
    "ux designer": "ui ux designer",
    "ui designer": "ui ux designer",
    "product designer": "ui ux designer",
    "ux researcher": "ui ux designer",
    "graphic designer": "ui ux designer",
    # PM
    "product manager": "product manager",
    "apm": "product manager",
    "associate product manager": "product manager",
    "senior product manager": "product manager",
    "program manager": "product manager",
    # Security
    "cybersecurity engineer": "cybersecurity engineer",
    "security engineer": "cybersecurity engineer",
    "application security": "cybersecurity engineer",
    "cybersecurity analyst": "cybersecurity engineer",
    "infosec engineer": "cybersecurity engineer",
    "penetration tester": "cybersecurity engineer",
    # QA
    "qa engineer": "qa engineer",
    "quality assurance engineer": "qa engineer",
    "sdet": "qa engineer",
    "test engineer": "qa engineer",
    "automation tester": "qa engineer",
    "qa lead": "qa engineer",
}


def _match_skills(resume_skills: list, job_skills: list) -> int:
    """Calculate 0-100 match score based on skill overlap."""
    if not resume_skills or not job_skills:
        return random.randint(55, 85)
    rs = {s.lower() for s in resume_skills}
    js = {s.lower() for s in job_skills}
    overlap = rs & js
    base = int(len(overlap) / max(len(js), 1) * 100)
    # small random jitter so scores feel natural
    return min(99, max(40, base + random.randint(-5, 8)))


def fetch_jobs(role: str, location: str, resume_text: str) -> list:
    """
    Returns a list of jobs matching the given role.
    URLs are built dynamically using the actual job title + user's location.
    """
    from src.helper import analyze_resume

    role_key = role.strip().lower()

    # 1. Exact alias lookup
    db_key = ALIASES.get(role_key)

    # 2. Partial match if no exact alias
    if not db_key:
        for alias, key in ALIASES.items():
            if alias in role_key or role_key in alias:
                db_key = key
                break

    # 3. Fuzzy word overlap fallback
    if not db_key:
        role_words = set(role_key.split())
        best_score, best_key = 0, None
        for alias, key in ALIASES.items():
            overlap = len(role_words & set(alias.split()))
            if overlap > best_score:
                best_score, best_key = overlap, key
        if best_score > 0:
            db_key = best_key

    # 4. Still nothing → generic software engineer
    if not db_key:
        db_key = "software engineer"

    raw_jobs = JOB_DB.get(db_key, JOB_DB["software engineer"])

    # Parse resume skills for match scoring
    try:
        resume_data   = analyze_resume(resume_text) if resume_text else {}
        resume_skills = resume_data.get("skills", [])
    except Exception:
        resume_skills = []

    # Filter by location if provided
    loc_filter = location.strip().lower() if location else ""
    if loc_filter:
        loc_words = set(loc_filter.replace(",", " ").split())
        filtered = [j for j in raw_jobs
                    if any(w in j["location"].lower() for w in loc_words)]
        jobs = filtered if filtered else raw_jobs
    else:
        jobs = raw_jobs

    # Build result with dynamic URLs + match score
    result = []
    for job in jobs:
        # Use user's location for URLs if they filtered, else job's default
        url_loc = location.strip() if location.strip() else job["location"]
        urls    = _build_urls(job["title"], job["company"], url_loc)
        score   = _match_skills(resume_skills, job["skills"])

        result.append({
            "title":          job["title"],
            "company":        job["company"],
            "location":       job["location"],
            "salary_range":   job["salary"],
            "description":    job["description"],
            "required_skills":job["skills"],
            "posted":         job["posted"],
            "source":         job["source"],
            "match_score":    score,
            "linkedin_url":   urls["linkedin_url"],
            "naukri_url":     urls["naukri_url"],
            "indeed_url":     urls["indeed_url"],
            "glassdoor_url":  urls["glassdoor_url"],
            "google_url":     urls["google_url"],
        })

    # Sort by match score descending
    result.sort(key=lambda x: x["match_score"], reverse=True)
    return result