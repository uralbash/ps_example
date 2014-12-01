$(function () {

    'use strict';

    $('.popup').on('click', '.popup-inner__content-link', function (event) {
        $('.popup').hide();
        return event.preventDefault();
    });

    $(document).on('click', function (event) {
        if ($(event.target).closest($('.popup-inner')).length > 0) {
            return event;
        }
        $('.popup').hide();
    });
});
