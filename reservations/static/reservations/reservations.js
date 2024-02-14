document.addEventListener("DOMContentLoaded", function () {
  loadAll();
});

function loadAll() {
  fetch("/getReservations")
    .then((response) => {
      if (!response.ok) {
        console.log("Something went wrong");
      }
      return response.json();
    })
    .then((json) => {
      console.log(json);
      const reservationsDiv = document.querySelector("#reservations");
      json.forEach((element) => {
        const reservation = document.createElement("div");
        reservation.id = `reservation${element.id}`;
        reservation.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">${element.restaurant_name}</h5>
                <small>${element.timestamp}</small>
            </div>
            <p class="mb-1">For ${element.numberOfDiners} persons at <strong>${element.time}</strong></p>
            `;
        const activeTag = document.createElement("small");
        const cancel_reservation = document.createElement("button");
        if (element.active) {
          activeTag.innerHTML = "Active";
          cancel_reservation.innerHTML = "Cancel Reservation";
          cancel_reservation.onclick = function(){
            cancel_reserve(element.id)
          }
          reservation.append(cancel_reservation);
        } else {
          activeTag.innerHTML = "Inactive";
        }
        reservation.append(activeTag);
        reservationsDiv.append(reservation);
      });
    });
}

function cancel_reserve(id) {
  fetch("/cancel", {
    method: "PUT",
    body: JSON.stringify({
      id: id,
    }),
  }).then((response) => {
    if (!response.ok) {
      console.log("Something went wrong");
    } else {
      location.reload();
    }
  });
}