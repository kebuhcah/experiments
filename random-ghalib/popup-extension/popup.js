'use strict';

function gotoRandomFrenchUrl() {
    const url =  `file:///Users/sunkev/Downloads/french_synonym_pages/page-${(18+(Math.floor(Math.random() * 465))).toString().padStart(3, "0")}.jpg`;
    chrome.tabs.update({ url });
}

function gotoRandomGermanUrl() {
    const url =  `file:///Users/sunkev/Downloads/german_synonym_pages/page-${(29+(Math.floor(Math.random() * 253))).toString().padStart(3, "0")}.jpg`;
    chrome.tabs.update({ url });
}

function gotoRandomHindustaniUrl() {
    const url =  `https://dsal.uchicago.edu/cgi-bin/app/platts_query.py?page=${Math.floor(Math.random() * 1254)}`;
    chrome.tabs.update({ url });
}

function gotoRandomJapaneseUrl() {
    const url =  `file:///Users/sunkev/Downloads/japanese_synonym_pages/page-${(18+(Math.floor(Math.random() * 390))).toString().padStart(3, "0")}.jpg`;
    chrome.tabs.update({ url });
}

function gotoRandomLevantineUrl() {
    const url =  `file:///Users/sunkev/Downloads/olive_tree_large/page-${1+(Math.floor(Math.random() * 640))}.jpg`;
    chrome.tabs.update({ url });
}


function gotoRandomRussianUrl() {
    const url =  `file:///Users/sunkev/Downloads/russian_synonym_pages/page-${(25+(Math.floor(Math.random() * 542))).toString().padStart(3, "0")}.jpg`;
    chrome.tabs.update({ url });
}

function gotoRandomSpanishUrl() {
    const url =  `file:///Users/sunkev/Downloads/spanish_synonym_pages/page-${(19+(Math.floor(Math.random() * 582))).toString().padStart(3, "0")}.jpg`;
    chrome.tabs.update({ url });
}

function gotoRandomTeluguUrl() {
    const url =  `https://dsal.uchicago.edu/dictionaries/gwynn/jpg/${(1+(Math.floor(Math.random() * 574))).toString().padStart(3, "0")}.jpg`;
    chrome.tabs.update({ url });
}


// An Alarm delay of less than the minimum 1 minute will fire
// in approximately 1 minute increments if released
document.getElementById('fr').addEventListener('click', gotoRandomFrenchUrl);
document.getElementById('de').addEventListener('click', gotoRandomGermanUrl);
document.getElementById('hi').addEventListener('click', gotoRandomHindustaniUrl);
document.getElementById('jp').addEventListener('click', gotoRandomJapaneseUrl);
document.getElementById('apc').addEventListener('click', gotoRandomLevantineUrl);
document.getElementById('ru').addEventListener('click', gotoRandomRussianUrl);
document.getElementById('es').addEventListener('click', gotoRandomSpanishUrl);
document.getElementById('te').addEventListener('click', gotoRandomTeluguUrl);