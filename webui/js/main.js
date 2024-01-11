var all_sounds = {
	"success": new Audio('success.mp3'),
	"error": new Audio('error.mp3'),
	"info": new Audio('info.mp3')
};

function lerp (start, end, amt){
  return (1-amt)*start+amt*end
}
const clamp = (num, min, max) => Math.min(Math.max(num, min), max);


var interestingSentences = [
	"This may take some time",
	"Wait till the end",
	"It's almost done",
	"Something happening"
];

function changeWordsLoading( element ) {
	setTimeout(function() {
		if( !$(element).is(":disabled") )
			return;
		if( !$(element).html().includes("spinner-border-sm") )
			return;

		const random = Math.floor(Math.random() * interestingSentences.length);

		element.html( `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>   ` + interestingSentences[random] + `...` );
		changeWordsLoading( element )
	},5000);
}

$(document).ready( function () {
	$(document).on ("click", "button",function() {
		var callback = $(this).attr("obj");
		var callback_def = $(this).attr("def");
		if( callback && callback_def && !$(this).attr("prev-html") ){
			$(this).prop('disabled', true);
			//if( !$(this).attr("prev-html") )
			//	$(this).attr("prev-html", $(this).html());

			var newText = $(this).html();
			newText = newText.replaceAll("Load", "Loading").replaceAll("Write", "Writing").replaceAll("Process", "Processing");

			//$(this).html( `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ` + newText + "..." );
			var parent = $(this);

			//changeWordsLoading(parent)
			
			var args = [];
			//if( parent.hasClass("need-texture") )
			//	args.push( "texture=" + parent.attr("texture-name") )
			var blackList = ["disabled", "class", "obj", "callback", "def", "prev-html", "role", "value", "id", "aria-labelledby", "style", "src", "href"];
			$.each(this.attributes, function() {
				if(this.specified && !blackList.includes(this.name) ) {
					args.push( this.name + "=" + this.value )
				}
			});

			if(  args.length > 0 )
				args = "?" + args.join('&')
			else
				args = ""

			$.get("/object/" + callback + "/" + callback_def + args, function( data ) {
				//parent.html( data );
				//parent.prop('disabled', true);

				if( parent.hasClass("need-texture") ){
				}
				parent.prop('disabled', false)

				//setTimeout(function() {
				//	parent.prop('disabled', false);
				//	parent.html( parent.attr("prev-html") );
				//	parent.attr("prev-html", "")
				//},3000);

				if( !data.includes("[") )
					return;
				data = JSON.parse(data);

				toastr.options = {
					"closeButton": false,
					"newestOnTop": false,
					"positionClass": "toast-bottom-right",
					"preventDuplicates": false,
					"showDuration": "300",
					"hideDuration": "0",
					"timeOut": "8000",
					"extendedTimeOut": "8000",
					"showEasing": "swing",
					"hideEasing": "linear",
					"showMethod": "slideDown",
					"hideMethod": "slideUp"
				}

				toastr[data[0]]( data[1] );
				all_sounds[data[0]].play();
			});
		}
	});

	setTimeout(function() {
	$("input").map(function() {
		var index = $( "input" ).index( this );
		var value = localStorage.getItem('input-' + index);
		//console.log(value);

		if ( value !== null )
			$(this).val(value);
	});
	},1500);


	$(document).on("keyup", "input",function() {
		//console.log();
		var value = $(this).val();
		var index = $( "input" ).index( this );

		localStorage.setItem('input-' + index, value);
		//console.log("saved " + index + " " + value);
		//if (localStorage.getItem('input-' + index) !== null)
	});

});
