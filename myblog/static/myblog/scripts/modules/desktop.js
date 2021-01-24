function enoughSpace(firstChild, lastChild) {
    // if there is not enough space for last child, it gets automatically
    // "Moved" to top, and it's top offset becomes negative
    return firstChild.height() === lastChild.height();
}
let previousWindowWidth = {
    value: -1
}
export function handleDesktopNavigation(desktopItems, windowWidth) {
    // This function is responsible of adjusting how many links are visible
    // In the desktop navigation bar. When the last link starts to overlap
    // With search form(box), it replaces that link with 3 dots('...') and places
    // It in the dropdown menu
    if(previousWindowWidth.value === -1 || previousWindowWidth.value > windowWidth)  {
        previousWindowWidth.value = windowWidth;
        let childrenCount = desktopItems.children().length;

        // There must be at least 2 children for this operation
        // One is deleted and one is replaced
        if(childrenCount >= 2) {
            while(!enoughSpace(desktopItems.children().first(),
                    desktopItems.children().last())) {
                desktopItems.children().last().remove();
                console.log("remove");
                childrenCount -= 1;
                let hiddenChildrenPopup = $("<div>...</div>");
                hiddenChildrenPopup.addClass("hidden-children-popup");
                //hiddenChildrenPopup.css("position", "relative");
                // Nth-child selector is 1-based, thus we don't subtract 1 from childrenCount
                //desktopItems.children(`:nth-child(${childrenCount})`).replaceWith(hiddenChildrenPopup);
            }
        }

    }

}