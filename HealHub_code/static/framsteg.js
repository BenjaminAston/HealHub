
document.getElementById('feedback-form').onsubmit = function(event) {
    event.preventDefault(); 


    document.getElementById('feedback-dialog').innerHTML = `
        <h3>Tack för din feedback!</h3>
        <button onclick="document.getElementById('feedback-dialog').close()">Stäng</button>`;
}