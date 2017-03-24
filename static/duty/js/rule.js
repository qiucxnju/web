
var RULE_TYPE_SWAP = 1;
var RULE_TYPE_ADD_PEOPLE = 2;
var RULE_TYPE_DEL_PEOPLE = 3;
var RULE_TYPE_JUMP_WEEK = 4;
var RULE_TYPE_JUMP_DAY = 5;
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}




showRuleDialog = function(){
	$('#RuleDialogTrigger').click();
	$("#start").val(new Date().Format("yyyy-MM-dd"));
}

submit = function(){
	var type = parseInt($("#type").val());
	var times = parseInt($("#times").val());
	console.log(type + times);
	var name = $("#name").val();
	var start = $("#start").val();
	if (type == RULE_TYPE_ADD_PEOPLE){
		if (name.length == 0){
			alert("name not set");
			return;
		}
		if ($("#start").val().length != 10){
			alert("start time not set");
			return;
		}
	}
	$.ajax({
		url: "../duty/add",
		type: "POST",
		data: {
			csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
			type : type,
			times : times,
			name : name,
			start : start,
		},
	}).done(function(data) {
		console.log(data);
	});
}

jumpDay = function(a){
	console.log(a);
	console.log(a.find('time'));
	console.log(a.find('time').attr('datetime'));

	var day = a.find('time').attr('datetime');
	var type = RULE_TYPE_JUMP_DAY;

	$.ajax({
		url: "../duty/add",
		type: "POST",
		data: {
			csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
			type : type,
			day : day,
		},
	}).done(function(data) {
		console.log(data);
	});
}