import random
from agents.base_agent import BaseAgent

class InterviewAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are an expert technical interviewer conducting a mock interview for a software developer. "
            "Ask one clear technical or behavioral interview question based on the user's input. "
            "Keep your response under 3 sentences. "
            "Return JSON format strictly: {\"reply\": \"your feedback and next question here\"}"
        )
        super().__init__(system_prompt)
        
        # بنك أسئلة احتياطي يتغير ديناميكياً
        self.default_questions = [
            "Can you explain the difference between REST APIs and WebSockets, and when to use each?",
            "How do you handle error management and status codes in a Flask backend application?",
            "Describe a challenging bug you encountered in Python or Java and how you debugged it.",
            "How do you manage database connections and prevent SQL injection in SQLite/SQL?",
            "What is your experience with Object-Oriented Programming (OOP) principles in software development?",
            "How do you prioritize tasks when working on a project with a tight deadline?"
        ]
        self.current_step = 0

    def generate_response(self, user_message, context=""):
        # محاولة الاستعلام من الـ AI
        prompt = f"Candidate Answer: {user_message}"
        res = self.query(prompt)
        
        # التأكد من صحة الاستجابة القادمة من الـ API
        if isinstance(res, dict) and "reply" in res and res["reply"]:
            return res["reply"]
        
        # إذا تعثر الـ API، اختر سؤالاً ديناميكياً من القائمة لمنع التكرار
        question = self.default_questions[self.current_step % len(self.default_questions)]
        self.current_step += 1
        
        return f"Great point! Let's continue. Next question: {question}"