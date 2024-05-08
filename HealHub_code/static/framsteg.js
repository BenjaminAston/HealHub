document.getElementById('progess').addEventListener('submit',function(event){
    var progessInput = document.getElementById('progress')
    if (progressInput.value.trim() === '') {
        alert('Framsteg fält kan inte vara tom');
        event.preventDefault();
    }
});