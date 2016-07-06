 

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
        		//alert(email);
        		followers_insert(name,email);

        	}

        	},
        error:function() { alert("Error loading content. Please refresh the page.");}

		});

 }