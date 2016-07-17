$(document).ready(function()
		{	

getFeed(0);




});


function getFeed(no)
{
	var url='/feed/';
	var apiKey=$('#dummy').text().trim();
//alert(apiKey);
	url=url+apiKey+'/'+no

	$.ajax({
        url:url,
        success:function(data){ alert(JSON.stringify(data));createAndInsert(data);},
        error:function(data) {alert("error:"+JSON.stringify(data)); alert("Error loading content. Please refresh the page.");}

		});


}


function createAndInsert(data)
{
	if(data['feed'].length==0) {intro_insert(0);}

		else {


// alert(data['feed'].length);
for(var i=0;i<data['feed'].length;i++)
  {
	var img_url=data['feed'][i]['right']['img_url'];
	var text=data['feed'][i]['right']['text'];
	var title=data['feed'][i]['right']['title'];
	var views=data['feed'][i]['right']['views'];
	var url=data['feed'][i]['right']['url'];
	var domain=data['feed'][i]['right']['domain'];
	var id=data['feed'][i]['right']['id'];
	var name=data['feed'][i]['right']['user-name'];
		
	var Text=text.slice(0,200)+'...';
	if (img_url.trim()=='') img_url='static/images/img_broken.jpg';
	create(img_url,title,Text,url,domain,name,id,views);

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


function create(img_url,title,text,url,domain,name,id,views)
{//alert(img_url);
	 $('.insert').append(
	 	'<div class="row item top">'+
	 		'<span class="label" style="color:rgba(0,0,0,.8);">Tagged by '+name+'</span><br/>'+
	 		'<div class="col-md-5 col-sm-5 col-xs-5 left" style="background-image:url('+img_url+'); background-size:cover;"> </div>'+
	 		'<div class="col-md-3 col-sm-3 col-xs-3 right">'+
	 		'<span class="label">Story from <a href="'+url+'" ><i>'+domain+'</a></i></span>'+
	 			'<!--<a href="#" data-reveal-id="myModal"><h3>Google Allo  </h3></a>-->'+
'<a href="#myMoal" class="title_main" onclick="display(this); " id='+id+' data-toggle="modal"><h3 class="title" >'+title+'</h3></a>'+

	 			'<p> '+text+'</p>'+

				        		

	 			'<div class="metrics"> <img class="inline" src="static/images/eyes.png" width="20" height="20" / > <p class="inline">'+views+'</p> </div>'+


	 		'</div>'+
	 		
	 		 
	 	
	  '</div> ' );
		 

 


}



function intro_insert(val)
{
	var done0=0,done1=0,done2=0;
	if (val==0 && done0==0){
	$('.insert').prepend(
	 	'<div class="row item top">'+
 	'<div class="col-md-5 col-sm-5 col-xs-5 left" style="background-image:url(static/images/follow.jpg); background-size:cover;"> </div>'+
	 		 '<div class="col-md-3 col-sm-3 col-xs-3  right">'+
	 		 
	 			'<!--<a href="#" data-reveal-id="myModal"><h3>Google Allo  </h3></a>-->'+
'<h3 class="title" >Welcome to Taggem</h3>'+

	 			'<p style="font-style:bold;">'+'Taggem lets you find the best things from web that interests you ,'+
	 			'through suggestions and recommendation  from your friends.You can follow anyone in taggem and '+
	 			'find those contents that excites you most from the ocean of information i.e internet.</p>'+
	 			'<a id="learn" href="#" onclick=" intro_insert(1);" >Learn how to use Taggem  </a>'+

			 
	 		'</div>'+ 	 		 
	 	
	  '</div> ' );

	}
	else if(val==1 && done1==0)
	{


		$('.insert').prepend(
	 	'<div class="row item top">'+
 	'<div class="col-md-5 col-sm-5 col-xs-5  left" style="background-image:url(static/images/bg2.png); background-size:cover;"> </div>'+
	 		 '<div class="col-md-3 col-sm-3 col-xs-3 right">'+
	 		 
	 			'<!--<a href="#" data-reveal-id="myModal"><h3>Google Allo  </h3></a>-->'+
'<h3 class="title" >Connect</h3>'+

	 			'<p style="font-style:bold;"> Connect and follow your friends.Get everything that they tag from web.You can also follow the best rated taggers in Taggem.</p><a id="learn" href="#" onclick="intro_insert(2);">Learn how to Tag </a>'+

				 
	 		'</div>'+
	 		
	 		 
	 	
	  '</div> ' );	
	

	}

	else if(val==2 )
	{


		$('.insert').prepend(
	 	'<div class="row item top">'+
 	'<div class="col-md-5 col-sm-5 col-xs-5  left" style="background-image:url(static/images/bg3.png); background-size:cover;"> </div>'+
	 		 '<div class="col-md-3 col-sm-3 col-xs-3 right">'+
	 		 
	 			'<!--<a href="#" data-reveal-id="myModal"><h3>Google Allo  </h3></a>-->'+
'<h3 class="title" >Taggem</h3>'+

	 			'<p style="font-style:bold;"> Whenever you find something interesting in web,share to your followers by just a press on Taggem chrome extension <a id="learn" href="https://drive.google.com/file/d/0By8yos6-tmUZa0t5aTAwZXhud1U/view?usp=sharing" >Download chrome extension</a></p>'+

				 '<h3>HAPPY TAGGING</h3>'+
	 		'</div>'+
	 		
	 		 
	 	
	  '</div> ' );	done2=1;


	}



}
