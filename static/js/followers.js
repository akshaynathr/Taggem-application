 

function followers(link)
{
		var url='/followers/';
	var apiKey=$('#dummy').text();
// alert(apiKey);
	url=url+apiKey

	$.ajax({
        url:url,
        success:function(data){ //alert(JSON.stringify(data));
        	 
        	for(var i=0;i<data['followers'].length;i++)
        	{	 
        		name=data['followers'][i]['name'];
        		email=data['followers'][i]['email'];
        		img=data['followers'][i]['img'];
        		//alert(email);
        		followers_insert(name,email,img);

        	}

        	},
        error:function() { alert("Error loading content. Please refresh the page.");}

		});






}


function followers_insert(name,email,img)
{
	$('.mm').prepend('<div class="row block" style="border-top:1px rgba(255,255,255,.6) solid;color:#fff; text-align:center;padding:10px;">'+
		'<img src="/static/uploads/'+img+'"   style="width:100px; height:100px;"/>'+'<h4  >'+name+ '</h4>'+'<h5 class="inline"> Email:'+email+' </h5>'+ '<button class="btn btn-danger inline">Unfollow</button>'+

     '</div>'  	 );
}




$('#myModal2').on('hidden.bs.modal', function () { $('.mm').empty();} );
