/*
 * Custom scripts from Tathagata
 * --------------------------------------------------
 */

// document ready 
$(document).ready(function () {

    // hide feedback panel and alert on submit on load 
    $("#feedback").hide();
    $("#submit").hide();

    $("#valAlertPositive").hide();
    $("#valAlertNegative").hide();

    // gridstack not resizable

    $('.grid-stack').gridstack({
        resizable: {
            handles: ''
        }
    });

    // disable add buttons to begin with unless something is selected
    $( ".addButton" ).prop("disabled", true);
    $( ".addButton" ).addClass( "disabled-button" );

    // method :: initialize student info from state JSON
    $.ajax({
        url: "static/files/state.json",
        dataType: "json",
        success: function(data) {

            $( '#specialization' ).find('.badge').html(data.specialization);

            if ( data["international"] == 'no' ) {
                $( '#international' ).find('.fas').removeClass('fa-check');
                $( '#international' ).find('.fas').addClass('fa-times');
            } else {
                $( '#international' ).find('.fas').removeClass('fa-times');
                $( '#international' ).find('.fas').addClass('fa-check');
            }

            if ( data["ra/ta"] == 'no' ) {
                $( '#rata' ).find('.fas').removeClass('fa-check');
                $( '#rata' ).find('.fas').addClass('fa-times');
            } else {
                $( '#rata' ).find('.fas').removeClass('fa-times');
                $( '#rata' ).find('.fas').addClass('fa-check');
            }

            $.each( data.deficiency , function( index, value ) {
                if ( value === "no" ) {
                    $( '#' + index ).find('.fas').removeClass('fa-check');
                    $( '#' + index ).find('.fas').addClass('fa-times');
                } else {
                    $( '#' + index ).find('.fas').removeClass('fa-times');
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

            var entry_string = '<a class="dropdown-item" href="#select-[INDEX]">[[INDEX]] [NAME] ([TYPE])</a>';

            $.each( data , function( index, value ) {

                temp = entry_string.replace('[INDEX]', index).replace('[INDEX]', index);
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
    $( ".spy-enabled" ).click( function() {
        $( "html,body" ).animate({scrollTop: $($(this).attr('href')).offset().top - 60}, 'slow');
    });

    // method :: set selected option as active dropdown item
    $(document).on( "click", ".dropdown-item", function() {
        $(this).parent().siblings( ".dropdown-toggle" ).html( $(this).html() );
        $(this).parent().parent().parent().find( ".addButton" ).prop("disabled", false);
        $(this).parent().parent().parent().find( ".addButton" ).removeClass( "disabled-button" );
        $(this).parent().parent().parent().find( ".addButton" ).removeClass( "btn-outline-success" );
        $(this).parent().parent().parent().find( ".addButton" ).addClass( "btn-success" );
    });


    // method :: sanity check on final submit 
    $( "#submitFinal" ).click( function() { 

        var success = true;

        $( "#feedback .form-control" ).each( function( index ) {

            if ( !$(this).val().trim() && !$(this).hasClass( "optional" ) ) {

                success = false;
                return false;

            } 

        });

        var count = 0;
        
        $( ".likert .list-group-item" ).each( function( index ) {

            if ( $(this).hasClass( "active" ) ) {

                count++;
                JSONlog["Q"+count] = $(this).html().trim();

            }

        });

        if ( count < 5 ) {
            success = false;            
        }

        if ( $( "#youare" ).html().trim() == 'Click to Select' ) {
            success = false;            
        }

        if (success) {

            var now = new Date().getTime();
            JSONlog["time"] += now - startTime;
            JSONlog["which-class"] = $( "#youare" ).html().trim();
            JSONlog["which-department"] = $( "#which-department" ).val().trim();

            JSONlog["yes-feedback"] = $( "#yes-feedback" ).val().trim();
            JSONlog["no-feedback"] = $( "#no-feedback" ).val().trim();
            JSONlog["mange-more-feedback"] = $( "#mange-more-feedback" ).val().trim();
            JSONlog["other-feedback"] = $( "#other-feedback" ).val().trim();
            console.log(JSONlog);
  
            var finalIPOS = new Array();
            $( ".grid-stack-item-content .display-action-name" ).each( function() {
                finalIPOS.push( $( this ).html().trim() )
            });

            JSONlog["final-IPOS"] = finalIPOS;

            console.log(JSONlog);

            $.ajax({
                type: 'POST',
                url: 'logs/',
                data: JSON.stringify(JSONlog),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data) {
                    $( "body" ).html( '<div class="container align-midmiddle end "><i class="fas fa-check-circle fa-10x text-success"></i></div>' );
                }
            });
            logStorage.setItem("reset", true);

        } else {

             $( "#completeCheck" ).removeClass( "alert-secondary" );
             $( "#completeCheck" ).addClass( "alert-danger" );
        }


    });

    // method :: manage time, moeny and diffiuclty

    var course_cost = 3500;
    var semester_cost = 2000;

    var num_courses = 0;
    var num_semesters = 0;

    // start logging time
    var update_flag = true;
    var time_limit = 1.5;

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

        if( $("#feedback").css('display') == 'block') {
            update_flag = false;
        }

        if (update_flag) {

            num_courses = 0;
            num_semesters = 0;

            $( ".grid-stack-item-content .form-control" ).each( function( index ) {

                if ( $(this).html().indexOf("Semester") != -1 || $(this).html().indexOf("Defense") != -1 ) {
                    num_semesters++;
                }

                if ( $(this).html().indexOf("Add Course") != -1 ) {
                    num_courses++;
                }

            });

            // money 
            cost = course_cost * num_courses + semester_cost * num_semesters;
            $( "#money" ).html( "$" +  cost );

            // difficulty 
            if ( num_semesters == 0) {
                $( "#difficulty" ).html( num_courses );
            } else {
                $( "#difficulty" ).html( ( num_courses / num_semesters ).toFixed(2) );
            }

            // Display the result in the element with id "countdown"
            $("#countdown").html( minutes + "m " + seconds + "s" )

            // If the count down is finished transition to feedback
            if (interval < 0) {

                $("#countdown").html("EXPIRED");

                $("#countdown").removeClass("badge-secondary");
                $("#countdown").addClass("badge-danger");

                $( ".grid-stack" ).removeClass( "grid-stack" );

                $( ".delete-action" ).each( function( index ) {
                    $(this).parent().remove();
                });

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

    // methods for loggings

    var JSONlog = {
        "num_rearranges" : 0,
        "num_deletes" : 0,
        "num_rearranges_of_suggestions" : 0,
        "num_deletes_of_suggestions" : 0,
        "num_add" : 0,
        "num_val" : 0,
        "num_suggest" : 0,
        "num_explain" : 0,
        "num_checked" : 0,
        "time": 0
    };

    // method for saving logs across sessions
    var logStorage = window.localStorage;

    // initialize values of keys for logStorage
    var updateStorageCount = function(log){
        var value = $("#session_id").val();
        var keys = Object.keys(log);
        for(var i = 0; i < keys.length; i++){
            var key = keys[i];
            logStorage.setItem(key, log[key]);
        }
        // setting up the logstorage session for checking the value
        logStorage.setItem("session", value);
    };

    // update the value of logs from logStorage
    var updateLocalCount = function(log){
        var keys = Object.keys(log);
        for(var i = 0; i < keys.length; i++){
            var key = keys[i];
            log[key] = parseInt(logStorage.getItem(key));
        }

        return log;
    };

    // method to decide whether to update or reset the logStorage when the page loads
    var updateCount = function(){
        var session_id = $("#session_id").val();
        if(logStorage.getItem("session") == session_id)
            updateLocalCount(JSONlog);
        else
            updateStorageCount(JSONlog);
    };

    $(document).on('click', '.addButton', function(event) {
        JSONlog["num_add"]++; 
    });

    $(document).on('click', '.delete-action', function(event) {

        JSONlog["num_deletes"]++; 

        if ( $(this).find('.form-control').hasClass('text-success') ) {
            JSONlog["num_deletes_of_suggestions"]++; 
        }

    });

    var drag_flag = false;

    $(document).on('mousedown', '.grid-stack-item', function(event) {
        drag_flag = false;
    });

    $(document).on('mousemove', '.grid-stack-item', function(event) {
        drag_flag = true;
    });

    $(document).on('mouseup', '.grid-stack-item', function(event) {

        if( drag_flag ) {

            JSONlog["num_rearranges"]++; 
            if ( $(this).find('.form-control').hasClass('text-success') ) {
                JSONlog["num_rearranges_of_suggestions"]++; 
            }
            console.log("666", JSONlog["num_rearranges"]);

        }

    });

    $('#validatePlan').click( function() {
        JSONlog["num_val"]++; 
    });

    $('#suggestPlan').click( function() {
        JSONlog["num_suggest"]++; 
    });

    $('#explainPlan').click( function() {
        JSONlog["num_explain"]++; 
    });

    $('#check').click( function() {
        JSONlog["num_checked"]++; 
    });

    // storing the json log values to storage before page unloads.
    window.onbeforeunload = function() {
        var now = new Date().getTime();
        JSONlog["time"] += (now - startTime);
        updateStorageCount(JSONlog);
    };

    // setup storage called as soon as page loads
    updateCount(JSONlog);

});
