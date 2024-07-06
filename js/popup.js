document.getElementById('sendPrompt').addEventListener('click', sendPrompt);
document.getElementById('breakdownPrompt').addEventListener('click', breakDownResponse);
document.getElementById('getLastResponse').addEventListener('click', getLastResponseAsMarkdown);
document.getElementById('getGmailEmails').addEventListener('click', getGmailEmails);

let previousPrompt = '';
let previousResponse = '';

// Initialize EasyMDE
var easyMDE = new EasyMDE({ element: document.getElementById("markdown-editor") });


// Function to generate a unique identifier
function generateUniqueId() {
    return 'prompt-' + Math.random().toString(36).substr(2, 9);
}

// Function to send the initial prompt to GPT
function sendPrompt() {
    console.log("Send Prompt button clicked");
    const promptInput = document.getElementById('promptInput').value;
    const autoSubmit = document.getElementById('autoSubmit').checked;

    if (!promptInput) {
        console.error("No prompt input provided");
        return;
    }

    console.log("Prompt input:", promptInput);
    previousPrompt = promptInput;
    document.getElementById('promptInput').setAttribute('data-prompt-id', generateUniqueId());

    // Inject the prompt into the ChatGPT input
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            func: (prompt, autoSubmit) => {
                const textarea = document.querySelector('textarea'); // Update with the actual selector
                const form = textarea.closest('form');
                textarea.value = prompt;

                // Trigger input event to enable the submit button
                const inputEvent = new Event('input', {
                    bubbles: true,
                    cancelable: true,
                });
                textarea.dispatchEvent(inputEvent);

                if (autoSubmit) {
                    // Find the submit button and click it
                    const submitButton = form.querySelector('button[type="submit"]'); // Update with the actual selector
                    if (submitButton) {
                        submitButton.click();
                    } else {
                        console.error("Submit button not found");
                    }
                }
            },
            args: [promptInput, autoSubmit]
        });
    });
}

// Function to break down GPT response
function breakDownResponse() {
    console.log("Break Down Response button clicked");
    const responseText = previousResponse;
    simulateBreakdownCall(responseText).then(breakdownResponse => {
        try {
            const breakdownPrompts = JSON.parse(breakdownResponse);
            displayDetailedPrompts(breakdownPrompts);
        } catch (e) {
            console.error('Invalid JSON response:', breakdownResponse);
            simulateBreakdownCall(responseText, true).then(reissueResponse => {
                const breakdownPrompts = JSON.parse(reissueResponse);
                displayDetailedPrompts(breakdownPrompts);
            });
        }
    });
}

// Function to simulate breakdown call (replace with actual API call)
function simulateBreakdownCall(responseText, reissue = false) {
    const promptForBreakdown = `How would you break down the following response into detailed prompts? Respond in valid JSON format: ${responseText}`;
    if (reissue) {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(`[{"prompt":"Detail prompt 1"},{"prompt":"Detail prompt 2"}]`);
            }, 1000);
        });
    } else {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(`[{"prompt":"Detail prompt 1"},{"prompt":"Detail prompt 2"}]`);
            }, 1000);
        });
    }
}

// Function to display detailed prompts
function displayDetailedPrompts(prompts) {
    console.log("Displaying detailed prompts");
    const detailedPromptsDiv = document.getElementById('detailedPrompts');
    detailedPromptsDiv.innerHTML = '';
    prompts.forEach((p, index) => {
        const promptElement = document.createElement('div');
        promptElement.innerText = p.prompt;
        promptElement.setAttribute('data-index', index);
        promptElement.addEventListener('click', () => executePrompt(index));
        detailedPromptsDiv.appendChild(promptElement);
    });
    detailedPromptsDiv.style.display = 'block';
}

// Function to execute a detailed prompt
function executePrompt(index) {
    const prompt = document.querySelector(`[data-index="${index}"]`).innerText;
    document.getElementById('promptInput').value = prompt;
    sendPrompt();
}

// Function to convert HTML to Markdown

function html2md(htmlContent, options = {}) {
    const turndownService = new TurndownService(options);
    return turndownService.turndown(htmlContent);
}

const options = {
    headingStyle: 'atx',
    hr: '---',
    bulletListMarker: '*',
    codeBlockStyle: 'indented',
    fence: '```',
    emDelimiter: '*',
    strongDelimiter: '**',
    linkStyle: 'inlined',
    linkReferenceStyle: 'full',
    preformattedCode: true
};




// Function to get the last GPT response from the page and convert to Markdown
function getLastResponseAsMarkdown() {
    console.log("Get Last Response button clicked");
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            func: () => {
                const divs = document.querySelectorAll('div[data-message-author-role="assistant"]');
                if (divs.length > 0) {
                    const lastDiv = divs[divs.length - 1];
                    console.log("Last Assistant Response:", lastDiv.innerHTML);
                    return lastDiv.innerHTML;
                } else {
                    return 'No assistant responses found.';
                }
            }
        }, (results) => {
            if (results && results[0] && results[0].result) {
                const htmlContent = results[0].result;

                // Convert HTML to Markdown
                const markdown = html2md(htmlContent);

                // Update responseOutput and EasyMDE editor
                document.getElementById('responseOutput').innerText = markdown;
                easyMDE.value(markdown);
            } else {
                document.getElementById('responseOutput').innerText = 'No response found.';
                easyMDE.value('');
            }
        });
    });
}

function getGmailEmails() {
    const emails = [];
    //find all the tr with the class name zA
    const emaillist = document.querySelectorAll('tr.zA');
    emaillist.forEach((email) => {
        const emailContent = email.querySelector('span.bog').innerText;
        emails.push(emailContent);
 
    });
    console.log(emails);
    return emails;
}



// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'GPT_RESPONSE') {
        previousResponse = message.response;
        console.log('Received GPT response:', previousResponse);
        document.getElementById('responseOutput').innerText = previousResponse;
        document.getElementById('breakdownPrompt').style.display = 'block';
    } else if (message.type === 'USER_PROMPT') {
        previousPrompt = message.prompt;
        console.log('Received user prompt:', previousPrompt);
    }
});
