var Global=0;
$(document).ready(function()
		{	
var pagination_count=0;
getMyFeed(pagination_count);



$(window).scroll(function() {

	if($(window).scrollTop()+$(window).height()>$(document).height()-500)	{
	//alert("near bottom");
	
$('.insert').append('<img id="loading" style="margin-left:100px;"src="static/images/loader.gif">');
	getMyFeed(++pagination_count);
}
});


$('.insert').append('<img id="loading" style="margin-left:100px;"src="static/images/loader.gif">');

});

function getMyFeed(no)
{

	var url='/myfeed/';
	var apiKey=$('#dummy').text().trim();
// alert(apiKey);
	url=url+apiKey+'/'+no;

	$.ajax({
        url:url,
        success:function(data){ /*alert(JSON.stringify(data));*/CreateAndInsert(data);},
        error:function(data) {/*alert(JSON.stringify(data));*/ alert("Error loading content. Please refresh the page.");}

		});

}


function followers(link)
{
		var url='/followers/';
	var apiKey=$('#dummy').text();
//alert(apiKey);
	url=url+apiKey

	$.ajax({
        url:url,
        success:function(data){ /*alert(JSON.stringify(data));*/},
        error:function() { alert("Error loading content. Please refresh the page.");}

		});


	$('#myModal2')



}



function CreateAndInsert(data)
{
	if(data['feed'].length==0 && Global==0)
	{
		$('.insert').append('<h3>No tags yet.When you find anything interesting from web tag that content.It get stored here. To start tagging download our chrome extension</h3>');
	}
	else if(data['feed'].length==0 && Global==1)
	{$('#loading').remove();
		//alert("None");
	//	 $('.insert').append("<p>No tags yet.</p><br/><p>All the contents you tag from internet will be available here in My Tags. Download our chrome plugin and start tagging</p>");
	 
	}
	else {
Global=1;
$('#loading').remove();

// alert(data['feed'].length);
for(var i=0;i<data['feed'].length;i++)
{	var img_url=data['feed'][i]['img_url'];
	var text=data['feed'][i]['text'];
	var title=data['feed'][i]['title'];
	var views=data['feed'][i]['views'];
	var url=data['feed'][i]['url'];
	var domain=data['feed'][i]['domain'];
	var id=data['feed'][i]['id'];
	var date=data['feed'][i]['date'];
	
	var _text=text.slice(0,200)+'...';
	if(img_url.trim()=='') img_url='static/images/img_broken.jpg';
	
	Create(img_url, title,_text,url,domain,id,date,views);

}
}
}


$('#myModal').on('hidden.bs.modal', function () {

 
	$('.modal-title').html(''); 
	$('#modal_img').attr('src','');
	// $('.data').html(data['feed'][0]['text']);

	$('.modal-body').empty();
    // do something…
});


function Create(img_url, title,text,url,domain,id,date,views=0)

{
	$('#loading').remove();
	 $('.insert').append(
	 	'<div class="row item top">'+

	 		'<span class="label" style="color:rgba(0,0,0,.8);">'+'Added on '+date+'</span><br/>'+
	 		'<div class="col-md-5 col-sm-5 col-xs-5 left" style="background-image:url('+img_url+'); background-size:cover;"> </div>'+
	 		'<div class="col-md-3 col-md-3 col-xs-3 right">'+
	 		'<span class="label">Story from <a href="'+url+'" ><i>'+domain+'</a></i></span>'+
	 			'<!--<a href="#" data-reveal-id="myModal"><h3>Google Allo  </h3></a>-->'+
'<a href="#myMoal" class="title_main" onclick="display(this); " id='+id+' data-keyboard="true" data-toggle="modal"><h3 class="title" >'+title+'</h3></a>'+

	 			'<p> '+text+'</p>'+

				        		

	 			'<div class="metrics"> <img class="inline" src="static/images/eyes.png" width="20" height="20" / > <p class="inline">'+views+'</p> </div>'+

	 		'</div>'+
	 		
	 		 
	 	
	  '</div> ' );
		 

 


}

