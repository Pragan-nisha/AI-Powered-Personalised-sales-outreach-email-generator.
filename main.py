import subprocess
import subprocess
import json
import sys
import json
from send_email import send_email

def run_scraper(url):
    result = subprocess.run(
        [sys.executable, "scraper.py", url],  # <- use the current env Python
        capture_output=True, text=True
    )
    print("Scraper stdout:", result.stdout)
    
    print("Scraper stderr:", result.stderr)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print("Scraper output invalid")
        return {"error": "Scraper failed"}
    

def run_pdf_reader(file_path):
    result = subprocess.run(
       [sys.executable, "pdfreader.py", file_path],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)


def clean_json_output(output: str):
    # DeepSeek often adds "Thinking..." before the JSON.
    if "{" in output:
        return output[output.index("{"):]  # keep from first { onward
    return output


def generate_email(profile_data, pdf_data, sender_name):
    
    prompt = f"""
Return ONLY valid JSON (no explanation, no thinking).
Format strictly as:
{{
  "subject": "<catchy subject>",
  "body": "<email body under 150 words **ending with 'Best regards, {sender_name}' in new line in the left corner**>"
}}

Recipient's info:
r.Name: {profile_data.get('name')}
Headline: {profile_data.get('headline')}
Bio: {profile_data.get('bio')}

Product info:
{pdf_data.get('content')}

Requirements:
- Greet the recipient by their actual name ({profile_data.get('r.Name', 'there')}).
- Use '{sender_name}' as the sender (signature).
- Personalise the email for the sender to sell this product make it attractive.
- Keep it professional, under 100 words, no emojis.no stars.
"""

    result = subprocess.run(
        ["ollama", "run", "deepseek-r1:1.5b", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )


    output = result.stdout.strip()
    cleaned = clean_json_output(output)

    try:
        data = json.loads(cleaned)
        subject = data.get("subject")
        body = data.get("body")
    except Exception as e:
        print("⚠️ Failed to parse JSON, using fallback:", e)
        subject = "Follow-up: AI Solutions"
        body = f"Hi {profile_data.get('name', 'there')},\n\nI wanted to share our solution: {pdf_data.get('content')}\n\nBest regards,\n{sender_name}"

    return subject, body
    
if __name__ == "__main__":
    
    url = input("Enter LinkedIn profile URL: ").strip()
    pdf_path = input("Enter product PDF file path: ").strip()

    print("\nScraping LinkedIn profile...")
    profile_data = run_scraper(url)

    print("Reading PDF...")
    pdf_data = run_pdf_reader(pdf_path)
    
    sender_name= input("Enter sender name: ").strip()
    print("\nGenerating email with DeepSeek...\n")
    

    # 1️⃣ Capture DeepSeek output
    subject, body = generate_email(profile_data, pdf_data,sender_name)      

    # 2️⃣ Ask user for SMTP info
    sender_email = input("Enter your email: ").strip()
    sender_password = "fgvo tayv zopc gffp"
    recipient_email = input("Enter recipient email: ").strip()

    # 3️⃣ Send the email
    send_email(sender_email, sender_password, recipient_email, subject, body)

