

 $("#search").keyup(function (e) {
            if (e.keyCode == 13) {
                // Do something wjen enter key is pressed


                var apiKey=$('#dummy').text();
                var url='/search/'+apiKey
                var key=$('#search').val();

	if (key.trim()!='')
	{
		var data={ 'key':key}

		$.ajax({
			type:'POST' ,
			url:url,

			dataType:'json',
			data:JSON.stringify(data),
			success:function(data){ alert(JSON.stringify(data));  $('.insert').empty(); createAndInsertSearchFeed(data);},
			error:function(data){ alert(JSON.stringify(data));},
			contentType:'application/json'

		});



	}

	else { /*alert("No value");}*/
            }
       

}


        });







function createAndInsertSearchFeed(data)
{
	if(data['feed'].length==0) {  /* alert("Hello. add some friends to get the feed ");*/ }

		else  {


// alert(data['feed'].length);
for(var i=0;i<data['feed'].length;i++)
  { var img_url=data['feed'][i]['img_url'];
	var text=data['feed'][i]['text'];
	var title=data['feed'][i]['title'];
	var views=data['feed'][i]['views'];
	var url=data['feed'][i]['url'];
	var domain=data['feed'][i]['domain'];
	var id=data['feed'][i]['id'];
	var _text=text.slice(0,200)+'...';
	//_text=text;
	if(img_url.trim()=='') img_url='static/images/img_broken.jpg';
	createSearchResult(img_url, title,_text,url,domain,id,views);

	}
		}
}



function createSearchResult(img_url, title,text,url,domain,id,views=0)

{
	 $('.insert').append(
	 	'<div class="row item top">'+

	 		 
	 		'<div class="col-md-5 left" style="background-image:url('+img_url+'); background-size:cover;"> </div>'+
	 		'<div class="col-md-3 right">'+
	 		'<span class="label">Story from <a href="'+url+'" ><i>'+domain+'</a></i></span>'+
	 			'<!--<a href="#" data-reveal-id="myModal"><h3>Google Allo  </h3></a>-->'+
'<a href="#myMoal" class="title_main" onclick="display(this); " id='+id+' data-toggle="modal"><h3 class="title" >'+title+'</h3></a>'+

	 			'<p> '+text+'</p>'+

				        		

	 			'<div class="metrics"> <img class="inline" src="static/images/eyes.png" width="20" height="20" / > <p class="inline">'+views+'</p> </div>'+

	 		'</div>'+
	 		
	 		 
	 	
	  '</div> ' );
		 



}
