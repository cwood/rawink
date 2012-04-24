(function($) {
	
	function loadjs(filename, filetype){
		if (filetype=="js"){ //if filename is a external JavaScript file
			var fileref=document.createElement('script')
			fileref.setAttribute("type","text/javascript")
			fileref.setAttribute("src", filename)
		}
		else if (filetype=="css"){ //if filename is an external CSS file
			var fileref=document.createElement("link")
			fileref.setAttribute("rel", "stylesheet")
			fileref.setAttribute("type", "text/css")
			fileref.setAttribute("href", filename)
		}
		if (typeof fileref!="undefined")
			document.getElementsByTagName("head")[0].appendChild(fileref)
	}
	
	
	/*
loadjs("/static/layout/js/mega-dropdown.js", "js");
	
	if( $('body').hasClass('video-detail') )
		loadjs("/static/layout/js/video-template.js", "js");
*/
	
	
	artistsShown = 0;
	workShown = 0;
	userShown = 0;

	$('.artists')
		.live('pageshow', function(e){
		if(artistsShown == 0) {
			artistsShown = 1;
			$('article figure').live('click', function(){
			
				var li = $(this).parent();
				var others = li.siblings();
				var section = $(this).siblings('section');
			
				li.toggleClass('open').siblings().removeClass('open');
				section.toggle()
				others.find('section').hide();
			
				if( section.is(':visible') ) {
					others.addClass('fade');
					li.removeClass('fade');
				} else {
					others.removeClass('fade');
				}
			});
		}
	});

	$('.work')
		.live('pageshow', function(e){
			$('.work article ul')
				.cycle({
					fx:     'scrollHorz',
					speed: '1000',
				    timeout: 0,
				    next:   '#next', 
				    prev:   '#prev'
				})
				.swipeleft(function(event, ui){
					$('#next').click();
				})
				.swiperight(function(event, ui){
					$('#prev').click();
				});
				
			$('.message a').click(function(e){
				e.preventDefault();
				$(this).parent().hide();
				$(this).parent().siblings('.overlay').hide();
			});
	});
	
	$('.user')
		.live('pageshow', function(e){
		if(userShown == 0){
			userShown = 1;
			$('#intro a, .back').live('click',function(event){
				event.preventDefault();
				var selector = $(this).attr('href');
				var tgt = $( selector );
				var intro = $('#intro');
				intro.closest('.content').fadeOut(300, function(){
					tgt.fadeIn();
					if( selector == '#intro' ) $('#signup').fadeOut();
				})
			});
			
			$('input[type=checkbox]').live('click', function(){
				if($(this).is(':checked')) {
					$(this).closest('.ui-checkbox').siblings('.toggle').slideDown();
				} else {
					$(this).closest('.ui-checkbox').siblings('.toggle').slideUp();
				}
			});
			
			$('input[name=payment_type]').change(function(){
				alert('poop');
				if( $('#id_payment_type_0:checked') ) $('#id_payment_rate').val('120')
			});
		}
	});
	
	$('.customer')
		.live('pageshow', function(e){
			
			$('input[name=payment_type]').change(function(){
				if( $('#id_payment_type_0:checked') ) $('#id_payment_rate').val('120')
			});
			
			refreshPage = function(){
				// $('#appointments form').submit();
				var form = document.createElement('form');
				form.method = 'post';
		        form.action = './';
		        document.body.appendChild(form);
		        form.submit();
			}
			
			$('.start a, .stop a').click(function(event){
				event.preventDefault();
				var tgt = $(this).attr('href');
				$('#ajax').load( tgt, refreshPage );
			});
		});
		
	
	function chbx() {
		var input = $('input[type=checkbox]').wrap('<div class="chbx" />');
		input.change(function(i){
			el = $(i.target);
			el.parent().attr('data-checkbox', el.prop('checked'));
		});
	}
	
	chbx();
	

}(window.jQuery));


