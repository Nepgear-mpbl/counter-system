layui.use('table', function () {
    var table = layui.table;
    table.render({
        elem: '#business'
        , url: '/admin/business/get' //数据接口
        , page: true
        , cols: [[{field: 'username', title: '用户名', width: '40%',fixed: 'left'}
            , {field: 'post_time', title: '叫号时间', width: '60%', sort: true}
        ]]
    });
    $('#accept-button').click(function () {
        $.post('/admin/business/accept', {}, function (retJson) {
            if (retJson.status) {
                layer.msg(retJson.message);
                setTimeout('location.reload()', 1000);
            } else {
                layer.msg(retJson.message);
            }
        },'json');
    });
    $('#finish-button').click(function () {
        $.post('/admin/business/finish', {}, function (retJson) {
            if (retJson.status) {
                layer.msg(retJson.message);
                setTimeout('location.reload()', 1000);
            } else {
                layer.msg(retJson.message);
            }
        },'json');
    });
});