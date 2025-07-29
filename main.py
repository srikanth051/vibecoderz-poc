
import vertexai
from config import PROJECT_ID, LOCATION
from agent import ProactiveAgent
from events import simulate_failed_quiz_event

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)
print("✅ Vertex AI Initialized.")

if __name__ == "__main__":
    proactive_agent = ProactiveAgent()
    event_data = simulate_failed_quiz_event(user_id='priya', topic='CSS Flexbox')
    final_output = proactive_agent.run_interaction(event=event_data)
    print("\n--- AGENT'S FINAL OUTPUT ---")
    print(final_output)
    print("--------------------------\n")
