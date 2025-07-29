
import json
from typing import Dict
from vertexai.generative_models import (
    GenerativeModel,
    Tool,
    FunctionDeclaration,
    Part,
)
from tools import generate_byte_course_artifact

PROACTIVE_AGENT_TOOLBOX = Tool(
    function_declarations=[
        FunctionDeclaration.from_func(generate_byte_course_artifact),
    ]
)

class LimAgent:
    def __init__(self, model_name: str, tools: list = None):
        self._model = GenerativeModel(model_name, tools=tools)
        self.chat = self._model.start_chat()

class ProactiveAgent(LimAgent):
    def __init__(self):
        super().__init__(model_name="gemini-2.0-flash-001", tools=[PROACTIVE_AGENT_TOOLBOX])
        print("🤖 ProactiveAgent is online.")

    def run_interaction(self, event: Dict) -> str:
        print(f"\n▶️ Agent received event: {event}")

        prompt = f"""
        You are "Agent Zero," a helpful AI Tutor. Your primary goal is to help users by generating a byte course when they struggle.
        A system event has just been triggered: {json.dumps(event)}.
        Based on this, first, decide if you need to call the `generate_byte_course_artifact` tool.
        If you call the tool, then after you get the result back, formulate a friendly user-facing message containing the result.
        """

        response = self.chat.send_message(prompt)

        function_call = None
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    function_call = part.function_call
                    break

        if function_call:
            print(f"✅ Agent decided to run the tool: {function_call.name}")
            args = {key: value for key, value in function_call.args.items()}
            tool_output = generate_byte_course_artifact(**args)
            print("▶️ Sending tool output back to the model for final synthesis...")

            response = self.chat.send_message(
                Part.from_function_response(
                    name=function_call.name,
                    response={"content": tool_output},
                ),
                stream=False
            )
            final_message = response.text
        else:
            print("✅ Agent decided to respond directly.")
            final_message = response.text

        print(f"✅ Agent generated final user-facing message.")
        return final_message
