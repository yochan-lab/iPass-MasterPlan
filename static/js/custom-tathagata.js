/*
 * Custom scripts from Tathagata
 * --------------------------------------------------
 */

// document ready 
$(document).ready(function () {

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

            var entry_string = '<a class="dropdown-item" href="#select-[INDEX]">[NAME] ([TYPE])</a>';

            $.each( data , function( index, value ) {

                temp = entry_string.replace('[INDEX]', index);
                temp = temp.replace('[NAME]', value[0]);
                temp = temp.replace('[TYPE]', value[1]);

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
    });

});
