async function change() {
    const button = document.getElementById("klikklik");
    const http = new XMLHttpRequest();
    let url = `../sala/change/${button.getAttribute("classroomid")}/`;
    http.open("POST", url);
    http.send();
    http.onreadystatechange = (d) => {
        console.log(http.responseText)
    }
    window.setTimeout(() => {
        window.location.reload();
    }, 1500);
};

