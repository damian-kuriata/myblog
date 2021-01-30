/* Namespace for global variables */
let globalVars = {
    commentAddingThresholdMillis: 10000,
    canAddComment: true
};

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

function renderFormErrors(form, allErrors) {
    allErrors = JSON.parse(allErrors);
    let formFieldset = form.children[0];
    let fieldsetChildren = formFieldset.children;

    for(let fields in allErrors) {
        let field = allErrors[fields];
        const errorListClassName = "errorlist";
        let errorsHtml = ``;
        for(let messagesArray in field) {
            let message = field[messagesArray].message;
            errorsHtml += `<li role="alert">${message}</li>`;
        }

        let errorList = document.createElement("ul");
        errorList.innerHTML = errorsHtml;
        errorList.classList.add(errorListClassName);

        if(fields === "text") {
            fieldsetChildren[3].appendChild(errorList);
        }
        else if(fields === "author_nickname") {
            fieldsetChildren[2].appendChild(errorList);
        }
        else if(fields === "author_email") {
            fieldsetChildren[1].appendChild(errorList);
        }
        globalVars.canAddComment = true;
    }
}

function renderNewComment(commentsList, commentData) {
    let newComment = $(`<p>${commentData.author_nickname}, ${commentData.creation_datetime}: <br>${commentData.text}</p>`);
    newComment.attr("class", "comment");
    commentsList.append(newComment);
}

function updateCommentsHeaderValue(commentsHeader) {
    // Add 1 to current value
    const regex = /\d+/;
    let commentsHeaderValue = parseInt(commentsHeader.text().match(regex).join(''));
    commentsHeaderValue += 1;
    commentsHeader.text(commentsHeader.text().replace(regex, commentsHeaderValue.toString()))
}
function cleanFormErrors() {
    const classToDelete = "errorlist";
    const errors = document.querySelectorAll(`#comment-form .${classToDelete}`);
    errors.forEach(e => e.remove());
}
const submitButton = $(".comment-input input[type='submit']");
submitButton.click((event) => {
    event.preventDefault();

    if(!globalVars.canAddComment) {
        alert(gettext("Wait a moment before adding next comment"));
        return;
    }
    globalVars.canAddComment = false;

    // Block adding comments for a given threshold
    setTimeout(() => {
        globalVars.canAddComment = true;
    }, globalVars.commentAddingThresholdMillis);

    const commentForm = $("#comment-form").get(0);
    const commentTextarea = $("#comment-form textarea");
    const commentsHeader = $(".comments-section h3");
    let formData = new FormData(commentForm);
    // Escape HTML in text and author_nickname fields
    formData.set("text", escapeHtml(formData.get("text")));
    formData.set("author_nickname", escapeHtml(formData.get("author_nickname")));
    let csrftoken = getCookie("csrftoken");
    const actionUrl = commentForm.action;
    const init = {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: formData
    }
    cleanFormErrors(commentForm);
    const commentsList = $(".comments-list");

    fetch(actionUrl, init).then((response) => {
        const contentType = response.headers.get("content-type");
        if(!contentType || !contentType.includes("application/json")) {
            throw new Error("Invalid server response format: " + contentType);
        }
        return response.json();
    }).then((data) => {
        if(data.errors) {
            renderFormErrors(commentForm, data.errors);
        }
        else {
            renderNewComment(commentsList, data);
            // Clean the comment area
            commentTextarea.val("");
            updateCommentsHeaderValue(commentsHeader);
        }
    }).catch((error) => {
        alert(error);
    })
})