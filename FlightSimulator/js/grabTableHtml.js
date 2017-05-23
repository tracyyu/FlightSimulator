function GetCurrentLatLng() {

	$.ajax({
		url: "../tableData/adbpTable.html",
		cache: false
	})
	.done(function( data ) 
	{
		if(data != "") {
			$( "#ADBPtable" ).html( data );
		}
	});

}

$(document).ready(function(){

	// poll latest points
	setInterval(GetCurrentLatLng,1000);

	GetCurrentLatLng();
}); 
