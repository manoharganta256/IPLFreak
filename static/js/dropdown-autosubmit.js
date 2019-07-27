function autosubmit() {
    let year = document.getElementById('seasons').value;

    window.location.href = `/seasons/${year}/`;
}