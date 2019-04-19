window.addEventListener ?
window.addEventListener("load",loadMap,false) :
window.attachEvent && window.attachEvent("onload", loadMap());


//window.onload = loadMap();

var map = null;
var key = 'vpHW7GwCtgbrt9V3d6Wlk4OYz2d6m22w';
var startpt = '201 N Goodwin Ave, Urbana, IL 61801';

$(document).ready(function() {
    $(".eventTable tr").click(function() {
        //alert("Table clicked");
        //alert("Listener enabled");
        var row = this.innerHTML;
        //alert(row);
        var loc = row.search("id");
        new_str = row.substring(loc + 9);
        var endpt = new_str.substring(0, new_str.search("<"));
        console.log(endpt);
        route_url = "http://www.mapquestapi.com/directions/v2/alternateroutes?key=" + key  + "&from=" + startpt + "&to=" + endpt + "&maxRoutes=2&timeOverage=25";
        $.getJSON(route_url, function (result) {
            console.log(result.route.distance);
            $.ajax({
                type: "GET",
                url: "https://www.fueleconomy.gov/ws/rest/fuelprices",
                dataType: "xml",
                success: function (xml) {
                    var price = $(xml).find("regular").text();
                    console.log(price);
                    calculate_mileage(result.route.distance, price)
                }
               });
            });
            //calculate_mileage(result.route.distance);
            map.remove();
            newMap(endpt)
        });
        //var endpt = this.target.getAttribute('loc');
        //alert(endpt);


});


function calculate_mileage(distance, price) {
    //("Calculating " + price + " " + distance);
    var table = document.getElementById('cars');
    for (var r = 1, n = table.rows.length; r < n; r++) {
        car_mpg = table.rows[r].cells[2].textContent;
        console.log("Car " + r + " : " + car_mpg);
        table.rows[r].cells[3].innerHTML = ((distance / car_mpg) * price).toFixed(2);
    }
}



function loadMap () {
    L.mapquest.key = key;

    map = L.mapquest.map('map', {
        center: [37.7749, -122.4194],
        layers: L.mapquest.tileLayer('map'),
        zoom: 12
    });
    map.addControl(L.mapquest.control());
    L.mapquest.directions().route({
          start: startpt,
          end: 'Chicago, IL',
          options: {
            timeOverage: 25,
            maxRoutes: 3,
          }
        });
}

function newMap(endpt) {
    L.mapquest.key = key;

    map = L.mapquest.map('map', {
        center: [37.7749, -122.4194],
        layers: L.mapquest.tileLayer('map'),
        zoom: 12
    });
    map.addControl(L.mapquest.control());
    L.mapquest.directions().route({
          start: startpt,
          end: endpt,
          options: {
            timeOverage: 25,
            maxRoutes: 3,
          }
        });
}