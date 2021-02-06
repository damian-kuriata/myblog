function handleDesktopNavigation(desktopItems,
                                 windowWidth,
                                 categoriesDropdown) {
    /*
     This function is responsible of adjusting how many links are visible
     In the desktop navigation bar. When the last link starts to overlap
     With search form(box), it replaces that link with 3 dots('...') and places
     It in the dropdown menu
    */
    /* TODO: Fix navigation */
    if (handleDesktopNavigation.previousWindowWidth === undefined) {
        handleDesktopNavigation.previousWindowWidth = -1;
    }
    let previousWindowWidth = handleDesktopNavigation.previousWindowWidth;
    if (previousWindowWidth === -1 || previousWindowWidth > windowWidth)  {
        handleDesktopNavigation.previousWindowWidth = windowWidth;
        previousWindowWidth = handleDesktopNavigation.previousWindowWidth;
        let desktopItemsWidth = desktopItems.width();
        let desktopItemsChildren = desktopItems.children();
        while (desktopItemsWidth + 0.05 * windowWidth >= 0.8 * windowWidth) {
            desktopItemsChildren.last().addClass("display-block");
            desktopItemsChildren.eq(-2).detach().appendTo(categoriesDropdown);
        }
    }
}

export {handleDesktopNavigation};