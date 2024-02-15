document.addEventListener("DOMContentLoaded", function () {
    loadAll()
  });

function loadAll(){
    // Fetch all restaurants
    fetch("/getAllRestaurants")
        .then(response => {
            if (!response.ok){
                console.log("Something went wrong");
            }
            return response.json();
        })
        .then(jsonResponse =>{
            const restaurants_div = document.querySelector("#allRestaurants")
            // For each reastaurant create its structure
            jsonResponse.forEach(element => {
                restaurants_div.innerHTML += `
                <div class="col-md-3 mb-4">
                    <div class="card h-100">
                        <img class="card-img-top" src="${element.img_URL}">
                        <div class="card-body">
                            <h5 class="card-title">${element.name}</h5>
                            <p class="card-text">${element.address}</p>
                            <a href="/reserve/${element.id}" class="btn btn-primary"> Reserve </a>
                        </div>
                    </div>
                </div>
                `
            });
        })
}