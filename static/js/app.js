//get all friends
var getAllfriends = function (){
	console.log("hi ya me3'lbani")
	var friendsList = []
	$.ajax({
		method: 'get',
		url: 'http://localhost:8888/people',
		data: {"userid": 4},

		success: function(res){
			//my friends
			$("#application").append("<div id='top'>");
			for(var j=0; j<Object.keys(res).length; j++)
			{
				friendsList[j] = res[j]._id
				var path = "static" + res[j].img
				var record = "<div class='per'>";
				if(res[j].status == 1.0)
				{
					record += '<img class="private" value = ' + res[j]._id + ' src=' + path + '>';
				}
				else if(res[j].status == 0)
				{
					record += '<img value = ' + res[j]._id + ' src=' + path + '>';
				}
				record += '<p>' + res[j].userName  + '</p>';
				if(res[j].status == 1.0)
				{
					record += '<button class="remove" id="' + res[j]._id + '">unfriend</button>';
				}
				else if(res[j].status == 0)
				{
					record += '<button class="accept" id=" ' + res[j]._id + '">Accept</button>';
				}

				record +='</div>';
				$("#top").append(record);
			}

			$("#people").append("</div>");
		}
	})
}
//get all user except friends
function getAllUsers(){

	$.ajax({
		method: 'get',
		url: 'http://localhost:8888/allpeople',
		data: {"userid": 2},

		success: function(res){
			//all users
			$("#application").append("<div id='bot'>");
			for(var j=0; j<Object.keys(res).length; j++)
			{
				var path = "static" + res[j].image
				var record = "<div class='per'>";
				record += '<img value = ' + res[j]._id + ' src=' + path + '>';
				record += '<p>' + res[j].username  + '</p>';
				record += '<button class="add" id=" ' + res[j]._id + '">Add</button>';
			   	record += '</div>';
				$("#bot").append(record);
			}

			$("#people").append("</div>");
		}
	})
}

//accept friends request
function updateFriends(){
	$.ajax({
		method: 'get',
		url: 'http://localhost:8888/update',
		data: {"userid": 2, "friendid": 13},

		success: function(res){
			//my friends
			console.log("from update ",res)

		}
	})
}
function addFriends(){
	$.ajax({
		method: 'get',
		url: 'http://localhost:8888/add',
		data: {"userid": 2, "friendid": 10},

		success: function(res){
			//my friends
			console.log("from add ", res)
		}
	})
}
// remove friends
function removeFriends(){
	$.ajax({
		method: 'get',
		url: 'http://localhost:8888/remove',
		data: {"userid": 2, "friendid": 10},

		success: function(res){
			//my friends
			console.log("from remove fun ",res)
	}
})
}
//removeFriends()
//addFriends()
//updateFriends()
