# app/Advisors/ExitAdvisor/ExitAdvisor.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ── After fine-tuning, replace this with your fine-tuned model ID ────────────
# Example: "ft:gpt-4o-mini-2024-07-18:my-org::ABC123"
#FINE_TUNED_MODEL = os.getenv("EXIT_ADVISOR_MODEL", "gpt-4o-mini")

FINE_TUNED_MODEL = "ft:gpt-4o-mini-2024-07-18:personal::DLnxtr15"

SYSTEM_PROMPT = (
    "You are a recruiter assistant deciding whether to END a conversation with a job candidate. "
    "Reply with exactly one word: 'True' to end the conversation, or 'False' to continue. "
    "END if the candidate expresses disinterest, asks to stop, or is clearly unqualified. "
    "CONTINUE if the candidate is engaged or there is not enough information yet."
)


class ExitAdvisor:

    def __init__(self, job_description: str):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.job_description = job_description
        self.model = FINE_TUNED_MODEL

        prompt_path = os.path.join(os.path.dirname(__file__), "exit_advisor_prompt.txt")
        with open(prompt_path, "r", encoding="utf-8") as f:
            self.prompt_template = f.read()

    def should_end(self, history: list, message: str) -> bool:
        user_content = self.prompt_template.format(
            job_description=self.job_description,
            history=self._format_history(history),
            message=message
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_content}
            ],
            temperature=0,
            max_tokens=5
        )

        raw = response.choices[0].message.content.strip()
        return raw.lower().startswith("true")

    def _format_history(self, history: list) -> str:
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
