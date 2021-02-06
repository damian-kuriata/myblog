function handleCommentsHideShow() {
    /* Comments showing/hiding */
    const showHideButton = $(".comments-section > button");
    const commentsContainer = $(".comments-section .comments-list");
    let commentsHidden = false;

    showHideButton.click(function(event) {
        /* Gettext is a function provided by Django */
        if (commentsHidden) {
            commentsContainer.show();
            showHideButton.text(gettext("hide"));
            commentsHidden = false;
        } else {
            commentsContainer.hide();
            showHideButton.text(gettext("show"));
            commentsHidden = true;
        }
    });
    /* Comments reply system */
    const commentTextInput = $("#id_text");
    commentsContainer.children("article").each(function(index, comment) {
        /* Convert to JQuery object */
        comment = $(comment);
        const replyButton = comment.find(".reply-button").eq(0);
        replyButton.click(function (event) {
            let commentHeaderText = comment.children("h6").eq(0).text();
            const fromIndex = 0;
            const toIndex = commentHeaderText.indexOf(",")
            let nickname = commentHeaderText.substr(fromIndex, toIndex);
            /* Append @nickname to current input value */
            commentTextInput.val(commentTextInput.val() + ` @${nickname}`);
        });
    });
}

export {handleCommentsHideShow};
