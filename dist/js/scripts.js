//The below function opens and fills the location info pop-up (modal) with data for each location
function openModal() { 
	$("area").each(function(i){ 
		$(this).click(function(e){
			e.preventDefault();
			$("#modal").hide();
			var id = $(this).attr("id"); 
			$.ajax({
			  	url: "data/dataExample.json?id="+id,	//Needs to be replaced with server url so that server knows to get data pertaining to the given location's id. Currently takes data from dummy data
			  	dataType:"json"
			}).done(function(data) { //fills the modal with the location's data from database
				$("#modal .title h2, #modal div.score, #modal p.description, #modal ul.comments").html("");
				$("#modal .title h2").html(data.placeName);
				$("#modal div.score").html("Average Score: "+data.score.average);
				$("#modal p.description").html(data.placeDescription);
				$("#modal button.openform").attr("data-id",id); 	//the button operates the openform function which takes a location id as a parameter, so we pass the appropriate id in here
				data.opinions.forEach(function(opinion){
					$("#modal ul.comments").append('<li><p>'+opinion.comments+'</p><p class="signature">'+opinion.userName+'</p></li>') //format how the specific part to each comment are displayed with the appropriate data
				});
				$("#modal").show(100);
				openForm(data);
			}).fail(function(xhr){
				console.log(xhr.responseText);
			});
		});
	});
}

function closeModal() {
	$("#modal .close").click(function(e){
		e.preventDefault();
		$("#modal").hide(100);
	});
}

function openForm(data) {
	$("#modal button.openform").click(function(){
		$("#modal").css({"top":"0.3%"})
		$("#modal .info").hide();
		$("#modal form h2 span").html(data.placeName);
		$("#modal form input[name='id']").val(data.id);
		$("#modal form").show();
	});
}

function myfunct(){
	console.log("submitted");
	var noiserating = document.getElementById("noise1").value;
	var lightrating = document.getElementById("light1").value;
	var smellrating = document.getElementById("smells1").value;
	console.log(noiserating);
	console.log(lightrating);
	console.log(smellrating);
	$.ajax({
		url: "data/dataExample.json?noise=3&light=2&smells="+4,	//Needs to be replaced with server url so that server knows to get data pertaining to the given location's id. Currently takes data from dummy data
		dataType:"json"
	}).done(function(data){
		console.log(data.placeName);
		var test =document.getElementById("txtHint");
		var para = document.createElement("BUTTON");
		para.setAttribute("onclick","displaydata(this)");
		para.setAttribute("id",data.id);
		console.log($(para).attr("id"));
		var node = document.createTextNode(data.placeName);
		para.appendChild(node);
		test.appendChild(para);
	});
}

function displaydata(btn){
	var answer;
	var id = btn.getAttribute('id');
	console.log(id);
	$.ajax({
		url: "data/dataExample.json?id="+id,	//Needs to be replaced with server url so that server knows to get data pertaining to the given location's id. Currently takes data from dummy data
		dataType:"json"
	}).done(function(data){
		console.log(data.placeName);
		var item = document.getElementById("content");
		
		var nameplace =document.createElement("H1");
		var text =document.createTextNode(data.placeName);
		nameplace.appendChild(text);
		item.appendChild(nameplace);
		if(data.score.people <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Are there usually a lot of people in this space? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.movement <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Are people moving chaotically? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.talking <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Are people talking a lot? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.noise <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Is there a lot of background noise? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.light <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Is there a lot of light? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.lightBright <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Is the light bright? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.lightFlickering <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Is the light flickering? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.lightColourPeculiar <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Is the light colour peculiar? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.smells <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Are there strong smells? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.floorSticky <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Is the floor sticky? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.floorUneven <=2){
			answer ="no";
		}else{
			answer="yes";
		}
		text = document.createTextNode("Is the floor uneven? \t" +answer+"\n");
		item.appendChild(text);
		if(data.score.seatsHard <=3){
			answer ="soft";
		}else{
			answer="hard";
		}
		text = document.createTextNode("Are the seats hard/soft? " +answer+"\n");
		item.appendChild(text);
		if(data.score.seatsHard <=3){
			answer ="smooth";
		}else{
			answer="rough";
		}
		text = document.createTextNode("Are the textures smooth/rough? \t" +answer+"\n");
		item.appendChild(text);
	});
}
openModal();
closeModal();
