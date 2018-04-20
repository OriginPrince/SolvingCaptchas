/**
 * Created by jacob on 2018/3/22.
 */
function user_post(url1,url2, data, text,csrf) {
    $.ajax({
        cache: false,
        type: "POST",
        url: url1,
        data: data,
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
       success: function (data) {
            if (data.status == 'fail') {
                    $("#AlertMessage").text(data.msg);
                    $("#example").modal('toggle');
            } else if (data.status == 'success') {
                $("#textMessage").text(text);
                $("#TextSubmit").click(function () {
                        window.location.href = url2;
                    });
                $("#textExample").modal('toggle');
            }
        }
    });
}