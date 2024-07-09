function getRandomUrl() {
    return `file:///Users/sunkev/Downloads/olive_tree_pages/page-${(16 + Math.floor(Math.random() * 640)).toString().padStart(3, "0")}.jpg`;
}

chrome.action.onClicked.addListener((tab) => {
    const randomUrl = getRandomUrl();
    chrome.tabs.update(tab.id, { url: randomUrl });
});