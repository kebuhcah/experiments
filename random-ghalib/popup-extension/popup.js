'use strict';

function setAlarm(event) {
  const minutes = parseFloat(event.target.value);
  chrome.action.setBadgeText({ text: 'ON' });
  chrome.alarms.create({ delayInMinutes: minutes });
  chrome.storage.sync.set({ minutes: minutes });
  window.close();
}
// An Alarm delay of less than the minimum 1 minute will fire
// in approximately 1 minute increments if released
document.getElementById('es').addEventListener('click', setAlarm);
document.getElementById('fr').addEventListener('click', setAlarm);
document.getElementById('de').addEventListener('click', setAlarm);
document.getElementById('ru').addEventListener('click', setAlarm);