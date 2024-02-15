document.addEventListener("DOMContentLoaded", function () {
  loadAll();
});

function loadAll() {
  // Fetch all reservations
  fetch("/getReservations")
    .then((response) => {
      if (!response.ok) {
        console.log("Something went wrong");
      }
      return response.json();
    })
    .then((json) => {
      console.log(json);
      // Get the reservations div
      const reservationsDiv = document.querySelector("#reservations");
      json.forEach((element) => {
        // Construct each reservation structure
        const reservation = document.createElement("div");
        reservation.className = "reservation-item";
        reservation.id = `reservation${element.id}`;
        reservation.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">${element.restaurant_name}</h5>
                <small>${element.timestamp}</small>
            </div>
            <p class="mb-1">For ${element.numberOfDiners} persons at <strong>${element.time}</strong></p>
            `;
        const activeTag = document.createElement("small");
        // Assing tags for active or incactives reservations
        activeTag.className = element.active ? "active-tag" : "inactive-tag";
        const cancel_reservation = document.createElement("button");
        cancel_reservation.className = "btn btn-danger";
        reservation.append(activeTag);
        reservation.append(document.createElement("br"));
        // If reservation is active assign cancel button
        if (element.active) {
          activeTag.innerHTML = "Active";
          cancel_reservation.innerHTML = "Cancel Reservation";
          cancel_reservation.onclick = function () {
            cancel_reserve(element.id);
          };
          reservation.append(cancel_reservation);
          // else asign unarchive button
        } else {
          activeTag.innerHTML = "Inactive";
          const unarchive = document.createElement("button");
          unarchive.className = "btn btn-danger";
          unarchive.innerHTML = "Unarchive";
          unarchive.onclick = function () {
            unarchive_reserve(element.id);
          };
          reservation.append(unarchive);
        }
        // Append each reservation to the reservations div
        reservationsDiv.append(reservation);
      });
    });
}

// Function called by the cancel button. Given the reservation id, fetch it and cancel it
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
      // Alert to show the reservation was deleted
      let okAlert = document.createElement("div")     
      okAlert.innerHTML = `
        <div class="alert alert-info" role="alert">
          Your reservation was succesfully deleted
        </div>
        `;
      document.querySelector("#reservations").prepend(okAlert);
      // Reload the window to update status of the reservations after 3 secs to show the alert
      setTimeout(function(){
        location.reload();
      }, 3000)
    }
  });
}

// Function called by the unarchive button. Given the reservation id, fetch it and unarchive it
function unarchive_reserve(id) {
  fetch("/unarchive", {
    method: "POST",
    body: JSON.stringify({
      id: id,
    }),
  }).then((response) => {
    if (!response.ok) {
      console.log("Something went wrong");
    } else {
      // Alert to show the reservation was unarchived
      let okAlert = document.createElement("div");
      okAlert.innerHTML = `
        <div class="alert alert-warning" role="alert">
          Your reservation was succesfully unarchived
        </div>
        `;
      document.querySelector("body").prepend(okAlert);
      // Reload the window to update status of the reservations after 3 secs to show the alert
      setTimeout(function(){
        location.reload();
      }, 3000)
    }
  });
}
