# Proactive Byte Course Agent - Proof of Concept

**Author:** [Your Name]
**Version:** 1.0.0
**Status:** Proof of Concept - Ready for Integration Review

---

## 1. Overview

This repository contains the Proof of Concept (POC) for the **Proactive Byte Course Agent**, a foundational AI component for the Vibecoderz "Superficient Learning" platform.

The agent's primary function is to intelligently detect when a learner is struggling with a specific topic (e.g., repeatedly failing a quiz) and proactively intervene. It uses the Gemini API to automatically generate a personalized, bite-sized micro-course (a "Byte Course") to help the user overcome their learning obstacle in real-time.

The goal is to increase learner engagement, reduce frustration, and create a truly supportive and interactive learning experience that feels magical to the user. This POC demonstrates the core agentic loop: **Observe -> Reason -> Act**.

## 2. How to Set Up and Run the POC

This POC is a standalone Python script (`poc.py`) that simulates the agent's core logic. Follow these steps precisely to run it on your local machine.

### Prerequisites

*   Python 3.9+
*   A Google Cloud Platform (GCP) account with an active billing account.
*   The `gcloud` command-line tool installed and updated (`gcloud components update`).

### Step-by-Step Setup

1.  **Clone the Repository:**
    ```bash
    git clone [Your GitHub Repository URL]
    cd [Your Repository Folder Name]
    ```

2.  **Set Up a Virtual Environment:**
    This isolates the project's dependencies from your system's Python.
    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate it (on Windows PowerShell)
    .\venv\Scripts\activate

    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install Dependencies:**
    A `requirements.txt` file is included with the necessary libraries.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Google Cloud Project Setup (CRITICAL First-Time Setup):**
    This agent requires a correctly configured GCP project. Our testing has shown that new or existing projects can sometimes have incomplete provisioning. **Creating a new, clean project is the most reliable method to avoid access-related errors.**

    a. **Create a New GCP Project:** Go to the [GCP Console](https://console.cloud.google.com/projectcreate) and create a new project. Give it a unique name (e.g., `my-ai-agent-test`).

    b. **Get the Project ID:** On the project dashboard, find and copy the **Project ID** (e.g., `my-ai-agent-test-123456`). You will need this for the next steps.

    c. **Enable Billing:** Go to the [Billing Page](https://console.cloud.google.com/billing) and ensure your new project is linked to an active billing account. This is required to use the Vertex AI API, though the usage for this POC will fall within the free tier.

    d. **Enable the Vertex AI API:** This is a crucial step. Go to the [Vertex AI API Page for your project](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com) (make sure your new project is selected in the top bar) and click the **ENABLE** button. Wait a few minutes for this to take effect.

    e. **Authenticate the `gcloud` CLI:** Run the following command. It will open a browser window for you to log in and consent. This is for general CLI access.
       ```bash
       gcloud auth login
       ```

    f. **Set Up Application Default Credentials (ADC):** This is what your Python script will use to authenticate. Run the following command and grant all requested permissions in the browser, especially for "Google Cloud Platform".
       ```bash
       gcloud auth application-default login
       ```

5.  **Configure the POC Script:**
    Open the `poc.py` file and update the `PROJECT_ID` variable with your new, working GCP Project ID from step 4b.
    ```python
    # poc.py
    PROJECT_ID = "your-new-working-project-id" # <-- Update this value
    ```

### Running the Agent Simulation

Once the setup is complete, run the script from your terminal (ensure your virtual environment is still active):

```bash
python poc.py