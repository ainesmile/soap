$( document ).ready(function() {
    function toggleBarMeun() {
        if (document.documentElement.clientWidth >= 600) {
            $('#menu').addClass('show');
        } else {
            $('#menu').removeClass('show');
        }
    }
    toggleBarMeun();
    $(window).resize(function() {
        toggleBarMeun();
    });
});






