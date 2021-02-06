function handleMobileNavigation() {
    const mobileNavigationButton = $(".mobile-nav-button");
    const mobileNavigationList = $("nav .mobile-navigation-list");
    mobileNavigationButton.click((event) => {
        if(mobileNavigationList.is(":hidden")) {
            mobileNavigationList.show(300, () => {
                mobileNavigationList.addClass("display-flex");
            });
        }
        else {
            mobileNavigationList.hide(300);
        }
    });
}

export {handleMobileNavigation};