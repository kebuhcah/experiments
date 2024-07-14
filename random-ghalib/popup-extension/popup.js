'use strict';

function gotoRandomRussianUrl() {
    const url =  `file:///Users/sunkev/Downloads/russian_synonym_pages/page-${(25+(Math.floor(Math.random() * 542))).toString().padStart(3, "0")}.jpg`;
    console.log('HEY');
    chrome.tabs.update({ url });
}

// An Alarm delay of less than the minimum 1 minute will fire
// in approximately 1 minute increments if released
//document.getElementById('de').addEventListener('click', setAlarm);
//document.getElementById('es').addEventListener('click', setAlarm);
//document.getElementById('fr').addEventListener('click', setAlarm);
//document.getElementById('jp').addEventListener('click', setAlarm);
document.getElementById('ru').addEventListener('click', gotoRandomRussianUrl);