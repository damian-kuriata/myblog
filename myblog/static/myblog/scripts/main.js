import {handleMobileNavigation} from "./modules/mobile.js";
import {handleComments} from "./modules/comments.js";
import {handleDesktopNavigation} from "./modules/desktop.js";

$(document).ready(() => {
    //const isMobile =  /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
   // console.log(isMobile);
    handleMobileNavigation();
    handleComments();

    const windowNodes = {
        desktopItems: $("nav .navigation-container .desktop-items"),
        searchForm: $("nav .navigation-container #search")
    }
    handleDesktopNavigation(windowNodes);

    //handleDesktopNavigation(windowNodes);
    $(window).resize(() => {
        handleDesktopNavigation(windowNodes);
    })
})