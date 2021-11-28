var fadeEffect=function(){
	//Download by http://www.codesc.net
	return{
		init:function(id, flag, target){
			this.elem = document.getElementById(id);
			clearInterval(this.elem.si);
			this.target = target ? target : flag ? 100 : 0;
			this.flag = flag || -1;
			this.alpha = this.elem.style.opacity ? parseFloat(this.elem.style.opacity) * 100 : 0;
			this.si = setInterval(function(){fadeEffect.tween()}, 20);
		},
		tween:function(){
			if(this.alpha == this.target){
				clearInterval(this.si);
			}else{
				var value = Math.round(this.alpha + ((this.target - this.alpha) * .05)) + (1 * this.flag);
				this.elem.style.opacity = value / 100;
				this.elem.style.filter = 'alpha(opacity=' + value + ')';
				this.alpha = value
			}
		}
	}
}();

function start_score(){
    //使用ajax加载csv文件的数据
	myresult=[];
	alert("正在评分，请稍等...");
	var url2 = document.getElementById("video2_url").value;  //获取放入的视频的名字  test1
	var url1 = document.getElementById("video1_url").value;  //标准视频的名字，需要传给后端！
	url2 = url2.replace('.mp4',''); //把后面的去掉
	debugger;
	var data= {
		data: JSON.stringify({
			'filename': url2,
			'standard': url1
		}),
	}
	console.log(data)
	setTimeout(function(){

    $.ajax({

            url: "/getScore",
			data:data,
			dataType: 'json',
            method:"POST",
            success: function(result) {
				myresult = result;
            	console.log(result);
            for(i=0;i<=myresult.length-1;i++){
                td_body_name = "td_body_"+i;
				td_rhythm_name = "td_rhythm_"+i;
                $("#"+td_body_name).html(parseFloat(myresult[i-1].motion_score).toFixed(2));
				$("#"+td_rhythm_name).html(parseFloat(myresult[i-1].rhythm_score).toFixed(2));
                //alert($("#"+td_name).html());   
			}
	var motion = document.getElementById("motion_score").value
	document.getElementById("motion_score").value = "动作评分为:" +parseFloat(myresult[myresult.length-1].motion_score).toFixed(2);
	var rhythm = document.getElementById("rhythm_score").value
	document.getElementById("rhythm_score").value = "节奏评分为:" +parseFloat(myresult[myresult.length-1].rhythm_score).toFixed(2);
	// document.getElementById("leida_photo").src = "../static/img/score_" + url2 + '.png'
	document.getElementById("leida_photo").src = "../DanceWorkbench/output/capacity" + '.png'
	document.getElementById("leida_photo").style.visibility="visible"
	// $("#motion_score").val("动作评分为:"+myresult[0]);
	// $("#rhythm_score").val("节奏评分为:"+myresult[1]);
	$("#motion_score_1").fadeIn(2000);
	$("#rhythm_score_2").fadeIn(2000);
	}
	});
	},2000);
}