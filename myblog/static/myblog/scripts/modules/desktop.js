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
    let desktopItemsWidth = desktopItems.width();
    if (handleDesktopNavigation.previousWindowWidth === -1 ||
        handleDesktopNavigation.previousWindowWidth > windowWidth) {
        handleDesktopNavigation.previousWindowWidth = windowWidth;
        while (desktopItemsWidth + 0.05 * windowWidth >= 0.8 * windowWidth) {
            let desktopItemsChildren = desktopItems.children();
            desktopItemsChildren.last().addClass("display-block");
            desktopItemsChildren.eq(-2).detach().appendTo(categoriesDropdown);
            desktopItemsWidth = desktopItems.width();
        }
    }
    /*
    else if (handleDesktopNavigation.previousWindowWidth < windowWidth) {
        handleDesktopNavigation.previousWindowWidth = windowWidth;
        console.log("Smaller");
        let desktopItemsWidth = desktopItems.width();
        while (desktopItemsWidth + 0.05 * windowWidth < 0.8 * windowWidth) {
            let desktopItemsChildren = desktopItems.children();
            categoriesDropdown.eq(-1).detach().appendTo(desktopItemsChildren);
            desktopItemsWidth = desktopItems.width();
        }
    }*/
}

function handleLeftNavigationExpand(categoriesExpand, leftCategoriesPanel) {
    /*
     Controls whether expand button is visible or not
     */
    const animationDuration = 400;
    leftCategoriesPanel.find(".categories-shrink").click(() => {
        leftCategoriesPanel.toggleClass("visibility-hidden");
        categoriesExpand.css("visibility", "visible");
    });
    categoriesExpand.click(() => {
        leftCategoriesPanel.toggleClass("visibility-hidden");
        categoriesExpand.css("visibility", "hidden");
        //categoriesExpand.addClass("visibility-hidden");
        //categoriesExpand.hasClass("visibility-hidden")?categoriesExpand.removeClass("visibility-hidden"):categoriesExpand.addClass("visibility-hidden");
        /* TODO: Write an animation */
        /*console.log(leftCategoriesPanel.width());
        leftCategoriesPanel.animate({
            width: "toggle"
        }, animationDuration, () => {
            categoriesExpand.toggleClass("visibility-hidden");
            leftCategoriesPanel.toggleClass("visibility-hidden");
        });*/
    });
}

export { handleDesktopNavigation, handleLeftNavigationExpand };