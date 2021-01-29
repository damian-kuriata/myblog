let is_colliding = function( div1, div2 ) {
	// Div 1 data
	var d1_offset             = div1.offset();
	var d1_height             = div1.outerHeight( true );
	var d1_width              = div1.outerWidth( true );
	var d1_distance_from_top  = d1_offset.top + d1_height;
	var d1_distance_from_left = d1_offset.left + d1_width;

	// Div 2 data
	var d2_offset             = div2.offset();
	var d2_height             = div2.outerHeight( true );
	var d2_width              = div2.outerWidth( true );
	var d2_distance_from_top  = d2_offset.top + d2_height;
	var d2_distance_from_left = d2_offset.left + d2_width;

	var not_colliding = ( d1_distance_from_top < d2_offset.top || d1_offset.top > d2_distance_from_top || d1_distance_from_left < d2_offset.left || d1_offset.left > d2_distance_from_left );

	// Return whether it IS colliding
	return ! not_colliding;
};
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