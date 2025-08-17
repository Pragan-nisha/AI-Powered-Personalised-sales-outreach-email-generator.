import subprocess
import json
import sys


def run_scraper(url):
    result = subprocess.run(
        [sys.executable, "TOOLS/scraper.py", url],  # <- use the current env Python
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
       [sys.executable, "TOOLS/pdfreader.py", file_path],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)
def clean_json_output(output: str):
    # DeepSeek often adds "Thinking..." before the JSON.
    if "{" in output:
        return output[output.index("{"):]  # keep from first { onward
    return output

def generate_email(profile_data, pdf_data):
    sender_name = input("Enter your name (sender): ").strip()

    prompt = f"""
Write a short personalized sales outreach email.

Recipient's info:
Name: {profile_data.get('name')}
Headline: {profile_data.get('headline')}
Bio: {profile_data.get('bio')}

Product info:
{pdf_data.get('content')}

Requirements:
- Greet the recipient by their name.
- Use '{sender_name}' as the sender, do NOT confuse it with the recipient.
- Write a catchy subject line relevant to the product.
- Keep the email under 100 words, professional, friendly, and relevant to the recipient's background.
- Do NOT include any emojis or stars.
"""


    # Call DeepSeek via Ollama
    ollama_cmd = ["ollama", "run", "deepseek-r1:1.5b", prompt]
    subprocess.run(ollama_cmd)
    


if __name__ == "__main__":
    url = input("Enter LinkedIn profile URL: ").strip()
    pdf_path = input("Enter product PDF file path: ").strip()

    print("\nScraping LinkedIn profile...")
    profile_data = run_scraper(url)

    print("Reading PDF...")
    pdf_data = run_pdf_reader(pdf_path)

    print("\nGenerating email with DeepSeek...\n")
    generate_email(profile_data, pdf_data)
