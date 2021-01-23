function isOverlap(objOne,objTwo){
        let offsetOne = objOne.offset(),
            offsetTwo = objTwo.offset(),
            topOne=offsetOne.top,
            topTwo=offsetTwo.top,
            leftOne=offsetOne.left,
            leftTwo=offsetTwo.left,
            widthOne = objOne.width(),
            widthTwo = objTwo.width(),
            heightOne = objOne.height(),
            heightTwo = objTwo.height();
        let leftTop = leftTwo > leftOne && leftTwo < leftOne+widthOne                  && topTwo > topOne && topTwo < topOne+heightOne,             rightTop = leftTwo+widthTwo > leftOne && leftTwo+widthTwo < leftOne+widthOne                  && topTwo > topOne && topTwo < topOne+heightOne,             leftBottom = leftTwo > leftOne && leftTwo < leftOne+widthOne                  && topTwo+heightTwo > topOne && topTwo+heightTwo < topOne+heightOne,             rightBottom = leftTwo+widthTwo > leftOne && leftTwo+widthTwo < leftOne+widthOne                  && topTwo+heightTwo > topOne && topTwo+heightTwo < topOne+heightOne;
        return leftTop || rightTop || leftBottom || rightBottom;
}

export function handleDesktopNavigation(windowNodes) {
    // This function is responsible of adjusting how many links are visible
    // In the desktop navigation bar. When the last link starts to overlap
    // With search form(box), it replaces that link with 3 dots('...') and places
    // It in the dropdown menu
    console.log(windowNodes);
    let lastChild = windowNodes.desktopItems.lastChild;
    let searchForm = windowNodes.searchForm;
    //console.log(isOverlap(lastChild, searchForm));
}