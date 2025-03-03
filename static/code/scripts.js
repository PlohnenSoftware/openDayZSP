// Nawiązujemy połączenie WebSocket z serwerem
const ws = new WebSocket(`ws://${location.host}/openday/ws`);

ws.onmessage = function(event) {
    let data = JSON.parse(event.data);
    let classroom_id = data.classroom_id;
    let status = data.status;  // true: "Zajęte", false: "Wolne"
    
    // Aktualizujemy element statusu
    let statusEl = document.getElementById("status-" + classroom_id);
    if (statusEl) {
         if (status) {
              statusEl.classList.remove("wolne");
              statusEl.classList.add("zajete");
              statusEl.textContent = "Zajęte";
         } else {
              statusEl.classList.remove("zajete");
              statusEl.classList.add("wolne");
              statusEl.textContent = "Wolne";
         }
    }
    
    // Aktualizujemy przycisk (jeśli jest)
    let buttonEl = document.querySelector(`input.przyciskacz[classroomid="${classroom_id}"]`);
    if (buttonEl) {
         if (status) {
              buttonEl.value = "Zwolnij";
         } else {
              buttonEl.value = "Zajmij";
         }
    }
};

function change(e) {
    const classroom_id = e.target.getAttribute("classroomid");
    const http = new XMLHttpRequest();
    const url = `${location.host}/openday/sala/change/${classroom_id}/`;
    http.open("POST", url);
    http.send();
    http.onreadystatechange = () => {
        console.log(http.responseText);
    };
}

// Rejestracja event listenerów dopiero po załadowaniu DOM
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".przyciskacz").forEach(function(elem) {
         elem.addEventListener('click', change);
    });
});
