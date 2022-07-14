var title = document.title;
var count = 0;

function changeTitle() {
    count++;
    var newTitle = '(' + count + ') ' + title;
    document.title = newTitle;
}

function resetTitle() {
    document.title = title;
    count = 0;
}

function checkTabFocused() {
    if (document.visibilityState === 'visible') {
        console.log('✅ browser tab has focus');
        resetTitle();
    } else {
        console.log('⛔️ browser tab does NOT have focus');
        changeTitle();
    }
}
