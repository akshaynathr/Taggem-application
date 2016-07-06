$(document).ready(function()
		{	
	var url='/feed/';
	var apiKey=$('#dummy').text();
//alert(apiKey);
	url=url+apiKey

	$.ajax({
        url:url,
        success:function(data){ /*alert(JSON.stringify(data));*/createAndInsert(data);},
        error:function() { alert("Error loading content. Please refresh the page.");}

		});








});



function createAndInsert(data)
{
// alert(data['feed'].length);
for(var i=0;i<data['feed'].length;i++)
{	var img_url=data['feed'][i]['right']['img_url'];
	var text=data['feed'][i]['right']['text'];
	var title=data['feed'][i]['right']['title'];
	var views=data['feed'][i]['right']['views'];
	var url=data['feed'][i]['right']['url'];
	var domain=data['feed'][i]['right']['domain'];
	var id=data['feed'][i]['right']['id'];
	
	var _text=text.slice(0,200)+'...';
	create(img_url, title,_text,url,domain,id,views);

}
}


$('#myModal').on('hidden.bs.modal', function () {

 
	$('.modal-title').html(''); 
	$('#modal_img').attr('src','');
	// $('.data').html(data['feed'][0]['text']);

	$('.modal-body').empty();
    // do something…
});


function create(img_url, title,text,url,domain,id,views=0)

{
	 $('.insert').prepend(
	 	'<div class="row item top">'+

	 		'<span class="label" style="color:rgba(0,0,0,.8);">Recommended by'+'Anand'+'</span><br/>'+
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
