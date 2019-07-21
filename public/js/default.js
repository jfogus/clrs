'use strict';
// on click hide parent
// find sibling div of parent and show
$(function() {
    //- TODO: default race should be the most recent race. May need to change order of divs in results.pug
    var tar = window.location.hash;
    var recentResultDiv = $('.results_container > div:first-of-type');
    if (!tar || tar == '#results') {
        $(recentResultDiv).show();
    } else if (tar) {
        $(tar).show();
    }

    var truncArray = $('.race_info p');
    console.log(truncArray);
    truncArray.each(i => {
        $clamp(truncArray[i], {clamp: 2});
    });
    

    $('.info_button').click(function(e) {
        e.preventDefault();

        var parentDiv = $(e.target).parent().parent();
        
        var speed = 400;
    
        parentDiv.fadeOut({
            duration: speed,
            complete: function() {
                parentDiv.siblings('div').fadeIn(speed);
            }
        });
    });

    $('.result_link').click(function(e) {
        e.preventDefault();
        var tar = $(e.target).attr('href');
        var speed = 400;

        $('.results_container > div:visible').fadeOut({
            duration: speed,
            complete: function() {
                $(tar).fadeIn();
                window.location.hash = tar
            }
        });
    });
});
