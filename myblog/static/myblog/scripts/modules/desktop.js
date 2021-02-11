function handleDesktopNavigation(desktopItems,
                                 windowWidth,
                                 categoriesDropdown) {
    /*
     This function is responsible of adjusting how many links are visible
     In the desktop navigation bar. When the last link starts to overlap
     With search form(box), it replaces that link with 3 dots('...') and places
     It in the dropdown menu
    */
    if (handleDesktopNavigation.previousWindowWidth === undefined) {
        handleDesktopNavigation.previousWindowWidth = -1;
    }
    if (handleDesktopNavigation.previousWindowWidth === -1 ||
        handleDesktopNavigation.previousWindowWidth > windowWidth)  {
        handleDesktopNavigation.previousWindowWidth = windowWidth;
        let desktopItemsWidth = desktopItems.width();
        while (desktopItemsWidth + 0.05 * windowWidth >= 0.8 * windowWidth) {
            let desktopItemsChildren = desktopItems.children();
            desktopItemsChildren.last().addClass("display-block");
            desktopItemsChildren.eq(-2).detach().appendTo(categoriesDropdown);
            desktopItemsWidth = desktopItems.width();
        }
    }
}

export {handleDesktopNavigation};