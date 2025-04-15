# AI-Powered Resume Analyzer & Job Matcher

An AI-powered web application that analyzes uploaded resumes and matches them with the most relevant job listings. Built using Flask, NLP (via Sentence Transformers), and a job dataset, this platform helps users discover their best-fit jobs and allows admin-level analysis of submissions.

---

## 🚀 Features

- User authentication (Login/Register)
- Resume parsing (PDF, DOCX)
- AI-based job recommendation engine
- Job match scores out of 100
- Download matched jobs as PDF or CSV
- Admin dashboard with logs
- Analytics via interactive charts
- Mobile responsive and user-friendly UI

---

## 🗂 Directory Structure

```
AIResumeMatcher/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── utils.py
│   ├── recommender.py
│   ├── database.py
│   ├── models.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── result.html
│   │   ├── admin.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── charts.js
├── uploads/
├── jobs.csv
├── requirements.txt
├── run.py
└── README.md
```

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AIResumeMatcher.git
cd AIResumeMatcher
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create SQLite Database
```bash
python
>>> from app import create_app
>>> from app.models import db
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

### 5. Run the Application
```bash
python run.py
```

Open in browser: `http://127.0.0.1:5000`

---

## 📊 Demo (GIF)

Add a screen-recorded GIF here showing:
- Landing page
- Uploading resume
- Getting results
- Downloading PDF/CSV
- Viewing admin dashboard

---

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3, Bootstrap, Plotly.js
- **Backend**: Python, Flask
- **NLP**: Sentence Transformers, Torch
- **Resume Parsing**: PyPDF2, docx2txt
- **Database**: SQLite (via SQLAlchemy)

---

## 📁 Dataset

A CSV file `jobs.csv` is used for matching with job listings.

---

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)

---

## 👨‍💻 Developed by
Your Name | [GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-profile)

---

