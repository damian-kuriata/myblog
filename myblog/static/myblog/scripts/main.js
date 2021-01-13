import {handleMobileNavigation} from "./modules/mobile.js";

$(document).ready(() => {
    console.log("hello");
    const isMobile =  /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    console.log(isMobile);
    if(isMobile) {
        handleMobileNavigation();
    }
})