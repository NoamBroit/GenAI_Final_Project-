# app/main.py

from agents.main_agent import MainAgent


def run():
    agent = MainAgent()
    history = []

    while True:
        user_input = input("User: ")

        result = agent.handle_message(history, user_input)

        print(f"Bot: {result['response']}")

        history.append({"user": user_input, "bot": result["response"]})


if __name__ == "__main__":
    run()