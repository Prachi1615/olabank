"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from prompts import system_instruction
import streamlit as st
from anomaly_detection import analyze_transactions, transactions


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

sender_email=os.getenv("sender_email")
password=os.getenv("password")

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
def get_user_input():
  """
  Prompts the user for anomaly detection parameters within a Streamlit UI.
  """
  amount_threshold = st.number_input("Minimum amount threshold for anomalies:", min_value=0.0)
  unusual_merchants = st.text_input("Comma-separated list of unusual merchants (e.g., 'Jewelry Store,Casino'): ")
  if unusual_merchants:
    unusual_merchants = unusual_merchants.split(",")
  return {"amount_threshold": amount_threshold, "unusual_merchants": unusual_merchants}

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["casino=$4000"]
  },
  {
    "role": "model",
    "parts": ["## Casino Transaction Detected! \n\nThis is an alert regarding a potential anomaly in your recent transactions. A significant amount of \\$4,000 was spent at a casino. \n\n**Recommended Actions:**\n\n* **Verify Transaction:** Please confirm if this transaction was authorized by you. \n* **Review Spending:** If the transaction is legitimate, it might be helpful to review your spending habits and consider if adjustments are needed.  \n* **Seek Assistance:** If you believe this transaction is fraudulent, please contact your bank immediately to report it and take necessary security measures.\n\n**Additional Resources:**\n\n* **National Problem Gambling Helpline:** 1-800-522-4700\n* **Financial Counseling Services:** (You may want to research reputable financial counseling services in your area)"]
  },
])

def get_llm_response(prompt):
  """
  Sends a prompt to the LLM model and returns the generated response.
  """
  global convo  # Access the global convo object from the main program

  # Send the prompt to the LLM model using the conversation object
  convo.send_message(prompt)
  return convo.last.text


# convo.send_message("food=$20")
# print(convo.last.text)
st.title("Bank Transaction Anomaly Detection")

# Get user input for anomaly detection parameters
parameters = get_user_input()

# Analyze transactions based on user input
anomalies = analyze_transactions(transactions.copy(), parameters)

def send_email(recipient_email, subject, body):
    """
    Sends an email with the specified recipient, subject, and body.
    """
    sender_email = os.getenv("sender_email")
    password = ("password")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    

    try:
            # Connect to the SMTP server (in this case, Gmail's SMTP server)
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                # Start TLS for security'\
                server.ehlo()
                server.starttls()
                # Login to the email account
                server.login(sender_email, password)
                # Send the email
                server.sendmail(sender_email, recipient_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Display anomaly results (if any)
if anomalies:
  st.subheader("Potential Anomalies Detected:")
  for anomaly in anomalies:
    st.write(f"- Amount: ${anomaly['amount']}, Merchant: {anomaly['merchant']}")

    # Add loading indicator while generating LLM response
    with st.spinner("Generating insights..."):
      llm_response = get_llm_response(f"Detected anomaly: ${anomaly['amount']} at {anomaly['merchant']}")
    st.write(llm_response)  # Display LLM response below the anomaly details

    recipient_email = st.text_input("Enter recipient email address:")

    # Button to trigger email generation and sending
    if st.button("Send Email Alert"):
      if recipient_email:
        # Send email using the function defined earlier
        send_email(recipient_email, f"Anomaly Detected: {anomaly['merchant']}", llm_response)
      else:
        st.error("Please enter a valid email address.")

else:
  st.success("No anomalies found in transactions.")