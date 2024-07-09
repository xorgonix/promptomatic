import json

# Load SEO analysis data from JSON file
def load_seo_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Generate HTML content with progress bars
def generate_html(seo_data):
    seo_analysis = seo_data["seo_analysis"]
    progress_bars_html = ""

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
            
        

        progress_bars_html += f"""
        <div style="margin-bottom: 50px;">
            <div>{analysis}</div>
            <div style="position: relative; height: 30px;">
                <progress max="10" value="{score}" style="width: 100%; height: 100%;"></progress>
                <span style="position: absolute; top: 0; left: 50%; transform: translateX(-50%); color: {color}; font-weight: bold;">{score}/10</span>
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
            progress[value] {{
                appearance: none;
                -webkit-appearance: none;
                width: 100%;
                height: 20px;
            }}
            progress[value]::-webkit-progress-bar {{
                background-color: #eee;
                border-radius: 5px;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
            }}
            progress[value]::-webkit-progress-value {{
                background-color: {color};
                border-radius: 5px;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <main class="container">
            <h1>SEO Analysis Report</h1>
            {progress_bars_html}
        </main>
    </body>
    </html>
    """
    return html_content

# Save HTML content to file
def save_html(html_content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Main function
def main():
    seo_data = load_seo_data('url_analysis.json')
    html_content = generate_html(seo_data)
    save_html(html_content, 'seo_report.html')
    print("SEO report generated. Check 'seo_report.html' for results.")

if __name__ == "__main__":
    main()
