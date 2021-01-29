let previousWindowWidth = {
    value: -1
}
export function handleDesktopNavigation(desktopItems,
                                        windowWidth,
                                        categoriesDropdown) {
    // This function is responsible of adjusting how many links are visible
    // In the desktop navigation bar. When the last link starts to overlap
    // With search form(box), it replaces that link with 3 dots('...') and places
    // It in the dropdown menu
    if(previousWindowWidth.value === -1 || previousWindowWidth.value > windowWidth)  {
        previousWindowWidth.value = windowWidth;
        //desktopItems = $(".desktop-items");
        while(desktopItems.width() + 0.05 * windowWidth >= 0.8 * windowWidth) {
        	let children = desktopItems.children();
        	//console.log(categoriesDropdown);
        	children.last().addClass("display-block");
        	//$("<div>tst</div>").appendTo(categoriesDropdown);
        	//children.eq(-2).remove();
        	//console.log(categoriesDropdown.children());
			//let copy = children.eq(-2);
            children.eq(-2).detach().appendTo(categoriesDropdown);
            //.eq(-2).remove();
            //copy.appendTo(categoriesDropdown);
			//console.log("remove");
        }
    }


}