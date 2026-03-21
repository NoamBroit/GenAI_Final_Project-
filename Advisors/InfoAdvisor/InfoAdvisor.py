# app/Advisors/InfoAdvisor/InfoAdvisor.py

from app.Services.llm_service import LLMService

class InfoAdvisor:
    def __init__(self, job_description):
        from app.Services.llm_service import LLMService
        self.llm = LLMService()
        self.job_description = job_description

    def generate_response(self, history, message):
        prompt = f"""
        You are a recruiter assistant. 
        Use the following Job Description to screen the candidate:
        ---
        {self.job_description}
        ---
        Based on the history and the requirements above, continue the conversation.
        History: {history}
        User message: {message}
        """
        return self.llm.generate(prompt)
    
    def ending_llm_response(self, history, message):
        prompt = f"""
        You are a recruiter assistant. 
        you should decide if it's time to end the convestation and reject the candidate.
        if you decide to reject the candidate, or the candidate expresses disinterest, you replay "True".
        you cannot reply anything else but "True" or "False"
        ---
        {self.job_description}
        ---
        Based on the history and the requirements above, decside if ending the conversation is appropriate. 
        History: {history}
        User message: {message}
        """
        return self.llm.generate(prompt)

