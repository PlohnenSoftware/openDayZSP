async function change(e) {

    const http = new XMLHttpRequest();
    let url = `../sala/change/${e.target.getAttribute("classroomid")}/`;
    http.open("POST", url);
    http.send();
    http.onreadystatechange = (d) => {
        console.log(http.responseText)
    }
    window.setTimeout(() => {
        window.location.reload();
    }, 1500);
};
{
    window.setTimeout(() => {
        console.log("reload");
        window.location.reload();
    }, 15000);
}
