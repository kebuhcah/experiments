function getRandomUrl() {
    return `https://dsal.uchicago.edu/cgi-bin/app/platts_query.py?page=${Math.floor(Math.random() * 1254)}`;
}

chrome.action.onClicked.addListener((tab) => {
    const randomUrl = getRandomUrl();
    chrome.tabs.update(tab.id, { url: randomUrl });
});