import json
import time
import openai

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


# Function to generate a prompt for the AI based on the email data
def generate_promptxc(email):
    prompt = f"""
    The following is a customer email to a brewery/restaurant. Respond to the email appropriately.
    
    here are some examples of the type of responses you must provide:
    {
    "Response": "Dear [Customer Name], Thank you for reaching out to Brewery-Red for your reservation inquiry. We currently have availability for 4 people on Saturday evening. Would you like to proceed with the reservation? Please let us know your preferred time and any special requests. We look forward to hosting you at Brewery-Red!",
    "Type": "Reservation",
    "Action": "Confirm_reservation"
    }
    or 
    {
    "Response": "Dear [Customer Name], Thank you for reaching out to us. We appreciate your interest in The Barn. I've attached a digital copy of our current menu to this email to help you review your dining options considering your dietary restrictions. If you need any further assistance or have specific questions about the menu items, feel free to let us know.",
    "Type": "Reservation",
    "Action": "Send_menu"
    }
    
    {
    "Response": "Dear [Customer Name], Thank you for sharing your feedback, and we are delighted to hear that you enjoyed your dining experience at The Brewery. We appreciate your kind words and look forward to welcoming you back soon. If you have any further comments or suggestions, please do not hesitate to let us",
    "Type": "Reservation",
    "Action": ""
    }


    """
    if 'previous_complaints' in email:
        for complaint in email['previous_complaints']:
            prompt += f"\n\nPrevious Complaint (Date: {complaint['date']}): {complaint['message']}"
    prompt += "\n\nAI Response:"
    return prompt

def generate_prompt(email):
    prompt = f"""
    The following is a customer email to a brewery/restaurant. Respond to the email appropriately.

    Customer Email:
    Subject: {email['subject']}
    Message: {email['message']}
    """
    if 'previous_complaints' in email:
        for complaint in email['previous_complaints']:
            prompt += f"\n\nPrevious Complaint (Date: {complaint['date']}): {complaint['message']}"
    prompt += """
    here are some examples of the type of responses you must provide:
    {
    "Response": "Dear [Customer Name], Thank you for reaching out to Brewery-Red for your reservation inquiry. We currently have availability for 4 people on Saturday evening. Would you like to proceed with the reservation? Please let us know your preferred time and any special requests. We look forward to hosting you at Brewery-Red!",
    "Type": "Reservation",
    "Action": "Confirm_reservation"
    }
    or 
    {
    "Response": "Dear [Customer Name], Thank you for reaching out to us. We appreciate your interest in The Barn. I've attached a digital copy of our current menu to this email to help you review your dining options considering your dietary restrictions. If you need any further assistance or have specific questions about the menu items, feel free to let us know.",
    "Type": "Reservation",
    "Action": "Send_menu"
    }
    
    {
    "Response": "Dear [Customer Name], Thank you for sharing your feedback, and we are delighted to hear that you enjoyed your dining experience at The Brewery. We appreciate your kind words and look forward to welcoming you back soon. If you have any further comments or suggestions, please do not hesitate to let us",
    "Type": "Reservation",
    "Action": ""
    }
    AI Response:
    {
    "Response": (the text to be sent to the customer)
    "Type":  (of customer query e.g., reservation, complaint, inquiry):
    "Action": ( needed by the business ownere.g., send_menu, confirm_reservation, phone_call, call_police,):
    }
    """
    return prompt




# Function to get the AI response using the updated method
def get_ai_response(prompt):
    print("Sending query to LLM...")
    start_time = time.time()
    
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an English copywriting expert."},
            {"role": "user", "content": prompt}
        ]
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    #print(response.choices[0].message)

    message_content = response.choices[0].message.content
    
    # Extract token usage information
    completion_tokens = response.usage.completion_tokens
    prompt_tokens = response.usage.prompt_tokens
    total_tokens = response.usage.total_tokens
    
    # Print the parsed information
    print("AI Response:", message_content)
    print("Completion Tokens:", completion_tokens)
    print("Prompt Tokens:", prompt_tokens)
    print("Total Tokens:", total_tokens)
    
    return message_content


def get_ai_responsex(prompt):
    # Simulated response for debugging
    simulated_response = (
        "Dear Customer,\n\n"
        "Thank you for reaching out to us. We apologize for any inconvenience caused. "
        "Your feedback is important to us, and we will take the necessary steps to address the issue. "
        "Please feel free to reach out if you have any further concerns.\n\n"
        "Best regards,\n"
        "Customer Support Team"
    )
    return simulated_response



# Load the emails from the JSON file
with open('emails.json', 'r') as f:
    data = json.load(f)

# Prepare the new data structure to hold the original emails and AI responses

processed_emails = []  # Initialize the list here

# Loop through each email, generate the prompt, get the AI response, and store the results
for email in data['emails'][:200]:
    prompt = generate_prompt(email)
    ai_response = get_ai_response(prompt)
    email_with_response = {
        "email": email,
        "ai_response": ai_response
    }
    processed_emails.append(email_with_response)

# HTML content generation
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
    <title>Email Responses</title>
    <style>
        .email-box, textarea {
            width: 100%;
            height: auto;
            min-height: 300px; /* This ensures a minimum height but allows the element to grow */
            overflow: visible; /* Ensure content is visible without scrolling */
            resize: none; /* Prevent manual resizing */
            box-sizing: border-box;
        }
        .email-box {
            border: 1px solid #ccc;
            padding: 10px;
            white-space: pre-wrap; /* Ensure the text wraps */
            word-wrap: break-word; /* Ensure long words break correctly */
        }
        table {
            width: 100%;
        }
        td, th {
            width: 50%; /* AI response column width */
        }
        td:first-child, th:first-child {
            width: 37.5%; /* Original email column width */
        }
        td:last-child, th:last-child {
            width: 12.5%; /* Action column width */
        }
    </style>
</head>
<body>
    <main class="container">
        <h1>Email Responses</h1>
        <table>
            <thead>
                <tr>
                    <th>Original Email</th>
                    <th>AI Suggested Response</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
'''

for item in processed_emails:
    original_email = f"Subject: {item['email']['subject']}\nMessage: {item['email']['message']}"
    ai_response = item['ai_response']

    html_content += f'''
                <tr>
                    <td><div class="email-box">{original_email}</div></td>
                    <td><textarea>{ai_response}</textarea></td>
                    <td><button>Send</button></td>
                </tr>
    '''

html_content += '''
            </tbody>
        </table>
    </main>
</body>
</html>
'''

# Write the HTML content to a new file
with open('emails_with_ai_responses.html', 'w') as f:
    f.write(html_content)

print("Processing complete. Check 'emails_with_ai_responses.html' for results.")