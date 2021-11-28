layui.use(['upload', 'layer'], function () {
  var $ = layui.jquery
      , layer = layui.layer
      , upload = layui.upload;
  upload.render({
      method: 'post'
    , elem: '#selectFile1'
    , url: '/upload'  //传到的后端函数
    // , url: '/upload'
      , auto: false
      , accept:'file' //视频
      //,multiple: true
      , bindAction: '#uploadFile1'
      , choose: function (obj) {
         // var file = this.files = obj.pushFile();
          obj.preview(function (index, file, result) {
              //debugger;
              var files = obj.pushFile();
            //   console.log(files)S
             console.log(files[index].name);
             document.getElementById("size1").style.backgroundColor = 'transparent';
              document.getElementById("size1").style.display = "inline";
              var xx = document.getElementById("size1").value = file.name+'【'+(file.size / 1024 / 1024).toFixed(2) + 'MB'+'】';
              document.getElementById("video1_url").value = null
              var url1 = document.getElementById("video1_url").value = file.name;
          })

      }
      , done: function (res) {
        console.log(res);
        alert('上传成功');
          // if(res.code==0){
          //   layer.alert('上传失败');
          //     return layer.msg('上传失败-------');
          // }else {
          //   layer.alert('上传成功');
          //   alert('上传成功');
          //   return  layer.msg('上传成功-------');
          // }
      }
  });

});

layui.use(['upload', 'layer'], function () {
  var $ = layui.jquery
      , layer = layui.layer
      , upload = layui.upload;
  upload.render({
      method: 'post'
    , elem: '#selectFile2'
    , url: '/upload'  //传到的后端函数
    // , url: '/upload'
      , auto: false
      , accept:'file' //视频
      //,multiple: true
      , bindAction: '#uploadFile2'
      , choose: function (obj) {
         // var file = this.files = obj.pushFile();
          obj.preview(function (index, file, result) {
              //debugger;
              var files = obj.pushFile();
            //   console.log(files)S
             console.log(files[index].name);
             document.getElementById("size2").style.backgroundColor = 'transparent';
              document.getElementById("size2").style.display = "inline";
              var xx = document.getElementById("size2").value = file.name+'【'+(file.size / 1024 / 1024).toFixed(2) + 'MB'+'】';
              document.getElementById("video2_url").value = null
              var url1 = document.getElementById("video2_url").value = file.name;
          })

      }
      , done: function (res) {
        console.log(res);
        alert('上传成功');
          // if(res.code==0){
          //   layer.alert('上传失败');
          //     return layer.msg('上传失败-------');
          // }else {
          //   layer.alert('上传成功');
          //   alert('上传成功');
          //   return  layer.msg('上传成功-------');
          // }
      }
  });

});

function prev_1(){
  var url1 = document.getElementById("video1_url").value;
  var FZ_VIDEO = new createVideo(
    "testBox",	//容器的id
    {
        url 		: "/static/video/"+url1, 	//视频地址
        autoplay	: false				//是否自动播放
    }
  );
  FZ_VIDEO.setUrl("/static/video/"+url1);
}


function prev_2(){
  var url2 = document.getElementById("video2_url").value;
  var FZ_VIDEO = new createVideo(
    "testBox",	//容器的id
    {
        url 		: "/static/video/"+url2, 	//视频地址
        autoplay	: false				//是否自动播放
    }
);
FZ_VIDEO.setUrl("/static/video/"+url2);
}

layui.use('layCascader', function () {
var layCascader = layui.layCascader;
var demo1_1 = layCascader({
elem: '#demo1_1',
options: options
});
demo1_1.changeEvent(function (value, node) {
console.log('value:' + value + ',Node:' + JSON.stringify(node.data))
//layer.msg('value:' + value + ',Node:' + JSON.stringify(node.data));
// var url1 = document.getElementById("video1_url").value = value+'.mp4';
// var name = demo1_1.getCheckedValues();
// var node = demo1_1.getCheckedNodes();
var parent = node.parentNode.data.value
console.log('name:' + name + ',Node:' + node.data);
console.log(parent)
var url1 = '/'+parent+'/'+value
});
});