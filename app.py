from flask import Flask, request, jsonify, render_template 
import sqlite3
import datetime
import logging

app = Flask(__name__, static_folder='.', static_url_path='')
DATABASE_NAME = 'patients.db'


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verify_patient_in_db(first_name, last_name, dob_str, phone_number):
    
    if not all([first_name, last_name, dob_str, phone_number]):
        logging.error(f"Missing one or more required parameters for verification: FName={first_name}, LName={last_name}, DOB={dob_str}, Phone={phone_number}")
        return False
    

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        dob_date_obj = datetime.datetime.fromisoformat(dob_str.replace('Z', '+00:00'))
        dob_formatted = dob_date_obj.strftime('%Y-%m-%d')
        logging.info(f"Parsed DOB from Dialogflow: {dob_str} to {dob_formatted}")
    except ValueError as e:
        logging.error(f"Error parsing DOB from Dialogflow '{dob_str}': {e}")
        return False 

    
    phone_number_cleaned = ''.join(filter(str.isdigit, phone_number))
    logging.info(f"Cleaned phone number: {phone_number} to {phone_number_cleaned}")

   
    cursor.execute('''
        SELECT * FROM patients
        WHERE LOWER(first_name) = ?
        AND LOWER(last_name) = ?
        AND dob = ?
        AND phone_number = ?
    ''', (first_name.lower(), last_name.lower(), dob_formatted, phone_number_cleaned))

    result = cursor.fetchone() 
    conn.close() 
    
    if result:
        logging.info(f"Patient found in DB: {first_name} {last_name}")
    else:
        logging.info(f"No match found for: {first_name} {last_name}, DOB:{dob_formatted}, Phone:{phone_number_cleaned}")

    return result is not None 

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    logging.info(f"Received Dialogflow webhook request: {req}")
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName')

    if intent_name == 'GatherPhoneNumber':
        
        first_name = None
        last_name = None
        dob = None
        
        phone_number = req.get('queryResult', {}).get('parameters', {}).get('phone-number')

       
        for context in req.get('queryResult', {}).get('outputContexts', []):
            context_params = context.get('parameters', {})

           
            if 'first-name' in context_params and first_name is None:
                first_name = context_params.get('first-name')
            
            
            if 'last-name' in context_params and last_name is None:
                last_name = context_params.get('last-name')

            
            if 'dob' in context_params and dob is None:
                dob = context_params.get('dob')
            
           
            if 'phone-number' in context_params and phone_number is None:
                 phone_number = context_params.get('phone-number')

        
        logging.info(f"Extracted parameters: FName={first_name}, LName={last_name}, DOB={dob}, Phone={phone_number}")

        
        if verify_patient_in_db(first_name, last_name, dob, phone_number):
            fulfillment_text = "Patient verified. How can I help you today?"
        else:
            fulfillment_text = "Sorry, those details do not match our records. Let me gather some more information. Can you please state your full address?"
            session_id = req.get('session')
            output_context = [{
                "name": f"{session_id}/contexts/awaiting_address_after_no_match",
                "lifespanCount": 1
            }]
            return jsonify({'fulfillmentText': fulfillment_text, 'outputContexts': output_context})
        return jsonify({'fulfillmentText': fulfillment_text})
    return jsonify({'fulfillmentText': "I'm sorry, I encountered an unexpected issue."})


@app.route('/')
def serve_index():
    return render_template('index.html')

if __name__ == '__main__':

    app.run(debug=True, port=5000)