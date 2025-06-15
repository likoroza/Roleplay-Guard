import groq
import re

class AI():
    def __init__(self, api_key):
        self.api_key=api_key
        self.engine=groq.Client(api_key=api_key)

    def chat(self, prompt):
        result = self.engine.chat.completions.create(temperature=0.0, messages=[{"role":"user","content":prompt}], model='deepseek-r1-distill-llama-70b')
        result_string = result.choices[0].message.content
        result_without_process = re.sub(r"<think>.*?</think>", "", result_string , flags=re.DOTALL)
        
        return result_without_process.strip()