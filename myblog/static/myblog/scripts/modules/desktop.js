function enoughSpace(lastChild) {
    // if there is not enough space for last child, it gets automatically
    // "Moved" to top, and it's top offset becomes negative
    console.log(lastChild.offset().top);
    return lastChild.offset().top >= 0;
}
export function handleDesktopNavigation(windowNodes) {
    // This function is responsible of adjusting how many links are visible
    // In the desktop navigation bar. When the last link starts to overlap
    // With search form(box), it replaces that link with 3 dots('...') and places
    // It in the dropdown menu

    let lastChild = $("nav .navigation-container .desktop-items").children().last();
    let desk = $("nav .navigation-container .desktop-items");
    let searchForm = windowNodes.searchForm;
    if(!enoughSpace(lastChild)) {
        console.log("no space");
        let n = $("<div>...</div>");
        lastChild.replaceWith(n);
    }


}