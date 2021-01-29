export function handleComments() {
    // Comments hiding/showing
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

    // Comments reply system
    const commentTextInput = $("#id_text");
    for(let singleComment of commentsContainer.children("article")) {
        // Convert to JQuery object
        singleComment = $(singleComment);
        const replyButton = singleComment.find(".reply-button").eq(0);
        replyButton.click((event) => {
            let commentHeaderText = singleComment.children("h6").eq(0).text();
            let nickname = commentHeaderText.substr(0, commentHeaderText.indexOf(','));
            commentTextInput.text(commentTextInput.text() + `@${ nickname }: `);
        });
    }
}