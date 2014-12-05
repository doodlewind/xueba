$(document).ready(function() {
    $('.btn').removeAttr('disabled');
    $('#ustcId').focus();

    $("#mainPanel").hide();
    $("form").submit(function(e) {
        e.preventDefault();

        var id = $('#ustcId').val().toUpperCase();
        var password = $('#password').val();
        var loginData = {"ustc_id": id, "password": password};
        var btn = $('.btn');
        btn.attr('disabled', true);

        $.ajax({
            type: 'POST',
            url: '/login',
            data: loginData,
            dataType: 'json',
            success: function(json, textStatus) {
                $("#loginForm").hide(500);
                $("#mainPanel").show(500);
                $('name').html(json['name']);
                $('rate').html(json['rate']);
            },
            error: function(xhr, textStatus, error) {
                btn.removeAttr("disabled");
                alert("Sorry, login failed.");
            }
        });
    });
});