# app/agents/main_agent.py

import os
import PyPDF2
from Advisors.ExitAdvisor.ExitAdvisor import ExitAdvisor
from Advisors.SchedulingAdvisor.SchedulingAdvisor import SchedulingAdvisor
from Advisors.InfoAdvisor.InfoAdvisor import InfoAdvisor


class MainAgent:

    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_path = os.path.join(current_dir, "../../PythonDeveloperJobDescription.pdf")

        job_description = self._extract_text_from_pdf(pdf_path)

        self.exit_advisor = ExitAdvisor(job_description)
        self.scheduling_advisor = SchedulingAdvisor(job_description)
        self.info_advisor = InfoAdvisor(job_description)

    def _extract_text_from_pdf(self, file_path):
        text = ""
        try:
            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text += page.extract_text()
            else:
                print(f"Warning: PDF file not found at {file_path}")
                text = "General Developer role"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            text = "General Developer role"
        return text

    def handle_message(self, conversation_history, user_message,
                       scheduling_in_progress=False, interview_confirmed=False):

        # Once interview is confirmed, only allow friendly wrap-up via InfoAdvisor
        if interview_confirmed:
            response = self.info_advisor.generate_response(
                conversation_history, user_message
            )
            return {"action": "confirmed", "response": response}

        # While slots are being negotiated, skip ExitAdvisor
        if not scheduling_in_progress:
            if self.exit_advisor.should_end(conversation_history, user_message):
                return {
                    "action": "end",
                    "response": "Requirements can't be met. Thank you for your time."
                }

        scheduling_result = self.scheduling_advisor.try_schedule(
            conversation_history, user_message
        )

        if scheduling_result:
            return scheduling_result

        response = self.info_advisor.generate_response(
            conversation_history, user_message
        )

        return {"action": "continue", "response": response}
