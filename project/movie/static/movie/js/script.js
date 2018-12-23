$(document).ready(function() {
	$('#search-input').on("input", function() {
		var poisk = $(this).val().toLowerCase();
		if (poisk.length > 0) {
			$('.film-block').each(function() {
				var film = $(this);var k = 0;
				film.find('span').each(function() {
					var name = $(this).text();
					var i = name.toLowerCase().indexOf(poisk);
					if (i + 1) {
						var up = name.substr(i, poisk.length);
						var span = '<span style="background: darkorange;color: black">' + up + '</span>';
						var rename = name.replace(up, span);
						$(this).html(rename);
						k += 1;
					} else {
						$(this).find('span').each(function() {						
							$(this).css('background', 'rgba(0,0,0,0)');
							$(this).css('color', 'white');
						})
					}
				});
				if (k == 0) {
					film.hide();
				} else {
					film.show();
				}
			});
		} else {
			$('.film-block').each(function() {
				var film = $(this);
				film.find('span').each(function() {
					$(this).css('background', 'rgba(0,0,0,0)');
					$(this).css('color', 'white');
				});
				$(this).show();
			});
		}
	});
});

function trailer(link) {
	$('#trailer').show();
	var html = '<div style="width: 964px;height: 544px;position: fixed;left: calc(50% - 480px);top: 70px;z-index: 101;border: 2px solid black;padding: 0;"><iframe width="960" height="540" src="https://www.youtube.com/embed/'+link+'" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>';
	$('#trailer').html(html);
}

$('#trailer').click(function () {
	$(this).hide();
	$(this).html('');
});

$('#open-auth').click(function () {
	// $('#auth-block').show();
	$('#auth-block').slideDown(20);
});

function auth() {
	window.scrollTo(0, 0);
	$('#auth-block').slideDown(20);
}

$('#register-link').click(function() {
	$('#auth-block').hide();
	$('#registration-block').show();
});

$('#auth-link').click(function() {
	$('#registration-block').hide();
	$('#auth-block').show();
});