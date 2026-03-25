# app/Advisors/InfoAdvisor/InfoAdvisor.py

import os
from app.Services.llm_service import LLMService
from app.Services.chroma_service import ChromaService


class InfoAdvisor:

    def __init__(self):
        self.llm    = LLMService()
        self.chroma = ChromaService()

        prompt_path = os.path.join(os.path.dirname(__file__), "info_advisor_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def generate_response(self, history, message) :
        context = self.chroma.query(message, n_results=3)

        prompt = self.prompt_template.format(
            context=context,
            history=self._format_history(history),
            message=message
        )

        return self.llm.generate(prompt)

    def _format_history(self, history) :
        if not history:
            return "(no prior turns)"
        lines = []
        for turn in history:
            if isinstance(turn, dict):
                user = turn.get("user", "")
                bot  = turn.get("bot", "")
                if user:
                    lines.append(f"Candidate: {user}")
                if bot:
                    lines.append(f"Recruiter: {bot}")
            else:
                lines.append(str(turn))
        return "\n".join(lines)
