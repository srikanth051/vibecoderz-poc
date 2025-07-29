# ✅ Proactive Learning Support Agent – Design Document

## 📌 Title: Proactive Learning Support Agent – Design Document

---

## 🧱 Architecture Overview

### High-Level Diagram:

```
                    ┌────────────────────────────┐
                    │    AssessmentAgent         │
                    │ (emits failed topic event) │
                    └────────────┬───────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │     ProactiveAgent         │
                    │ (Listens & reacts to event)│
                    └────────────┬───────────────┘
                                 │
             ┌──────────────────┴───────────────────┐
             │                                      │
             ▼                                      ▼
┌────────────────────────────┐         ┌────────────────────────────┐
│ AgenticMemory              │         │ Tool: generateByteCourse   │
│ (checks user history)      │         │ (calls LLM to generate     │
│                            │         │  3-slide summary)          │
└────────────────────────────┘         └────────────────────────────┘
             │                                      │
             └──────────────────┬───────────────────┘
                                ▼
                   ┌────────────────────────────┐
                   │ User Notification / Output │
                   │ "Here’s a quick recap on..."│
                   └────────────────────────────┘
```

---

## 🧠 Event Triggers (Ambient Behavior)

This agent is designed as an **Ambient Agent**, meaning it passively observes the environment and takes action without explicit prompts.

### 🔔 Trigger Sources:

- **AssessmentAgent** emits events like:
```json
{"event_type": "quiz_failed", "user_id": "priya", "topic": "CSS Flexbox"}
```

### 📈 Future triggers (to be added):

- Repeated help requests on the same topic
- Long pauses or user inactivity
- Manual user flagging of confusion

The `ProactiveAgent` listens to these signals (via Pub/Sub or event listeners), processes them, and takes action.

---

## 🧠 Agentic Memory

Agentic memory ensures the agent can:

- Remember failed attempts or repeated struggles
- Avoid sending the same explanation again
- Suggest review if a topic hasn’t been practiced recently

### 🛠️ Implementation Options

Use a lightweight JSON/SQLite/Firestore key-value store to maintain user memory:

```json
{
  "user_id": "priya",
  "history": [
    {"topic": "CSS Flexbox", "last_failed": "2025-07-27", "interventions": 2},
    {"topic": "Grid Layout", "last_failed": "2025-07-14", "interventions": 1}
  ]
}
```

### 🔍 Memory Module Checks:

- Has this user failed this topic before?
- Have we already suggested byte artifacts for it?
- Is the number of interventions too frequent?

---

## 🛠️ Tooling Required

| Tool Name                    | Purpose                                                  |
|-----------------------------|----------------------------------------------------------|
| `generateByteCourseArtifact(topic)` | Calls LLM API (e.g., Gemini) to create a 3-slide summary JSON |
| `getUserActivityLog(user_id)`       | Retrieves recent assessments or user activity data (mocked) |
| `AgenticMemoryStore`               | Reads/writes user-topic interactions to memory             |

---

## ⚠️ Risks and Mitigations

| Risk                  | Description                                       | Mitigation                                      |
|-----------------------|---------------------------------------------------|-------------------------------------------------|
| Annoying UX           | Agent may intervene too frequently or inappropriately | Use memory and cooldown period per topic/user |
| Poor Quality Suggestions | Byte courses may be too generic                   | Fine-tune prompt and add contextual relevance   |
| Latency               | LLM call may be slow                             | Use asynchronous generation and caching         |
| Repetition            | Recommends same artifact repeatedly              | Track delivered artifacts using memory          |
| Privacy               | Handling user activity data                      | Permission-based scoped data access             |

---

