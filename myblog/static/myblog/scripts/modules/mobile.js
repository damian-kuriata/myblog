// A module containing mobile-specific functions


export function handleMobileNavigation() {
    const mobileNavigationButton = $(".mobile-nav-button");
    const mobileNavigationList = $("nav .mobile-navigation-list");
    //$('body').on('click','img',function(){alert('it works');})
    mobileNavigationButton.click((event) => {
        if(mobileNavigationList.is(":hidden")) {
            mobileNavigationList.show(300, () => {
                mobileNavigationList.addClass("display-flex");
                //mobileNavigationList.css("display", "flex");
            })
        }
        else {
            mobileNavigationList.hide(300);
        }
    })

}