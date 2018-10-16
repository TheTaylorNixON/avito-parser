$('body').mousemove(function (e) {
    var moveX = (e.pageX * -1/40);
    var moveY = (e.pageY * -1/40);
    $('.bg').css('background-position', moveX + 'px ' + moveY + 'px');
})

var a = window.location.href.split('/')
if(a[a.length-1] == 'viewresults') {
    $('.bg').css({'position':'fixed', 'width':'100%'});
    $('body').unbind('mousemove');
    $('.authorization-button').css({'display':'none'})
}


// --- preloader ---
$('#pushme').on('click', function () {
                                $('.preloader').addClass('active');
                            });


//-------- Ajax ------ viewresults ------------//


$(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() >= $(document).height()) {
        $.get("/viewresultsajax", function (data) {
            if(!data) {
                $(window).unbind('scroll');
            }
            $('tbody').append(data);
        });
    }
});