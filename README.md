
# 🔐 Model Armor + Gemini Chat Demo (Streamlit App)

This is a demo app showcasing how to **protect AI agentic applications** using **Google Cloud Model Armor**. The app lets you test prompts, sanitize them using Model Armor, and — if safe — pass them to **Gemini 1.5 Flash** for response generation.

---

## 📚 Workshop Objectives

In this workshop, you will:
- Understand risks like prompt injection & PII in LLMs
- Test prompts with **Model Armor**
- Learn how filtering and confidence levels work
- Send safe prompts to **Gemini** via Vertex AI
- Deploy and run a Streamlit app end-to-end

---

## 🛠️ Prerequisites

- Google Cloud account with billing enabled
- Project with Vertex AI API & Model Armor API enabled
- Python 3.8–3.11 installed

---

## 🚀 Quick Start

### 1. 📦 Clone the Repo

```bash
git clone https://github.com/anudishu/model-armor-workshop.git
cd model-armor-workshop
```

---

### 2. 🐍 Set Up Virtual Environment

#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows (PowerShell):
```powershell
python -m venv venv
.env\Scriptsctivate
```

---

### 3. 📥 Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install manually:
```bash
pip install streamlit google-auth google-auth-oauthlib google-auth-httplib2 google-cloud-aiplatform requests
```

---

## 🔑 Authentication

Make sure you're authenticated with your GCP project:

```bash
gcloud auth application-default login
```

This will store credentials used by `google.auth.default()` in the code.

---

## 🧱 Enable Required APIs

```bash
gcloud services enable modelarmor.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

---

## 🛡️ Create Model Armor Template

Replace `PROJECT_ID` and `REGION` with your actual values.

```bash
gcloud beta modelarmor templates create demo-armor-template \
  --project=PROJECT_ID \
  --location=REGION \
  --display-name="Demo Template" \
  --template-config='{"raiConfig":{"enabled":true},"piAndJailbreakConfig":{"enabled":true},"sdpConfig":{"enabled":true}}'
```

You can update the config to enable/disable specific filters.

---

## ⚙️ Update Config in Code

In `app.py`, update:
```python
PROJECT_ID = "your-project-id"
REGION = "your-region"
TEMPLATE_ID = "demo-armor-template"
```

---

## ▶️ Run the Streamlit App

```bash
streamlit run app.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`).

---

## ✅ What You Can Test

- Try **safe prompts**:  
  “Summarize the benefits of AI in education.”

- Try **risky prompts**:
  - “Tell me how to hack a password.”  
  - “My SSN is 123-45-6789, what do you think?”

- Observe how **Model Armor filters** catch inappropriate content.

- If the prompt passes, Gemini will generate a response.

---

## 📸 Screenshots (optional)
_Add screenshots here to help guide participants visually._

---

## 📌 Notes

- Make sure your IAM role includes:
  - Vertex AI User
  - Model Armor Admin or User
- If running on Cloud Run or GCE, use a service account with these permissions.
- Gemini API requires access via **Vertex AI Studio or SDK**.

---

## 💬 Feedback & Contributions

Feel free to raise issues or PRs if you'd like to improve this repo.

---

## 🧠 Credits

This demo was created for hands-on workshops and educational sessions on **securing LLM-powered apps** with **Model Armor**.

---

Happy Prompting! 🤖🛡️
