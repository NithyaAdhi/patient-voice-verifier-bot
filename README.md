# patient-voice-verifier-bot

## 1. Introduction

This project implements a **Patient Voice Verifier Bot** . The primary goal of this voice bot is to securely verify a patient's identity by collecting key personal information (first name, last name, date of birth, and phone number) and matching it against a simulated database. If a match is found, the patient is verified; otherwise, the bot prompts for alternative verification details (e.g., address).


## 2. Features

*   **Conversational Flow:** Guides the user through collecting necessary personal details.
*   **First Name Collection:** Prompts and captures the patient's first name.
*   **Last Name Collection:** Prompts and captures the patient's last name.
*   **Date of Birth Collection:** Prompts and captures the patient's date of birth.
*   **Phone Number Collection:** Prompts and captures the patient's phone number.
*   **Identity Verification:** Compares collected data against a simulated patient database.
*   **Verification Confirmation:** Announces "Patient verified" upon a successful match.
*   **Verification Denial & Fallback:** Announces "Not a match" and initiates a fallback flow (e.g., asking for an address).

## 3. Proof of Concept Scope

This repository focuses on demonstrating the fundamental interaction and verification logic.
**It is explicitly a Proof of Concept and is NOT production-ready, especially concerning data security, scalability, and full compliance.**

## 4. Technologies Used

*   **Google Dialogflow ES:** For Natural Language Understanding (NLU), dialogue management, Speech-to-Text (STT), and Text-to-Speech (TTS).
*   **Python :** For the backend webhook logic.
*   **Flask:** A lightweight Python web framework for creating the webhook endpoint.
*   **`ngrok`:** A utility to expose the local Flask development server to the internet, allowing Dialogflow to access the webhook.
*   **JSON (Simulated Database):** A simple JSON file (`patients.json`) is used to mimic a patient database for quick PoC development.

## 5. Project Structure
.
├── app.py # Flask backend for Dialogflow webhook fulfillment
├── patients.json # Simulated patient database
├── requirements.txt # Python dependencies
└── README.md # This README file
code
Code


## 6. Setup and Installation

### Prerequisites

