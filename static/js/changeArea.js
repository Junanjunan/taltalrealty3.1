const toggle_m2 = document.querySelector(".toggle_m2")
const toggle_area = document.getElementsByClassName("toggle_area")
const toggle_money = document.querySelector(".toggle_money")
const toggle_money_area = document.getElementsByClassName("toggle_money_area")

function toggling() {
    if(toggle_m2.value==="m2"){
        for (var i=0; i<toggle_area.length; i++){
            const tgarea = Number(toggle_area[i].innerHTML);
            const tgarea_p = (tgarea/3.306).toFixed(2);
            toggle_area[i].innerHTML = tgarea_p
            toggle_m2.innerHTML = "면적단위(평)"
            toggle_m2.value = "p"
        }       
    } else{
        for (var i=0; i<toggle_area.length; i++){
            const tgarea = Number(toggle_area[i].innerHTML);
            const tgarea_m2 = (tgarea*3.306).toFixed(2);
            toggle_area[i].innerHTML = tgarea_m2;
            toggle_m2.innerHTML = "면적단위(m2)"
            toggle_m2.value = "m2"
        }
    }
}

function togglingMoney() {
    if(toggle_money.value==="manwon"){
        for (var i=0; i<toggle_money_area.length; i++){
            const tgmoney = Number(toggle_money_area[i].innerHTML);
            const tgmoney_uc = tgmoney/10000;
            toggle_money_area[i].innerHTML = tgmoney_uc
            toggle_money.innerHTML = "금액단위(억원)"
            toggle_money.value = "ucwon"
        }       
    } else{
        for (var i=0; i<toggle_money_area.length; i++){
            const tgmoney = Number(toggle_money_area[i].innerHTML);
            const tgmoney_uc = tgmoney*10000;
            toggle_money_area[i].innerHTML = tgmoney_uc;
            toggle_money.innerHTML = "금액단위(만원)"
            toggle_money.value = "manwon"
        }
    }
}
