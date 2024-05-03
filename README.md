# Anomaly Detection in Bank Accounts

## Inspiration
The purpose of this project is to generate detailed notifications using genAI technology for bank accounts.

## What it does
It analyses a list of transactions and detects if there are any suspicious transactions and generates a message and sends a notification to the user.

## How I built it
It is built on python leveraging Gemini 1.5 pro, and steamlit for UI.

## Challenges I ran into
No actual data to deal with and see if it works as efficiently, hence hardcoded the transactions for the prototype.

## Accomplishments that I'm proud of
Successfully accomplished sending email notifications to customers if anomalies/suspicious transactions appear in the bank statement.

## What I learned
How to integrate Gemini into my application and generate responses using prompt engineering.

## What's next for Anomaly Detection in Bank Statements
Next up is streaming the bank transactions instead of hardcoding them to trigger notification when suspicious transaction is noticed.

# To run
Install streamlit and google-generativeai
Update your env variables
streamlit run app.py