function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}
const submitButton = $(".comment-input input[type='submit']");
submitButton.click((event) => {
    event.preventDefault();

    const commentForm = $("#comment-form").get(0);
    const formData = new FormData(commentForm);
    let cookies = document.cookie.split("; ");
    console.log(cookies);
    let csrftoken = getCookie("csrftoken");
    const init = {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken
        },
        body: formData
    }
    fetch("/add_comment/", init);
})