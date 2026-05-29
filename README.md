# MIRA — Medical Intelligence Robotic Automation
A Health Prediction Application built with Python and Streamlit that collects patient blood test data, stores it in a local SQLite database, and generates AI-powered health screening remarks using Google Gemini API.

## Features
- Add, View, Update, and Delete patient records (Full CRUD)
- AI-generated health remarks based on Glucose, Haemoglobin, and Cholesterol values
- Input validation (email format, future DOB check, numeric blood values)
- Persistent local storage using SQLite
- Auto-resets patient ID counter when all records are deleted

## Tech Stack
- **Frontend & Backend:** Python + Streamlit
- **Database:** SQLite
- **AI Integration:** Google Gemini 2.5 Flash API

## Project Structure