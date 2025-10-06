// function format(state) {
//     if (!state.id) return state.text; // optgroup

//     var originalOption = state.element;

//     return "<img class='status' src='" + $(originalOption).attr('data-img-src') + "'/>" + state.text;
// }
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
function formatBytes(bytes,decimals) {
    if(bytes == 0) return '0 Byte';
    var k = 1000;
    var dm = decimals + 1 || 3;
    var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    var i = Math.floor(Math.log(bytes) / Math.log(k));
    return (bytes / Math.pow(k, i)).toPrecision(dm) + ' ' + sizes[i];
}
$(document).ready(function () {
    if ( ! window.console ) console = { log: function(){} };
    var csrftoken = getCookie('csrftoken');
    var addXCSRFHeader = function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    };
    var scrollTo = function($tag, speed) {
        if (typeof speed === 'undefined') {
            speed = 2000;
        }
        if(!$tag.visible()) {
            var $page = $('html, body');
            // interrupt scroll if user scrolls window by himself
            $page.on("scroll mousedown wheel DOMMouseScroll mousewheel keyup touchmove", function () {
                $page.stop();
            });
            $page.animate({scrollTop: $tag.offset().top}, speed, function () {
                $page.off("scroll mousedown wheel DOMMouseScroll mousewheel keyup touchmove");
            });
        }
    };
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            addXCSRFHeader(xhr, settings);
            $('#overlay-spinner').show();
        },
        complete: function() {
            $('#overlay-spinner').hide();
        }
    });
    $.noty.defaults.timeout = 5000;
    var mainOptionsLTR = {
        loop: true,
        autoPlay: true,
        paginationSpeed: 400,
        singleItem: true,
        pagination: true,
        slideSpeed: 300,
        itemsScaleUp: true
    };
    var mainOptionsRTL = {
       loop: true,
        autoPlay: true,
        paginationSpeed: 400,
        singleItem: true,
        pagination: true,
        slideSpeed: 300,
        itemsScaleUp: true,
        direction: 'rtl'
    };
    var articleOptionsLTR = {
        loop: true,
        autoPlay: true,
        lazyLoad : true,
        stopOnHover: true,
        paginationSpeed: 400,
        singleItem: true,
        pagination: true,
        slideSpeed: 300,
        itemsScaleUp: true
    };
    var articleOptionsRTL = {
        loop: true,
        autoPlay: true,
        lazyLoad : true,
        stopOnHover: true,
        paginationSpeed: 400,
        singleItem: true,
        pagination: true,
        slideSpeed: 300,
        itemsScaleUp: true,
        direction: 'rtl'
    };
    var singleOptionsLTR = {
        loop: true,
        autoPlay: false,
        stopOnHover: true,
        paginationSpeed: 400,
        singleItem: true,
        lazyLoad : true,
        pagination: false,
        navigation: true,
        slideSpeed: 300,
        itemsScaleUp: true,
        navigationText: [
            "<i class='icon-arrow-prev-79'></i>",
            "<i class='icon-arrow-next-79'></i>"
        ]
    };
    var singleOptionsRTL = {
        loop: true,
        autoPlay: false,
        stopOnHover: true,
        paginationSpeed: 400,
        singleItem: true,
        lazyLoad : true,
        pagination: false,
        navigation: true,
        slideSpeed: 300,
        itemsScaleUp: true,
        navigationText: [
            "<i class='icon-arrow-prev-79'></i>",
            "<i class='icon-arrow-next-79'></i>"
        ],
        direction: 'rtl'
    };
    var $body = $('body');
    var slider = $("#main-slider");
    var slider2 = $("#article-slider");

    var lang_code = $body.attr('data-lang-code');
    $.datepicker.setDefaults( $.datepicker.regional[lang_code] );
    if ($body.attr('id') == 'arabic') {
        slider.owlCarousel(mainOptionsRTL);
        slider2.owlCarousel(articleOptionsRTL);
    } else {
        slider.owlCarousel(mainOptionsLTR);
        slider2.owlCarousel(articleOptionsLTR);
    }
    var init_single_image_gallery = function() {
        var $galleries = $(".find-gallery-single");
        var carousel_options;
        if ($body.attr('id') == 'arabic') {
            carousel_options = singleOptionsRTL;
        } else {
            carousel_options = singleOptionsLTR;
        }
        var $not_initialized_galleries = $galleries.filter(function(){
            return typeof ($(this).data('owl-init')) === 'undefined';
        });

        $not_initialized_galleries.owlCarousel(carousel_options);
    };
    init_single_image_gallery();
    //  select LANG andcustom scrollbar for lang select atart

    var $selectLang = $('#select-lang'),
        $langDrop = $('#lang-drop'),
        hider = {
            'display':'none'
        },
        opener = {
            'display':'block'
        };
    $selectLang.removeClass('open');
    $langDrop.css(hider);

    $selectLang.click(function () {
        var $this = $(this),
            outerClick = true;
                  
        if ($this.hasClass('open')) {
             $this.removeClass('open');
             $langDrop.css(hider);
        } else {
            $this.addClass('open');
            $langDrop.css(opener);
            $langDrop.niceScroll({
                horizrailenabled: false,
                autohidemode: false,
                cursorcolor: "#d2cfcf",
                cursorwidth: 8
            });
        }
        $(document).on('click.outerEvent', function(e) {
            if (!outerClick && $(e.target).closest('#select-lang').length == 0) {
                $selectLang.removeClass('open');
                $langDrop.css(hider);
                $(document).off('click.outerEvent');
            }
            outerClick = false;
        });
    });
    $('.select-lang__label.check-language').click(function() {
        // e.preventDefault();
        var $this = $(this);
        $selectLang.find('img').attr('src', $this.find('img').attr('src'));
        $selectLang.removeClass('open');
        $langDrop.css(hider);
    });
    $('input[name="language"]').on('change', function(){
        this.form.submit();
    });
     // select LANGcustom scrollbar for lang select end
     
    function set_status_select2_styling(val, $selected_val, noshow_opt, confirmed_opt) {
         switch (val) {
             case noshow_opt: //no show
                 $selected_val.addClass('status-noshow').removeClass('status-confirmed');
             break;

             case confirmed_opt: // confirmed
                 $selected_val.select2("container").removeClass('status-noshow').addClass('status-confirmed');
             break;
         }
    }

    function init_select2_status(idx, select2_el) {
        var $select2_tag = $(select2_el),
            success_message = $select2_tag.attr('data-success-message'),
            noshow_opt = $select2_tag.attr('data-noshow-opt'),
            confirmed_opt = $select2_tag.attr('data-conf-opt'),
            url = $select2_tag.attr('data-url'),
            action = $select2_tag.attr('data-action'),
            $booking_tr = $select2_tag.closest('.cabinet__book-tr'),
            curr_val = $select2_tag.val();
        $select2_tag.select2({
            minimumResultsForSearch: -1,
            containerCssClass: "statusdrop",
            dropdownCssClass: "status-option",
            dropdownAutoWidth: true
        }).on('change', function (e) {
            var new_val = e.val;
            set_status_select2_styling(new_val, $(this).parent().find('.select2-chosen'), noshow_opt, confirmed_opt);
            if (new_val === noshow_opt) {
                $.post(url, {action: action}, function( data ) {
                    if (data['status'] === 'success') {
                        $booking_tr.html(data['html']);
                        noty({text: success_message, type: 'success'});
                    } else {
                        noty({text: data['message'], type: 'error'});
                    }
                });
            }
        });
        set_status_select2_styling(curr_val, $select2_tag.parent().find('.select2-chosen'), noshow_opt, confirmed_opt);
    }

    $body.on('click', '.cabinet__undoaction', function() {
        var success_message = $(this).attr('data-success-message'),
            url = $(this).attr('data-url'),
            action = $(this).attr('data-action'),
            $booking_tr = $(this).closest('.cabinet__book-tr');
        $.post(url, {action: action}, function( data ) {
            if (data['status'] === 'success') {
                $booking_tr.html(data['html']);
                init_select2_status(0, $booking_tr.find(".select-status"));
                noty({text: success_message, type: 'success'});
            } else {
                noty({text: data['message'], type: 'error'});
            }
        });
        return false;
    });

    var init_select2_statuses_array = function ($array) {
         $array.each(init_select2_status);
    };
    init_select2_statuses_array($('.select-status'));

    var init_select_qty = function () {
        $('.select-qty').select2({
            minimumResultsForSearch: -1,
            containerCssClass: "qtydrop",
            dropdownCssClass: "qty-option",
            dropdownAutoWidth: true,
            //formatResult: format,
            //formatSelection: format,
            escapeMarkup: function (m) {
                return m;
            }
        });
    };
    init_select_qty();
    var init_selects_on_create_room_page = function($base) {
        $base.find('.select-method').select2({
            minimumResultsForSearch: -1,
            allowClear: true,
            containerCssClass: "methoddrop",
            dropdownCssClass: "method-option",
            dropdownAutoWidth: true
        });
    };
    init_selects_on_create_room_page($body);

    var init_country_dropdown_on_profile_edit_page = function($base) {
        var countrySelectEditPage = $base.find('select').select2({
            minimumResultsForSearch: 0,
            // allowClear: true,
            placeholder: 'Country',
            containerCssClass: "methoddrop",
            dropdownCssClass: "method-option",
            dropdownAutoWidth: true
        });

        // custom scrollbar start
        countrySelectEditPage.on("select2-open", function () {
                s = $('.select2-drop-active > .select2-results');
                s.niceScroll({
                    horizrailenabled: false,
                    autohidemode: false,
                    cursorcolor: "#d2cfcf",
                    cursorwidth: 8
                });
        });
        // custom scrollbar end
    };
    init_country_dropdown_on_profile_edit_page($(".country-select-profile-edit-page"));

    var init_selects_on_choose_country = function($base) {
        var countrySelect = $base.find('select').select2({
            minimumResultsForSearch: 0,
            // allowClear: true,
            placeholder: 'Country',
            containerCssClass: "countrydrop",
            dropdownCssClass: "country-option",
            dropdownAutoWidth: true
        });

        // custom scrollbar start
        countrySelect.on("select2-open", function () {
            // var s;
            // if (!s) {
                s = $('.select2-drop-active > .select2-results');
                s.niceScroll({
                    horizrailenabled: false,
                    autohidemode: false,
                    cursorcolor: "#d2cfcf",
                    cursorwidth: 8
                });
            // }
        });
        // custom scrollbar end
    };
    init_selects_on_choose_country($(".select-country-container"));

    $('#menu-popup').click(function () {
        $('#menu-drop').toggle();
    });
    $('#menu-switch').click(function () {
        $('#menu-dropdown').toggle();
    });
    // toggle blog meny start
    function toggleMenu(){
        if ($(window).width() < 768 ){
            $("#article-dropdown").hide();
            $("#article-switch").click(function() {
                $("#article-dropdown").toggle();
            });
        }else $("#article-dropdown").show();
    }
    $(window).load(toggleMenu);
    $(window).resize(toggleMenu);
    // toggle blog meny end

    //price slider start
    var init_price_slider_on_find_pages = function () {
        var $slider_price = $('#slider-price');
        if ($slider_price.length > 0) {
            var used_min_price = $slider_price.attr('data-used-min'),
                used_max_price = $slider_price.attr('data-used-max'),
                min_price = $slider_price.attr('data-min'),
                max_price = $slider_price.attr('data-max');
            $slider_price.noUiSlider({
                start: [parseInt(used_min_price), parseInt(used_max_price)],
                connect: true,
                step: 1,
                range: {
                    'min': parseInt(min_price),
                    'max': parseInt(max_price)
                },
                format: wNumb({
                    decimals: 1
                })
            });
            $slider_price.Link('lower').to($('#price-value-min'), null, wNumb({
                decimals: 0,
                postfix: '$'
            }));
            $slider_price.Link('lower').to($('#id_from_price'));
            $slider_price.Link('upper').to($('#price-value-max'), null, wNumb({
                decimals: 0,
                postfix: '$'
            }));
            $slider_price.Link('upper').to($('#id_to_price'));
        }
    };
    init_price_slider_on_find_pages();
    //price slider end
    //number of rooms slider start
    var init_room_num_slider_on_find_apts = function () {
        var $room_num_slider = $('#room-num-slider');
        if ($room_num_slider.length > 0) {
            var used_min_num = $room_num_slider.attr('data-used-min'),
                used_max_num = $room_num_slider.attr('data-used-max'),
                min_num = $room_num_slider.attr('data-min'),
                max_num = $room_num_slider.attr('data-max');
            $room_num_slider.noUiSlider({
                start: [parseInt(used_min_num), parseInt(used_max_num)],
                connect: true,
                step: 1,
                range: {
                    'min': parseInt(min_num),
                    'max': parseInt(max_num)
                },
                format: wNumb({
                    decimals: 0
                })
            });
            $room_num_slider.Link('lower').to($('#room-num-value-min'));
            $room_num_slider.Link('lower').to($('#id_room_num_from'));
            $room_num_slider.Link('upper').to($('#room-num-value-max'));
            $room_num_slider.Link('upper').to($('#id_room_num_to'));
        }
    }
    init_room_num_slider_on_find_apts();
    //number of rooms slider end


    $(document).on('click', function (e) {
        if (e.target.className.match(/\bui-[a-z]+\b/)) {
            return;
        }
        $('#calendar-box').datepicker('destroy');
    });

    var show_messages = function () {
        $("#contrib_messages").find("li").each(function() {
            var type = $(this).attr('data-type');
            if (typeof type === 'undefined') {
                type = 'warning'
            }
            noty({text: $(this).text(), type: type});
        });
    };
    show_messages();

    //calendar start
    var show_dates = function () {
        $('.selected-date').show().html($('#from-date').val() + ' - ' + $('#to-date').val());
        $('.header-m__link.date').removeClass('date-active');
        $('.header__link.date').removeClass('date-active');
        $('.date-calendar').hide();
    };
    if ($('#from-date').val() && $('#to-date').val()) {
        show_dates();
    }

    $body.on('submit', '#save_dates_and_guests_form', function(e) {
        var $form = $(this);
        $form.ajaxSubmit({
            success: function (resp) {
                if (resp['status'] === 'fail') {
                    $.each(resp['errors'], function( idx, val ) {
                        noty({text: val, type: 'error'});
                    });
                    if ('arrival' in resp) {
                        $("#from-date").val(resp['arrival']);
                        $("#to-date").val(resp['departure']);
                        show_dates();
                    } else {
                        $("#from-date").val('');
                        $("#to-date").val('');
                        $('.selected-date').hide().html('');
                    }
                } else {
                    // replicate dates changes from header form to form in service detail page
                    var $detail_arrival = $("#id_detail-arrival"), $detail_departure = $("#id_detail-departure");
                    if ($detail_arrival.length > 0 && $detail_departure.length > 0) {
                        $detail_arrival.val($('#from-date').val());
                        $detail_departure.val($('#to-date').val());
                    }
                    // header dates&guests form was successfully submitted
                    if ($('#find-hotel-list').length > 0) {
                        $('#search-form').trigger('submit');
                    } else if ($('#rooms-list').length > 0) {
                        // hotel, apartment detail page
                        $('#search-rooms-by-dates').trigger('submit');
                    } else if ($('#items-list').length > 0) {
                        // transport, sports, excursions, entertainment detail page
                        var $items_arrival = $("#id_time_based-arrival"), $items_departure = $("#id_time_based-departure");
                        if ($items_arrival.length > 0 && $items_departure.length > 0) {
                            $items_arrival.val($('#from-date').val());
                            $items_departure.val($('#to-date').val());
                        }
                        update_service_items_on_dates_update(false);
                    }
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        e.preventDefault();
        return false;
    });

    //datepicker helper functions start
    var nextDayOf = function(date) {
        var next_day_of_date = new Date(date);
        next_day_of_date.setDate(next_day_of_date.getDate() + 1);
        return next_day_of_date
    };
    var parseDate = function(date) {
        return $.datepicker.parseDate('dd.mm.yy', date);
    };
    var formatDate = function(date_in_str) {
        return $.datepicker.formatDate('dd.mm.yy', date_in_str);
    };
    var limitDepartureDateOnArrivalDateClose = function($arrival_input, $departure_input) {
        var arrival_date = $arrival_input.datepicker('getDate');
        var departure_date = $departure_input.datepicker('getDate');
        if (departure_date === null || arrival_date >= departure_date) {
            $departure_input.datepicker('option', 'minDate', nextDayOf(arrival_date));
        }
    };
    var limitDepartureDateOnDepartureBeforeShow = function($arrival_input, $departure_input) {
        var new_min_date_to;
        if ($arrival_input.val() !== '') {
            new_min_date_to = nextDayOf($arrival_input.datepicker('getDate'));
        } else {
            new_min_date_to = "+1"
        }
        $departure_input.datepicker('option', 'minDate', new_min_date_to);
    };
    //datepicker helper functions end

    $.each(['from', 'to'], function (key, inp) {
        var $date_el = $('#' + inp + '-date');
        $date_el.on('click', function (e) {
            e.stopPropagation();
            var opts = {
                showOtherMonths: true,
                buttonImageOnly: true,
                dateFormat: 'dd.mm.yy',
                onSelect: function (newVal, dp) {
                    var prevVal = dp.lastVal,
                        $box = $('#calendar-box');
                    if (prevVal !== newVal) {
                        $('#' + inp + '-date').val(newVal);
                        if (inp === 'from') {
                            var new_date_from = $box.datepicker('getDate');
                            var $input_with_date_to = $('#to-date');
                            var date_to = $input_with_date_to.val();
                            if (date_to) {
                                // change departure date if only there is already some variable
                                var date_to_val = parseDate(date_to);
                                if (new_date_from >= date_to_val) {
                                    $input_with_date_to.val(formatDate(nextDayOf(new_date_from)));
                                }
                            }
                        }
                        if ($('#from-date').val() && $('#to-date').val()) {
                            $('#save_dates_and_guests_form').trigger('submit');
                        }
                    }
                    $box.datepicker('destroy');
                    if ($('#from-date').val() && $('#to-date').val()) {
                        show_dates();
                    } else {
                        $('.selected-date').hide().html('');
                    }
                }
            };

            if (inp == 'from') {
                opts.minDate = 0;
            }

            if (inp == 'to') {
                if ($('#from-date').val()) {
                    var date_from = parseDate($('#from-date').val());
                    opts.minDate = nextDayOf(date_from)
                } else {
                    opts.minDate = "+1"
                }
            }

            //if ($('#to-date').val() && inp == 'from') {
            //    opts.maxDate = $('#to-date').val();
            //}

            var $box = $('#calendar-box');
            $box.datepicker('destroy');
            $box.datepicker(opts);
            $box.datepicker('setDate', $date_el.val());
        });
    });
    //calendar end
    //header adults and children dropdown on change
    var $select_guests = $('.select-guests');
    $select_guests.on("open", function() {
        var $this = $(this);
        $this.attr('data-val', $this.val());
    });
    $select_guests.on("change", function() {
        var $this = $(this);
        var prev_val = $(this).attr('data-val');
        if (!prev_val || prev_val != $this.val()) {
            $('#save_dates_and_guests_form').trigger('submit');
        }
    });
    //header adults and children dropdown on change end
    //calendar index start
    $("#id_index-arrival").datepicker({
        dateFormat: 'dd.mm.yy',
        numberOfMonths: 1,
        minDate: 0,
        beforeShow: function() {
            $(this).datepicker('option', 'minDate', 0);
        },
        onClose: function( selectedDate ) {
            if (selectedDate !== '') {
                limitDepartureDateOnArrivalDateClose($(this), $( "#id_index-departure" ));
            }
        }
    });
    $("#id_index-departure").datepicker({
        dateFormat: 'dd.mm.yy',
        numberOfMonths: 1,
        beforeShow: function() {
            limitDepartureDateOnDepartureBeforeShow($("#id_index-arrival"), $(this));
        }
    });
    //calendar index end
    //hotel details booking start
     //  select ROOm QTY andcustom scrollbar  start
    var init_roomqty_dropdowns = function () {
        $('.select-room-qty').removeClass('open');
        $('.room-qty-drop').hide();
    };
    init_roomqty_dropdowns();
    $body.on('click', '.select-room-qty', function (e) {
        var $this = $(this),
            outerClick = true,
            $roomQtyDrop = $this.siblings('.room-qty-drop');
        $roomQtyDrop.hide();

        if ($this.hasClass('open')) {
             $this.removeClass('open');
             $roomQtyDrop.hide();
        } else {
            $this.addClass('open');
            $roomQtyDrop.show();
            $roomQtyDrop.niceScroll({
                horizrailenabled: false,
                autohidemode: false,
                cursorcolor: "#d2cfcf",
                cursorwidth: 8
            });
        }
        $(document).on('click.outerEvent', function(e) {
            if (!outerClick && $(e.target).closest('.select-room-qty').length == 0) {
                $this.removeClass('open');
                $roomQtyDrop.hide();
                $(document).off('click.outerEvent');
            }
            outerClick = false;
        });
    });
    $body.on('click', '.js-room-qty-selecting-link:not(".disabled")', function(e) {
        var $this = $(this),
            $container = $this.closest('.js-room-qty-select'),
            $roomQtyDrop = $this.closest('.room-qty-drop');
        $container.siblings('.js-room-qty-selected').find('label').text($this.text());
        $container.removeClass('open');
        $roomQtyDrop.hide();
    });
     // select ROOM QTY scrollbar for  select end

    $body.on('change', 'input[name^="pc_"]', function() {
        var $group = $(this).closest('.js-room-qty-select');
        var $total_numbers = $('.js-total-number > span');
        var $total_amounts = $('.js-total-amount > span');
        var prev_total_number = parseInt($total_numbers.first().text());
        var prev_total_amount = parseFloat($total_amounts.first().text());
        //var $room_container = $group.closest(".js-room-container");
        var $current_price_container = $group.closest(".js-current-price-category");
        //var allotment = parseInt($room_container.find(".js-room-number").text());
        var max_opt = parseInt($group.attr('data-max-num'));
        var $pc_container = $group.closest(".js-price-categories-list");
        var prev_val = parseInt($group.attr('data-prev-val'));
        var new_val = parseInt($(this).val());
        var price_per_room = parseFloat($current_price_container.find(".js-price-per-room").text());
        var prev_amount = prev_val * price_per_room;
        var new_amount = new_val * price_per_room;
        $total_numbers.text(prev_total_number - prev_val + new_val);
        $total_amounts.text(prev_total_amount - prev_amount + new_amount);
        var total_rooms_chosen = 0;
        $pc_container.find('input[name^="pc_"]:checked').each(function(){
            total_rooms_chosen += parseInt($(this).val());
        });
        $pc_container.find('.js-room-qty-select').not($group[0]).each(function(){
            var curr_val = parseInt($(this).find('input[name^="pc_"]:checked').val());
            if (new_val > prev_val) {
                var disable_all_with_bigger_val = max_opt - (total_rooms_chosen - curr_val);
                $(this).find('.js-room-qty-item').each(function(){
                    var $input = $(this).find('input'),
                        $label = $(this).find('label'),
                        opt_val = parseInt($input.val());
                    if (opt_val > disable_all_with_bigger_val) {
                        $input.prop("disabled", "disabled");
                        $label.addClass("disabled");
                    }
                });
            } else {
                var enable_all_with_less_val = max_opt - (total_rooms_chosen - curr_val);
                $(this).find('.js-room-qty-item').each(function(){
                    var $input = $(this).find('input'),
                        $label = $(this).find('label'),
                        opt_val = parseInt($input.val());
                    if (opt_val <= enable_all_with_less_val) {
                        $input.prop("disabled", false);
                        $label.removeClass("disabled");
                    }
                });
            }
        });
        $group.attr('data-prev-val', new_val);
    });
    $body.on('submit', "#room_booking_form", function () {
        var at_least_1_was_checked = false;
        $(this).find('input[name^="pc_"]:checked').each(function(){
            var val = parseInt($(this).val());
            if (val > 0) {
                at_least_1_was_checked = true;
            }
        });
        if (!at_least_1_was_checked) {
            noty({text: $(this).attr("data-warning"), type: 'warning'});
            return false;
        }
    });
    //hotel details booking end
    //transport details booking start
    $body.on('change', 'input[name^="i_"]', function() {
        var $group = $(this).closest('.js-room-qty-select');
        var $total_numbers = $('.js-total-number > span');
        var $total_amounts = $('.js-total-amount > span');
        var prev_total_number = parseInt($total_numbers.first().text());
        var prev_total_amount = parseFloat($total_amounts.first().text());
        //var $room_container = $group.closest(".js-room-container");
        var $current_price_container = $group.closest(".js-current-price-category");
        //var allotment = parseInt($room_container.find(".js-room-number").text());
        var max_opt = parseInt($group.attr('data-max-num'));
        var $i_container = $group.closest(".js-price-categories-list");
        var prev_val = parseInt($group.attr('data-prev-val'));
        var new_val = parseInt($(this).val());
        var $item_based_only_container = $(this).closest(".js-qty-and-dates-container-of-item-based");
        if ($item_based_only_container.length > 0) {
            var $first_dt = $item_based_only_container.find('.js-first-datetime'),
                $second_dt = $item_based_only_container.find('.js-second-datetime'),
                $plus_btn = $item_based_only_container.find('.add-item-input'),
                $minus_btn = $item_based_only_container.find('.remove-item-input');
            if (new_val == 0) {
                $first_dt.hide();
                $second_dt.hide();
                $plus_btn.hide();
                $minus_btn.hide();
            } else if (new_val == 1) {
                $first_dt.show();
                $second_dt.hide();
                $plus_btn.hide();
                $minus_btn.hide();
            } else if (new_val == 2) {
                $first_dt.show();
                if (!$second_dt.is(':visible')) {
                    $plus_btn.show();
                }
            }
        }
        var price_per_room = parseFloat($current_price_container.find(".js-price-per-room").text());
        var prev_amount = prev_val * price_per_room;
        var new_amount = new_val * price_per_room;
        $total_numbers.text(prev_total_number - prev_val + new_val);
        $total_amounts.text(prev_total_amount - prev_amount + new_amount);
        var total_rooms_chosen = 0;
        $i_container.find('input[name^="i_"]:checked').each(function(){
            total_rooms_chosen += parseInt($(this).val());
        });
        /*$i_container.find('.js-room-qty-select').not($group[0]).each(function(){
            var curr_val = parseInt($(this).find('input[name^="i_"]:checked').val());
            if (new_val > prev_val) {
                var disable_all_with_bigger_val = max_opt - (total_rooms_chosen - curr_val);
                $(this).find('.js-room-qty-item').each(function(){
                    var $input = $(this).find('input'),
                        $label = $(this).find('label'),
                        opt_val = parseInt($input.val());
                    if (opt_val > disable_all_with_bigger_val) {
                        $input.prop("disabled", "disabled");
                        $label.addClass("disabled");
                    }
                });
            } else {
                var enable_all_with_less_val = max_opt - (total_rooms_chosen - curr_val);
                $(this).find('.js-room-qty-item').each(function(){
                    var $input = $(this).find('input'),
                        $label = $(this).find('label'),
                        opt_val = parseInt($input.val());
                    if (opt_val <= enable_all_with_less_val) {
                        $input.prop("disabled", false);
                        $label.removeClass("disabled");
                    }
                });
            }
        });*/
        $group.attr('data-prev-val', new_val);
    });
    $body.on('click', '.add-item-input', function() {
        var $btn = $(this);
        var $item_based_only_container = $(this).closest(".js-qty-and-dates-container-of-item-based");
        var $second_dt = $item_based_only_container.find('.js-second-datetime');
        $second_dt.find('input').prop("disabled", false);
        $second_dt.show();
        $item_based_only_container.find('.remove-item-input').show();
        $btn.hide();
    });
    $body.on('click', '.remove-item-input', function() {
        var $btn = $(this);
        var $item_based_only_container = $(this).closest(".js-qty-and-dates-container-of-item-based");
        $item_based_only_container.find('.add-item-input').show();
        var $second_dt = $item_based_only_container.find('.js-second-datetime');
        $second_dt.find('input').prop("disabled", true);
        $second_dt.hide();
        $btn.hide();
    });
    $body.on('submit', "#detail_page_items_booking_form", function () {
        var at_least_1_was_checked = false;
        $(this).find('input[name^="i_"]:checked').each(function(){
            var val = parseInt($(this).val());
            if (val > 0) {
                at_least_1_was_checked = true;
            }
        });
        if (!at_least_1_was_checked) {
            noty({text: $(this).attr("data-warning"), type: 'warning'});
            return false;
        }
    });
    //transport details booking end
    //calendar hotel details start
    var onSelectDateCallbackForServiceDetailPage = function (newVal, dp) {
        var prevVal = dp.lastVal;
        if (prevVal !== newVal) {
            $(this).val(newVal);
            var $date_from = $("#id_detail-arrival"),
                $date_to = $("#id_detail-departure");
            if ($date_from.val() && $date_to.val()) {
                var date_1 = $date_from.datepicker('getDate'),
                    date_2 = $date_to.datepicker('getDate');
                if (date_1 >= date_2) {
                    $date_to.val(formatDate(nextDayOf(date_1)));
                }
                $('#search-rooms-by-dates').trigger('submit');
            }
        }
    };
    var show_error_messages_using_noty_if_any = function () {
        var $form_errors = $('#ajax-date-form-errors');
        if ($form_errors.length > 0) {
            $form_errors.find('li').each(function(){
                noty({text: $(this).text(), type: 'error'});
            });
            $form_errors.remove();
        }
    };
    show_error_messages_using_noty_if_any();
    var calendar_init_on_detail_pages = function() {
        $("#id_detail-arrival").datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            minDate: 0,
            onSelect: onSelectDateCallbackForServiceDetailPage,
            onClose: function (selectedDate) {
                if (selectedDate !== '') {
                    limitDepartureDateOnArrivalDateClose($(this), $('#id_detail-departure'));
                }
            }
        });
        $("#id_detail-departure").datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            beforeShow: function () {
                limitDepartureDateOnDepartureBeforeShow($("#id_detail-arrival"), $(this));
            },
            onSelect: onSelectDateCallbackForServiceDetailPage
        });
    };
    calendar_init_on_detail_pages();

    var calendar_time_init_on_detail_pages = function() {
        //made with timepicker AddOn http://trentrichardson.com/examples/timepicker/#range_examples
        var datetimeTable = $('.datetime-table');
        datetimeTable.each(function() {
            var $this = $(this);
            var startDateTextBox = $this.find('.detail-from-datetime');
            var endDateTextBox = $this.find('.detail-to-datetime');
            
            if (!startDateTextBox.length || !endDateTextBox.length) {
                return;
            }

            startDateTextBox.datetimepicker({
                dateFormat: 'dd.mm.yy',
                timeFormat: 'HH:mm',
                controlType: 'select',
                oneLine: true,
                minDate: 0
            });

            endDateTextBox.datetimepicker({
                dateFormat: 'dd.mm.yy',
                timeFormat: 'HH:mm',
                controlType: 'select',
                oneLine: true,
                minDate: 0
            });
            //$.timepicker.datetimeRange(
            //    startDateTextBox,
            //    endDateTextBox,
            //    {
            //        minInterval: (1000*60*60), // 1hr
            //        dateFormat: 'dd.mm.yy',
            //        timeFormat: 'HH:mm',
            //        controlType: 'select',
            //        oneLine: true,
            //        start: {
            //            minDate: 0
            //        },
            //        end: {
            //        }
            //    }
            //);
        });
        
    };
    calendar_time_init_on_detail_pages();
    //calendar hotel details end
    // hotel detail page - room search start
    $body.on('submit', '#search-rooms-by-dates', function (e) {
        var $form = $(this);
        var data = $form.serialize();
        $form.ajaxSubmit({
            success: function (resp) {
                var url = '?' + data;
                History.pushState('', '', url);
                $('#rooms-list').html(resp);
                calendar_init_on_detail_pages();
                init_roomqty_dropdowns();
                init_room_amenities_popup();
                init_items_gallery();
                shorten_item_description_on_all_devices(true);
                show_error_messages_using_noty_if_any();
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        e.preventDefault();
        return false;
    });
    // hotel detail page - room search end
    // transport, sport, excursions, entertainment time based item search start
    var onSelectDateCallbackForTimeBasedItemsOnDetailPage = function (newVal, dp) {
        var prevVal = dp.lastVal;
        if (prevVal !== newVal) {
            $(this).val(newVal);
            var $date_from = $("#id_time_based-arrival"),
                $date_to = $("#id_time_based-departure");
            if ($date_from.val() && $date_to.val()) {
                var date_1 = $date_from.datepicker('getDate'),
                    date_2 = $date_to.datepicker('getDate');
                if (date_1 >= date_2) {
                    $date_to.val(formatDate(nextDayOf(date_1)));
                }
                update_service_items_on_dates_update(true);
            }
        }
    };
    var calendar_init_for_time_based_items_on_detail_pages = function() {
        $("#id_time_based-arrival").datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            minDate: 0,
            onSelect: onSelectDateCallbackForTimeBasedItemsOnDetailPage,
            onClose: function (selectedDate) {
                if (selectedDate !== '') {
                    limitDepartureDateOnArrivalDateClose($(this), $('#id_time_based-departure'));
                }
            }
        });
        $("#id_time_based-departure").datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            beforeShow: function () {
                limitDepartureDateOnDepartureBeforeShow($("#id_time_based-arrival"), $(this));
            },
            onSelect: onSelectDateCallbackForTimeBasedItemsOnDetailPage
        });
    };
    calendar_init_for_time_based_items_on_detail_pages();

    $body.on('click', '.js-discount-price', function() {
        var $this = $(this);
        var days = $this.attr('data-days');
        var int_days = parseInt(days);
        if (!isNaN(int_days)) {
            var new_departure_date = $('#id_time_based-arrival').datepicker('getDate');
            new_departure_date.setDate(new_departure_date.getDate() + int_days);
            var $departure_input = $('#id_time_based-departure');
            var old_departure_date = $departure_input.datepicker('getDate');
            if (old_departure_date.valueOf() !== new_departure_date.valueOf()) {
                $departure_input.datepicker('setDate', new_departure_date);
                update_service_items_on_dates_update(true);
            }
        }
    });

    var update_service_items_on_dates_update = function(time_based_only) {
        var data = {};
        var change_url = false;
        var $items_arrival = $("#id_time_based-arrival"), $items_departure = $("#id_time_based-departure");
        if ($items_arrival.length > 0 && $items_departure.length > 0) {
            var history_data = {
                'time_based-arrival': $items_arrival.val(),
                'time_based-departure': $items_departure.val()
            };
            change_url = true;
        }
        if (time_based_only) {
            data = $.extend(true, {}, history_data);
            data['update-time-based-booking-dates'] = 1;
            // remove time-based items from booking
            $('#js-time-based-items-list').find('input[name^=i_][value=0]').trigger('click');
        }

        $.ajax({
            url: '.',
            data: data,
            success: function (resp) {
                if (time_based_only) {
                    History.replaceState('', '', '?' + $.param(history_data));
                    var $container = $('#js-time-based-items-list');
                    $container.html(resp);
                    if ($('#ajax-date-form-errors').length > 0) {
                        scrollTo($container);
                    }
                } else {
                    if (change_url) {
                        History.replaceState('', '', '?' + $.param(history_data));
                    }
                    $('#items-list').html(resp);
                    calendar_time_init_on_detail_pages();
                }
                calendar_init_for_time_based_items_on_detail_pages();
                init_roomqty_dropdowns();
                //init_room_amenities_popup();
                init_items_gallery();
                shorten_item_description_on_all_devices(true);
                show_error_messages_using_noty_if_any();
            },
            error: function (resp) {
                console.log(resp);
            }
        });
    };
    // transport, sport, excursions, entertainment time based item search end
    //comments of services and blogposts start
    var $comment_form = $('#comment-form');
    if ($comment_form.length > 0) {
        var login_url = $comment_form.attr('data-login-url');
        if (typeof(login_url) !== 'undefined') {
            var $textarea = $comment_form.find('.js-comment-textarea'),
                $btn = $comment_form.find('.js-submit-comment-btn');
            $textarea.on('focus', function() {
                window.location = login_url;
            });

            $btn.on('click', function() {
                window.location = login_url;
                return false;
            });
        }
    }

    var $comments_container = $('#comments_container');
    if ($comments_container.length > 0) {
        console.log($.url().param('scroll'));
        if ($.url().param('scroll') === '1') {
            scrollTo($comments_container);
        }
    }

    $body.on('submit', '#comment-form', function(e) {
        var $form = $(this),
            success_message = $form.attr('data-success-message');
        $form.ajaxSubmit({
            success: function (resp) {
                if (resp['status'] == 'success') {
                    noty({text: success_message, type: 'success'});
                    $('.comment-container').remove();
                } else {
                    $form.replaceWith(resp['html']);
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        e.preventDefault();
        return false;
    });
    //comments of services and blogposts end
    //comments hotel and blog details pagination start
    var comments_pagination_on_scroll = function() {
        var $showmore_btn = $('.find__showmore-btn-link.comment-pagination');
        if ($showmore_btn.length > 0) {
            $(window).scroll(function(){
                if ($(window).scrollTop() > $showmore_btn.offset().top - $(window).height() - 100){
                    $(window).off('scroll');
                    var $showmore_panel = $showmore_btn.parent();
                    var url = $showmore_btn.attr('data-url');
                    var next_page = $showmore_btn.attr('data-next-page');
                    var entity_id = $showmore_btn.attr('data-entity-id');
                    var $container = $showmore_btn.closest('.comment-list-container');
                    $.ajax({
                        url: url,
                        data: {
                            next_page: next_page,
                            entity_id: entity_id
                        },
                        success: function(resp) {
                            if (resp['status'] == 'success') {
                                $showmore_panel.remove();
                                $container.append(resp['html']);
                                shorten_comments(true);
                                comments_pagination_on_scroll();
                            } else {
                                console.log(resp['message']);
                            }
                        },
                        error: function (resp) {
                            console.log(resp);
                        }
                    });
                }
            });
        }
    };
    comments_pagination_on_scroll();
    //comments hotel and blog details pagination end
    //calendar onclick start
    $('.date').on('click', function (e) {
        if (e.target.className.match(/\bui-[a-z]+\b/)) {
            return;
        }
        e.stopPropagation();
        $(this).toggleClass('date-active');
        $('.date-calendar').toggle();
        $(this).removeClass('date-box');
    });
    //calendar onclick end

    //img-gallery begin
    var optionsLTR = {
        navigation: true,
        lazyLoad : true,
        loop: true,
        navigationText: [
            "<i class='icon-find-arrow-prev'></i>",
            "<i class='icon-find-arrow-next'></i>"
        ],
        items: 9,
        itemsDesktop: [1350, 9],
        itemsDesktopSmall: [979, 7],
        itemsTablet: [767, 6],
        itemsMobile: [479, 5],
        pagination: false,
        responsiveRefreshRate: 100
    };
    var optionsRTL = {
        navigation: true,
        lazyLoad : true,
        loop: true,
        navigationText: [
            "<i class='icon-find-arrow-prev'></i>",
            "<i class='icon-find-arrow-next'></i>"
        ],
        items: 9,
        itemsDesktop: [1350, 9],
        itemsDesktopSmall: [979, 7],
        itemsTablet: [767, 6],
        itemsMobile: [479, 5],
        pagination: false,
        responsiveRefreshRate: 100,
        direction: 'rtl'
    };
    var find_service_gallery_init = function() {
        var $galleries = $('.find-gallery-multiply');
        var carousel_options;
        if ($body.attr('id') == 'arabic') {
            carousel_options = optionsRTL;
        } else {
            carousel_options = optionsLTR;
        }
        var $not_initialized_galleries = $galleries.filter(function(){
            return typeof ($(this).data('owl-init')) === 'undefined';
        });

        $not_initialized_galleries.owlCarousel(carousel_options);

        var $find_gallery_preview = $('.find-gallery-preview');
        $find_gallery_preview.animate({"opacity": "1"}, 700);
        $find_gallery_preview.on('load', function() {
            $(this).animate({"opacity": "1"}, 100);
        });
    };
    find_service_gallery_init();

    $body.on('click', '.find-gallery-multiply .owl-item', function (e) {
        var $this = $(this);
        $this.siblings().removeClass('currentSlide');
        if($this.hasClass('currentSlide')){
          $this.removeClass('currentSlide');
        } else{
          $this.addClass('currentSlide');
        }

        e.preventDefault();

        var mainImg = $('#' + $(this).parents('.find-gallery-multiply').attr('data-previewId'));
        var newSrc = $(this).children('.item').attr('data-bigImg');
        if (mainImg.attr('src') == newSrc) {
            return;
        }
        // mainImg.animate({"opacity": "0"}, 100);
        mainImg.animate({"opacity": "0.5"}, 100);
        mainImg.attr('src', newSrc);
    });


    //img gallery end

    //rateit start
    var init_rateit_score_on_find_hotel_page = function () {
        $('#rateit').raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            path: RATEIT_ICONS_BASE_PATH,
            starOn: 'ratestar-wt19.png',
            starOff: 'ratestar-tr19.png',
            hints: ['', '', '', '', ''],
            click: function(newScore) {
                var prevScore = $('input[name="score"]').val();
                if (newScore != prevScore) {
                    var $form = $('#search-form');
                    $form.find('input[name="rating"]').val(newScore);
                    $form.find('#id_from_price, #id_to_price').remove();
                    $form.trigger('submit');
                }
                //alert('ID: ' + this.id + "\nscore: " + newScore + "\nevent: " + evt + "\nprev: " + );
            }
        });
    };
    init_rateit_score_on_find_hotel_page();
    var createhotelrate_init = function() {
        $('#createHotelRate').raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            path: RATEIT_ICONS_BASE_PATH,
            starOn: 'rate-a.png',
            starOff: 'rate-b.png',
            hints: ['', '', '', '', ''],
            click: function (newScore) {
                var $select = $('select[name="rating"]');
                var prevScore = $select.val();
                if (newScore != prevScore) {
                    $select.val(newScore);
                }
                //alert('ID: ' + this.id + "\nscore: " + newScore + "\nevent: " + evt + "\nprev: " + );
            }
        });
    };
    createhotelrate_init();
    //rateit end

    //rateit start
    // var disabled_stars_init = function() {
    //     $('.rate-disable').raty({
    //         number: 5,
    //         score: function () {
    //             return $(this).attr('data-score');
    //         },
    //         readOnly: true,
    //         path: RATEIT_ICONS_BASE_PATH,
    //         starOn: 'rate-a.png',
    //         starOff: 'rate-b.png',
    //         hints: ['', '', '', '', '']
    //     });
    // };
    // disabled_stars_init();
    //rateit end

    var set_business_header_and_text = function($element) {
        $('.business-header').html($element.attr('data-header'));
        $('.business-text-description').html($element.attr('data-text'));
    };

    var $business_login_tab = $('#tab-owner-login');
    if ($business_login_tab.length > 0) {
        set_business_header_and_text($business_login_tab);
    }

    /*
    replace text/header here if login tab is active now
     */
    $body.on('click', '#tab-owner-login', function () {
        set_business_header_and_text($(this));
    });

    /*
    replace text/header here if register tab is active now
     */
    $body.on('click', '#tab-owner-register', function () {
        var $selected_business_type = $('.bus-type-selected');
        set_business_header_and_text($selected_business_type);
    });

    //reg form onclick start
    $body.on('click', '.signup-form__type-item', function (e) {
        $('#js-empty__bustype').removeClass('bus-type-selected');
        $('.signup-form__type-item').removeClass('bus-type-selected');
        $(this).toggleClass('bus-type-selected');
        var val = $(this).attr('data-value');
        $('#id_service_type').val(val);

        /*
        replace text/header according to current service type
         */
        set_business_header_and_text($(this));
    });
    /* set initial selected service type icon */
    function init_service_type() {
        var initial = $('#id_service_type').val();
        if (isNaN(parseInt(initial))) {
            $('#js-empty__bustype').addClass('bus-type-selected');
        } else {
            $('.signup-form__type-item[data-value="' + initial + '"]').addClass('bus-type-selected');
        }
    }
    init_service_type();
    //reg form onclick end


    $body.on('focusin', 'input', function() {
        var input = $(this);
        input.data('place-holder-text', input.attr('placeholder'));
        input.attr('placeholder', '');
    });

    $body.on('focusout', 'input', function() {
        var input = $(this);
        input.attr('placeholder', input.data('place-holder-text'));
    });
    $body.on('focusout', 'input', function() {
        var input = $(this);
        input.attr('placeholder', input.data('place-holder-text'));
    });
    // business owner login&signup forms start
    $body.on('submit', '.ajax-form', function () {
        var $form = $(this);
        $form.ajaxSubmit({
            success: function (resp) {
                window.location = resp['location'];
            },
            error: function (resp) {
                $form.replaceWith(resp.responseJSON.html);
                init_service_type();
                init_terms_and_privacy_popup();
            }
        });
        return false;
    });
    $body.on('change', '.js-country-dropdown', function () {
        var $phone_field = $('.js-phone-field'),
            $this = $(this),
            new_country = $this.val();
        
        if (new_country !== '') {
            var prev_phone_code = $this.attr('data-prev-phone-code'),
                new_phone_code = $this.find('option[value=' + new_country + ']').attr('data-phone-code'),
                phone_field_val = $phone_field.val();

            if (phone_field_val == prev_phone_code || phone_field_val == '') {
                $phone_field.val(new_phone_code);
                $this.attr('data-prev-phone-code', new_phone_code);
            }
        }
    });
    // business owner login&signup forms end
    // find hotel/apartment filter form start
    var services_pagination_on_scroll = function() {
        var $showmore_btn = $('.find__showmore-btn-link.find-page');
        if ($showmore_btn.length > 0) {
            $(window).scroll(function(){
                if  ($(window).scrollTop() > $showmore_btn.offset().top - 2 * $(window).height()){
                    $(window).off('scroll');
                    var $showmore_panel = $showmore_btn.parent();
                    var $find_hotel_list = $('#find-hotel-list');
                    var $form = $('#search-form');
                    var prev_val = $find_hotel_list.attr('data-page');
                    $find_hotel_list.attr('data-page', parseInt(prev_val) + 1);
                    $form.ajaxSubmit({
                        beforeSubmit: function(contentArray, $form, options) {
                        for (var i = 0; i< contentArray.length; i++) {
                            if(contentArray[i].name == "page") {
                                    contentArray[i].value = $find_hotel_list.attr('data-page');
                                }
                            }
                        },
                        success: function (resp) {
                            $showmore_panel.remove();
                            var $resp = $(resp);
                            $find_hotel_list.find('.find__article:last').after($resp);
                            services_pagination_on_scroll();
                            find_service_gallery_init();
                            init_single_image_gallery();
                            text_ellipsis();
                        },
                        error: function (resp) {
                            console.log(resp);
                        }
                    });
                }
            });
        }
    };
    services_pagination_on_scroll();
    $body.on('change', '#search-form input[name=type]', function () {
        if ($('input[name="type"]:checked').length == 0) {
            //$(this).prop('checked', 'checked');
            noty({text: $('.js-service-with-type-filter-search').attr('data-warning-msg'), type: 'warning'});
        } else {
            var $form = $('#search-form');
            $form.find('#id_from_price, #id_to_price').remove();
            $form.find('#id_room_num_from, #id_room_num_to').remove();
            $form.trigger('submit');
        }
    });
    $body.on('submit', '#search-form', function () {
        var $find_hotel_list = $('#find-hotel-list');
        $(this).ajaxSubmit({
            beforeSubmit: function(contentArray, $form, options) {
            for (var i = 0; i< contentArray.length; i++) {
                if(contentArray[i].name == "page") {
                        contentArray[i].value = 1;
                    }
                }
            },
            success: function (resp) {
                $find_hotel_list.attr('data-page', 1);
                $find_hotel_list.html(resp);
                var data = $('#search-form').serialize();
                var url = '?' + data;
                History.pushState('', '', url);
                services_pagination_on_scroll();
                find_service_gallery_init();
                init_price_slider_on_find_pages();
                init_room_num_slider_on_find_apts();
                init_rateit_score_on_find_hotel_page();
                init_single_image_gallery();
                text_ellipsis();
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        return false;
    });
    // find hotel/apartment filter form end
    $body.on('click', '.js-service-with-type-filter-search', function(){
        if ($('input[name="type"]:checked').length == 0) {
            noty({text: $(this).attr('data-warning-msg'), type: 'warning'});
            return false;
        }
    });
    // cabinet tabs start
    //profiles avatar image actions start
    $body.on('click', '.change-avatar-link', function() {
        $('.change-avatar-button').trigger('click');
    });
    $body.on('change', '.change-avatar-button', function() {
        var $file_summary = $(this).siblings('.cabinet__info-title');
        var files = $(this).prop('files');
        if (files.length > 0) {
            var file_names = [];
            $.each($(this).prop('files'), function (idx, file) {
                file_names.push(file.name);
            });
            $file_summary.find('.file-names').text(file_names.join(', '));
            $file_summary.show();
        } else {
            $file_summary.hide();
        }
    });
    //profiles avatar image actions end
    //hotel form featured image actions start
    $body.on('click', '.delete-featured-image-link', function() {
        var $checkbox = $('#featured_image-clear_id');
        var prevVal = $checkbox.prop('checked');
        $checkbox.prop('checked', !prevVal);
        var $image = $(this).siblings('.cabinet__hotel-pic').find('img');
        $(this).toggleClass('on_delete');
        $image.toggleClass('waiting_for_delete');
    });
    var init_progress_box = function($progress_box) {
        var $progress = $progress_box.find('.progress .progress-bar');
        $progress.attr('data-transitiongoal', 0).progressbar({display_text: 'fill', transition_delay: 0});
        $progress_box.show();
    };
    var update_progress_box = function($progress_box, position, total, percent) {
        var $progress = $progress_box.find('.progress .progress-bar');
        $progress_box.find('.js-uploaded-size').text(formatBytes(position));
        $progress_box.find('.js-total-size').text(formatBytes(total));
        $progress.attr('data-transitiongoal', percent).progressbar({display_text: 'fill', transition_delay: 0});
    };
    var destroy_progress_box = function($progress_box) {
        var $progress = $progress_box.find('.progress .progress-bar');
        $progress_box.hide();
        $progress_box.find('.js-uploaded-size').text(0);
        $progress_box.find('.js-total-size').text(0);
        $progress.attr('data-transitiongoal', 0).progressbar({display_text: 'fill', transition_delay: 0});
    };
    var featured_image_change_btn_click = function() {
        $('#id_featured_image').click();
    };
    $body.on('click', '.change-featured-image-link', featured_image_change_btn_click);
    $body.on('change', '#id_featured_image', function() {
        var file_objects = $(this).prop('files');
        if (file_objects.length > 0) {
            var $form = $('#featured-image-form');
            var cancel_label = $form.attr('data-cancel-label');
            var $that = $(this);
            var $link = $('.js-add-featured-before-this-block');
            var $pk_field = $('#id_featured_image_pk');
            var type = 'featured';
            $form.ajaxSubmit({
                success: function(resp) {
                    if ('status' in resp && resp['status'] === 'success') {
                        var valid_images = resp['valid'];
                        if (valid_images.length > 0) {
                            var source   = $("#photos-template").html();
                            var template = Handlebars.compile(source);
                            var context = {files: valid_images, cancel_label: cancel_label, type: type};
                            var html = template(context);

                            var $old_image = $('.js-existing-featured-image').find('img'),
                            old_image_exists = $old_image.length > 0,
                            $change_btn = $('.js-change-featured-image-btn'),
                            $crop_btn = $('.js-crop-featured-image-btn'),
                            $featured_stub = $('.js-featured-image-stub'),
                            featured_stub_exists = $featured_stub.length > 0,
                            $add_featured_image_btn = $('.js-featured-image-add-btn');
                            if (old_image_exists) {
                                $old_image.addClass('waiting_for_delete');
                                $change_btn.hide();
                                $crop_btn.hide();
                            } else if (featured_stub_exists) {
                                $featured_stub.hide();
                                $add_featured_image_btn.hide();
                            }
                            $link.before(html);
                            $pk_field.val(valid_images[0]['pk']);
                        }
                        $.each(resp['invalid'], function(idx, val) {
                            noty({text: val, type: 'warning'});
                        });
                    } else {
                        console.log('AjaxUploadImages.debug: unpredicted error has occurred.');
                    }
                    // clear file input after work is done
                    $that.replaceWith($that = $that.clone(true));
                },
                error: function(resp) {
                    console.log(resp);
                    if (resp.status === 413) {
                        var request_exceeded_max_msg = $('.js-service-container').attr('data-request-exceeded-maximum');
                        noty({text: request_exceeded_max_msg, type: 'warning'});
                    }
                    //destroy_progress_box($('.js-featured-image-upload-progress'));
                    //$('.change-featured-image-link').css({opacity: 1});
                    //$body.on('click', '.change-featured-image-link', featured_image_change_btn_click);
                },
                uploadProgress: function(event, position, total, percent) {
                    update_progress_box($('.js-featured-image-upload-progress'), position, total, percent);
                },
                // this is required here to override default behaviour during ajax queries defined in ajaxSetup
                beforeSend: function(xhr, settings) {
                    init_progress_box($('.js-featured-image-upload-progress'));
                    addXCSRFHeader(xhr, settings);
                    $('.change-featured-image-link').css({opacity: 0.3});
                    $body.off('click', '.change-featured-image-link');
                },
                complete: function() {
                    destroy_progress_box($('.js-featured-image-upload-progress'));
                    $('.change-featured-image-link').css({opacity: 1});
                    $body.on('click', '.change-featured-image-link', featured_image_change_btn_click);
                }
            });
        }
    });
    //hotel form featured image actions end
    var multiple_images_upload_btn_click = function() {
        $('#id_multiple_images').click();
    };
    $body.on('click', '.multiple-images-link', multiple_images_upload_btn_click);
    $body.on('change', '#id_multiple_images', function() {
        var file_objects = $(this).prop('files');
        if (file_objects.length > 0) {
            var $form = $('#multiple-images-form');
            var cancel_label = $form.attr('data-cancel-label');
            var $that = $(this);
            var $link = $('.js-add-images-before-this-block');
            var type = 'multiple';
            $form.ajaxSubmit({
                success: function(resp) {
                    if ('status' in resp && resp['status'] === 'success') {
                        var valid_images = resp['valid'];
                        if (valid_images.length > 0) {
                            var source   = $("#photos-template").html();
                            var template = Handlebars.compile(source);
                            var context = {files: valid_images, cancel_label: cancel_label, type: type};
                            var html = template(context);
                            $link.before(html);
                            var $gallery_stub = $('.js-gallery-images-stub');
                            if ($gallery_stub.length > 0 && $gallery_stub.is(':visible')) {
                                $gallery_stub.hide();
                            }
                            var $pk_field = $('#id_multiple_image_pk'),
                                current_val = $pk_field.val();
                            if (current_val) {
                                current_val += ','
                            }
                            $.each(valid_images, function(idx, img) {
                                current_val += img['pk'] + ',';
                            });
                            $pk_field.val(current_val.slice(0, current_val.length - 1));
                        }
                        $.each(resp['invalid'], function(idx, val) {
                            noty({text: val, type: 'warning'});
                        });
                    } else {
                        console.log('AjaxUploadImages.debug: unpredicted error has occurred.');
                    }
                    // clear file input after work is done
                    $that.replaceWith($that = $that.clone(true));
                },
                error: function(resp) {
                    console.log(resp);
                    if (resp.status === 413) {
                        var request_exceeded_max_msg = $('.js-service-container').attr('data-request-exceeded-maximum');
                        noty({text: request_exceeded_max_msg, type: 'warning'});
                    }
                },
                uploadProgress: function(event, position, total, percent) {
                    update_progress_box($('.js-multiple-images-upload-progress'), position, total, percent);
                },
                // this is required here to override default behaviour during ajax queries defined in ajaxSetup
                beforeSend: function(xhr, settings) {
                    init_progress_box($('.js-multiple-images-upload-progress'));
                    addXCSRFHeader(xhr, settings);
                    $('.multiple-images-link').css({opacity: 0.3});
                    $body.off('click', '.multiple-images-link');
                },
                complete: function() {
                    destroy_progress_box($('.js-multiple-images-upload-progress'));
                    $('.multiple-images-link').css({opacity: 1});
                    $body.on('click', '.multiple-images-link', multiple_images_upload_btn_click);
                }
            });
        }
    });
    $body.on('click', '.js-cancel-image', function() {
        var $this = $(this),
            pk = $this.attr('data-pk'),
            data = {pk: pk},
            $container = $('.js-service-container'),
            url = $container.attr('data-delete-image-url'),
            $pic_block = $(this).closest('.pic-item'),
            type = $pic_block.attr('data-type');
        $.post(url, data, function(resp) {
            if ('status' in resp && resp['status'] === 'success') {
                $pic_block.remove();
                if (type === 'featured') {
                    // clear field
                    $('#id_featured_image_pk').val('');
                    var $old_image = $('.js-existing-featured-image').find('img'),
                    old_image_exists = $old_image.length > 0,
                    $change_btn = $('.js-change-featured-image-btn'),
                    $crop_btn = $('.js-crop-featured-image-btn'),
                    $featured_stub = $('.js-featured-image-stub'),
                    featured_stub_exists = $featured_stub.length > 0,
                    $add_featured_image_btn = $('.js-featured-image-add-btn');
                     if (old_image_exists) {
                        $old_image.removeClass('waiting_for_delete');
                        $change_btn.show();
                        $crop_btn.show();
                    } else if (featured_stub_exists) {
                        $featured_stub.show();
                        $add_featured_image_btn.show();
                    }
                } else if (type == 'multiple') {
                    var $pk_field = $('#id_multiple_image_pk'),
                        prev_val = $pk_field.val(),
                        values = prev_val.split(',');
                    if (values.length > 1) {
                        var new_val = '';
                        $.each(values, function(idx, val) {
                            if (val !== pk) {
                                new_val += val + ',';
                            }
                        });
                        $pk_field.val(new_val.slice(0, new_val.length - 1));
                    } else {
                        var $gallery_stub = $('.js-gallery-images-stub');
                        if ($gallery_stub.length > 0 && !$gallery_stub.is(':visible')) {
                            $gallery_stub.show();
                        }
                        $pk_field.val('');
                    }
                }
            }
        });

        //var $checkbox = $(this).closest('.pic-item').find('.delete-image-checkbox');
        //var prevVal = $checkbox.prop('checked');
        //$checkbox.prop('checked', !prevVal);
        //var $image = $(this).siblings('.cabinet__hotel-pic').find('img');
        //$(this).toggleClass('on_delete');
        //$image.toggleClass('waiting_for_delete');
    });
    //hotel form multiple images actions start
    $body.on('click', '.change-image-link', function() {
        $(this).siblings('.change-image-button').trigger('click');
    });
    $body.on('click', '.delete-image-link', function() {
        var $checkbox = $(this).closest('.pic-item').find('.delete-image-checkbox');
        var prevVal = $checkbox.prop('checked');
        $checkbox.prop('checked', !prevVal);
        var $image = $(this).siblings('.cabinet__hotel-pic').find('img');
        $(this).toggleClass('on_delete');
        $image.toggleClass('waiting_for_delete');
    });
    //hotel form multiple images actions end
    //room list start
    $body.on('click', '.ajax-delete-room', function(e) {

        var $this = $(this),
            confirm_message = $this.attr('data-confirm-message'),
            approval_word = $this.attr('data-approval-word'),
            decline_word = $this.attr('data-decline-word'),
            success_message = $this.attr('data-success-message'),
            url = $this.attr('href'),
            $room_tr = $this.closest('.cabinet__room-tr'),
            $rooms_trs = $this.closest('.js-rooms-list'),
            $rooms_block = $this.closest('.js-rooms-block');
        noty({
            text: confirm_message,
            type: 'confirm',
            dismissQueue: false,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'cabinet__approve', text: approval_word, onClick: function($noty) {

                        // this = button element
                        // $noty = $noty element

                        $noty.close();
                        $.post(url, function( data ) {
                            if (data['status'] === 'success') {
                                if ($rooms_trs.children().length == 1) {
                                    $rooms_block.remove();
                                } else {
                                    $room_tr.remove();
                                }
                                noty({text: success_message, type: 'success'});
                            } else {
                                noty({text: data['message'], type: 'error'});
                            }
                        });
                    }
                },
                {
                    addClass: 'cabinet__decline', text: decline_word, onClick: function($noty) {
                        $noty.close();
//                        noty({text: 'You clicked "Cancel" button', type: 'error'});
                    }
                }
            ]
        });
        e.preventDefault();
        return false;
    });
    var timeout_submits = {};
    var send_allotment = function(id) {
        delete timeout_submits[id];
        var $input = $("#" + id);
        var url = $input.attr('data-url');
        $.post(url, {val: $input.val()}, function(resp) {
            if (resp['status'] === "fail") {
                console.log(resp["message"]);
            }
        });
    };
    var cancel_submit = function(key) {
        if (key in timeout_submits) {
            var timeout_submit = timeout_submits[key];
            if(typeof timeout_submit == "number") {
                window.clearTimeout(timeout_submit);
            }
        }
    };
    $body.on('click', '.plus-this', function(){
        var $this = $(this);
        var $container = $this.closest('.cabinet__allotment');
        var $qty = $container.find('.change-value');
        var timeout_key = $qty.attr('id');
        cancel_submit(timeout_key);
        var currVal = parseInt($qty.val());
        var newVal = currVal + 1;
        $qty.val(newVal);
        $container.find('.current-value').text(newVal);
        timeout_submits[timeout_key] = setTimeout(send_allotment, 500, timeout_key)
    });
    $body.on('click', '.minus-this', function(){
        var $this = $(this);
        var $container = $this.closest('.cabinet__allotment');
        var $qty = $container.find('.change-value');
        var timeout_key = $qty.attr('id');
        var currVal = parseInt($qty.val());
        if (currVal > 0) {
            cancel_submit(timeout_key);
            var newVal = currVal - 1;
            $qty.val(newVal);
            $container.find('.current-value').text(newVal);
            timeout_submits[timeout_key] = setTimeout(send_allotment, 500, timeout_key)
        }
    });
    $body.on('change', '.ajax-show-on-site-attr-change', function() { //room, apartment
        var $this = $(this);
        var val = $this.prop('checked');
        var url = $this.attr('data-url');
        var data = val ? {enable: ""} : {};
        $.post(url, data, function(resp) {
            if (resp['status'] === "fail") {
                console.log(resp["message"])
            }
        });
    });
    //room list end
    //apt list start
    $body.on('click', '.ajax-delete-apt', function() {

        var $this = $(this),
            confirm_message = $this.attr('data-confirm-message'),
            approval_word = $this.attr('data-approval-word'),
            decline_word = $this.attr('data-decline-word'),
            success_message = $this.attr('data-success-message'),
            url = $this.attr('href'),
            $apt_tr = $this.closest('.cabinet__room-tr'),
            $apts_trs = $this.closest('.js-apts-list'),
            $apts_block = $this.closest('.js-apts-block');
        noty({
            text: confirm_message,
            type: 'confirm',
            dismissQueue: false,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'cabinet__approve', text: approval_word, onClick: function($noty) {

                        // this = button element
                        // $noty = $noty element

                        $noty.close();
                        $.post(url, function( data ) {
                            if (data['status'] === 'success') {
                                if ($apts_trs.children().length == 1) {
                                    $apts_block.remove();
                                } else {
                                    $apt_tr.remove();
                                }
                                noty({text: success_message, type: 'success'});
                            } else {
                                noty({text: data['message'], type: 'error'});
                            }
                        });
                    }
                },
                {
                    addClass: 'cabinet__decline', text: decline_word, onClick: function($noty) {
                        $noty.close();
//                        noty({text: 'You clicked "Cancel" button', type: 'error'});
                    }
                }
            ]
        });
        return false;
    });
    var init_calendars_on_create_offline_booking_page = function() {
        var $from = $(".from_date_offline_booking"), $to = $(".to_date_offline_booking");
        $from.datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            onClose: function( selectedDate ) {
                if (selectedDate !== '') {
                    var $this = $(this);
                    limitDepartureDateOnArrivalDateClose($this, $('.to_date_offline_booking'))
                }
            }
        });
        $to.datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            beforeShow: function() {
                var $this = $(this);
                limitDepartureDateOnDepartureBeforeShow($('.from_date_offline_booking'), $this);
            }
        });
    };
    init_calendars_on_create_offline_booking_page();
    //apt list end
    //room form special price actions start
    var init_calendars_on_create_room_page = function($elem) {
        var $from = $elem.find(".from_date_input"), $to = $elem.find(".to_date_input");
        $from.datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            beforeShow: function() {
                var $this = $(this),
                    today = new Date(),
                    curr_date = $this.datepicker('getDate');
                var min_date;
                if (curr_date === null || curr_date >= today) {
                    min_date = '0'
                } else {
                    min_date = curr_date;
                }
                $this.datepicker('option', 'minDate', min_date);
            },
            onClose: function( selectedDate ) {
                if (selectedDate !== '') {
                    var $this = $(this);
                    limitDepartureDateOnArrivalDateClose($this, $this.closest(".special-price-block").find('.to_date_input'))
                }
            }
        });
        $to.datepicker({
            dateFormat: 'dd.mm.yy',
            numberOfMonths: 1,
            beforeShow: function() {
                var $this = $(this);
                limitDepartureDateOnDepartureBeforeShow($this.closest(".special-price-block").find('.from_date_input'), $this);
            }
        });
    };
    init_calendars_on_create_room_page($(".special-price-block:visible, .existing-room"));
    $body.on('click', '.delete-price-link', function() {
        var $checkbox = $(this).closest('.cabinet__room-tr').find('.delete-price-checkbox');
        var prevVal = $checkbox.prop('checked');
        $checkbox.prop('checked', !prevVal);
        $(this).toggleClass('on_delete');
    });
    $body.on('click', '.js-delete-existent-special-price', function() {
        var $this = $(this);
        var $special_price_block = $this.closest('.special-price-block');
        var $delete_checkbox = $special_price_block.find('.js-delete-special-price-checkbox');
        $delete_checkbox.prop('checked', true);
        $special_price_block.addClass('on_removal');
    });
    $body.on('click', '.js-restore-special-price-link', function() {
        var $this = $(this);
        var $special_price_block = $this.closest('.special-price-block');
        var $delete_checkbox = $special_price_block.find('.js-delete-special-price-checkbox');
        $delete_checkbox.prop('checked', false);
        $special_price_block.removeClass('on_removal');
    });
    $body.on('click', '.js-delete-non-existent-special-price', function() {
        var $this = $(this);
        var $special_price_block = $this.closest('.special-price-block');
        $special_price_block.remove();
    });
    $body.on('click', '.ajax-add-price-category-form-link', function() {
        var $this = $(this);
        var $add_before_this_block = $this;
        var url = $this.attr('data-url');
        $.ajax({
            url: url,
            success: function(resp) {
                if ('html' in resp) {
                    var $new_category_form = $(resp['html']);
                    $new_category_form.insertBefore($add_before_this_block);
                    init_selects_on_create_room_page($new_category_form);
                    init_calendars_on_create_room_page($new_category_form.find(".special-price-block:visible"));
                }
            },
            error: function(resp) {
                console.log(resp);
            }
        });
        return false;
    });
    $body.on('submit', '.ajax-price-category-submit', function() {
        var $form = $(this);
        $form.ajaxSubmit({
            success: function (resp) {
                if ('html' in resp) {
                    var $category_form = $(resp['html']);
                    if ($category_form.is('form')) {
                        $form.replaceWith($category_form);
                        init_selects_on_create_room_page($category_form);
                        init_calendars_on_create_room_page($category_form.find(".special-price-block:visible"));
                    } else {
                        // if it is update form of existing category then replace this form with its new view
                        if ($form.attr("data-update_view") === "True") {
                            $form.replaceWith($category_form);
                        } else {
                            $form.remove();
                            $(".cabinet__hotel > .js-saved-price-categories-header").after($category_form);
                        }
                    }
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        return false;
    });
    $body.on('click', '.ajax-cancel-category-edit', function() {
        var $form = $(this).closest('form');
        // if it is update form of existing category then return back its view
        if ($form.attr("data-update_view") === "True") {
            var view_url = $form.attr('data-view-url');
            $.ajax({
                url: view_url,
                success: function(resp) {
                    if ('html' in resp) {
                        $form.replaceWith($(resp['html']));
                    }
                },
                error: function(resp) {
                    console.log(resp);
                }
            });
        } else {
            $form.remove();
        }
        return false;
    });
    $body.on('click', '.ajax-edit-category', function(e) {
        var $this = $(this);
        var url = $this.attr('data-url');
        var $view = $this.closest(".cabinet__price__category");
        $.ajax({
            url: url,
            success: function(resp) {
                if ('html' in resp) {
                    var $new_category_form = $(resp['html']);
                    $view.replaceWith($new_category_form);
                    init_selects_on_create_room_page($new_category_form);
                    init_calendars_on_create_room_page($new_category_form.find(".special-price-block:visible"));
                }
            },
            error: function(resp) {
                console.log(resp);
            }
        });
    });
    $body.on('click', '.ajax-delete-category', function() {
        var confirm_message = $(this).attr('data-confirm-message'),
            approval_word = $(this).attr('data-approval-word'),
            decline_word = $(this).attr('data-decline-word'),
            success_message = $(this).attr('data-success-message'),
            url = $(this).attr('href'),
            $category = $(this).closest('.cabinet__price__category');
        noty({
            text: confirm_message,
            type: 'confirm',
            dismissQueue: false,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'cabinet__approve', text: approval_word, onClick: function($noty) {
                        // this = button element
                        // $noty = $noty element
                        $noty.close();
                        $.post(url, function( data ) {
                            if (data['status'] === 'success') {
                                $category.remove();
                                noty({text: success_message, type: 'success'});
                            } else {
                                noty({text: data['message'], type: 'error'});
                            }
                        });
                    }
                },
                {
                    addClass: 'cabinet__decline', text: decline_word, onClick: function($noty) {
                        $noty.close();
                    }
                }
            ]
        });
        return false;
    });
    $body.on('click', '.js-show-more-hidden-special-price', function() {
        var $prices_container = $(this).closest('.special-prices-container');
        var $hidden_price_block = $prices_container.find('.special-price-block:hidden:first');
        $hidden_price_block.show();
        init_calendars_on_create_room_page($hidden_price_block);
    });
    $body.on('click', '.ajax-delete-special-price', function() {
        var confirm_message = $(this).attr('data-confirm-message'),
            approval_word = $(this).attr('data-approval-word'),
            decline_word = $(this).attr('data-decline-word'),
            success_message = $(this).attr('data-success-message'),
            url = $(this).attr('href'),
            $special_price = $(this).closest('.cabinet__room-tr');
        noty({
            text: confirm_message,
            type: 'confirm',
            dismissQueue: false,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'cabinet__approve', text: approval_word, onClick: function($noty) {
                        // this = button element
                        // $noty = $noty element
                        $noty.close();
                        $.post(url, function( data ) {
                            if (data['status'] === 'success') {
                                $special_price.remove();
                                noty({text: success_message, type: 'success'});
                            } else {
                                noty({text: data['message'], type: 'error'});
                            }
                        });
                    }
                },
                {
                    addClass: 'cabinet__decline', text: decline_word, onClick: function($noty) {
                        $noty.close();
                    }
                }
            ]
        });
        return false;
    });
    //room form special price actions end
    //apt form special price actions start
    $body.on('click', '.ajax-add-apt-price-category-form-link', function() {
        var $this = $(this);
        var $add_before_this_block = $this;
        var url = $this.attr('data-url');
        $.ajax({
            url: url,
            success: function(resp) {
                if ('html' in resp) {
                    var $new_category_form = $(resp['html']);
                    $new_category_form.insertBefore($add_before_this_block);
                    $add_before_this_block.hide();
                    init_selects_on_create_room_page($new_category_form);
                    init_calendars_on_create_room_page($new_category_form.find(".special-price-block:visible"));
                }
            },
            error: function(resp) {
                console.log(resp);
            }
        });
        return false;
    });
    $body.on('click', '.ajax-cancel-apt-category-edit', function() {
        var $form = $(this).closest('form');
        // if it is update form of existing category then return back its view
        if ($form.attr("data-update_view") === "True") {
            var view_url = $form.attr('data-view-url');
            $.ajax({
                url: view_url,
                success: function(resp) {
                    if ('html' in resp) {
                        $form.replaceWith($(resp['html']));
                    }
                },
                error: function(resp) {
                    console.log(resp);
                }
            });
        } else {
            $form.remove();
            $('.ajax-add-apt-price-category-form-link').show();
        }
        return false;
    });
    $body.on('submit', '.ajax-apt-price-category-submit', function() {
        var $form = $(this);
        $form.ajaxSubmit({
            success: function (resp) {
                if ('html' in resp) {
                    var $category_form = $(resp['html']);
                    if ($category_form.is('form')) {
                        $form.replaceWith($category_form);
                        init_selects_on_create_room_page($category_form);
                        init_calendars_on_create_room_page($category_form.find(".special-price-block:visible"));
                    } else {
                        // if it is update form of existing category then replace this form with its new view
                        if ($form.attr("data-update_view") === "True") {
                            $form.replaceWith($category_form);
                        } else {
                            $form.remove();
                            $('.js-add-price-categories-header').hide();
                            var $header = $(".cabinet__hotel > .js-saved-price-categories-header");
                            $header.show();
                            $header.after($category_form);
                        }
                    }
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        return false;
    });
    $body.on('click', '.ajax-delete-apt-price-category', function() {
        var confirm_message = $(this).attr('data-confirm-message'),
            approval_word = $(this).attr('data-approval-word'),
            decline_word = $(this).attr('data-decline-word'),
            success_message = $(this).attr('data-success-message'),
            url = $(this).attr('href'),
            $category = $(this).closest('.cabinet__price__category');
        noty({
            text: confirm_message,
            type: 'confirm',
            dismissQueue: false,
            layout: 'center',
            theme: 'defaultTheme',
            buttons: [
                {
                    addClass: 'cabinet__approve', text: approval_word, onClick: function($noty) {
                        // this = button element
                        // $noty = $noty element
                        $noty.close();
                        $.post(url, function( data ) {
                            if (data['status'] === 'success') {
                                $category.remove();
                                $('.js-saved-price-categories-header').hide();
                                $('.js-add-price-categories-header').show();
                                $('.ajax-add-apt-price-category-form-link').show();
                                noty({text: success_message, type: 'success'});
                            } else {
                                noty({text: data['message'], type: 'error'});
                            }
                        });
                    }
                },
                {
                    addClass: 'cabinet__decline', text: decline_word, onClick: function($noty) {
                        $noty.close();
                    }
                }
            ]
        });
        return false;
    });
    $body.on('submit', '.ajax-apt-options-submit', function() {
        var $form = $(this);
        $form.ajaxSubmit({
            success: function (resp) {
                if ('html' in resp) {
                    var $options_form = $(resp['html']);
                    $form.replaceWith($options_form);
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        return false;
    });
    //apt form special price actions end
    // transport, sport, excursions, entertainment time-based discount prices start
    $body.on('click', '.js-clear-non-existent-discount-block', function() {
        var $this = $(this);
        var $discount_block = $this.closest('.js-discount-block');

        $discount_block.find('.js-clear-this-input').val('');
    });
    $body.on('click', '.js-show-more-hidden-discount-price-blocks', function() {
        var $prices_container = $(this).closest('.js-discount-blocks-container');
        var $hidden_discount_block = $prices_container.find('.js-discount-block:hidden:first');
        $hidden_discount_block.show();
        if ($('.js-discount-block:hidden').length === 0) {
            $(this).closest('.cabinet__hotel-block').hide();
        }
    });
    // transport, sport, excursions, entertainment time-based discount prices end

    //item-based time-based start
    var check_related_item_type_radio = function($tag) {
        if (typeof $tag === 'undefined') {
            $tag = $('select.js-item-type-dropdown');
        }

        var new_val = $tag.val(),
            related_radio_id = $tag.find('option[value=' + new_val + ']').attr('data-related-radio-id'),
            $related_radio = $('#' + related_radio_id);

        if ($related_radio.length > 0) {
            $related_radio.prop('checked', 'checked');
        }
    };
    check_related_item_type_radio();
    $body.on('change', 'select.js-item-type-dropdown', function() {
        check_related_item_type_radio($(this));

        // initially it's processed correctly (displayed or hidden) so any further change of two values requires just
        // toggling back and forth
        $('.js-discount-prices-core-block').toggle();
    });
    //item-based time-based end
    //cartitem delete start
    $body.on('click', '.delete-cartitem-link', function(e) {
        var url = $(this).attr('href');
        $.post(url, function(resp) {
            if (resp['status'] == 'success') {
                location.reload();
            } else {
                console.log(resp['message']);
            }
        });
        e.preventDefault();
        return false;
    });
    //cartitem delete end
    //my owner bookings start
    $body.on('click', '.change-orderitem', function(e) {
        var success_message = $(this).attr('data-success-message'),
            url = $(this).attr('data-url'),
            action = $(this).attr('data-action'),
            $booking_tr = $(this).closest('.cabinet__book-tr');
        $.post(url, {action: action}, function( data ) {
            if (data['status'] === 'success') {
                $booking_tr.html(data['html']);
                init_select2_status(0, $booking_tr.find(".select-status"));
                noty({text: success_message, type: 'success'});
            } else {
                noty({text: data['message'], type: 'error'});
            }
        });
        e.preventDefault();
        return false;
    });
    //my owner bookings end
    var tab_elements_init = function() {
        show_messages();
        // edit profile
        init_country_dropdown_on_profile_edit_page($(".country-select-profile-edit-page"));
        // create/update hotel tab
        createhotelrate_init();
        // create/update room tab
        init_selects_on_create_room_page($body);
        // business owner bookings tab
        init_select2_statuses_array($('.select-status'));
        // create offline booking tab
        init_calendars_on_create_offline_booking_page();
        if (typeof(image_cropping) !== "undefined") {
            image_cropping.init();
        }
        check_related_item_type_radio();
    };
    $body.on('click', '.ajax-change-tab', function () {
        var $tab = $(this);
        var url = $tab.attr('data-url');
        $.ajax({
            url: url,
            success: function(resp) {
                if (typeof resp == 'string' || resp instanceof String) {
                    // login is required situation
                    location.reload();
                } else {
                    $('.cabinet__tab-panel').empty();
                    // url is taken from response to process redirects
                    History.pushState('', '', resp['url']);
                    $("input:radio[name='tabs']:checked").siblings('.cabinet__tab-panel').html(resp['html']);
                    var $tabs = $('.cabinet__tab-label');
                    if ($tabs.length > 0) {
                        scrollTo($tabs, 1000);
                    }
                    tab_elements_init();
                }
            }
        });
    });
    $body.on('click', '.ajax-post-in-tab', function (e) {
        $(this).closest('form').ajaxSubmit({
            success: function (resp) {
                if (typeof resp == 'string' || resp instanceof String) {
                    // login is required situation
                    location.reload();
                } else {
                    if ('reload' in resp && resp['reload'] === true) {
                        window.location = resp['url'];
                        return
                    }
                    $('.cabinet__tab-panel').empty();
                    // url is taken from response to process redirects
                    History.pushState('', '', resp['url']);
                    $("input:radio[name='tabs']:checked").siblings('.cabinet__tab-panel').html(resp['html']);
                    var $errors = $('.error');
                    if ($errors.length > 0) {
                        var $first_error = $errors.eq(0),
                            $container = $first_error.closest('div.js-scroll-to-this-if-error');

                        if ($container.length > 0) {
                            scrollTo($container, 1000);
                        } else {
                            scrollTo($first_error, 1000);
                        }
                    } else {
                        var $tabs = $('.cabinet__tab-label');
                        if ($tabs.length > 0) {
                            scrollTo($tabs, 1000);
                        }
                    }
                    tab_elements_init();
                }
            },
            error: function (resp) {
                console.log(resp);
            }
        });
        e.preventDefault();
        return false;
    });
    // cabinet tabs end
    // open all tabs for android browser support start
    $body.on('click', 'input:radio[name=tabs]', function () {
        var selected = $(this).filter(':checked').siblings('.cabinet__tab-panel').css('display', 'inline');
    });
    // open all tabs for android browser support end
    // text-overflow ellipsis start
    var text_ellipsis = function () {
        $('.find__article-text').ellipsis({
          // lines: 3,           // force ellipsis after a certain number of lines. Default is 'auto'
          ellipClass: 'ellip',  // class used for ellipsis wrapper and to namespace ellip line
          responsive: true     // set to true if you want ellipsis to update on window resize. Default is false
        });
    };
    text_ellipsis();
    // text-overflow ellipsis end

    //show more or less text start
    var shorten_service_description_on_mobile = function(ajax) {
        if (typeof ajax === 'undefined') {
            ajax = false;
        }
        var $descriptions_to_shorten = $('.hotels__text');
        if (ajax) {
            $descriptions_to_shorten = $descriptions_to_shorten.filter(function(index) {
                return $(".morectnt", this).length === 0;
            });
        }
        $descriptions_to_shorten.each(function() {
            var content = $(this).html();
            if (content.length > MAX_DESCRIPTION_LENGTH_ON_MOBILE) {
                var con = content.substr(0, MAX_DESCRIPTION_LENGTH_ON_MOBILE);
                var hcon = content.substr(MAX_DESCRIPTION_LENGTH_ON_MOBILE, content.length - MAX_DESCRIPTION_LENGTH_ON_MOBILE);
                var txt= con +  '<span class="morectnt"><span>' + hcon + '</span>&nbsp;&nbsp;<a href="" class="showmoretxt">' + SHOW_MORE_TEXT + '</a></span>';
                $(this).html(txt);
            }
        });
    };
    shorten_service_description_on_mobile();
    var shorten_item_description_on_all_devices = function(ajax) {
        if (typeof ajax === 'undefined') {
            ajax = false;
        }
        var $descriptions_to_shorten = $('.long-discr');
        if (ajax) {
            $descriptions_to_shorten = $descriptions_to_shorten.filter(function(index) {
                return $(".morectnt", this).length === 0;
            });
        }
        $descriptions_to_shorten.each(function() {
            var content = $(this).html();
            if (content.length > MAX_ITEM_DESCRIPTION_LENGTH) {
                var con = content.substr(0, MAX_ITEM_DESCRIPTION_LENGTH);
                var hcon = content.substr(MAX_ITEM_DESCRIPTION_LENGTH, content.length - MAX_ITEM_DESCRIPTION_LENGTH);
                var txt= con +  '<span class="morectnt"><span>' + hcon + '</span>&nbsp;&nbsp;<a href="" class="showmoretxt">' + SHOW_MORE_TEXT + '</a></span>';
                $(this).html(txt);
            }
        });
    };
    shorten_item_description_on_all_devices();

    $body.on('click', '.showmoretxt', function() {
        var $this = $(this);
        if ($this.hasClass("sample")) {
            $this.removeClass("sample");
            $this.text(SHOW_MORE_TEXT);
        } else {
            $this.addClass("sample");
            $this.text(SHOW_LESS_TEXT);
        }
        $this.parent().prev().toggle();
        $this.prev().toggle();
        return false;
    });

    var shorten_comments = function (ajax){
        if (typeof ajax === 'undefined') {
            ajax = false;
        }
        var $comments_to_shorten = $('.hotels__comment-text');
        if (ajax) {
            $comments_to_shorten = $comments_to_shorten.filter(function(index) {
                return $(".morectnt", this).length === 0;
            });
        }
        $comments_to_shorten.each(function() {
            var content = $(this).html();
            if (content.length > MAX_COMMENT_LENGTH_ON_MOBILE) {
                var con = content.substr(0, MAX_COMMENT_LENGTH_ON_MOBILE);
                var hcon = content.substr(MAX_COMMENT_LENGTH_ON_MOBILE, content.length - MAX_COMMENT_LENGTH_ON_MOBILE);
                var txt= con + '<span class="morectnt"><span>' + hcon + '</span>&nbsp;&nbsp;<a href="" class="readmoretxt">' + READ_MORE_COMMENT + '</a></span>';
                $(this).html(txt);
            }
        });
    };
    shorten_comments();
    $body.on('click', '.readmoretxt', function() {
        var $this = $(this);
        if ($this.hasClass("sample")) {
            $this.removeClass("sample");
            $this.text(READ_MORE_COMMENT);
        } else {
            $this.prev().toggle();
            $this.hide();
        }
        return false;
    });
    //show more or less text end
    //rateit hotel
    var rateHotel_init = function() {
        var $rateHotel = $('#rateHotel'),
            readOnly = $rateHotel.attr('data-can-review') == "False",
            url = $rateHotel.attr('data-url'),
            hotel_pk = $rateHotel.attr('data-hotel-pk');

        $rateHotel.raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            readOnly: readOnly,
            starType: 'i',
            hints: ['', '', '', '', ''],
            click: function(newScore, evt) {
                $(this).find('i').unbind('click');
                $.post(url, {rate: newScore, pk: hotel_pk}, function(resp) {
                    if (resp['status'] == "success") {
                        $rateHotel.closest('.review-container').html(resp['html']);
                        rateHotel_init();
                    } else {
                        console.log(resp);
                    }
                });
                //var prevScore = $('input[name="score"]').val();
                //if (newScore != prevScore) {
                //    $('#search-form').find('input[name="rating"]').val(newScore);
                //}
                //alert('ID: ' + this.id + "\nscore: " + newScore + "\nevent: " + evt + "\nprev: " + );
            }
        });
    };
    rateHotel_init();
    //rateit hotel end
    //rateit apartment start
    var rateApartment_init = function() {
        var $rateApartment = $('#rateApartment'),
            readOnly = $rateApartment.attr('data-can-review') == "False",
            url = $rateApartment.attr('data-url'),
            apartment_pk = $rateApartment.attr('data-apartment-pk');

        $rateApartment.raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            readOnly: readOnly,
            starType: 'i',
            hints: ['', '', '', '', ''],
            click: function(newScore, evt) {
                $(this).find('i').unbind('click');
                $.post(url, {rate: newScore, pk: apartment_pk}, function(resp) {
                    if (resp['status'] == "success") {
                        $rateApartment.closest('.review-container').html(resp['html']);
                        rateApartment_init();
                    } else {
                        console.log(resp);
                    }
                });
                //var prevScore = $('input[name="score"]').val();
                //if (newScore != prevScore) {
                //    $('#search-form').find('input[name="rating"]').val(newScore);
                //}
                //alert('ID: ' + this.id + "\nscore: " + newScore + "\nevent: " + evt + "\nprev: " + );
            }
        });
    };
    rateApartment_init();
    //rateit apartment end
    //rateit transport start
    var rateTransport_init = function() {
        var $rateTransport = $('#rateTransport'),
            readOnly = $rateTransport.attr('data-can-review') == "False",
            url = $rateTransport.attr('data-url'),
            transport_pk = $rateTransport.attr('data-transport-pk');

        $rateTransport.raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            readOnly: readOnly,
            starType: 'i',
            hints: ['', '', '', '', ''],
            click: function(newScore, evt) {
                $(this).find('i').unbind('click');
                $.post(url, {rate: newScore, pk: transport_pk}, function(resp) {
                    if (resp['status'] == "success") {
                        $rateTransport.closest('.review-container').html(resp['html']);
                        rateTransport_init();
                    } else {
                        console.log(resp);
                    }
                });
                //var prevScore = $('input[name="score"]').val();
                //if (newScore != prevScore) {
                //    $('#search-form').find('input[name="rating"]').val(newScore);
                //}
                //alert('ID: ' + this.id + "\nscore: " + newScore + "\nevent: " + evt + "\nprev: " + );
            }
        });
    };
    rateTransport_init();
    //rateit transport end
    //rateit sport start
    var rateSport_init = function() {
        var $rateSport = $('#rateSport'),
            readOnly = $rateSport.attr('data-can-review') == "False",
            url = $rateSport.attr('data-url'),
            sport_pk = $rateSport.attr('data-sport-pk');

        $rateSport.raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            readOnly: readOnly,
            starType: 'i',
            hints: ['', '', '', '', ''],
            click: function(newScore, evt) {
                $(this).find('i').unbind('click');
                $.post(url, {rate: newScore, pk: sport_pk}, function(resp) {
                    if (resp['status'] == "success") {
                        $rateSport.closest('.review-container').html(resp['html']);
                        rateSport_init();
                    } else {
                        console.log(resp);
                    }
                });
            }
        });
    };
    rateSport_init();
    //rateit sport end
    //rateit excursion start
    var rateExcursion_init = function() {
        var $rateExcursion = $('#rateExcursion'),
            readOnly = $rateExcursion.attr('data-can-review') == "False",
            url = $rateExcursion.attr('data-url'),
            excursion_pk = $rateExcursion.attr('data-excursion-pk');

        $rateExcursion.raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            readOnly: readOnly,
            starType: 'i',
            hints: ['', '', '', '', ''],
            click: function(newScore, evt) {
                $(this).find('i').unbind('click');
                $.post(url, {rate: newScore, pk: excursion_pk}, function(resp) {
                    if (resp['status'] == "success") {
                        $rateExcursion.closest('.review-container').html(resp['html']);
                        rateExcursion_init();
                    } else {
                        console.log(resp);
                    }
                });
            }
        });
    };
    rateExcursion_init();
    //rateit excursion end
    //rateit entertainment start
    var rateEntertainment_init = function() {
        var $rateEntertainment = $('#rateEntertainment'),
            readOnly = $rateEntertainment.attr('data-can-review') == "False",
            url = $rateEntertainment.attr('data-url'),
            entertainment_pk = $rateEntertainment.attr('data-entertainment-pk');

        $rateEntertainment.raty({
            number: 5,
            score: function () {
                return $(this).attr('data-score');
            },
            readOnly: readOnly,
            starType: 'i',
            hints: ['', '', '', '', ''],
            click: function(newScore, evt) {
                $(this).find('i').unbind('click');
                $.post(url, {rate: newScore, pk: entertainment_pk}, function(resp) {
                    if (resp['status'] == "success") {
                        $rateEntertainment.closest('.review-container').html(resp['html']);
                        rateEntertainment_init();
                    } else {
                        console.log(resp);
                    }
                });
            }
        });
    };
    rateEntertainment_init();
    //rateit entertainment end
    //blog menu toggle start
    $('.blog__menu-link').click(function() {
        if (!$(this).next('.blog__menu-content-box:visible').length) {
            return;
        }
        $(this).parent().toggleClass('active');
        $(this).next('.blog__menu-content-box').children('.blog__menu-content').slideToggle('fast');
    });
    //blog menu toggle end
    //youtube popup start
    var videoPopup = $('.video-popup');
    videoPopup.magnificPopup({
      items: {
             src: videoPopup.attr('data-link')
         },
      type: 'iframe',
      iframe: {
            markup: '<div class="mfp-iframe-scaler">'+
                    '<div class="mfp-close"></div>'+
                    '<iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>'+
                    '</div>', 
        patterns: {
            youtube: {
                  index: 'youtube.com/', 
                  id: 'v=', 
                  src: '//www.youtube.com/embed/%id%?autoplay=1' 
                }
             },
             srcAction: 'iframe_src'
        },
        overflowY: 'scroll',
        fixedContentPos: true,
        fixedBgPos: true
    });
    //youtube popup end
    // room amenities popup start
    var init_room_amenities_popup = function (){
        $('.roomAmenities').magnificPopup({
            type: 'inline',
            fixedContentPos: false,
            fixedBgPos: true,
            overflowY: 'auto',
            closeBtnInside: true,
            preloader: false,
            midClick: true,
            removalDelay: 300,
            mainClass: 'my-mfp-zoom-in',
            mainClass: 'white-popup-layout'
        });
    };
    init_room_amenities_popup();
    // room amenities popup end
    // blog post popup start
        var imagePostPopup = $('.image-post-popup');
        imagePostPopup.magnificPopup({
            type: 'image',
            fixedContentPos: false,
            fixedBgPos: true,
            overflowY: 'auto',
            closeBtnInside: true,
            preloader: false,
            midClick: true,
            removalDelay: 300,
            gallery: {
                enabled: true
            },
            image: {
                verticalFit: true
            },
            zoom: {
                enabled: true,
                duration: 300
            }
        });

    // blog post popup end

    // multiply items popup start
    var init_items_gallery = function() {
        var itemsGallery = $('.itemsGallery');
        itemsGallery.each(function(){
            $(this).magnificPopup({
                delegate: 'a',
                type: 'image',
                fixedContentPos: false,
                fixedBgPos: true,
                overflowY: 'auto',
                closeBtnInside: true,
                preloader: false,
                midClick: true,
                removalDelay: 300,
                gallery: {
                    enabled: true
                },
                image: {
                    verticalFit: true
                },
                zoom: {
                    enabled: true,
                    duration: 300
                }
            });
       });
    };
    init_items_gallery();
    // multiply items popup end

    //terms and privacy popup start
    var init_terms_and_privacy_popup = function() {
        var pagePopup = $('.inline-popup');
        pagePopup.magnificPopup({
            fixedContentPos: true,
            fixedBgPos: true,
            overflowY: 'auto',
            closeBtnInside: true,
            preloader: false,
            midClick: true,
            removalDelay: 300,
            mainClass: 'white-popup-layout'
        });
    };
    init_terms_and_privacy_popup();
    //terms and privacy popup end

    //custom Scroll start
    function scroller() {
        var textScroll = $('.customScroll');
        var windowWidth = $(window).width();
        if (windowWidth>=980) {
            textScroll.niceScroll({
                horizrailenabled: false,
                autohidemode: false,
                cursorcolor: "#d2cfcf",
                cursorwidth: 8
            });
        } else {
           return true;
        }
    }
    scroller();

    $(window).on('resize',function(){
        scroller();
    });
    //custom Scroll end


});
$('body').css('visibility', 'visible');
