import streamlit as st
import json
import sys
import subprocess
from send_email import send_email
from main import run_scraper, run_pdf_reader, generate_email

st.title("AI Sales Outreach Email Generator")

# Inputs
url = st.text_input("Enter LinkedIn profile URL:")
pdf_file = st.file_uploader("Upload Product PDF", type=["pdf"])
sender_name = st.text_input("Enter your name (sender):")
sender_email = st.text_input("Sender Email:")
sender_password = st.text_input("Sender App Password:", type="password")
recipient_email = st.text_input("Recipient Email:")

if st.button("Generate Email"):
    if url and pdf_file and sender_name:
        # Save uploaded PDF temporarily
        pdf_path = "uploaded_temp.pdf"
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        st.write("🔎 Scraping LinkedIn profile...")
        profile_data = run_scraper(url)

        st.write("📖 Reading PDF content...")
        pdf_data = run_pdf_reader(pdf_path)

        st.write("🤖 Generating Email with DeepSeek...")
        subject, body = generate_email(profile_data, pdf_data, sender_name)

        st.subheader("📧 Suggested Email")
        st.write(f"**Subject:** {subject}")
        st.text_area("Body", body, height=200)

        if st.button("Send Email"):
            send_email(sender_email, sender_password, recipient_email, subject, body)
            st.success(f"✅ Email sent to {recipient_email}")
    else:
        st.error("⚠️ Please provide all inputs (LinkedIn URL, PDF, and Sender Name).")
