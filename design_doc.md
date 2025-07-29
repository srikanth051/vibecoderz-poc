
# 📐 Design Document: Proactive Byte Course Agent

## Overview

The **ProactiveAgent** improves learner engagement by monitoring for learning obstacles and delivering short, personalized educational content at just the right time.

---

## 🧱 Architecture

```
[Quiz or Activity System] --triggers--> [Event: quiz_failed_repeatedly]
                                            |
                                      [Pub/Sub Message]
                                            |
                                   [ProactiveAgent (LimAgent)]
                                            |
                                [Tool: generate_byte_course_artifact]
                                            |
                         [Gemini API → Generates 3-slide course JSON]
                                            |
                          [Human-readable message returned to UI]
```

---

## 🌐 Ambient Event Triggers

This agent passively listens for:

- `quiz_failed_repeatedly`
- `low_engagement_signals`
- `help_request_events`

In this POC, only one is simulated (`quiz_failed_repeatedly`).

---

## 🧠 Agentic Memory Strategy

In a full implementation, the agent will:

- Store historical topic failures
- Avoid repeating the same suggestions
- Suggest revisiting topics if forgetting is detected

---

## 🔧 Tools Used

- `generate_byte_course_artifact(topic: str) -> str`: Generates a JSON object of 3 slides using Gemini 2.0 Flash.

---

## ⚠️ Risks

- **Over-triggering:** Too many proactive messages can be annoying.
- **Personalization Gaps:** Without memory, suggestions may repeat.
- **Latency:** Calls to Gemini should be optimized for low wait times.

---

## ✅ Next Steps

- Add agentic memory via Firestore or Vector DB.
- Streamlined feedback loop to detect effectiveness of interventions.
