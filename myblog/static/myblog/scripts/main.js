import {handleMobileNavigation} from "./modules/mobile.js";
import {handleCommentsHideShow} from "./modules/comments.js";
import {handleDesktopNavigation} from "./modules/desktop.js";
import { animateLogo } from "./modules/logo.js";

$(document).ready(function() {
    handleMobileNavigation();
    handleCommentsHideShow();

    const logo = $(".logo");
    //animateLogo(logo);
    let desktopItems = $("nav .navigation-container .desktop-items");
    let window_ = $(window);
    let categoriesDropdown = $(".categories-dropdown");
    handleDesktopNavigation(desktopItems, window_.width(), categoriesDropdown);
    window_.resize(function() {
        handleDesktopNavigation(desktopItems, window_.width(),
            categoriesDropdown);
    });
});