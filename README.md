
---

# AI-Powered-Personalised-sales-outreach-email-generator

An AI-powered tool that automates **personalized sales outreach emails**.
It scrapes LinkedIn profiles (using cookies), extracts product details from a PDF, and generates a tailored outreach email with **DeepSeek via Ollama**, then sends it via **SMTP**.

---

## ✨ Features

* 🔎 **LinkedIn Scraper** – extracts recipient name, headline, and bio using Selenium with exported cookies.
* 📄 **PDF Reader** – parses your product/service brochure.
* 🤖 **AI Email Generator** – uses DeepSeek (via Ollama) to generate:

  * Catchy subject line
  * Personalized body text
* 📧 **Email Sender** – sends the generated email using SMTP (e.g., Gmail with App Passwords).
* 🖥️ **Pluggable UI** – can be extended with Flask / Streamlit for web deployment.

---

## 📂 Project Structure


---



### Setup LinkedIn Scraper

* Export your **LinkedIn cookies** using a Chrome/Edge extension like **EditThisCookie**.
* Save them in `cookies.json` in the project folder.
* The scraper (`scraper.py`) loads these cookies into Selenium to access profile pages.

### Setup Ollama + DeepSeek

Install [Ollama](https://ollama.ai) and pull DeepSeek:

```bash
ollama pull deepseek-r1:1.5b
```

### Setup SMTP (for Gmail users)

* Enable **2FA** on your Gmail.
* Generate an **App Password** (not your real Gmail password).
* Use it in place of your password when running the script.

---

## 🚀 Usage

Run the tool:

```bash
python main.py
```
for streamlit

```
streamlit run app.py
```

Follow prompts:

1. Enter LinkedIn profile URL
2. Upload your product PDF
3. Enter sender details (name, email, app password)
4. Enter recipient email

The script will:
✅ Scrape LinkedIn → ✅ Read PDF → ✅ Generate email via DeepSeek → ✅ Send via SMTP

---

## 🔮 Future Improvements

* Database to store past outreach attempts.
* Multi-profile batch outreach.

---

## ⚠️ Disclaimer

This project is for **educational purposes only**.
Scraping LinkedIn may violate their Terms of Service. Use responsibly and with your own data.

---
