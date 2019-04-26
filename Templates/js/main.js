$(document).ready(function () {
    $("input[name=riderSelect]").click(function () {
        addToForm();
    });

});

$(document).ready(function () {
    $("#org_select").change(function (e) {
        //alert("Clicked dropdown");
        $("#org_select option[value=0]").remove();
        addNewOrg();
    })
});

function addNewOrg() {
    if (document.getElementById("org_select").value === "1") {
        //alert("Entered if");
        add_html = '<br>' +
            '<div class="form-row">' +
            '    <div class="form-group col-md-6">' +
            '        <label for="inputOrg">Add Organization</label>' +
            '        <input type="text" class="form-control" name="inputOrg" placeholder="Ex. Track, Field, Etc.">' +
            '    </div>' +
            '</div>';
        $("#org_form-extension").html(add_html);
    }
    else {
        add_html = "";
        $("#org_form-extension").html(add_html);
    }

}

function addToForm() {
    var radioVal = $("input[name='riderSelect']:checked").val();
    var riderDiv = document.getElementById("riderDiv");
    var formextend = document.getElementById("form-extension")
    if(radioVal === "driver"){
        add_html = '<br>' +
            '<div class="form-row">' +
            '    <div class="form-group col-md-6">' +
            '        <label for="inputCar">Car</label>' +
            '        <input type="text" class="form-control" name="inputCar" placeholder="Format: Year Brand Car (Ex: 1998 Toyota Camry)">' +
            '    </div>' +
            '    <div class="form-group col-md-6">' +
            '        <label for="inputSeats">Number of Seats</label>' +
            '        <input type="number" class = "form-control" name="inputSeats" placeholder="# of Seats">' +
            '    </div>' +
            '</div>';
            riderDiv.style.display = "none";
            formextend.style.display = "block";
    } else if(radioVal === "rider"){
            riderDiv.style.display = "block";
            formextend.style.display = "none";
            add_html = '';
    } else {
        add_html = '';
        formextend.style.display = "none";
        riderDiv.style.display = "block";
    }
    $("#form-extension").html(add_html);

}