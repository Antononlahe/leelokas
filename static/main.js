function swapColors() {
    var body = document.body;
    var buttons = document.getElementsByTagName('button');
    var currentBodyBackgroundColor = getComputedStyle(body).backgroundColor;
    var currentButtonBackgroundColor = getComputedStyle(buttons[0]).backgroundColor;
    body.style.backgroundColor = currentButtonBackgroundColor;
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].style.backgroundColor = currentBodyBackgroundColor;
    }
    localStorage.setItem('bodyBackgroundColor', currentButtonBackgroundColor);
    localStorage.setItem('buttonBackgroundColor', currentBodyBackgroundColor);
}
function loadColors() {
    var body = document.body;
    var buttons = document.getElementsByTagName('button');
    var bodyBackgroundColor = localStorage.getItem('bodyBackgroundColor');
    var buttonBackgroundColor = localStorage.getItem('buttonBackgroundColor');
    if (bodyBackgroundColor) {
        body.style.backgroundColor = bodyBackgroundColor;}
    if (buttonBackgroundColor && buttons.length > 0) {
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].style.backgroundColor = buttonBackgroundColor;}}}

window.onload = loadColors;