import random
from agents.base_agent import BaseAgent

class InterviewAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are an expert technical interviewer conducting a mock interview for a software developer. "
            "Ask one clear technical question based on the user's input. "
            "Return JSON format strictly: {\"reply\": \"your feedback and next question here\"}"
        )
        super().__init__(system_prompt)
        
        self.default_questions = [
            "Can you explain the difference between REST APIs and WebSockets, and when to use each?",
            "How do you handle error management and status codes in a Flask backend application?",
            "Describe a challenging bug you encountered in Python or Java and how you debugged it.",
            "How do you manage database connections and prevent SQL injection in SQLite/SQL?"
        ]
        self.current_step = 0

    def generate_response(self, user_message, context=""):
        if self.current_step >= len(self.default_questions):
            self.current_step = 0 
            return (
                "🎉 **Interview Completed!**\n\n"
                "**Performance Summary:**\n"
                "- **Communication:** Good\n"
                "- **Technical Readiness:** 75%\n"
                "- **Key Recommendation:** Focus on practicing backend error handling and database security concepts."
            )

        question = self.default_questions[self.current_step]
        self.current_step += 1

        prompt = f"Candidate Answer: {user_message}. Give a short reaction and ask: {question}"
        res = self.query(prompt)
        
        if isinstance(res, dict) and "reply" in res and res["reply"]:
            return res["reply"]
        
        return f"Thank you for your answer. Next question ({self.current_step}/4):\n\n👉 {question}"