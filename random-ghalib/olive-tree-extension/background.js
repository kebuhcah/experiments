function getRandomUrl() {
    return `file:///Users/sunkev/Downloads/olive_tree_dictionary.pdf#page=${16 + Math.floor(Math.random() * 640)}`;
}

chrome.action.onClicked.addListener((tab) => {
    const randomUrl = getRandomUrl();
    chrome.tabs.update(tab.id, { url: randomUrl });
});