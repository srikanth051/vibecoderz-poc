
import json
from vertexai.generative_models import GenerativeModel

def generate_byte_course_artifact(topic: str) -> str:
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
