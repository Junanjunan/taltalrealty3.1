const start_day = document.getElementsByClassName("start_day");
const last_day = document.getElementsByClassName("last_day");
const last_due_day = document.getElementsByClassName("last_due_day");
const report_due_day = document.getElementsByClassName("report_due_day");
const report_day = document.getElementsByClassName("report_day");
const contract_day = document.getElementsByClassName("contract_day");


function getTimeLastMinusToday() {
    for (var i=0; i<last_due_day.length; i++){
        const today = new Date();
        const leftMilSec = new Date(last_day[i].innerHTML) - today
        const leftSec = leftMilSec / 1000;
        const sec = Math.floor(leftSec % 60);
        const leftMin = leftMilSec / (1000 * 60);
        const min = Math.floor(leftMin % 60);
        const leftHours = leftMilSec / (1000 * 60 * 60);
        const hours = Math.floor(leftHours % 24);
        const leftDays = leftMilSec / (1000 * 60 * 60 * 24);
        const days = Math.ceil(leftDays);
        // last_due_day[i].innerText = `${days}일 ${hours < 10 ? `0${hours}` : hours}시간 ${sec < 10 ? `0${sec}` : sec}초`;
        last_due_day[i].innerText = `${days}`;
    }
}

function getTimeReportMinusToday() {
    for (var i=0; i<start_day.length; i++){
        const today = new Date();
        const startDay = new Date(start_day[i].innerHTML);
        startDay.setDate(startDay.getDate()+30);
        const leftMilSec = new Date(startDay) - today
        const leftSec = leftMilSec / 1000;
        const sec = Math.floor(leftSec % 60);
        const leftMin = leftMilSec / (1000 * 60);
        const min = Math.floor(leftMin % 60);
        const leftHours = leftMilSec / (1000 * 60 * 60);
        const hours = Math.floor(leftHours % 24);
        const leftDays = leftMilSec / (1000 * 60 * 60 * 24);
        const days = Math.floor(leftDays);
        // report_due_day[i].innerText = `${days}일 ${hours < 10 ? `0${hours}` : hours}시간 ${sec < 10 ? `0${sec}` : sec}초`;
        report_due_day[i].innerText = `${days}`;
        date = new Date(startDay);
        year = date.getFullYear();
        month = date.getMonth()+1;
        dt = date.getDate();
        if (dt < 10) {
        dt = '0' + dt;
        }
        if (month < 10) {
        month = '0' + month;
        }
        report_day[i].innerHTML = `${year}-${month}-${dt}`
        // last_due_day[i].innerText = `${days}일`;
        
    }
}


function getTimeReportMinusToday2() {
    for (var i=0; i<contract_day.length; i++){
        const today = new Date();
        const contractDay = new Date(contract_day[i].innerHTML);
        contractDay.setDate(contractDay.getDate()+30);
        const leftMilSec = new Date(contractDay) - today
        const leftSec = leftMilSec / 1000;
        const sec = Math.floor(leftSec % 60);
        const leftMin = leftMilSec / (1000 * 60);
        const min = Math.floor(leftMin % 60);
        const leftHours = leftMilSec / (1000 * 60 * 60);
        const hours = Math.floor(leftHours % 24);
        const leftDays = leftMilSec / (1000 * 60 * 60 * 24);
        const days = Math.floor(leftDays);
        // report_due_day[i].innerText = `${days}일 ${hours < 10 ? `0${hours}` : hours}시간 ${sec < 10 ? `0${sec}` : sec}초`;
        report_due_day[i].innerHTML = `${days}`;
        console.log("dhkdl")
        // date = new Date(startDay);
        // year = date.getFullYear();
        // month = date.getMonth()+1;
        // dt = date.getDate();
        // if (dt < 10) {
        // dt = '0' + dt;
        // }
        // if (month < 10) {
        // month = '0' + month;
        // }
        // report_day[i].innerHTML = `${year}-${month}-${dt}`
        // last_due_day[i].innerText = `${days}일`;
        
    }
}

getTimeLastMinusToday();
getTimeReportMinusToday();
getTimeReportMinusToday2();