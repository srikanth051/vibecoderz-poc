
from typing import Dict

def simulate_failed_quiz_event(user_id: str, topic: str) -> Dict:
    print(f"\n⚡ Simulating event: User '{user_id}' is struggling with '{topic}'.")
    return {
        "event_type": "quiz_failed_repeatedly",
        "user_id": user_id,
        "topic": topic,
        "details": "User failed the quiz 3 times in the last 15 minutes."
    }
