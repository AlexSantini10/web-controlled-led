document.addEventListener('DOMContentLoaded', () => {

    document.getElementById("led").addEventListener("click", (e) => {
        e.preventDefault();

        fetch('./setUpdate.php', { method: 'GET' })
        .catch(err => console.log(err));
		

    });

});