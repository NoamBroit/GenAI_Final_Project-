# app/Advisors/SchedulingAdvisor/SchedulingAdvisor.py

import os
import json
from app.Services.db_service import DBService
from app.Services.llm_service import LLMService


class SchedulingAdvisor:

    def __init__(self, job_description: str):
        self.db = DBService()
        self.llm = LLMService()
        self.job_description = job_description

        prompt_path = os.path.join(os.path.dirname(__file__), "scheduling_advisor_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def try_schedule(self, history: list, message: str) -> dict | None:
        slots = self.db.get_available_slots(limit=3)
        slots_text = self._format_slots(slots)

        prompt = self.prompt_template.format(
            job_description=self.job_description,
            slots=slots_text,
            history=self._format_history(history),
            message=message
        )

        raw = self.llm.generate(prompt).strip()

        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            return None

        action = result.get("action", "none")

        if action == "none":
            return None

        return {
            "action": action,  # "confirmed" or "schedule"
            "response": result.get("response", "")
        }

    def _format_slots(self, slots: list[dict]) -> str:
        if not slots:
            return "No available slots at this time."
        lines = []
        for s in slots:
            lines.append(f"- {s['date']} at {s['time']} ({s['position']})")
        return "\n".join(lines)

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
