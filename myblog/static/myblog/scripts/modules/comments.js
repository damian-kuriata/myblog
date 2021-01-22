export function handleComments() {
    const showHideButton = $(".comments-section > button");
    const commentsContainer = $(".comments-section .comments-list");
    let commentsHidden = false;

    showHideButton.click((event) => {
        if(commentsHidden) {
            commentsContainer.show();
            showHideButton.text(gettext("hide"));
            commentsHidden = false;
        }
        else {
            commentsContainer.hide();
            showHideButton.text(gettext("show"));
            commentsHidden = true;
        }
    });
}