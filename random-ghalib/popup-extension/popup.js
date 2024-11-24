'use strict';

// reminder: use pdftoppm to convert PDFs to JPEG pages
// example: pdftoppm -jpeg cyclonopedia.pdf -f 23 -l 237 cyclonopedia_pages/page

function gotoRandomCyclonopediaUrl() {
    const url =  `file:///Users/sunkev/Downloads/cyclonopedia_pages/page-${(23+(Math.floor(Math.random() * 214))).toString().padStart(3, "0")}.jpg`;
    chrome.tabs.update({ url });
}


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

document.getElementById('cyclo').addEventListener('click', gotoRandomCyclonopediaUrl);
document.getElementById('fr').addEventListener('click', gotoRandomFrenchUrl);
document.getElementById('de').addEventListener('click', gotoRandomGermanUrl);
document.getElementById('hi').addEventListener('click', gotoRandomHindustaniUrl);
document.getElementById('jp').addEventListener('click', gotoRandomJapaneseUrl);
document.getElementById('apc').addEventListener('click', gotoRandomLevantineUrl);
document.getElementById('ru').addEventListener('click', gotoRandomRussianUrl);
document.getElementById('es').addEventListener('click', gotoRandomSpanishUrl);
document.getElementById('te').addEventListener('click', gotoRandomTeluguUrl);