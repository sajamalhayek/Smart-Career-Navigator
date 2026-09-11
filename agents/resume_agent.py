from agents.base_agent import BaseAgent

class ResumeExtractorAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are an expert HR Data Extractor. Analyze the provided resume text and extract "
            "the candidate's profile information. Return a valid JSON object with the keys: "
            "\"candidate_name\", \"technical_skills\" (array), \"soft_skills\" (array), and \"experience_years\"."
        )
        super().__init__(system_prompt)

    def extract(self, resume_text):
        return self.query(resume_text)