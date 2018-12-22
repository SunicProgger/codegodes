function trailer(link) {
	$('#trailer').show();
	var html = '<div style="width: 964px;height: 544px;position: fixed;left: calc(50% - 480px);top: 70px;z-index: 101;border: 2px solid black;padding: 0;"><iframe width="960" height="540" src="https://www.youtube.com/embed/'+link+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>';
	$('#trailer').html(html);
}

$('#trailer').click(function () {
	$(this).hide();
	$(this).html('');
});