layui.use('form', function () {
    var form = layui.form;
    var $=layui.jquery;
    form.on('submit(login-filter)', function (data) {
        var formData = data.field;
        $.post('/login', formData, function (retJson) {
            console.log(retJson);
            if (retJson.status) {
                layer.msg(retJson.message);
                setTimeout('location.reload()', 1000);
            } else {
                layer.msg(retJson.message);
            }
        },'json');
        return false;
    });
});