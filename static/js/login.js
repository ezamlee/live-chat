$(document).ready(function(){
	$('#login-form').css('display','none')
	$('#registration-form').css('display','none')
	$("#btlogin").click(function(){
		var username  = $("#lgusername").val().length > 0 ? $("#lgusername").val() : null ;
		var password  = $("#lgpassword").val().length > 0 ? $("#lgpassword").val() : null;
		if(username && password){
			console.log("loging")
			$.ajax({
				url:"http://localhost:9888/check_user",
				data:{"username":username,"password":password},
				method:"GET",
				success:function(e){
					uid = e['_id']
					username = e['userName']
					image = e['image']
					console.log(uid)
					console.log(username)
					console.log(image)
					if(uid == undefined){
						$('#lgerrornotice').append("<p>PLEASE RECHECK YOUR USERNAME AND MATCHED PASSWORD</p>");
					}
					else{
						window.location = "http://localhost:8888/?userid="
															+uid
															+"&username="
															+username
															+"&imgeurl="
															+image;

					}

				},
				error:function(error){
					$('#lgerrornotice').text("")	
					$('#lgerrornotice').append("<p>PLEASE RECHECK YOUR USERNAME AND MATCHED PASSWORD</p>");
				}

			});
			console.log("ajax done")

		}
	});
	$("#btregister").click(function(){
		console.log("clicked")
		var username = $("#rgusername").val().length > 0 ? $("#rgusername").val() : null ;
		var password = $("#rgpassword").val() == $("#rrgpassword").val() && $("#rgpassword").val().length >0 ? $("#rgpassword").val() : null
		if(username && password){
			console.log("ajaxed")
			$.ajax({
				method:"GET",
				url:"http://localhost:7888/register/user_check?username="+username,
				success:function(res){
					console.log(res)
					if(res == "avaliable"){
						var imlist = ["A01.png","A02.png","A03.png","A04.png","A05.png","B01.png","B02.png","B03.png","B04.png","B05.png","C01.png","C02.png","C03.png","C04.png","C05.png","D01.png","D02.png","D03.png","D04.png","D05.png","E01.png","E02.png","E03.png","E04.png","E05.png","F01.png","F02.png","F03.png","F04.png","F05.png","FA01.png","FA02.png","FA03.png","FA04.png","FA05.png","FB01.png","FB02.png","FB03.png","FB04.png","FB05.png","FC01.png","FC02.png","FC03.png","FC04.png","FC05.png","FD01.png","FD02.png","FD03.png","FD04.png","FD05.png","FE01.png","FE02.png","FE03.png","FE04.png","FE05.png","FG01.png","FG02.png","FG03.png","FG04.png","FG05.png","FH01.png","FH02.png","FH03.png","FH04.png","FH05.png","FI01.png","FI02.png","FI03.png","FI04.png","FI05.png","G01.png","G02.png","G03.png","G04.png","G05.png","H01.png","H02.png","H03.png","H04.png","H05.png","I01.png","I02.png","I03.png","I04.png","I05.png","J01.png","J02.png","J03.png","J04.png","J05.png","K01.png","K02.png","K03.png","K04.png","K05.png","L01.png","L02.png","L03.png","L04.png","L05.png","M01.png","M02.png","M03.png","M04.png","M05.png","Male-Avatar-Bowler-Hat-icon.png","Male-Avatar-Bow-Tie-icon.png","Male-Avatar-Cool-Cap-icon.png","Male-Avatar-Cool-Sunglasses-icon.png","Male-Avatar-Emo-Haircut-icon.png","Male-Avatar-Goatee-Beard-icon.png","Male-Avatar-Hair-icon.png","Male-Avatar-icon.png","Male-Avatar-Mustache-icon.png","N01.png","N02.png","N03.png","N04.png","N05.png","O01.png","O02.png","O03.png","O04.png","O05.png"]
						$("#list-of-img").css("display","block")
						for (var i =0  ; i <imlist.length;i++ ){
							$("#list-of-img").append("<img class=\"profile_picture\"src=\"static/pic/"+ imlist[i] +"\"   width=\"50\">")
						}
						$(".profile_picture").click(function(e){
							var profilepic = e.target.src.substr(e.target.src.indexOf("/pic/"),e.target.src.length);
							$.ajax({
								method:"GET",
								url:"http://localhost:9888/update_user",
								data:{"username":username,"password":password,"pic":profilepic},
								success:function(res){
									console.log(res)
									if(res.split(":")[1]=="success")
									{
										window.location = 	 "http://localhost:8888/?userid="
															+res.split(":")[0]
															+"&username="
															+username
															+"&imgeurl="
															+profilepic;
									}
									else{
										$("#list-of-img").css("display","none")
										$("#rgusername").val("")
										$("#rgpassword").val("")
										$("#rrgpassword").val("")
										$('#rgerrornotice').append("<p>Username already taken</p>");

									}
								},
								error:function(error,r){
									$("#list-of-img").css("display","none")
									$("#rgusername").val("")
									$("#rgpassword").val("")
									$("#rrgpassword").val("")
									$('#rgerrornotice').append("<p>Username already taken</p>");
								}
							})
						});
					}
					else{
						$("#list-of-img").css("display","none")
						$("#rgusername").val("")
						$("#rgpassword").val("")
						$("#rrgpassword").val("")
						$('#rgerrornotice').append("<p>Username already taken</p>");
					}
				},
				error:function(error,k,l){
					console.log("error")
					console.log(error);
					console.log(k)
					console.log(l)
					$("#list-of-img").css("display","none")
					$("#rgusername").val("")
					$("#rgpassword").val("")
					$("#rrgpassword").val("")
					$('#rgerrornotice').append("<p>Username already taken</p>");
				}

			})
		}
	});
})
