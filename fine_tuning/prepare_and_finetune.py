# fine_tuning/prepare_and_finetune.py

import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONVERSATIONS   = os.path.join(BASE_DIR, "sms_conversations.json")
PDF_PATH        = os.path.join(BASE_DIR, "PythonDeveloperJobDescription.pdf")
OUTPUT_JSONL    = os.path.join(BASE_DIR, "fine_tuning", "exit_advisor_train.jsonl")

SYSTEM_PROMPT = (
    "You are a recruiter assistant deciding whether to END a conversation with a job candidate. "
    "Reply with exactly one word: 'True' to end the conversation, or 'False' to continue. "
    "END if the candidate expresses disinterest, asks to stop, or is clearly unqualified. "
    "CONTINUE if the candidate is engaged or there is not enough information yet."
)


def build_jsonl(conversations_path, output_path):
    with open(conversations_path, "r", encoding="utf-8") as f:
        conversations = json.load(f)

    samples = []

    for conv in conversations:
        turns = conv["turns"]
        history_lines = []

        for i, turn in enumerate(turns):
            if turn["speaker"] == "recruiter" and turn.get("label"):

                candidate_msg = ""
                for prev in reversed(turns[:i]):
                    if prev["speaker"] == "candidate":
                        candidate_msg = prev["text"]
                        break

                if not candidate_msg:
                    continue

                label = "True" if turn["label"] == "end" else "False"

                history_text = "\n".join(history_lines) if history_lines else "(no prior turns)"
                user_content = (
                    f"CONVERSATION HISTORY:\n{history_text}\n\n"
                    f"LATEST CANDIDATE MESSAGE:\n{candidate_msg}\n\n"
                    f"Decision (True or False):"
                )

                samples.append({
                    "messages": [
                        {"role": "system",    "content": SYSTEM_PROMPT},
                        {"role": "user",      "content": user_content},
                        {"role": "assistant", "content": label}
                    ]
                })

            if turn["speaker"] == "candidate":
                history_lines.append(f"Candidate: {turn['text']}")
            elif turn["speaker"] == "recruiter":
                history_lines.append(f"Recruiter: {turn['text']}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")

    print(f"[1/4] JSONL created: {len(samples)} samples → {output_path}")
    return len(samples)


def upload_file(jsonl_path):
    with open(jsonl_path, "rb") as f:
        response = client.files.create(file=f, purpose="fine-tune")
    file_id = response.id
    print(f"[2/4] File uploaded. ID: {file_id}")
    return file_id


def launch_finetune(file_id):
    job = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-4o-mini-2024-07-18",
        hyperparameters={"n_epochs": 3}
    )
    print(f"[3/4] Fine-tune job started. Job ID: {job.id}")
    print(f"      Status: {job.status}")
    return job.id


def wait_for_completion(job_id):
    print("[4/4] Waiting for fine-tune to complete (this may take 10-30 minutes)...")
    while True:
        job = client.fine_tuning.jobs.retrieve(job_id)
        status = job.status
        print(f"      Status: {status}")

        if status == "succeeded":
            model_id = job.fine_tuned_model
            print(f"\n Fine-tune complete!")
            print(f" Model ID: {model_id}")
            print(f"\n Update ExitAdvisor to use: '{model_id}'")
            return model_id

        elif status in ("failed", "cancelled"):
            print(f"\n Fine-tune {status}.")
            return None

        time.sleep(60)


if __name__ == "__main__":
    build_jsonl(CONVERSATIONS, OUTPUT_JSONL)
    file_id  = upload_file(OUTPUT_JSONL)
    job_id   = launch_finetune(file_id)
    wait_for_completion(job_id)
