import json
import time
import openai
import os
import requests
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Function to extract navigation links from the HTML content
def extract_links(soup):
    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])
    return links

# Function to extract email addresses from the HTML content
def extract_emails(soup):
    emails = []
    for mailto in soup.select('a[href^=mailto]'):
        emails.append(mailto['href'][7:])
    return emails

# Function to analyze SEO using LLM
def analyze_seo(html_content):
    seo_aspects = [
        "Analyze the overall SEO quality of the following HTML content.",
        "Identify the keywords that this page is optimized for.",
        "Provide recommendations to improve the SEO of this page.",
        "Evaluate the mobile-friendliness of this HTML content.",
        "Assess the page load speed based on the HTML content.",
        "Analyze the use and quality of meta tags in the HTML content.",
        "Evaluate the structure and use of header tags (H1, H2, H3, etc.) in the HTML content.",
        "Assess the internal linking strategy within the HTML content.",
        "Evaluate the use of external links and their relevance.",
        "Analyze the optimization of images within the HTML content.",
        "Evaluate the content quality and relevance for the target audience.",
        "Analyze the use of schema markup in the HTML content.",
        "Evaluate the presence and optimization of alt text for images.",
        "Assess the use of structured data for SEO in the HTML content.",
        "Evaluate the overall user experience based on the HTML content.",
        "Analyze the presence and effectiveness of call-to-actions (CTAs) in the HTML content."
    ]
    seo_analysis = {}
    for aspect in seo_aspects:
        prompt = f"{aspect}\n\nHTML Content:\n{html_content[:2000]}\n\nRespond in JSON format with the following structure: {{'analysis': 'your analysis here', 'score': 0-10}}"
        response = get_ai_response(prompt)
        seo_analysis[aspect] = response
    return seo_analysis



# Function to get the AI response using the specified method
def get_ai_response(prompt):
    print("Sending query to LLM...")
    start_time = time.time()
    
    response = openai.chat.completions.create(
        model="gpt-4o-2024-05-13",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an SEO expert. Respond in JSON format."},
            {"role": "user", "content": prompt}
        ]
    )

    end_time = time.time()
    elapsed_time = end_time - start_time

    message_content = response.choices[0].message.content
    
    # Extract token usage information
    completion_tokens = response.usage.completion_tokens
    prompt_tokens = response.usage.prompt_tokens
    total_tokens = response.usage.total_tokens

    # Attempt to parse the AI response as JSON
    try:
        message_content = json.loads(message_content)
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", message_content)
        # Optionally log the error to a file or take other appropriate actions
        return {"analysis": message_content, "score": 0}
    
    # Print the token usage information
    print("Completion Tokens:", completion_tokens)
    print("Prompt Tokens:", prompt_tokens)
    print("Total Tokens:", total_tokens)
    
    return message_content

# Function to process the URL and extract data
def process_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = extract_links(soup)
    emails = extract_emails(soup)
    seo_analysis = analyze_seo(str(soup))

    data = {
        "url": url,
        "links": links,
        "emails": emails,
        "seo_analysis": seo_analysis
    }

    return data

# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Main function
if __name__ == "__main__":
    url = input("Enter the URL to analyze: ")
    data = process_url(url)
    save_to_json(data, 'url_analysis.json')
    print("Processing complete. Check 'url_analysis.json' for results.")
