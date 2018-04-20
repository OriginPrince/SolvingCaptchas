function refresh_captcha() {
    $.get("/captcha/refresh/?" + Math.random(), function (result) {
        $('.captcha').attr("src", result.image_url);
        $('#id_captcha_0').attr("value", result.key);
    });
    return false;
}
$(function () {
    $('.captcha').click(refresh_captcha);
})
