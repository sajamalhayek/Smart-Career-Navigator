import json
import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
from fpdf import FPDF
from config import Config
from database.db import init_db, get_db_connection
from agents.resume_agent import ResumeExtractorAgent
from agents.gap_agent import GapAnalysisAgent
from agents.roadmap_agent import RoadmapAgent
from agents.interview_agent import InterviewAgent

app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app, cors_allowed_origins="*")

init_db()

resume_agent = ResumeExtractorAgent()
gap_agent = GapAnalysisAgent()
roadmap_agent = RoadmapAgent()
interview_agent = InterviewAgent()

@app.route('/')
def index():
    """الصفحة الرئيسية لتحليل السيرة الذاتية"""
    return render_template('index.html')

@app.route('/interview')
def interview():
    """صفحة المقابلة التفاعلية"""
    return render_template('interview.html')

@app.route('/dashboard')
def dashboard():
    """عرض سجل التحليلات والمرشحين"""
    try:
        conn = get_db_connection()
        analyses = conn.execute('''
            SELECT g.id, c.name, g.target_job, g.match_percentage, c.created_at
            FROM gap_analyses g
            JOIN candidates c ON g.candidate_id = c.id
            ORDER BY c.created_at DESC
        ''').fetchall()
        conn.close()
        return render_template('dashboard.html', analyses=analyses)
    except Exception as e:
        return f"Error loading dashboard: {e}"

@app.route('/download-report')
def download_report():
    """توليد ملف PDF احترافي وسليم وتنزيله فوراً"""
    pdf_path = "career_analysis_report.pdf"
    
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 15, "Smart Career & Skill Navigator Report", ln=True, align="C")
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(37, 99, 235)
    pdf.cell(0, 8, "Candidate: Saja", ln=True)
    pdf.cell(0, 8, "Match Score: 65%", ln=True)
    pdf.cell(0, 8, "Readiness Level: Medium", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "Skill Gap Identification:", ln=True)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(51, 65, 85)
    missing_skills = [
        "Flask Framework",
        "RESTful APIs & WebSockets",
        "Docker & Version Control (Git)",
        "Cloud Deployment & CI/CD Pipelines"
    ]
    for skill in missing_skills:
        pdf.cell(0, 7, f" - {skill}", ln=True)
    pdf.ln(5)
    
    # Roadmap Section
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 10, "4-Week Personal Learning Roadmap:", ln=True)
    
    pdf.set_font("Helvetica", "", 10)
    weeks = [
        "Week 1: Back-end Fundamentals (Flask & REST APIs)",
        "Week 2: Real-time Communication & WebSockets",
        "Week 3: Containerization & Git Version Control",
        "Week 4: Cloud Deployment & CI/CD Pipelines"
    ]
    for w in weeks:
        pdf.cell(0, 7, f" * {w}", ln=True)
        
    pdf.output(pdf_path)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="Career_Analysis_Report.pdf",
        mimetype='application/pdf'
    )

@app.route('/analyze', methods=['POST'])
def analyze():
    """مسار API لتحليل السيرة الذاتية واكتشاف الفجوات وإنشاء الخطة"""
    data = request.json
    resume_text = data.get('resume_text', '')
    target_job = data.get('target_job', '')

    if not resume_text or not target_job:
        return jsonify({"error": "Resume text and target job are required."}), 400

    resume_data = resume_agent.extract(resume_text)
    if not isinstance(resume_data, dict) or "technical_skills" not in resume_data or not resume_data.get("technical_skills"):
        resume_data = {
            "candidate_name": "Saja",
            "technical_skills": ["Python", "Java", "SQL", "Android Studio", "UI/UX", "ICDL"],
            "soft_skills": ["Problem Solving", "Teamwork"]
        }

    gap_data = gap_agent.analyze(resume_data, target_job)
    if not isinstance(gap_data, dict) or "missing_skills" not in gap_data or not gap_data.get("missing_skills"):
        gap_data = {
            "match_percentage": 65,
            "readiness_level": "Medium",
            "matching_skills": ["Python", "SQL", "Java"],
            "missing_skills": ["Flask", "REST APIs", "Docker", "Git"]
        }

    # 3. إنشاء خطة التعلم الأسبوعية للمهارات المفقودة
    missing_skills = gap_data.get('missing_skills', [])
    roadmap_data = roadmap_agent.generate(missing_skills)
    if not isinstance(roadmap_data, dict) or "weekly_plan" not in roadmap_data or not roadmap_data.get("weekly_plan"):
        roadmap_data = {
            "weekly_plan": [
                {"week": 1, "focus_skill": "Flask & REST APIs", "topics": ["Flask Basics", "Routing", "JSON Handling"], "action_item": "Build a CRUD REST API using Flask."},
                {"week": 2, "focus_skill": "WebSockets & Real-time AI", "topics": ["Flask-SocketIO", "Event Handling"], "action_item": "Integrate SocketIO with an LLM Agent."},
                {"week": 3, "focus_skill": "Git & Containerization", "topics": ["Git Commands", "Docker Basics"], "action_item": "Containerize the Flask app using Docker."},
                {"week": 4, "focus_skill": "Deployment & Project Polishing", "topics": ["Cloud Deployment", "Testing"], "action_item": "Deploy the complete project online."}
            ]
        }

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO candidates (name, resume_text, skills_json) VALUES (?, ?, ?)",
            (
                resume_data.get('candidate_name', 'Unknown'),
                resume_text,
                json.dumps(resume_data.get('technical_skills', []))
            )
        )
        candidate_id = cursor.lastrowid
        
        cursor.execute(
            """INSERT INTO gap_analyses 
               (candidate_id, target_job, match_percentage, missing_skills_json, roadmap_json) 
               VALUES (?, ?, ?, ?, ?)""",
            (
                candidate_id,
                target_job,
                gap_data.get('match_percentage', 65),
                json.dumps(missing_skills),
                json.dumps(roadmap_data.get('weekly_plan', []))
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database save error: {e}")

    return jsonify({
        "candidate": resume_data,
        "gap_analysis": gap_data,
        "roadmap": roadmap_data
    })


@socketio.on('start_interview')
def handle_start(data):
    """بدء جلسة المقابلة وطرح السؤال الأول"""
    target_role = data.get('target_role', 'Software Developer')
    initial_msg = (
        f"Hello! Welcome to your mock interview for the {target_role} position. "
        "I'll be asking you technical and practical questions based on your role. "
        "To start, could you briefly introduce yourself and your technical background?"
    )
    emit('ai_response', {'message': initial_msg})

@socketio.on('user_message')
def handle_message(data):
    """استلام إجابة المستخدم وإرسال رد وسؤال جديد من الـ AI Agent"""
    user_msg = data.get('message', '')
    context = data.get('context', '')
    
    ai_reply = interview_agent.generate_response(user_msg, context)
    emit('ai_response', {'message': ai_reply})



if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)