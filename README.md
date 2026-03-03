# Eduba

Eduba is an AI-integrated educational platform that combines structured curriculum-based mastery tracking with generative AI assistance.

Unlike traditional AI chatbots that provide direct answers without tracking learning progress, Eduba introduces a hybrid architecture that ensures adaptive, explainable, and scalable academic support across subjects.

---

## 🚀 Core Architecture

Eduba is built on five foundational pillars:

- **Deterministic Mastery Engine**  
  Tracks student progress in a structured and measurable way.

- **Structured Exercise System**  
  Curriculum-aligned exercises with controlled progression logic.

- **AI-Generated Explainable Responses**  
  Stepwise, contextual, and guided explanations instead of direct shortcuts.

- **JSON-Constrained Output Format**  
  Ensures predictable, machine-readable responses from the AI layer.

- **Intelligent Response Caching**  
  Reduces redundant API calls and improves system performance.

This hybrid architecture balances deterministic evaluation with generative flexibility.

---

## 🧠 System Overview

The Eduba pipeline works as follows:

1. User submits a query or exercise response.
2. The Mastery Engine evaluates learning state.
3. AI layer generates structured, explainable output.
4. Output is constrained into a defined JSON schema.
5. Response caching checks for reusable results.
6. Final structured response is returned to the client.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.x
- **Framework:** Flask
- **Database:** MySQL (via PyMySQL)
- **Environment Management:** python-dotenv
- **AI Integration:** OpenAI API
- **Frontend:** HTML, CSS, JavaScript

---

## 📦 Project Structure (Typical Layout)

```
eduba/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
│
├── static/
├── templates/
│
├── config.py
├── run.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Environment Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/mgmehra2005/eduba.git
cd eduba
```

### 2️⃣ Create Virtual Environment

**Linux / macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the root directory.

If `.env.example` exists:

```bash
cp .env.example .env
```

Add the following variables:

```env
CONFIG="production"
DB_HOST="127.0.0.1"
DB_USER="eduba_user"
DB_PASSWORD="eduba"
DB_NAME="eduba"
HF_API_KEY=""
```

Make sure:
- The database is running.
- Credentials are correct.
- Hugging Face API key is valid.

---

## 🗄️ Database Setup

1. Install MySQL locally or use a cloud provider.
2. Create a database:

```sql
CREATE DATABASE eduba_db;
```

3. Update `.env` with your database connection string.

If migrations are used:

```bash
flask db upgrade
```

(Adjust if migration framework differs.)

---

## ▶️ Running the Application

Start the development server:

```bash
flask run
```

OR

```bash
python run.py
```

Default local address:
```
http://127.0.0.1:5000
```

---

## 🧩 JSON Output Structure (Example)

```json
{
  "concept": "Linear Equations",
  "stepwise_explanation": [
    "Identify the variable",
    "Isolate the variable",
    "Solve for x"
  ],
  "final_answer": "x = 5",
  "mastery_update": {
    "status": "improved",
    "mastery_score": 0.82
  }
}
```

---

## 🧠 Design Philosophy

Traditional AI systems optimize for answer generation.

Eduba optimizes for:
- Concept mastery
- Structured reinforcement
- Explainability
- Predictable outputs
- Scalable academic tracking

This shifts the focus from "getting the answer" to "building understanding."

---

## 📈 Future Improvements

- Role-based authentication
- Student dashboards
- Teacher analytics panel
- Multi-subject expansion
- Offline inference layer
- Deployment-ready Docker configuration

---

## 🧪 Development Mode

To enable debug mode:

```env
FLASK_ENV=development
```

Never use development mode in production.

---

## 🚢 Production Deployment (Basic Outline)

1. Use Gunicorn:

```bash
pip install gunicorn
gunicorn run:app
```

2. Configure reverse proxy (Nginx recommended).
3. Use environment variables securely.
4. Enable HTTPS.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-feature-name
```

3. Commit changes:

```bash
git commit -m "Add new feature"
```

4. Push and create Pull Request.

---



## 🌍 Vision

Eduba aims to redefine AI-assisted education by merging deterministic mastery tracking with structured generative intelligence.

Not just answers.  
Not just chat.  
But measurable learning.

---