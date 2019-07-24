'use strict';

$(function() {
    // Keep card img aspect ratio to support IE11
    var cardImg = $('.card > .card-img-top');
    cardImg.height(cardImg.width());
    $(window).resize(function() {
        cardImg.height(cardImg.width());
    });

    // Update address hash on results change
    var tar = window.location.hash;
    var recentResultDiv = $('.results_container > div:first-of-type');
    if (!tar || tar == '#results') {
        $(recentResultDiv).show();
    } else if (tar) {
        $(tar).show();
    }

    // Truncate overflow of carousel info p
    var truncArray = $('.race_info p');
    console.log(truncArray);
    truncArray.each(function(i) {
        $clamp(truncArray[i], {clamp: 2});
    });
    
    // on click hide parent; find sibling div of parent and show
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

    // Display requested results
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
