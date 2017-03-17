
console.log("group loaded");
$(document).ready(function(){
    $("#menugroup").click(function(){
        $('#allgroups').remove();
        $('#mygroups').remove();
        $.ajax({
            url:"http://localhost:1111/mygroups",
            method:"GET",
            data:{"userid":userid},
            success:function(res){     
                gid_arr = res.groupid
                gname_arr = res.groupnames
                gstat = res.groupstat
                groupimage = res.groupimage

                //my groups
                $('#application').append('<div id="mygroups">');
                $('#mygroups').append("<h3> My Groups </h3> ");

                for(var i = 0 ; i < gname_arr.length ; i++){
                    var group_record = "<div class='per' style='width:300px;height:300px'>";
                    group_record +=  '<img  class="public" value="'+gid_arr[i]+'" src= "/static'+groupimage[i]+'">';
                    group_record += '<p>' + gname_arr[i]  + '</p>';

                    if ( gstat[i] == 1){
                        group_record += '<button id="leave" class="leave">Leave</button>';
                    }

                    else{
                        group_record += '<button class="requested">Requested</button>';
                    }

                    group_record +='</div>'
                    $('#mygroups').append(group_record);
                }

                $('#application').append('</div>');
            },
            error:function(error,k){
                    console.log(error)
                    console.log(k)
            }
        });
        $.ajax({
            url:"http://localhost:1111/allgroups",
            method:"GET",
            data:{ "userid":userid},
            success:function(res){     
                gid_arr_1 = res.groupid
                gname_arr_1 = res.groupnames
                gstat_1 = res.groupstat
                groupimage_1 = res.groupimage

                //all groups
                $('#application').append('<div id="allgroups">');
                $('#allgroups').append("<h3> All Groups </h3> ");

                for(var j = 0 ; j < gname_arr_1.length ; j++)
                {
                    var group_record_1 = "<div class='per' style='width:300px;height:300px'>";
                    group_record_1 +=  '<img id="imgid" class="public" value="'+gid_arr_1[j]+'" src= "/static'+groupimage_1[j] + '">';
                    group_record_1 += '<p>' + gname_arr_1[j]  + '</p>';
                    group_record_1 += '<button  class="join">Join</button>';
                    group_record_1 +='</div>'
                    $('#allgroups').append(group_record_1);
                }

                $('#application').append('</div>');
            },
            error:function(error,k){
                console.log(error)
                console.log(k)
            }
        });    
    });
    $("#application").on("click",".join",function(){
                gid = $(this).prev().prev().attr('value');
                console.log("group id",gid)
                $.ajax({
                            url:"http://localhost:1111/join",
                            method:"GET",
                            data:{ "userid":userid,"groupid":gid },
                            success:function(res)
                            {     
                                console.log("joined a group ")
                            }
                        });
    })
    $("#application").on("click",".leave",function(){
                gid = $(this).prev().prev().attr('value');
                console.log("group id",gid)
                $.ajax({
                        url:"http://localhost:1111/leave",
                        method:"GET",
                        data:{ "userid":userid,"groupid":gid },
                        success:function(res)
                        {     
                            console.log("leaved a group ")
                        }
                });
    });     
});
