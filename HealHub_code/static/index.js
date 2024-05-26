window.onload = function () {
    const pieces = document.getElementsByTagName('svg');
    for (var i = 0; pieces.length; i++) {
        let _piece = pieces[i];
        _piece.onclick = function(t) {
            if (t.target.getAttribute('data-position') != null) document.getElementById('data').innerHTML = t.target.getAttribute('data-position');
            if (t.target.parentElement.getAttribute('data-position') != null) document.getElementById('data').innerHTML = t.target.parentElement.getAttribute('data-position');
        }
    }
}
function showFeedback() {
    var feedbackText = document.getElementById('feedback').value.trim();
    if (feedbackText === '') {
        alert('Framsteg fält kan inte vara tomt');
        return;
    }

    document.getElementById('displayed-feedback').innerText = feedbackText;
    document.getElementById('feedback-display').style.display = 'block';
    document.getElementById('feedback-dialog').close();
}