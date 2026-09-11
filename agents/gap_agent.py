import json
from agents.base_agent import BaseAgent

class GapAnalysisAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are a Skill Gap Analysis Agent. Compare candidate skills against target job requirements. "
            "You MUST return a valid JSON object with EXACTLY these keys: "
            "\"match_percentage\" (integer between 0 and 100), "
            "\"missing_skills\" (array of strings for missing skills), "
            "\"matching_skills\" (array of strings for candidate's matching skills), "
            "and \"readiness_level\" (High, Medium, or Low)."
        )
        super().__init__(system_prompt)

    def analyze(self, candidate_data, job_description):
        input_data = json.dumps({
            "candidate_skills": candidate_data.get("technical_skills", []),
            "target_job": job_description
        })
        return self.query(input_data)