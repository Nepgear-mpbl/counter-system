layui.use('table', function(){
  var table = layui.table;
  table.render({
    elem: '#business'
    ,height: 315
    ,url: '/admin/business/get' //数据接口
    ,page: true
    ,cols: [[
      {field: 'user_id', title: '用户ID', width:80, sort: true, fixed: 'left'}
      ,{field: 'username', title: '用户名', width:80}
      ,{field: 'post_time', title: '叫号时间', width:80, sort: true}

    ]]
  });
});