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