import {handleMobileNavigation} from "./modules/mobile.js";
import {handleCommentsHideShow} from "./modules/comments.js";
import { handleDesktopNavigation, handleLeftNavigationExpand } from "./modules/desktop.js";
import { animateLogo } from "./modules/logo.js";

$(document).ready(function() {
    handleMobileNavigation();
    handleCommentsHideShow();

    const logo = $(".logo");
    let mainLogo = logo.find(".main-logo");
    let letters = mainLogo.children();
    animateLogo(letters);
    let desktopItems = $("nav .navigation-container .desktop-items");
    let window_ = $(window);
    let categoriesDropdown = $(".categories-dropdown");
    handleDesktopNavigation(desktopItems, window_.width(), categoriesDropdown);
    let categoriesExpand = $("aside > .categories-expand");
    let leftCategoriesPanel = $("aside > .left-categories-panel");
    handleLeftNavigationExpand(categoriesExpand, leftCategoriesPanel);
    window_.resize(function() {
        handleDesktopNavigation(desktopItems, window_.width(),
            categoriesDropdown);
    });
});