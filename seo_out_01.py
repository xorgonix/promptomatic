import json

# Load SEO analysis data from JSON file
def load_seo_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

# Function to format analysis text into HTML lists where applicable
def format_analysis_text(analysis_text):
    # Convert dictionary to a formatted string if necessary
    if isinstance(analysis_text, dict):
        analysis_text = json.dumps(analysis_text, indent=4)
    
    # Split the text into lines
    lines = analysis_text.split('. ')
    # Create HTML formatted list items
    formatted_lines = ''.join([f'<li>{line.strip()}</li>' for line in lines if line])
    # Return the text wrapped in <ul> tags
    return f'<ul>{formatted_lines}</ul>'

# Generate HTML content
def generate_html(seo_data):
    seo_analysis = seo_data["seo_analysis"]
    gauges_html = ""

    for aspect, details in seo_analysis.items():
        analysis = details['analysis']
        score = details['score']

        # Determine color based on score
        if score >= 8:
            color = "#28a745"  # Green
        elif score >= 5:
            color = "#ffc107"  # Yellow
        else:
            color = "#dc3545"  # Red

        formatted_analysis = format_analysis_text(analysis)

        gauges_html += f"""
        <div style="margin-bottom: 50px;">
            <h3>{aspect}</h3>
            {formatted_analysis}
            <div class="gauge">
                <div class="gauge__body">
                    <div class="gauge__fill" style="transform: rotate({score * 18}deg); background-color: {color};"></div>
                    <div class="gauge__cover">{score}/10</div>
                </div>
            </div>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SEO Analysis Report</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
        <style>
            .gauge {{
                width: 200px;
                height: 200px;
                border-radius: 50%;
                overflow: hidden;
                display: inline-block;
            }}
            .gauge__body {{
                width: 100%;
                height: 100%;
                background: #e6e6e6;
                position: relative;
            }}
            .gauge__fill {{
                position: absolute;
                width: 100%;
                height: 100%;
                background: inherit;
                transform-origin: center bottom;
                transform: rotate(0deg);
            }}
            .gauge__cover {{
                width: 75%;
                height: 75%;
                background: white;
                border-radius: 50%;
                position: absolute;
                top: 12.5%;
                left: 12.5%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5em;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <main class="container">
            <h1>SEO Analysis Report</h1>
            {gauges_html}
        </main>
    </body>
    </html>
    """
    return html_content

# Save HTML content to file
def save_html(html_content, filename):
    with open(filename, 'w') as file:
        file.write(html_content)

# Main function
def main():
    seo_data = load_seo_data('url_analysis.json')
    html_content = generate_html(seo_data)
    save_html(html_content, 'seo_report.html')
    print("SEO report generated. Check 'seo_report.html' for results.")

if __name__ == "__main__":
    main()
