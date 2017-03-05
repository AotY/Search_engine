$(document).on('ready', function () {


    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };

    var query = getUrlParameter('query');
    var from = Number(getUrlParameter('from'));
    var size = Number(getUrlParameter('size'));

    if (!from || !size) {
        from = 0;
        size = 10;
    }
    $.ajax({
        type: "GET",
        data: {
            'query': query,
            'from': from,
            'size': size
        },
        success: function () {
            console.log('query ----', query);
            $('#search').val(query);
        },
        complete: function () {
        },
        error: function (xhr, textStatus, thrownError) {
        }
    });
    event.preventDefault();


    $('.previous').click(function () {
        console.log('--previous---');
        if (from > 0) {
            from -= 1;
            $(location).attr('href', '/search_result?query=' + query + "&from=" + from + "&size=" + size);
        }
    });

    $('.next').click(function () {
        console.log('--next---');
        from += 1;
        if (from > Number($('.next').attr('role'))) {
            from = Number($('.next').attr('role'));
        }
        $(location).attr('href', '/search_result?query=' + query + "&from=" + from + "&size=" + size);
    });

    var displayResults, findAll, maxResults, names, resultsOutput, searchInput;

    names = ["贵州", "广州", "贵州 广州", "Tina", "Harper", "Hayes", "Tamera", "Shauna", "Mcfarland", "Charles", "Ortiz", "Maynard", "Julie", "Gay", "Wiggins", "Navarro", "Hopkins", "Candace", "Tammi", "Horton", "Erna", "Mills", "Opal", "Wolfe", "Walter", "Bonita", "Eleanor", "Rojas", "Ochoa", "Kirk", "Rosario", "Ball", "Lucile", "Kayla", "Carmela", "Miranda", "Middleton", "Lillie", "Sherry", "Jacqueline", "Deirdre", "Mueller", "Debra", "Jodi", "Joyce", "Estrada", "Liz", "Justine", "Francis", "Benton", "Henrietta", "Elise", "Lang", "Morse", "Farrell", "Tamra", "Darla", "Amy", "Kristie", "Wyatt", "Mcbride", "Talley", "Fay", "Sweet", "Fern", "Mcintosh", "Clemons", "Travis", "Kirsten", "Rios", "Newman", "Cook", "Jocelyn", "Mcmillan", "Mona", "Bessie", "Francis", "Rosemary", "Beverly", "Chandra", "Luella", "Parrish", "Ronda", "Earlene", "Bright", "Guthrie", "Shana", "Theresa", "Wells", "Green", "Schroeder", "Russo", "Randolph", "Livingston", "Carroll", "Velasquez", "Dana", "Bridget", "Hines", "Martha", "Marci", "Fuentes", "Stuart", "Glass", "Alejandra", "Thornton", "Britt", "Jeri", "Leach", "Cleo", "Lela", "Mattie", "Bonnie", "Lucille", "Mamie", "Kelly", "Obrien", "Carol", "Murphy", "Isabella", "Lowery", "Odom", "Norris", "Mullins", "Florine", "Morales", "Frederick", "Reynolds", "Janine", "Joyce", "Dean", "Marcy", "Allison", "Rena", "Saundra", "Flossie", "Kristi", "Monica", "Molina", "Guzman", "Loretta", "Levine", "Oneill", "Mccray", "Mann", "Constance", "English", "Eula", "Butler", "Erika"];

    findAll = (function (_this) {
        return function (wordList, collection) {
            return collection.filter(function (word) {
                word = word.toLowerCase();
                return wordList.some(function (w) {
                    return ~word.indexOf(w);
                });
            });
        };
    })(this);

    displayResults = function (resultsEl, wordList) {
        return resultsEl.innerHTML = (wordList.map(function (w) {
            // return '<li class="display_result">' + w + '</li>';
            return '<li class="display_result">' + w + '</li>';
        })).join('');
    };

    searchInput = document.getElementById('search');

    resultsOutput = document.getElementById('results');

    maxResults = 7;

    //向服务器请求用户的搜索记录
    searchInput.addEventListener('keyup', (function (_this) {
        return function (e) {

            var query = $('#search').val();
            console.log('--- query ----' + query);
            //向服务器发送查询词， 获取相关搜索词(suggestion)
            $.ajax({
                url: 'suggestion',
                type: "GET",
                data: {
                    'query': query
                },
                success: function (result) {
                    if (result.id == 1) {

                        console.log('---success ----' + result.result_list);

                        var suggested, value;
                        value = searchInput.value.toLowerCase().split(' ');

                        names = result.result_list.split(',');
                        suggested = (value[0].length ? findAll(value, names) : []);
                        return displayResults(resultsOutput, suggested);
                    }

                }
            });

            // var suggested, value;
            // value = searchInput.value.toLowerCase().split(' ');
            // suggested = (value[0].length ? findAll(value, names) : []);
            // return displayResults(resultsOutput, suggested);
        };
    })(this));


    $('#search').on('keydown', function (event) {
        console.log(" --- keydown --- " + event.which);
        var query = $(this).val();
        if ((event.which === 13)) {
            //与服务器进行交互
            var from = 0;
            var size = 10;
            if (query.trim() != '')
                $(location).attr('href', '/search_result?query=' + query + "&from=" + from + "&size=" + size);
        }
    });

    //获取用户点击新闻类别
    $('.list-group-item').click(function () {
        var class_ = $(this).attr('role');
        console.log(" --- class_ --- " + class_);
        $.ajax({
            url: 'class_',
            type: "GET",
            data: {
                'class_': class_,
                'query': query
            },
            success: function () {
                console.log('---success ----');
            },
            // complete: function () {
            // },
            // error: function (xhr, textStatus, thrownError) {
            // }
        });
    });

    $("#results").on("click", ".display_result", function (event) {
        var value = event.currentTarget.textContent;
        console.log('value ', value);
        var from = 0;
        var size = 10;
        if (query.trim() != '')
            $(location).attr('href', '/search_result?query=' + value + "&from=" + from + "&size=" + size);
    });
});