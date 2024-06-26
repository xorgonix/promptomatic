
const jsonDocument = {{
    "report": {
      "introduction": {
        "key_point": "Discussion on freelancing trends for 2023-24.",
        "implications": "Provides insights on what to expect, opportunities, and positioning strategies."
      },
      "freelancing in 2023-24": {
        "key_point": "Freelancing remains viable with more opportunities for full-stack developers and those with web marketing skills.",
        "implications": "Being versatile and able to offer additional services like social media setup and SEO can increase attractiveness to clients.",
        "risks_opportunities": {
          "risks": "Stiff competition; need to manage client expectations properly.",
          "opportunities": "Expanding skill set to include AI tools and solutions could open new market segments."
        }
      },
      "contracting vs. freelancing": {
        "key_point": "Contracting involves being a temporary employee, whereas freelancing offers more control over projects.",
        "implications": "Freelancing is suited for small businesses, offering broader skill application and higher autonomy.",
        "risks_opportunities": {
          "risks": "Freelancing requires strong client management skills.",
          "opportunities": "Broader skill sets in freelancing can lead to diverse project opportunities."
        }
      },
      "success in freelancing": {
        "key_point": "Success hinges on good interpersonal skills and effective client and project management.",
        "implications": "Setting clear expectations and having a well-drafted contract are crucial for project success.",
        "risks_opportunities": {
          "risks": "Poor communication can lead to project failure.",
          "opportunities": "Good client relationships can lead to repeat business and referrals."
        }
      },
      "important skills for 2024": {
        "key_point": "Understanding AI tools and their implementation can be beneficial.",
        "implications": "AI knowledge can provide a competitive edge in the market.",
        "risks_opportunities": {
          "risks": "Rapid changes in AI technology require continuous learning.",
          "opportunities": "Positioning oneself as knowledgeable in AI can attract more clients."
        }
      },
      "books and resources": {
        "key_point": "Recommended books include 'The Naked Ape' for understanding human behavior and 'Refactoring' for coding best practices.",
        "implications": "These resources can enhance understanding of client needs and improve coding skills.",
        "risks_opportunities": {
          "risks": "Investing time in reading might delay immediate project work.",
          "opportunities": "Improved skills and knowledge can lead to better project outcomes."
        }
      },
      "client management": {
        "key_point": "Effective client onboarding and project tracking are essential.",
        "implications": "Proper management ensures smooth project execution and client satisfaction.",
        "risks_opportunities": {
          "risks": "Overloading with too many clients can lead to burnout.",
          "opportunities": "Efficient management can handle more projects simultaneously."
        }
      },
      "personal development": {
        "key_point": "Continuous learning and tackling new challenges enhance cognitive functions.",
        "implications": "Improving brain function and staying updated with new skills keeps one competitive.",
        "risks_opportunities": {
          "risks": "Potential burnout from continuous learning.",
          "opportunities": "Enhanced problem-solving skills and adaptability."
        }
      }
    },
    "cocktail_party_talking_points": {
      "Freelancing Trends": "Freelancing is still a viable career option, especially for full-stack developers who can offer additional services like web marketing.",
      "Contracting vs. Freelancing": "Freelancing offers more project control and is ideal for small businesses, whereas contracting is more about fitting into an existing structure.",
      "AI in Freelancing": "Knowledge of AI tools can provide a significant competitive edge for freelancers.",
      "Success Tips": "Good client management and clear communication are key to successful freelancing.",
      "Recommended Reads": "Books like 'The Naked Ape' and 'Refactoring' can provide valuable insights into human behavior and coding best practices."
    }
  }
  

  function processNode(title, content) {
    let text = `### ${title}\n\n`;
  
    for (let key in content) {
      if (typeof content[key] === 'object') {
        for (let subKey in content[key]) {
          text += `${content[key][subKey]}\n\n`;
        }
      } else {
        text += `${content[key]}\n\n`;
      }
    }
  
    text += `---\n\n`;
    return text;
  }
  
  function generateTextFromJSON(json) {
    let outputText = "";
  
    if (json.report && json.report.chapters) {
      json.report.chapters.forEach((chapter) => {
        outputText += processNode(chapter.title, chapter.content);
      });
  
      if (json.report.conclusion) {
        outputText += `### Conclusion\n\n`;
        for (let key in json.report.conclusion) {
          outputText += `${json.report.conclusion[key]}\n\n`;
        }
        outputText += `---\n\n`;
      }
    }
  
    return outputText;
  }
  
  const outputText = generateTextFromJSON(jsonDocument);
  console.log(outputText);