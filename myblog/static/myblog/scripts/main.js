import {handleMobileNavigation} from "./modules/mobile.js";
import {handleComments} from "./modules/comments.js";
import {handleDesktopNavigation} from "./modules/desktop.js";

$(document).ready(() => {
    //const isMobile =  /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
   // console.log(isMobile);
    handleMobileNavigation();
    handleComments();

    let desktopItems = $("nav .navigation-container .desktop-items");
    let window_ = $(window);
    handleDesktopNavigation(desktopItems, window_.width());
    window_.resize(() => {
        handleDesktopNavigation(desktopItems, window_.width());
    })
})