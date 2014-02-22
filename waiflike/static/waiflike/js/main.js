$(document).ready(function(){
    //Apply img-thumbnail class to body-content images
    $('.body-content img').addClass("img-thumbnail");

    $(document).delegate('*[data-toggle="lightbox"]', 'click',
        function(event) {
            event.preventDefault();
            $(this).ekkoLightbox();
        });
});
