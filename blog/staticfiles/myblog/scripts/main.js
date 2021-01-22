import {handleMobileNavigation} from "./modules/mobile.js";
import {handleComments} from "./modules/comments.js";

$(document).ready(() => {
    //const isMobile =  /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
   // console.log(isMobile);
    handleMobileNavigation();
    handleComments();
})