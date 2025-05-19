import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from src.config.settings import *
from langchain_community.tools import DuckDuckGoSearchRun, tool,StructuredTool

@tool
def smtp_gmail(data: Dict) -> str:
    """
  Send a support query email to the dev team and optionally a confirmation to the user.

  Expected `data` format:
  {
      "user_message": "...",
      "user_name": "...",
      "user_email": "...",
  }
  """

    try:
        user_message = data.get("user_message", "")
        user_name = data.get("user_name", "Unknown")
        user_email = data.get("user_email", "")
        send_user_confirmation = True

        # --- Email to Dev Team ---
        msg_to_dev = MIMEMultipart()
        msg_to_dev["From"] = AVA_SERVICE_MAIL
        msg_to_dev["To"] = ", ".join(DEV_MAIL_LIST)
        msg_to_dev["Subject"] = f"[Ava Support] New Query from {user_name}"

        body_dev = f"""
        Hi Team,
        📨 New Support Query

        👤 Name: {user_name}  
        📧 Email: {user_email}

        💬 Message:
        {user_message}

        Sent via Ava ❤, the Virtual Assistant 🤖
        """

        msg_to_dev.attach(MIMEText(body_dev.strip(), "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(AVA_SERVICE_MAIL, SMTP_MAIL_APP_PASSWORD)
            server.sendmail(AVA_SERVICE_MAIL, DEV_MAIL_LIST, msg_to_dev.as_string())

        print("📩 Developer email sent.")

        # --- Optional Confirmation to User ---
        if send_user_confirmation:
            msg_to_user = MIMEMultipart()
            msg_to_user["From"] = AVA_SERVICE_MAIL
            msg_to_user["To"] = user_email
            msg_to_user["Subject"] = "Your query has been received – Ava's on it! 💌"

            body_user = f"""
            Hi {user_name},

            Thanks for contacting us! Ava received your message and passed it to our team 👩‍💻👨‍💻.

            We're reviewing it and will get back to you shortly.

            💬 Your message:
            {user_message}

            Love ❤,  
            Ava – Virtual Assistant 🩷  
            Cogniforge AI  
            📧 cogniforgeaiava@gmail.com
            """

            msg_to_user.attach(MIMEText(body_user.strip(), "plain"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(AVA_SERVICE_MAIL, SMTP_MAIL_APP_PASSWORD)
                server.sendmail(AVA_SERVICE_MAIL, user_email, msg_to_user.as_string())

            print("✅ Confirmation email sent to user.")

        return "📧 Email(s) sent successfully."

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return f"❌ Failed to send email: {e}"
