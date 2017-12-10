layui.use('form', function () {
    var form = layui.form;
    var $=layui.jquery;
    form.on('submit(register-filter)', function (data) {
        var formData = data.field;
        console.log(formData);
        $.post('/register', formData, function (retJson) {
            console.log(retJson);
            if (retJson.status) {
                layer.msg(retJson.message);
                setTimeout('location.href="/";', 1000);
            } else {
                layer.msg(retJson.message);
            }
        },'json');
        return false;
    });
});