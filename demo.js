$(document).ready(function() {
    $("#mainPanel").hide();
    $("form").submit(function(e) {
        e.preventDefault();
        $("#loginForm").hide(500);
        $("#mainPanel").show(500);
    });
});