/**
 * Created by jacob on 2018/6/14.
 */
function postData(url,csrf){
        var flag = $("#flag").val();
        var src = $("#id_captcha_0").prev().attr("src");
        var hashkey = $("#id_captcha_0").val();
        src = "http://127.0.0.1:8000" + src;
        $.ajax({
            type: 'POST',
            url: url,
            data: {"src": src, "hashkey": hashkey},
            async: true,
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken",csrf );
            },
            success: function (result) {
                //window.location.reload();
                $(".captcha").trigger("click");
                if(flag=="0")
                {
                    postData(url,csrf);
                }
            }
        });
    }
