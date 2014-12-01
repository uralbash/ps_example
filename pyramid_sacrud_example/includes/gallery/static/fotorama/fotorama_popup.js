$(function () {

    'use strict';

    $(document).on('click', '.fotorama div[class*="fotorama__loaded--img"][class*="fotorama__active"]', function(event) {
        var $popup_content = $('.popup-inner__content'),
            img_src = $(this).children('img').attr('src');
        $popup_content.find('.popup-inner__content-fotorama-image').attr('src', img_src);
        $popup_content.children('div').hide();
        $popup_content.find('.popup-inner__content-fotorama').show();
        $('.popup').css('display', 'table');
        event.stopPropagation();
    });
});
