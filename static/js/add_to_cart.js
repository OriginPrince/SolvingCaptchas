/**
 * Created by jacob on 2018/3/22.
 */
function add_fav(url1, url2, good_id, operation, csrf) {
    $.ajax({
        cache: false,
        type: "POST",
        url: url1,
        data: {'good_id': good_id, 'operation': operation},
        async: true,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf);
        },
        success: function (data) {
            if (data.status == 'fail') {
                if (data.msg == 'NeedLogin') {
                    $("#AlertMessage").text("失败");
                    $("#TextError").click(function () {
                        window.location.href = url2;
                    });
                    $("#example").modal('toggle');
                } else {
                    $("#AlertMessage").text("失败");
                    $("#example").modal('toggle');
                }
            } else if (data.status == 'success') {
                $("#textMessage").text("成功");
                $("#textExample").modal('toggle');
            }
        }
    });
}