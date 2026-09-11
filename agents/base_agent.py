import json
import requests
from config import Config

class BaseAgent:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000", # اختياري لمنع حظر OpenRouter
            "X-Title": "Smart Career Navigator"
        }

    def query(self, user_input):
        payload = {
            "model": Config.MODEL_NAME,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # فك ترميز JSON المعادة من الـ AI
                return json.loads(content)
            else:
                print(f"[API Error] Status Code: {response.status_code} - Response: {response.text}")
                return {"error": f"API Error {response.status_code}"}
                
        except json.JSONDecodeError as e:
            print(f"[JSON Decode Error] Failed to parse AI response: {e}")
            return {"error": "Invalid JSON format received from AI."}
            
        except requests.exceptions.RequestException as e:
            print(f"[Connection Error] Request failed: {e}")
            return {"error": f"Connection error: {str(e)}"}

        except Exception as e:
            print(f"[Unexpected Error]: {e}")
            return {"error": str(e)}