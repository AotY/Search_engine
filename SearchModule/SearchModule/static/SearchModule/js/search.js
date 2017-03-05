$(document).on('ready', function () {

    $('.field').on('focus', function () {
        $('body').addClass('is-focus');
    });

    $('.field').on('blur', function () {
        $('body').removeClass('is-focus is-type');
    });


    $('.field').on('keydown', function (event) {
        console.log(" --- keydown --- " + event.which);
        $('body').addClass('is-type');
        if ((event.which === 8) && $(this).val() === '') {
            $('body').removeClass('is-type');
        } else if ((event.which === 13)) {
            console.log($(".field").val());
            //与服务器进行交互
            var query = $(".field").val();
            var from = 0;
            var size = 10;

            if(query.trim() != '')
                $(location).attr('href', '/search_result?query=' + query + "&from=" + from + "&size=" + size);
        }

    });


});