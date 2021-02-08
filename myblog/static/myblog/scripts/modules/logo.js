function animateLetters(letters, logoPostfix, phrases) {
    if (animateLetters.currentLetterIndex === undefined) {
        animateLetters.currentLetterIndex = 0;
    }
    if(animateLetters.currentLetterIndex !== 0) {
        return;
    }
    let lettersBefore = letters.slice(0, animateLetters.currentLetterIndex);
    lettersBefore.each(function(index) {
       let this_ = $(this);
       this_.empty();
       this_.css("display", "inline");
    });
    let letter = letters.eq(animateLetters.currentLetterIndex);
    console.log(letter);
    letter.after(phrases[animateLetters.currentLetterIndex]);
    let otherLetters = letters.slice(animateLetters.currentLetterIndex + 1);
    otherLetters.each(function(index) {
        $(this).css("display", "none");
    });
    animateLetters.currentLetterIndex += 1;

    if (animateLetters.currentLetterIndex >= phrases.length) {
        /* Start animation again */
        animateLetters.currentLetterIndex = 0;
    }
}
function animateLogo(logo) {
    const phrases = [
        "okładność", // D
        "mbicja",  // a
        "otoryzacja", // m
        "nnowacja", // i
        "ranżacja", // a
        "aturalność", // n
        "ot", // K
        "rok", // u
        "ak", // r
        "kona", // i
        "nanas", // a
        "arcie", // t
        "abażur" // a
    ];
    let mainLogo = logo.find(".main-logo");
    let logoPostfix = logo.find(".logo-postfix");
    let letters = mainLogo.children();
    const animationIntervalMillis = 2000;
    setInterval(() => animateLetters(letters, logoPostfix, phrases),
        animationIntervalMillis);
}

export { animateLogo };