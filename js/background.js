// background.js
console.log('Background script loaded');
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('Message received:', message);
    if (message.type === 'GPT_RESPONSE') {
        chrome.storage.local.set({ 'lastGPTResponse': message.response }, () => {
            console.log('Stored GPT response:', message.response);
        });
    }
});
