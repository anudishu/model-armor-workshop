import time
import requests
from google.auth import default
from google.auth.transport.requests import Request
from vertexai.preview.language_models import ChatModel
from vertexai.generative_models import GenerativeModel

# === Configuration ===
PROJECT_ID = "projecta-418002"
REGION = "us-central1"
TEMPLATE_ID = "demo-armor-template"
USER_PROMPT = "can you remember my ITIN : ###-##-####"

# === Access Token ===
def get_access_token():
    credentials, _ = default()
    credentials.refresh(Request())
    return credentials.token

# === Send prompt to Model Armor ===
def sanitize_prompt(user_prompt):
    url = f"https://modelarmor.{REGION}.rep.googleapis.com/v1/projects/{PROJECT_ID}/locations/{REGION}/templates/{TEMPLATE_ID}:sanitizeUserPrompt"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }
    payload = {"user_prompt_data": {"text": user_prompt}}

    print("\n🔐 Step 1: Sending prompt to Model Armor for safety check...")
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    end_time = time.time()

    response_time = (end_time - start_time) * 1000
    return response.json(), response_time

# === Print beautiful summary ===
def pretty_print_armor_result(response):
    result = response.get("sanitizationResult", {})
    match_state = result.get("filterMatchState", "UNKNOWN")

    print("\n🛡️ Model Armor Evaluation Summary")
    if match_state == "MATCH_FOUND":
        print("❌ Prompt blocked due to policy violation\n")
    else:
        print("✅ Prompt is safe and allowed\n")

    print("🧾 Detailed Filter Breakdown")
    print("| Filter Name         | Match State     | Confidence Level  | Notes |")
    print("|---------------------|------------------|--------------------|-------|")

    filters = {
        "dangerous": "Dangerous Content",
        "harassment": "Harassment",
        "sexually_explicit": "Sexually Explicit",
        "hate_speech": "Hate Speech",
        "pi_and_jailbreak": "PI & Jailbreak",
        "csam": "CSAM (Child Safety)",
        "malicious_uris": "Malicious URIs",
        "sdp": "SDP (Sensitive Data)"
    }

    rai_filters = result.get("filterResults", {}).get("rai", {}).get("raiFilterResult", {}).get("raiFilterTypeResults", {})

    for key, name in filters.items():
        if key in rai_filters:
            item = rai_filters[key]
            state = item.get("matchState", "N/A")
            conf = item.get("confidenceLevel", "-")
        else:
            filter_key = next((k for k in result.get("filterResults", {}) if key in k), None)
            item = result.get("filterResults", {}).get(filter_key, {})
            if isinstance(item, dict):
                state = item.get("matchState", item.get(next(iter(item), {})).get("matchState", "N/A"))
                conf = item.get("confidenceLevel", "-")
            else:
                state, conf = "N/A", "-"

        emoji = "✅" if state == "NO_MATCH_FOUND" else "⚠️"
        print(f"| {name:<20} | {emoji} {state:<14} | {conf:<18} |")

# === Send to Gemini if clean ===
def call_vertex_ai_gemini(prompt_text):
    print("\n🧠 Step 2: Sending safe prompt to Gemini...")
    
    model = GenerativeModel("gemini-1.5-flash")  # or "gemini-1.5-pro"
    response = model.generate_content(prompt_text)

    return response.text

# === Main secure flow ===
def run_secure_prompt(user_input):
    armor_result, latency = sanitize_prompt(user_input)
    result = armor_result.get("sanitizationResult", {})
    match_state = result.get("filterMatchState")

    pretty_print_armor_result(armor_result)

    if match_state == "MATCH_FOUND":
        print("\n🚫 Unsafe input detected by Model Armor. Prompt will NOT be sent to Gemini.")
        return

    print("\n✅ Model Armor passed. Sending to Gemini...")
    gemini_reply = call_vertex_ai_gemini(user_input)
    print(f"\n🧠 Gemini's Response:\n{gemini_reply}")

# === Run the flow ===
run_secure_prompt(USER_PROMPT)
