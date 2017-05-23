$("#startBtn").click(function() {
  $.ajax({
      type: "POST",
  		url:"/cgi-bin/startServer.cgi",
  		cache: false,
      dataType: "html",
  		error: function(result) {
  			$('.panel-body').html(result);
			  $('.panel-danger').show("normal");
  		}
  	});

    $('#info-data').html("Server Started");
    $('.panel-info').show("fast").delay(3000).queue(function(n) {
      $(this).hide("fast"); n();
    });

}); 


$("#stopBtn").click(function(){
  $.ajax({
      type: "POST",
      url:"/cgi-bin/stopServer.cgi",
      cache: false,
      error: function(result) {
        $('.panel-body').html(result);
        $('.panel-danger').show("normal");
      }
    });

    $('#info-data').html("Server Stopped");
    $('.panel-info').show("fast").delay(3000).queue(function(n) {
      $(this).hide("fast"); n();
    });
}); 

function GetServerStatus() {

  $.ajax({
    url: "/cgi-bin/checkRunning.cgi",
    cache: false
  })
  .done(function( data ) 
  {
    if(data != "") {
      $( "#server-status" ).html( data );
    }
  });

}

$(document).ready(function(){

  // poll latest points
  setInterval(GetServerStatus,1000);

  GetServerStatus();
}); 
