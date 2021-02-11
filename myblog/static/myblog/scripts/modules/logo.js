function animateLogo(letters) {
    const defaultColor = letters.eq(0).css("color");
    const defaultFontSize = letters.eq(0).css("font-size");
    const highlightColor = "black";
    let previousLetter = null;
    let currentLetterIndex = 0;

    setInterval(() => {
        let styles = {};
        if (previousLetter !== null) {
            styles = {
                color: defaultColor,
                fontSize: defaultFontSize
            };
            previousLetter.css(styles);
        }
        let currentLetter = letters.eq(currentLetterIndex);
        styles = {
            color: highlightColor,
            fontSize: "1.2em"
        };
        currentLetter.css(styles);
        currentLetterIndex += 1;
        previousLetter = currentLetter;
        if (currentLetterIndex >= letters.length) {
            currentLetterIndex = 0;
        }
    }, 700);
}

export { animateLogo };