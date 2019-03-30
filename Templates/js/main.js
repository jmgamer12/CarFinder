$(document).ready(function () {

    $("input[name=riderSelect]").click(function () {
        addToForm();
    });

});

function addToForm() {
    var radioVal = $("input[name='riderSelect']:checked").val();
    if(radioVal == "driver"){
        add_html = '<br>' +
            '<div class="form-row">' +
            '    <div class="form-group col-md-6">' +
            '        <label for="inputCar">Car</label>' +
            '        <input type="text" class = "form-control" id="inputCar" placeholder="Car">' +
            '    </div>' +
            '    <div class="form-group col-md-6">' +
            '        <label for="inputSeats">Number of Seats</label>' +
            '        <input type="number" class = "form-control" id="inputSeats" placeholder="# of Seats">' +
            '    </div>' +
            '</div>' +
            '<div>' +
            '    <label>Time of Departure</label>' +
            '</div>' +
            '<select class="form-control">' +
            '    <option>Early</option>' +
            '    <option>Late</option>' +
            '    <option>On time</option>' +
            '</select>';
    } else {
        add_html = '';
    }

    $("#form-extension").html(add_html);

}