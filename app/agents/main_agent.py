# app/agents/main_agent.py

from Advisors.ExitAdvisor.ExitAdvisor import ExitAdvisor
from Advisors.SchedulingAdvisor.SchedulingAdvisor import SchedulingAdvisor
from Advisors.InfoAdvisor.InfoAdvisor import InfoAdvisor


class MainAgent:

    def __init__(self):
        self.exit_advisor       = ExitAdvisor()
        self.scheduling_advisor = SchedulingAdvisor()
        self.info_advisor       = InfoAdvisor()

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
