from flask import Flask, render_template, request
import random

app = Flask(__name__)

# ------------------------------
# FILTER OPTIONS
# ------------------------------
industries = [
    "School", "Healthcare", "Hospital", "Networking", "Barangay",
    "E-commerce", "Finance", "Entertainment", "Transportation", "Agriculture"
]

project_types = ["Mobile App", "Web App", "Desktop App", "IoT App", "AI App", "Data App"]
difficulties = ["Beginner", "Intermediate", "Advanced"]

# ------------------------------
# SUGGESTED LANGUAGES PER TYPE (Expanded & Context-Aware)
# ------------------------------
suggested_languages = {
    "Mobile App": {
        "recommended": ["Flutter", "Kotlin", "Java"],
        "others": ["React Native", "Swift", "Dart", "Ionic", "Xamarin"]
    },
    "Web App": {
        "recommended": ["HTML", "CSS", "JavaScript", "PHP"],
        "others": ["React", "Node.js", "Laravel", "Django", "Vue.js", "Express.js", "Bootstrap"]
    },
    "Desktop App": {
        "recommended": ["Python", "C#", "JavaFX"],
        "others": ["Electron", "C++", "VB.NET", "Qt", "Tkinter", "WPF"]
    },
    "IoT App": {
        "recommended": ["C++", "Python", "Arduino"],
        "others": ["Raspberry Pi", "MicroPython", "ESP32", "C"]
    },
    "AI App": {
        "recommended": ["Python", "TensorFlow", "PyTorch"],
        "others": ["Keras", "OpenCV", "Scikit-learn", "Jupyter Notebook"]
    },
    "Data App": {
        "recommended": ["Python", "SQL", "R"],
        "others": ["Pandas", "NumPy", "Tableau", "Power BI", "Excel", "Matplotlib"]
    }
}

# ------------------------------
# RELATED PROJECT SOURCES (expanded)
# ------------------------------
related_projects = {
    "Mobile App": [
        "https://github.com/topics/mobile-app",
        "https://dribbble.com/tags/app-design",
        "https://play.google.com/store/apps",
        "https://www.behance.net/search/projects?search=mobile+app"
    ],
    "Web App": [
        "https://github.com/topics/web-app",
        "https://vercel.com/templates",
        "https://www.frontendmentor.io/challenges",
        "https://dribbble.com/tags/web-design"
    ],
    "Desktop App": [
        "https://github.com/topics/desktop-app",
        "https://awesomeopensource.com/projects/desktop",
        "https://sourceforge.net/"
    ],
    "IoT App": [
        "https://github.com/topics/iot-projects",
        "https://www.hackster.io/",
        "https://create.arduino.cc/projecthub"
    ],
    "AI App": [
        "https://paperswithcode.com",
        "https://github.com/topics/ai",
        "https://huggingface.co/models",
        "https://www.kaggle.com/models"
    ],
    "Data App": [
        "https://kaggle.com/datasets",
        "https://github.com/topics/data-analysis",
        "https://data.world/",
        "https://public.tableau.com/en-us/s/gallery"
    ]
}

# ------------------------------
# REALISTIC TOPICS PER INDUSTRY
# ------------------------------
industry_topics = {
    "School": ["Student Attendance", "E-Learning", "Grading System", "Scheduling", "Library Management"],
    "Healthcare": ["Patient Monitoring", "Telemedicine", "Medical Records", "Health Tracking", "Appointment System"],
    "Hospital": ["Inventory Management", "Staff Scheduling", "Electronic Health Records", "Emergency Response"],
    "Networking": ["Network Security", "LAN Management", "IoT Device Connection", "VPN Monitoring"],
    "Barangay": ["Resident Database", "Incident Reporting", "Permit Request", "Barangay Information System"],
    "E-commerce": ["Product Management", "Customer Review", "Sales Analytics", "Inventory Control"],
    "Finance": ["Expense Tracker", "Budget Planner", "Loan Management", "Transaction System"],
    "Entertainment": ["Music Streaming", "Video Sharing", "Event Ticketing", "Fan Engagement App"],
    "Transportation": ["Vehicle Tracking", "Ride Booking", "Traffic Monitoring", "Logistics Management"],
    "Agriculture": ["Crop Monitoring", "Weather Prediction", "Smart Irrigation", "Farm Record System"],
}

# ------------------------------
# IDEA TEMPLATES
# ------------------------------
templates = [
    "A {ptype} for {topic} in the {industry} Industry",
    "Design and Implementation of a {ptype} focused on {topic} for {industry}",
    "Developing a Simple {ptype} to Assist {industry} with {topic}",
    "A Capstone Project: {topic} {ptype} for {industry} Applications",
    "Smart {topic} Solution using {language} for {industry}"
]

# ------------------------------
# IDEA GENERATOR FUNCTION
# ------------------------------
def generate_ideas(industry, ptype, difficulty, n=5):
    ideas = []

    lang_info = suggested_languages.get(ptype, {"recommended": ["Python"], "others": []})
    main_langs = lang_info["recommended"]
    other_langs = lang_info["others"]
    sources = related_projects.get(ptype, ["https://github.com/explore"])
    topics = industry_topics.get(industry, ["Automation", "Data Management", "Monitoring", "Tracking"])

    for _ in range(n):
        language = random.choice(main_langs)
        topic = random.choice(topics)
        template = random.choice(templates)

        idea_title = template.format(
            topic=topic,
            industry=industry or "General",
            ptype=ptype or "Application",
            language=language
        )

        ideas.append({
            "title": idea_title,
            "ptype": ptype or "General App",
            "language": language,
            "difficulty": difficulty or "Not Specified",
            "industry": industry or "General",
            "source": random.choice(sources),
            "suggested_languages": {
                "recommended": main_langs,
                "others": other_langs
            }
        })

    return ideas

# ------------------------------
# MAIN ROUTE
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    selected = {"industry": "", "ptype": "", "difficulty": ""}

    if request.method == "POST":
        selected["industry"] = request.form.get("industry")
        selected["ptype"] = request.form.get("ptype")
        selected["difficulty"] = request.form.get("difficulty")
        n = int(request.form.get("num_results", 5))

        results = generate_ideas(
            selected["industry"],
            selected["ptype"],
            selected["difficulty"],
            n
        )

    return render_template(
        "index.html",
        industries=industries,
        project_types=project_types,
        difficulties=difficulties,
        selected=selected,
        results=results
    )

# ------------------------------
# RUN APP
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
