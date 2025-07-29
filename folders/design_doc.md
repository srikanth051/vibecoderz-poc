
✅ Part 1: Proactive Agent Design Document (Draft)
(Format: You can copy-paste into a Markdown file or convert to PDF)

📌 Title: Proactive Learning Support Agent – Design Document
🧱 Architecture Overview
High-Level Diagram:

pgsql
Copy
Edit
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
🧠 Event Triggers (Ambient Behavior)
This agent is designed as an Ambient Agent, which means it passively observes the environment for relevant signals and takes action without explicit prompts.

Trigger Sources:

AssessmentAgent emits events like:
{"event_type": "quiz_failed", "user_id": "priya", "topic": "CSS Flexbox"}

Future triggers could include:

Repeated help requests on the same topic

Long pauses or user inactivity

Manual user flagging of confusion

The ProactiveAgent subscribes to these signals (via Pub/Sub or event listeners), processes them, and acts.

🧠 Agentic Memory
Agentic memory ensures the agent:

Remembers failed attempts or repeated struggles.

Avoids sending the same explanation again.

Can suggest a review if a topic hasn't been practiced in a long time.

Implementation Options:
Use a lightweight JSON/SQLite/Firestore key-value store to maintain:

json
Copy
Edit
{
  "user_id": "priya",
  "history": [
    {"topic": "CSS Flexbox", "last_failed": "2025-07-27", "interventions": 2},
    {"topic": "Grid Layout", "last_failed": "2025-07-14", "interventions": 1}
  ]
}
This memory module checks:

Has this user failed this topic before?

Have we already suggested byte artifacts for it?

Is the number of interventions too frequent?

🛠️ Tooling Required
The agent uses the following tools:

Tool Name	Purpose
generateByteCourseArtifact(topic)	Calls LLM API (e.g., Gemini) to create a 3-slide summary JSON.
getUserActivityLog(user_id)	Retrieves recent assessments or user activity data. (Mocked in POC)
AgenticMemoryStore	Reads/writes user-topic interactions to memory.

⚠️ Risks and Mitigations
Risk	Description	Mitigation
Annoying UX	Agent may intervene too frequently or at wrong times	Use memory and cooldown period per topic/user
Poor Quality Suggestions	Byte courses may be too generic	Fine-tune prompt and use relevant context
Latency	LLM call may be slow	Asynchronous artifact generation and caching
Repetition	Recommends same artifact repeatedly	Use agentic memory to track delivered artifacts
Privacy	Handling user activity data	Ensure all data access is permission-scoped