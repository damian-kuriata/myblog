function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function renderFormErrors(form, allErrors) {
    allErrors = JSON.parse(allErrors);
    let formFieldset = form.children[1];
    let fieldsetChildren = formFieldset.children;

    for(let fields in allErrors) {
        let field = allErrors[fields];
        const errorListClassName = "errorlist";
        let errorsHtml = ``;
        for(let messagesArray in field) {
            let message = field[messagesArray].message;
            errorsHtml += `<li>${message}</li>`;
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

    const commentForm = $("#comment-form").get(0);
    const commentTextarea = $("#comment-form textarea");
    const commentsHeader = $(".comments-section h3");
    const formData = new FormData(commentForm);
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