*   **Python 3:** [Download and Install Python](https://www.python.org/downloads/)
*   **`pip`:** Python package installer (usually comes with Python).
*   **Google Cloud Account:** Required to use Dialogflow ES.
*   **`ngrok`:** [Download and Install ngrok](https://ngrok.com/download) and set up your auth token.

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/patient-voice-verifier-bot-poc.git
    cd patient-voice-verifier-bot-poc
    ```
2.  **Create a Python virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure `requirements.txt` contains `Flask` and `ngrok`)*
4.  **Review `patients.json`:** This file contains sample patient data. You can modify it to test different scenarios.
    ```json
    [
        {
            "first_name": "John",
            "last_name": "Doe",
            "dob": "1990-01-01",
            "phone_number": "+15551234567",
            "address": "123 Main St"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "dob": "1985-05-15",
            "phone_number": "+15559876543",
            "address": "456 Oak Ave"
        }
    ]
    ```
    *Note: `dob` should be in `YYYY-MM-DD` format. `phone_number` should be in E.164 format (`+CountryCodePhoneNumber`).*

### Dialogflow ES Agent Setup

1.  **Go to Dialogflow ES Console:** [https://dialogflow.cloud.google.com](https://dialogflow.cloud.google.com)
2.  **Create a new Agent.**
3.  **Define Intents:** Create intents as described in the project documentation (or import an agent export if available). Key intents include:
    *   `Welcome`: Initiates the conversation.
    *   `Get_FirstName`: Captures first name (with `@sys.given-name` entity).
    *   `Get_LastName`: Captures last name (with `@sys.last-name` entity).
    *   `Get_DOB`: Captures date of birth (with `@sys.date` entity).
    *   `Get_PhoneNumber`: Captures phone number (with `@sys.phone-number` entity). This intent should have **Fulfillment enabled** to trigger the webhook.
    *   `Fallback` (or similar): For handling unmatched input.
    *   (Optional) `Ask_Address`: For the follow-up question when verification fails.
4.  **Enable Fulfillment:**
    *   Navigate to the `Fulfillment` section in Dialogflow.
    *   Enable the `Webhook` option.
    *   The `URL` field will be updated dynamically in the next step when you run `ngrok`.

## 7. How to Run

1.  **Start the Flask Backend:**
    Open your terminal in the project directory and run:
    ```bash
    python app.py
    ```
    This will start the Flask server, usually on `http://127.0.0.1:5000`.

2.  **Expose the Flask App using ngrok:**
    Open a *new* terminal window and run:
    ```bash
    ngrok http 5000
    ```
    `ngrok` will provide a temporary public HTTPS URL (e.g., `https://xxxx-xxxx-xxxx-xxxx.ngrok.io`).

3.  **Update Dialogflow Fulfillment URL:**
    *   Copy the `https://` URL from your `ngrok` terminal.
    *   Go to your Dialogflow agent's `Fulfillment` section.
    *   Paste the `ngrok` URL into the `URL` field.
    *   **Append `/webhook` to the URL** (e.g., `https://xxxx-xxxx-xxxx-xxxx.ngrok.io/webhook`).
    *   Scroll down and click `Save`.

4.  **Enable Webhook for `Get_PhoneNumber` Intent:**
    *   Go to the `Get_PhoneNumber` intent in Dialogflow.
    *   Scroll down to the `Fulfillment` section.
    *   Check the box `Enable webhook call for this intent`.
    *   Click `Save`.

5.  **Test the Bot:**
    *   Use the **Dialogflow Simulator** on the right side of the Dialogflow console.
    *   Start a conversation with "Hi" or "Hello".
    *   Provide details for a matching patient (e.g., John Doe, 1990-01-01, +15551234567).
    *   Provide details for a non-matching patient to see the "Not a match" response.
    *   (Optional) For live phone testing: Go to `Integrations` in Dialogflow, enable `Dialogflow Phone Gateway`, and call the provided number.

## 8. Usage Example

**User:** "Hello, I'd like to verify my identity."
**Bot:** "Hello! I can help you verify your identity. What is your first name?"
**User:** "My name is John."
**Bot:** "Thank you, John. What is your last name?"
**User:** "Doe."
**Bot:** "Okay, John Doe. What is your date of birth?"
**User:** "January 1st, 1990."
**Bot:** "Got it. And finally, what is your phone number?"
**User:** "My number is 555-123-4567."
**Bot:** "Patient verified."

---

**User:** "Hello, I'd like to verify my identity."
**Bot:** "Hello! I can help you verify your identity. What is your first name?"
**User:** "My name is Alice."
**Bot:** "Thank you, Alice. What is your last name?"
**User:** "Wonderland."
**Bot:** "Okay, Alice Wonderland. What is your date of birth?"
**User:** "December 25th, 1999."
**Bot:** "Got it. And finally, what is your phone number?"
**User:** "It's 555-000-1111."
**Bot:** "Not a match. Please provide your full address to continue."

## 9. Future Enhancements & Production Considerations

To move beyond a PoC and into a production environment, the following enhancements and considerations are critical:

*   **Real Database Integration:** Replace `patients.json` with a robust, scalable, and secure database (e.g., PostgreSQL, MySQL, MongoDB, or integration with an existing EHR/PMS system).
*   **Comprehensive Error Handling:** Implement more sophisticated error handling for invalid input, unexpected responses, and system failures.
*   **Robust Re-prompts:** Design clearer and more user-friendly re-prompts for when the bot doesn't understand.
*   **Human Agent Handoff:** Implement the ability to seamlessly transfer a conversation to a live human agent if the bot cannot resolve the query.
*   **Advanced Verification:** Add options for security questions, multi-factor authentication, or other verification methods.
*   **Full Address Collection:** Develop a complete conversational flow for collecting and validating full address details when initial verification fails.
*   **Telephony Integration:** Integrate with a robust telephony platform like Twilio or Vonage for production-grade phone call handling.
*   **Logging and Monitoring:** Implement comprehensive logging for debugging, auditing, and performance monitoring.
*   **Internationalization:** Support multiple languages and regional date/phone number formats.
*   **Scalability:** Ensure the backend and Dialogflow agent can handle a large volume of concurrent calls.
*   **User Experience (UX) Refinements:** Continuous tuning of bot responses, voice quality (TTS), and speech recognition (STT) for a natural and efficient interaction.

