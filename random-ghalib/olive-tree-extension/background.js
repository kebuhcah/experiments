function getRandomUrl() {
    return `file:///Users/sunkev/Downloads/olive_tree_large/page-${1+(Math.floor(Math.random() * 640))}.jpg`;
}

chrome.action.onClicked.addListener((tab) => {
    const randomUrl = getRandomUrl();
    chrome.tabs.update(tab.id, { url: randomUrl });
});