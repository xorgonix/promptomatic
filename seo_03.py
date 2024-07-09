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

# Function to extract image URLs from the HTML content
def extract_images(soup):
    images = []
    for img in soup.find_all('img', src=True):
        images.append(img['src'])
    return images

# Function to check for the presence of robots.txt
def check_robots_txt(url):
    robots_url = url.rstrip('/') + "/robots.txt"
    response = requests.get(robots_url)
    if response.status_code == 200:
        return response.text
    else:
        return "robots.txt not found"

# Function to check for the presence of sitemap.xml
def check_sitemap_xml(url):
    sitemap_url = url.rstrip('/') + "/sitemap.xml"
    response = requests.get(sitemap_url)
    if response.status_code == 200:
        return response.text
    else:
        return "sitemap.xml not found"
    


# Function to analyze SEO using LLM
def analyze_seo(html_content, robots_txt, sitemap_xml):
    seo_aspects = [
        """
        Analyze the overall SEO quality of the following HTML content.
        Please provide your analysis starting with an H3 heading, start with at least a paragraph of text and add points in an unordered list when needed.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Identify the keywords that this page is optimized for.
        Please provide your analysis starting with an H3 heading, and include a mix of text, a table with the identified words and frequency,  and points in an unordered list.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Evaluate the mobile-friendliness of this HTML content.
        Please provide your analysis starting with an H3 heading, start with at least a paragraph of text and add points in an unordered list when needed.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Assess the page load speed based on the HTML content.
        Please provide your analysis starting with an H3 heading, start with at least a paragraph of text and add points in an unordered list when needed.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Analyze the use and quality of meta tags in the HTML content.
        Please provide your analysis starting with an H3 heading, start with at least a paragraph of text and add points in an unordered list when needed, be sure to mention the tags and values used.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Evaluate the structure and use of header tags (H1, H2, H3, etc.) in the HTML content.
        Please provide your analysis starting with an H3 heading, start with at least a paragraph of text and add points in an unordered list when needed.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Analyze the internal and external linking strategy within the HTML content.
        Please provide your analysis starting with an H3 heading, start with at least a paragraph of text and add points in an unordered list when needed.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Analyze the optimization of images within the HTML content, including alt text.
        Please provide your analysis starting with an H3 heading, and include a mix of text and points in an unordered list.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Evaluate the content quality and relevance for the target audience.
        Please provide your analysis starting with an H3 heading, and include a mix of text and points in an unordered list.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Analyze the use of schema markup and structured data in the HTML content.
        Please provide your analysis starting with an H3 heading, and include a mix of text and points in an unordered list.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Evaluate the overall user experience based on the HTML content.
        Please provide your analysis starting with an H3 heading, and include a mix of text and points in an unordered list broken into Good: and Bad:.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Analyze the presence and effectiveness of call-to-actions (CTAs) in the HTML content.
        Please provide your analysis starting with an H3 heading, and include a mix of text and points in an unordered list.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """,
        """
        Check the presence and configuration of robots.txt and sitemap.xml.
        Please provide your analysis starting with an H3 heading, and include a mix of text and points in an unordered list.
        Be sure to escape any content that is only used as visible HTML for the report viewer.
        """
    ]
    
    seo_analysis = {}
    for aspect in seo_aspects:
        aspect_gist = aspect.split(".")[0]
        if aspect_gist.startswith("Check the presence and configuration of robots"):
            prompt = f"""
            {aspect}

            HTML Content:
            {html_content[:2000]}

            robots.txt Content:
            {robots_txt[:2000]}

            sitemap.xml Content:
            {sitemap_xml[:2000]}

            Respond in JSON format with the following structure: {{'analysis': 'your analysis here formatted in HTML', 'score': 0-10}}
            """
        else:       
            prompt = f"""
            {aspect}

            HTML Content:
            {html_content}

            Respond in JSON format with the following structure: {{'analysis': 'your analysis here formatted in HTML', 'score': 0-10}}
            """     
        
        
        

        print(f"Analyzing: {aspect_gist}")
        print("Prompt:", prompt)
        print("=====================================")
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
            {"role": "system", "content": "You are an SEO expert. Respond in JSON format with HTML for the analysis. Make sure to include a 'score' key with a value between 0 and 10 for every analysis."},
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
# Function to process the URL and extract data
def process_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove script tags
    for script in soup(["script", "style"]):
        script.decompose()

    links = extract_links(soup)
    emails = extract_emails(soup)
    images = extract_images(soup)
    html_content = str(soup)  # Capture the cleaned HTML content
    robots_txt = check_robots_txt(url)
    sitemap_xml = check_sitemap_xml(url)
    seo_analysis = analyze_seo(html_content, robots_txt, sitemap_xml)

    data = {
        "url": url,
        "links": links,
        "emails": emails,
        "images": images,  # Add the images to the data
        "html_content": html_content,  # Add the cleaned HTML content to the data
        "robots_txt": robots_txt,
        "sitemap_xml": sitemap_xml,
        "seo_analysis": seo_analysis
    }

    return data

# Function to save data to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Main function
if __name__ == "__main__":
    url = input("Enter the URL to analyze: ")
    data = process_url(url)
    save_to_json(data, 'url_analysis.json')
    print("Processing complete. Check 'url_analysis.json' for results.")
