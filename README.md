# AI CV Optimizer

AI-powered web application that analyzes your CV against job descriptions and provides actionable improvement suggestions.

## 🚀 Features

- CV and job description analysis using AI (Groq + LLaMA 3)
- Compatibility score (0–100)
- Missing keyword detection
- Personalized improvement suggestions
- History of past analyses

## 🛠 Tech Stack

- Python / Django
- Groq API (LLaMA 3)
- HTML / CSS
- SQLite (development)

## 📸 Demo

Paste a job description and your CV to receive:
- Match score
- Missing skills
- Tailored suggestions to improve your CV

## ⚙️ Installation

```bash
git clone https://github.com/SantinoBonarrigo/cv-optimizer-ai.git
cd cv-optimizer-ai

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
