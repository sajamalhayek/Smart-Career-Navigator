import json
from agents.base_agent import BaseAgent

class RoadmapAgent(BaseAgent):
    def __init__(self):
        system_prompt = (
            "You are a Career Curriculum Advisor. Generate a structured 4-week learning plan "
            "to bridge the candidate's missing skills. Return JSON with key \"weekly_plan\" containing "
            "an array of objects, each with: \"week\" (1-4), \"focus_skill\", \"topics\" (array), and \"action_item\"."
        )
        super().__init__(system_prompt)

    def generate(self, missing_skills):
        return self.query(json.dumps({"missing_skills": missing_skills}))