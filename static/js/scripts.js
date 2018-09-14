

$(document).ready(function(){
    //Скрыть PopUp при загрузке страницы
    // PopUpHide();
    // PopUpRegHide();

});
//Функция отображения PopUp
function PopUpShow(){
    $("#popup1").show();
}
//Функция скрытия PopUp
function PopUpHide(){
    $("#popup1").hide();
}

//Функция скрытия PopUp и открытия PopReg
function PopUpRegShow(){
    $("#popup1").hide();
    $("#popup2").show();
}
function PopUpRegHide(){
    $("#popup2").hide();
}

// $('.adm_order_item').click(AdmOrderItem);
// function AdmOrderItem() {
//         var ord_id = $(this).attr('data-order_id');
//
//         console.log(ord_id);
//         console.log("ORD_ID_NO")
//     }

jQuery(document).ready(function ($) {
    $('.info-user').click(profile_view);
    $('#change-profile').click(change_profile_view);
    $('#reg_btn').click(ValueReg);
    $('.product_list').click(AutoProductList);
    $('#change-product').click(changeproduct);

    var prodImgList = {};
    var form = $('#form_buying_product');

    form.on('submit', function (e) {
        // e.preventDefault();
        var submit_btn = $('#btn-by');
        // temp_price_per_item = submit_btn.data("price_per_itm");
        // console.log(temp_price_per_item);
        var product_price = +submit_btn.data("price_per_itm").replace(/,/,'.');
        console.log(product_price);
        $('#id_price_per_item').val(product_price);
        $('#id_sizes').val(document.getElementById('select-size').value);
        temp = document.getElementById('select-size').value;
        console.log(temp);
        return true
    });

    function AutoProductList() {
        var data = {};
        data.name = $(this).attr('data-productname');
        data.article = $(this).attr('data-article');
        data.price = $(this).attr('data-price');
        data.discount = $(this).attr('data-discount');
        data.category = $(this).attr('data-category');
        data.short_description = $(this).attr('data-short_description');
        data.description = $(this).attr('data-description');
        data.manufacturer = $(this).attr('data-manufacturer');
        data.year_model = $(this).attr('data-year_model');
        data.status_sale = $(this).attr('data-status_sale');
        data.status_new = $(this).attr('data-status_new');
        data.prod_active = $(this).attr('data-prod_active');
        data.fabric = $(this).attr('data-fabric');

        if (data.status_sale === "True"){
            $('#id_status_sale').prop('checked', true)
        }else {
            $('#id_status_sale').prop('checked', false)
        }
        if (data.status_new === "True"){
            $('#id_status_new').attr('checked', true)
        }else {
            $('#id_status_new').attr('checked', false)
        }
        if (data.prod_active === "True"){
            $('#id_prod_active').attr('checked', true)
        }else {
            $('#id_prod_active').attr('checked', false)
        }

        $('#id_product').val(data.name);
        $('#id_name').val(data.name);
        $('#id_article').val(data.article);
        $('#id_discount').val(data.discount);
        $('#id_category').val(data.category);
        $('#id_fabric').val(data.fabric);
        $('#id_short_description').val(data.short_description);
        $('#id_description').val(data.description);
        $('#id_year_model').val(data.year_model);
        $('#id_price').val(data.price);

        $.ajax({
            type: "GET",
            url: "adm_img/",
            data: data,
            dataType: "json",
            cache: false,


            success: function(data){
                prodImgList = data.products_img_list;
                $('#id_img-adm').empty();
                for (i=0; i < data.products_img_list.length; i++){

                    var url_img="{% url 'image_product'"+data.products_img_list[i][3]+"%}";
                    var img = "<img src='" + data.products_img_list[i][0] + "' class='img-adm' id="+data.products_img_list[i][3]+">";
                    console.log(img);
                    $('#id_img-adm').append("<a href=" + url_img + " >"+img+"</a><br>");
                    if (data.products_img_list[i][1] == true){
                        $('#id_img-adm').append("<input type='checkbox' checked class='img-adm-ck' id='"+data.products_img_list[i][3]+"_id_main'>is main");

                    }else {$('#id_img-adm').append("<input type='checkbox' class='img-adm-ck' id='"+data.products_img_list[i][3]+"_id_main'>is main");
                    }
                    if (data.products_img_list[i][2] == true){
                        $('#id_img-adm').append("<input type='checkbox' checked class='img-adm-ck' id='"+data.products_img_list[i][3]+"_id_active'>is active");

                    }else {$('#id_img-adm').append("<input type='checkbox' class='img-adm-ck' id='"+data.products_img_list[i][3]+"_id_active'>is active");
                    }

                }
            }
        })

    }
    function changeproduct() {
        var tdata = {};
        var data = {};

        for (i=0; i < prodImgList.length; i++){
            var el_id = prodImgList[i][3];
            var result_id_main = el_id + "_id_main";
            var result_id_active = el_id + "_id_active";
            var bool_main, bool_active;
            if (document.getElementById(result_id_main).checked == true) {
                bool_main = true
            }else{bool_main = false}
            if (document.getElementById(result_id_active).checked == true) {
                bool_active = true
            }else{bool_active = false}
            tdata[prodImgList[i][3]] = [bool_main, bool_active]
        }

        data.image_id = tdata;
        $.ajax({
            type: "GET",
            url: "product_save/",
            traditional: true,
            data: JSON.stringify(data),
            dataType: "json",
            cache: false,

            success: function (arv) {
                data = {};
                data.article = document.getElementById('id_article').value;
                data.description = document.getElementById('id_description').value;
                data.short_description = document.getElementById('id_short_description').value;
                data.description = document.getElementById('id_description').value;
                data.year_model = document.getElementById('id_year_model').value;
                data.price = document.getElementById('id_price').value;
                data.fabric = document.getElementById('id_fabric').value;
                data.category = document.getElementById('id_category').value;
                data.discount = document.getElementById('id_discount').value;
                data.name = document.getElementById('id_name').value;
                data.status_sale = document.getElementById('id_status_sale').checked;
                data.status_new = document.getElementById('id_status_new').checked;
                data.prod_active = document.getElementById('id_prod_active').checked;

                console.log("OOOOOO");
                $.ajax({
                type: "GET",
                url: "",
                data: data,

                success: function (data) {
                    location.reload();
                    }
                });
            }
        })

    }

    function ValueReg() {
        var val_email, val_pass, pass2, email, ve, pe, pass1;
        var data;
        pass1 = document.getElementById('id_password1').value;
        pass2 = document.getElementById('id_password2').value;
        email = document.getElementById('reg_user_id').value;
        ve = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        // pe = /(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}/g;
        pe = /(?=.*[0-9])(?=.*[a-z])[0-9a-zA-Z!@#$%^&*]{8,}/g;
        val_email = ve.test(String(email).toLowerCase());
        val_pass = pe.test(String(pass1));
        if (!val_email){
            alert("Не правильное мыло");
            return false;}

        if (!val_pass){
            alert("Пароль должен содержать не менее 8 символов, цифры и латинские симвлы, может содержать спц. символы");
            return false;}

        if (pass1 != pass2){
            alert("Пароли не совпадают");
            return false;}

        data = {};
        data.username = email;
        data.password1 = pass1;
        data.password2 = pass2;

        console.log("ajax ->" + data.username + "pass1 ->" + data.password1);

        var csrf_token = $('#reg_form [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            type: "POST",
            url: "/alt_register/",
            data: data,
            dataType: "html",
            cache: false,

            success: function (data) {

                console.log(data);
                if (data == ''){
                    console.log("все ОК");
                    location.reload();
                    // return true;
                }else {
                    alert(data);
                    location.reload();
                    return false;
                }
            }
        });


    }

    function profile_view() {
        var data = {};
        data.username = $(this).attr('data-username');
        data.user_id = $(this).attr('data-user_id');
        data.email = $(this).attr('data-email');
        data.superusers = $(this).attr('data-superusers');
        data.first_name = $(this).attr('data-first_name');
        data.is_active = $(this).attr('data-is_active');
        data.is_staff = $(this).attr('data-is_staff');

        data.phone = $(this).attr('data-phone');
        data.spare_phone = $(this).attr('data-spare_phone');
        data.address_delivery = $(this).attr('data-address_delivery');
        data.category = $(this).attr('data-category');
        data.discount = $(this).attr('data-discount');
        data.short_description = $(this).attr('data-short_description');

        $('.data-js h3').text(data.username);
        $('#first_name').val(data.first_name);
        $('#username').val(data.username);
        $('#user_id').val(data.user_id);

        $('#phone').val(data.phone);
        $('#spare_phone').val(data.spare_phone);
        $('#address_delivery').val(data.address_delivery);
        // $('#category').val(data.category);
        $('#category_val').val(data.category);
        $('#discount').val(data.discount);
        $('#short_description').val(data.short_description);

        if (data.is_active === "True"){
            $('#is_active').attr('checked', true)
        }else {
            $('#is_active').attr('checked', false)
        }
        if (data.is_staff === "True"){
            $('#is_staff').prop('checked', true)
        }else {
            $('#is_staff').prop('checked', false)
        }

        var csrf_token = $('#form-profile [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            type: "POST",
            url: "/orders/order_list/",
            data: data,
            success: function (arv) {

                var json_dict = JSON.parse(arv);
                var sum = 0;
                $('.order-item-list > tbody ').empty();
                $('.table_orders > tbody ').empty();
                $('.adm-prod_in_ord_img').empty();
                for (var i=0; i < json_dict.length; i++) {
                    $('.table_orders > tbody ').append('<tr>');
                    sum += parseFloat(json_dict[i][1]);
                    for (var j=0; j < json_dict[i].length; j++){
                        $('.table_orders > tbody tr:last-child').append('<td><a href="javascript:" class="adm_order_item"'
                             +' data-order_id="'+json_dict[i][0]+'">'+json_dict[i][j]+'</a>'+
                        '</td>');
                    }
                    $('.table_orders > tbody ').append('</tr>');
                }
                $('#total-orders-summ h3').text(sum.toFixed(2));
               $('.adm_order_item').click(AdmOrderItem);

            }
        })
    }
    function AdmOrderItem() {
        var ord_id = $(this).attr('data-order_id');
        var data = {};

        var csrf_token = $('#form-profile [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        data['ord_id'] = ord_id;

        $.ajax({
            type: "POST",
            url: "/orders/order_items/",
            data: data,

            success: function (arg) {
                var json_dict = JSON.parse(arg);
                var sum = 0;
                $('.adm-prod_in_ord_img').empty();
                $('.order-item-list > tbody ').empty();
                for (var i=0; i < json_dict.length; i++) {
                    $('.order-item-list > tbody ').append('<tr>');
                    // sum += Number(json_dict[i][1]);
                    for (var j=0; j < json_dict[i].length; j++){
                        $('.order-item-list > tbody tr:last-child').append('<td><a href="javascript:" class="adm_ord_prod_item"'
                             +' data-prod_id="'+json_dict[i][0]+'">'+json_dict[i][j]+'</a>'+
                        '</td>');
                    }
                    $('.order-item-list > tbody ').append('</tr>');
                }
                $('.adm_ord_prod_item').click(AdmOrdProdItem);
            }
        })
    }
    function AdmOrdProdItem() {
        var prod_id = $(this).attr('data-prod_id');
        var data = {};

        var csrf_token = $('#form-profile [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        data['prod_id'] = prod_id;

        $.ajax({
            type: "POST",
            url: "/orders/adm_ord_prod_items/",
            data: data,

            success: function (arg) {
                var json_dict = JSON.parse(arg);
                $('.adm-prod_in_ord_img').empty();
                for (var i=0; i < json_dict.length; i++) {
                    // $('#adm-prod_in_ord_img').append("<a href='' >"+json_dict[i][0]+"</a><br>");
                    var img = "<img src='/media/" + json_dict[i][0] + "' class='img-responsive-in-list-mini'>";
                    $('.adm-prod_in_ord_img').append(img);
                    $('.adm-prod_in_ord_img').append(json_dict[i][0]);
                }
                for (var ii=1; ii < json_dict[0].length; ii++){
                    if(ii == 1){
                        $('.adm-prod_in_ord_img').append("<h4>Текущая цена: "+json_dict[0][ii]+"</h4>");
                    }else if(ii == 2){
                        $('.adm-prod_in_ord_img').append("<h4>Текущая скидка: "+json_dict[0][ii]+"</h4>");
                    }else if(ii == 3){
                        $('.adm-prod_in_ord_img').append("<h4>Категория: "+json_dict[0][ii]+"</h4>");
                    }else{
                        $('.adm-prod_in_ord_img').append("<h4>Категория: "+json_dict[0][ii]+"</h4>");
                    }
                }
            }
        })

    }

    function change_profile_view() {
        var data = {};

        data.username = document.getElementById('username').value;
        data.user_id = document.getElementById('user_id').value;
        data.first_name = document.getElementById('first_name').value;
        data.is_active = document.getElementById('is_active').checked;
        data.is_staff = document.getElementById('is_staff').checked;

        data.phone = document.getElementById('phone').value;
        data.spare_phone = document.getElementById('spare_phone').value;
        data.address_delivery = document.getElementById('address_delivery').value;
        data.category = document.getElementById('category_val').value;
        data.discount = document.getElementById('discount').value;
        data.short_description = document.getElementById('short_description').value;

        var url = "/profile/";
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            dataType: "html",
            cache: false,


            success: function(){
                location.reload();
            }
       });
    }
});
