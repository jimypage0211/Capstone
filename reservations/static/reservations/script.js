document.addEventListener("DOMContentLoaded", function () {
    loadAll()
  });

function loadAll(){
    fetch("/getAllRestaurants")
        .then(response => {
            if (!response.ok){
                console.log("Something went wrong");
            }
            return response.json();
        })
        .then(jsonResponse =>{
            console.log(jsonResponse)
        })
}