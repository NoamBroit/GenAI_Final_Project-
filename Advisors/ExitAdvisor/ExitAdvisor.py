# app/Advisors/ExitAdvisor/ExitAdvisor.py

import os
from app.Services.llm_service import LLMService


class ExitAdvisor:

    def __init__(self, job_description: str):
        self.llm = LLMService()
        self.job_description = job_description

        prompt_path = os.path.join(os.path.dirname(__file__), "exit_advisor_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def should_end(self, history: list, message: str) -> bool:
        prompt = self.prompt_template.format(
            job_description=self.job_description,
            history=self._format_history(history),
            message=message
        )
        raw = self.llm.generate(prompt).strip()
        return raw.lower().startswith("true")

    def _format_history(self, history: list) -> str:
        if not history:
            return "(no prior turns)"
        lines = []
        for turn in history:
            if isinstance(turn, dict):
                user = turn.get("user", "")
                bot = turn.get("bot", "")
                if user:
                    lines.append(f"Candidate: {user}")
                if bot:
                    lines.append(f"Recruiter: {bot}")
            else:
                lines.append(str(turn))
        return "\n".join(lines)
