document.getElementById('progress').addEventListener('submit',function(event){
    var progessInput = document.getElementById('progress')
    if (progressInput.value.trim() === '') {
        alert('Framsteg fält kan inte vara tom');
        event.preventDefault();
    }
});

document.getElementById('submitFeedback').addEventListener('click', function() {
    var feedbackTextarea = document.getElementById('feedback');
    if (feedbackTextarea.value.trim() === '') {
        alert('Feedback fält kan inte vara tom');
    } else {
        alert('Tack för din feedback!');
        feedbackTextarea.value = '';
    }
});