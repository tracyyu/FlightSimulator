var stopTime;
var audio = new Audio('../alert.ogg');

function isEmpty(str) {
    return (!str || 0 === str.length);
}

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}

function getErrorMessage()
{
	$.ajax({
		url: "/errorData/errorMessage.html",
		cache: false
	})
	.done(function( data ) 
	{
		if(isEmpty(data) || isBlank(data)) {	
			$('.panel-danger').hide("normal");
			audio.pause();
		}
		else {
			$('#error-data').html(data);
			$('.panel-danger').show("normal");
			audio.play();
		}	
	})
	.fail(function() {
		$('.panel-danger').hide("normal");
		audio.pause();
	});

}

$(document).ready(function(){

	setInterval(getErrorMessage,3000);
	getErrorMessage();
}); 
