console.log('Content script loaded');


// Listen for messages from popup.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'FETCH_GPT_RESPONSES') {
        const responses = fetchAssistantResponses();
        sendResponse({ responses: responses });
    } else if (message.type === 'SEND_PROMPT') {
        const { prompt, autoSubmit } = message;
        const textarea = document.querySelector('textarea'); // Adjust selector if needed
        const form = textarea.closest('form');
        textarea.value = prompt;

        // Trigger input event to enable the submit button
        const inputEvent = new Event('input', {
            bubbles: true,
            cancelable: true,
        });
        textarea.dispatchEvent(inputEvent);

        if (autoSubmit) {
            const submitButton = form.querySelector('button[type="submit"]'); // Adjust selector if needed
            if (submitButton) {
                submitButton.click();
            } else {
                console.error("Submit button not found");
            }
        }
    }
});
