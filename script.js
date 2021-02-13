document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("led").addEventListener("click", (e) => {
        e.preventDefault();

        fetch('./setUpdate.php', { method: 'GET' })
        .catch(err => console.log(err));
    });

    var state = document.getElementById("state");

    const relState = async () => {
        fetch('./get_state.php', {method:'GET'})
        .then(res => res.json())
        .then(json => {
            //console.log(json);
            state.innerHTML = json.ledState == 1 ? 'LED Acceso' : 'LED Spento';
        })
        .catch(err => console.log(err));
    }

    relState();

    setInterval(relState, 500);

});
