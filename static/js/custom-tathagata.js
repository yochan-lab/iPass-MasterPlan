/*
 * Custom scripts from Tathagata
 * --------------------------------------------------
 */

// document ready 
$(document).ready(function () {

    // hide feedback panel and alert on submit on load 
    $("#feedback").hide();
    $("#valAlert").hide();

    // gridstack not resizable

    $('.grid-stack').gridstack({
        resizable: {
            handles: ''
        }
    });

    // disable add buttons to begin with unless something is selected
    // $( ".addButton" ).prop("disabled", true);

    // method :: initialize student info from state JSON
    $.ajax({
        url: "static/files/state.json",
        dataType: "json",
        success: function(data) {

            $( '#specialization' ).find('.badge').html(data.specialization);

            if ( data["international"] == 'no' ) {
                $( '#international' ).find('.fas').addClass('fa-times');
            } else {
                $( '#international' ).find('.fas').addClass('fa-check');
            }

            if ( data["ra/ta"] == 'no' ) {
                $( '#rata' ).find('.fas').addClass('fa-times');
            } else {
                $( '#rata' ).find('.fas').addClass('fa-check');
            }

            $.each( data.deficiency , function( index, value ) {
                if ( value == 'no' ) {
                    $( '#' + index ).find('.fas').addClass('fa-times');
                } else {
                    $( '#' + index ).find('.fas').addClass('fa-check');
                }
            });
        }
    });


    // populate course dropdown options on document load from courses

    $.ajax({
        url: "static/files/courses.json",
        dataType: "json",
        success: function(data) {

            var entry_string = '<a class="dropdown-item" href="#select-[INDEX]">[NAME] ([TYPE])</a>';

            $.each( data , function( index, value ) {

                temp = entry_string.replace('[INDEX]', index);
                temp = temp.replace('[NAME]', value[0]);
                temp = temp.replace('[TYPE]', value[1]);

                $( "#courseList" ).siblings( ".dropdown-menu" ).append( temp );

            });
        }
    });

    // populate course dropdown options on document load from courses

    $.ajax({
        url: "static/files/committee.json",
        dataType: "json",
        success: function(data) {

            var entry_string = '<a class="dropdown-item" href="#select-[INDEX]">[NAME] (Specialization: [TYPE])</a>';

            $.each( data , function( index, value ) {

                temp = entry_string.replace('[INDEX]', index);
                temp = temp.replace('[NAME]', value[0]);
                temp = temp.replace('[TYPE]', value[1].replace('_', ' '));

                $( "#chairList" ).siblings( ".dropdown-menu" ).append( temp );
                $( "#committeeList" ).siblings( ".dropdown-menu" ).append( temp );

            });
        }
    });


    // method :: re-focus
    $('.spy-enabled').click( function(){
        $('html,body').animate({scrollTop: $($(this).attr('href')).offset().top - 60}, 'slow');
    });

    // method :: set selected option as active dropdown item
    $(document).on( "click", ".dropdown-item", function() {
        $(this).parent().siblings( ".dropdown-toggle" ).html( $(this).html() );
        $(this).parent().find( ".addButton" ).prop("disabled", false);
    });


    // method :: manage time 

    // start logging time
    var update_flag = true;
    var time_limit = 1;

    var startTime = new Date().getTime();
    var endTime   = new Date().getTime() + time_limit * 1000000;

    var clock = setInterval(function() {

        // Get todays date and time
        var now = new Date().getTime();

        // Find the distance between now an the count down date
        var interval = endTime - now;

        // Time calculations for days, hours, minutes and seconds
        var minutes = Math.floor((interval % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((interval % (1000 * 60)) / 1000);

        if (update_flag) {

            // Display the result in the element with id "countdown"
            $("#countdown").html( minutes + "m " + seconds + "s" )

            // If the count down is finished transition to feedback
            if (interval < 0) {

                $("#countdown").html("EXPIRED");

                $("#countdown").removeClass("badge-secondary");
                $("#countdown").addClass("badge-danger");

                $("#info").addClass("fade-to-back");
                $("#info *").attr("disabled", "disabled").off('click');

                $("#plan-utils").addClass("fade-to-back");
                $("#plan-utils *").attr("disabled", "disabled").off('click');

                $("#add2plan").hide();
                $("#feedback").show();

                $('html, body').animate({
                    scrollTop: $("#feedback").offset().top
                }, 2000);

                update_flag = false;

            }

        }

    }, 1000);


});
