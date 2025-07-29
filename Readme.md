
# Vibecoderz Proactive Byte Course Agent

## 💡 What is This?

This is a proof-of-concept (POC) for the **Proactive Byte Course Agent** as part of the Vibecoderz AI Researcher/Engineer assessment. It simulates an AI Tutor that detects when a learner is struggling and proactively generates a short, personalized Byte Course to help them.

This solution is built using the **Google Agent Development Kit (ADK)** and **Gemini 2.0 APIs**, and follows modular architecture principles.

---

## 🚀 Features

- Listens for `quiz_failed_repeatedly` events
- Determines if a Byte Course intervention is helpful
- Generates a 3-slide educational artifact using Gemini
- Returns a human-friendly message with JSON slide data

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/srikanth051/vibecoderz-poc.git
cd vibecoderz-poc
```

### 2. Install Dependencies

```bash
pip install google-generativeai lim-agents markdown-pdf      
```

> Note: Ensure you have access to the **Vertex AI API** and have authenticated with `gcloud`.

### 3. Configure Project Settings

Edit `config.py`:

```python
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
```

### 4. Run the Agent

```bash
python main.py
```

---

## 🧩 Architecture Overview

This repo is split into the following files:

| File           | Responsibility                        |
|----------------|----------------------------------------|
| `main.py`      | Entry point & event simulation         |
| `config.py`    | GCP config values                      |
| `events.py`    | Quiz failure event generation          |
| `tools.py`     | Gemini tool to generate byte courses   |
| `agent.py`     | ProactiveAgent logic and tool usage    |

---

## 🔌 Integration Guide

In production, your backend or logging pipeline should publish the following message to a Pub/Sub topic:

```json
{
  "event_type": "quiz_failed_repeatedly",
  "user_id": "priya",
  "topic": "CSS Flexbox",
  "details": "User failed the quiz 3 times in 15 minutes."
}
```

This event will trigger the Proactive Agent which will generate and send the personalized learning artifact back to the user interface.

---

## 📩 Questions?

Email: [thota.srikanth2015@gmail.com](mailto:thota.srikanth2015@gmail.com)
