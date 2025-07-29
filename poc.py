# poc.py - Final Version using ChatSession for Robustness

import os
import json
from typing import Dict

# The core Google library for interacting with Vertex AI (including Gemini)
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
)

# --- Configuration ---
# IMPORTANT: Use your NEW, working Project ID
PROJECT_ID = "vibecoderz-poc"  # <--- Please update this
LOCATION = "us-east1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

print("✅ Vertex AI Initialized.")

# Base Agent Class
class LimAgent:
    def __init__(self, model_name: str, tools: list = None):
        self._model = GenerativeModel(model_name, tools=tools)
        # We will now use a ChatSession to automatically handle history
        self.chat = self._model.start_chat()

def generate_byte_course_artifact(topic: str) -> str:
    """
    Generates a simple 3-slide educational artifact on a given topic using an LLM.
    """
    print(f"🛠️ Tool 'generate_byte_course_artifact' called with topic: {topic}")
    tool_model = GenerativeModel("gemini-2.0-flash-001")
    prompt = f"""
    You are an expert instructional designer.
    Create a simple, 3-slide educational summary about the topic: {topic}.
    The output must be a single, valid JSON object.
    The JSON should have a key "slides" which is an array of 3 objects.
    Each object should have "title" (string) and "content" (string with 2-3 bullet points).
    """
    response = tool_model.generate_content(prompt)
    cleaned_json_string = response.text.strip().replace("```json", "").replace("```", "").strip()
    print(f"✅ Artifact generated for {topic}.")
    return cleaned_json_string

PROACTIVE_AGENT_TOOLBOX = Tool(
    function_declarations=[
        FunctionDeclaration.from_func(generate_byte_course_artifact),
    ]
)

class ProactiveAgent(LimAgent):
    """
    An agent that detects user struggle and proactively offers a personalized Byte Course.
    """
    def __init__(self):
        super().__init__(model_name="gemini-2.0-flash-001", tools=[PROACTIVE_AGENT_TOOLBOX])
        print("🤖 ProactiveAgent is online.")

    def run_interaction(self, event: Dict) -> str:
        """
        Processes an event and generates a user-facing response using a ChatSession
        to correctly handle conversation history and tool calls.
        """
        print(f"\n▶️ Agent received event: {event}")

        prompt = f"""
        You are "Agent Zero," a helpful AI Tutor. Your primary goal is to help users by generating a byte course when they struggle.
        A system event has just been triggered: {json.dumps(event)}.
        Based on this, first, decide if you need to call the `generate_byte_course_artifact` tool.
        If you call the tool, then after you get the result back, formulate a friendly user-facing message containing the result.
        """

        # --- REFACTORED LOGIC USING CHAT_SESSION ---
        
        # 1. Send the prompt to the chat. The chat session will manage the history.
        response = self.chat.send_message(prompt)
        
        # 2. Check if the model decided to call a tool.
        function_call = None
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_call = part.function_call
                    break
        
        # 3. If a tool call exists, execute it and send the result back to the SAME chat.
        if function_call:
            print(f"✅ Agent decided to run the tool: {function_call.name}")
            
            args = {key: value for key, value in function_call.args.items()}
            tool_output = generate_byte_course_artifact(**args)
            
            print("▶️ Sending tool output back to the model for final synthesis...")
            
            # The chat session automatically remembers the context. We only need to send the tool result.
            response = self.chat.send_message(
                Part.from_function_response(
                    name=function_call.name,
                    response={"content": tool_output},
                ),
                stream=False # Ensure we wait for the full response
            )
            final_message = response.text
        # 4. If no tool call, the model responded directly.
        else:
            print("✅ Agent decided to respond directly.")
            final_message = response.text

        print(f"✅ Agent generated final user-facing message.")
        return final_message

def simulate_failed_quiz_event(user_id: str, topic: str) -> Dict:
    """
    Creates a mock event dictionary that simulates a user failing a quiz.
    """
    print(f"\n⚡ Simulating event: User '{user_id}' is struggling with '{topic}'.")
    return {
        "event_type": "quiz_failed_repeatedly",
        "user_id": user_id,
        "topic": topic,
        "details": "User failed the quiz 3 times in the last 15 minutes."
    }

if __name__ == "__main__":
    proactive_agent = ProactiveAgent()
    event_data = simulate_failed_quiz_event(user_id='priya', topic='CSS Flexbox')
    final_output = proactive_agent.run_interaction(event=event_data)
    print("\n--- AGENT'S FINAL OUTPUT ---")
    print(final_output)
    print("--------------------------\n")