import {handleMobileNavigation} from "./modules/mobile.js";
import {handleComments} from "./modules/comments.js";
import {handleDesktopNavigation} from "./modules/desktop.js";

$(document).ready(function() {
    handleMobileNavigation();
    handleComments();

    let desktopItems = $("nav .navigation-container .desktop-items");
    let window_ = $(window);
    let categoriesDropdown = $(".categories-dropdown");
    handleDesktopNavigation(desktopItems, window_.width(), categoriesDropdown);
    window_.resize(function() {
        handleDesktopNavigation(desktopItems, window_.width(), categoriesDropdown);
    });
});