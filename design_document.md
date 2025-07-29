# Design Document: The Proactive Byte Course Agent

**Author:** [Your Name]
**Date:** [Current Date]

### 1. Architecture

*A high-level diagram and explanation of how this Proactive Agent fits into our existing multi-agent system.*

**Guiding Questions:**
*   How does information flow? Start from the user's action and end with the agent's message.
*   What other agents or systems does it need to talk to? (e.g., `AssessmentAgent`, `UserActivityDB`).
*   Draw a simple text-based diagram. Example:
    `[User Action on Frontend] -> [Logs to UserActivityDB] -> [AssessmentAgent detects struggle] -> [Pub/Sub Message: 'user_struggling'] -> [ProactiveAgent is triggered]`

*(Write your explanation here)*

### 2. Event Triggers (Ambient Behavior)

*How would this agent be an Ambient Agent? What specific events or signals would it listen for to trigger its intervention?*

**Guiding Questions:**
*   Be specific. What are 3-4 concrete, measurable signals of a user struggling?
*   Example Signal 1: **Failed Quiz.** The `AssessmentAgent` emits a `quiz_failed` event after the user fails the same quiz topic 3 times.
*   Example Signal 2: **Time-on-Task.** A background process notes that `user_id='priya'` has been on the 'CSS Flexbox' lesson page for over 20 minutes with low interaction.

*(List and describe your chosen triggers here)*

### 3. Agentic Memory

*How would this agent use Agentic Memory to make its suggestions personalized and not annoying?*

**Guiding Questions:**
*   **Short-Term Memory:** What does the agent need to remember *during* a single conversation? (e.g., the exact topic).
*   **Long-Term Memory:** What does the agent need to remember about the user over time to avoid being repetitive? (e.g., "I already offered Priya help with Flexbox yesterday."). Think about what data you'd need to store.
*   Example: The agent could use a simple database (like Firestore) to log every time it helps a user with a topic (`{user_id, topic, timestamp}`). Before acting, it would check this log.

*(Describe your memory strategy here)*

### 4. Tooling

*What specific "tools" would this agent need to function?*

**Guiding Questions:**
*   A "tool" is a function the agent can decide to call. The assessment gives you one: `generate_byte_course_artifact`.
*   What other functions might it need? Perhaps one to check the user's history?
*   Tool 1: `generate_byte_course_artifact(topic: str) -> str`: (Required) Generates the educational content.
*   Tool 2: `get_user_struggle_history(user_id: str, topic: str) -> dict`: Checks if the user has struggled with this topic before to add more context.

*(List and describe the tools the agent would need)*

### 5. Risks & Mitigations

*What are the biggest technical or UX risks of this feature?*

**Guiding Questions:**
*   **UX Risk:** The agent is too sensitive and triggers constantly, annoying the user.
    *   **Mitigation:** Implement a "cooldown" period. The agent won't trigger more than once per hour for the same user.
*   **Technical Risk:** The LLM call to generate the course is slow or fails.
    *   **Mitigation:** Implement a timeout and a retry mechanism. Have a fallback message like "I'm having a little trouble generating that right now, but you can find resources here..."

*(List 2-3 key risks and your proposed solutions)*