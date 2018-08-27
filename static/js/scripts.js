

$(document).ready(function(){
    //Скрыть PopUp при загрузке страницы
    PopUpHide();
    PopUpRegHide();

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

jQuery(document).ready(function ($) {
    $('.info-user').click(profile_view);
    $('#change-profile').click(change_profile_view);
    $('#reg_btn').click(ValueReg);
    $('.product_list').click(AutoProductList);
    $('#change-product').click(changeproduct);
    var prodImgList = {};

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
        console.log("TTTTT"+document.getElementById('id_product').value);

        $('#id_article').val(data.article);
        $('#id_discount').val(data.discount);

        $('#id_category').val(data.category);
        $('#id_fabric').val(data.fabric);
        // $('#id_manufacturer').val(data.manufacturer);
        // $('#123').val(data.manufacturer);

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
                    $('#id_img-adm').append("<a href=" + url_img + " >"+img+"</a><br>");


                    // $('#id_img-adm').append("<img src='" + data.products_img_list[i][0] + "' class='img-adm' id="+data.products_img_list[i][3]+">");
                    // console.log(data.products_img_list[i][1]);

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
            // console.log(prodImgList[i][3]);
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
            // tdata[data.products_img_list[i][3]] = [bool_main, bool_active]
            // tdata[data.products_img_list[i][3]] = [document.getElementById(result_id_main).checked, document.getElementById(result_id_active).checked]
        }

        data.image_id = tdata;
        //
        // data.article = document.getElementById('id_article').value;

        // console.log(prodImgList);

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

        $.ajax({
            type: "GET",
            url: "",
            data: data,
            dataType: "html",
            cache: false,

            success: function (data) {

                console.log(data);
                if (data == ''){
                    // console.log("все ОК");
                    location.reload();
                    // return true;
                }else {
                    alert(data);
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

        // data.csrfmiddlewaretoken = $('#form-profile [name="csrfmiddlewaretoken"]').val();

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
        // console.log(document.getElementById('category_val').value +' Ya ' + data.category);

        if (data.is_active === "True"){
            // console.log(data.is_active +' Ya');
            // $('#is_active').prop('checked', true)
            $('#is_active').attr('checked', true)
        }else {
            $('#is_active').attr('checked', false)
        }
        if (data.is_staff === "True"){
            $('#is_staff').prop('checked', true)
        }else {
            $('#is_staff').prop('checked', false)
        }


        // $('.data-js ul').append('<li>'+ data.username +'</li>');
    }

    function change_profile_view() {
        var data = {};

        data.username = document.getElementById('username').value;
        data.user_id = document.getElementById('user_id').value;
        // data.password = document.getElementById('password').value;
        data.first_name = document.getElementById('first_name').value;
        data.is_active = document.getElementById('is_active').checked;
        data.is_staff = document.getElementById('is_staff').checked;

        data.phone = document.getElementById('phone').value;
        data.spare_phone = document.getElementById('spare_phone').value;
        data.address_delivery = document.getElementById('address_delivery').value;
        data.category = document.getElementById('category_val').value;
        data.discount = document.getElementById('discount').value;
        data.short_description = document.getElementById('short_description').value;

        // console.log(data.user_id, data.username, data.first_name, data.is_active, data.is_staff);

        var url = "/profile/";
        $.ajax({
            type: "GET",
            url: url,
            data: data,
            dataType: "html",
            cache: false,


            success: function(){
                // $('.data-js h3').text(data.username);
                location.reload();
                // if (data == 'ok'){
                    //console.log(data);
                //
                // }
            }
       });
    }
});
