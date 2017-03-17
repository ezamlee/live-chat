console.log("user login");

$(document).ready(function(){
	var getAllfriends = function (){
			var friendsList = []
			$.ajax({
				method: 'get',
				url: 'http://localhost:2222/people',
				data: {"userid": userid},

				success: function(res){
					console.log("friends= ",res);
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
						else if(res[j].status == 0 || res[j].status == -1)
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
						else if(res[j].status == -1)
						{
							record += '<button class="requested" id=" ' + res[j]._id + '" disabled>Requested</button>';
						}
						record +='</div>';
						$("#top").append(record);
					}
					$("#people").append("</div>");
				},
				error:function(error,k){
					console.log(error)
					console.log(k)
				}
			})
	}
	// 	//get all user except friends
	function getAllUsers(){

			$.ajax({
				method: 'get',
				url: 'http://localhost:2222/allpeople',
				data: {"userid": userid},

				success: function(res){
					console.log("allpeople = ", res);
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

$("#menupeople").click(function(){
	console.log("Ready")
	$("#application").text("");
	getAllfriends()
	getAllUsers()
})

	// $("#application").on('click', 'button.remove' , function(){
	// 		console.log("inside remove but");
	// 		var removeid = this.id;
	//     	console.log(removeid);
	//
	// 		// remove friends
	// 		function removeFriends(){
	// 			$.ajax({
	// 				method: 'get',
	// 				url: 'http://localhost:2222/remove',
	// 				data: {"userid": userid, "friendid": removeid},
	// 				success: function(res){
	// 					//my friends
	// 					console.log("from remove fun ",res)
	// 					location.reload();
	// 			},
	// 			error:function(err){
	// 				console.log(err)
	// 			}
	//     })
	// 		}
	// })
	//
	// $("#application").on('click', 'button.accept' , function(){
	// 		console.log("inside accept but");
	// 		var acceptid = this.id;
	// 		//accept friends request
	// 		function updateFriends(){
	// 			$.ajax({
	// 				method: 'get',
	// 				url: 'http://localhost:2222/update',
	// 				data: {"userid": userid, "friendid": acceptid},
	//
	// 				success: function(res){
	// 					//my friends
	// 					$("#application").text("");
	// 					getAllfriends()
	// 					getAllUsers()
	// 				}
	// 			})
	// 		}
	// })
	$("#application").on('click', 'button.add', function(){
			console.log("inside add but");
			var addid  = this.id;
	   		console.log(addid);

				$.ajax({
					method: 'get',
					url: 'http://localhost:2222/add',
					data: {"userid": userid, "friendid": addid},

					success: function(res){
						console.log("from add ", res)
						$("#application").text("");
						getAllfriends()
						getAllUsers()
					}
				})
	})
	// $("#application").on('click', 'img' , function(){
	// 		var frndid = $("img").attr("value");
	// 		console.log(frndid);
	// })

});
