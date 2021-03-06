

// $(document).ready(function(){
    //Скрыть PopUp при загрузке страницы
    // PopUpHide();
    // PopUpRegHide();

// });
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

function delHide(btn, btn2, check) {
    console.log(btn);
    $("#"+check.id+"").prop('checked', false);
    $("#"+btn2.id+"").addClass('hidediv');
    $("#"+btn.id+"").removeClass('hidediv');
    }
function delHide2(btn2, btn1) {
    console.log(btn2.id, btn1.id);
    $("#"+btn1.id+"").addClass('hidediv');
    $("#"+btn2.id+"").toggleClass('hidediv');
}

jQuery(document).ready(function ($) {
    $('.info-user').click(profile_view);
    $('#change-profile').click(change_profile_view);
    $('#reg_btn').click(ValueReg);
    $('.product_list').click(AutoProductList);
    // $('#change-product').click(changeproduct);
    $('.href_on_ord').click(ord_filter);
    $('.href_on_prod').click(SelectedIdProduct);
    $('#btn_prod_filter').click(ProductFind);
    $('#btn_ord_calc').click(OrderRecount);
    $('#btn_create_ord').click(AddingNewOrder);
    $('#btn_prod_in_ord_list').click(AddBlockListShow);
    $('#btn_add_prod_to_ord').click(AddProductToOrder);

    $('#btn_list_cancel').click(function(){$("#add_block_list").hide(); sessionfalse()});
    $('#btn_add_prod_hide').click(function(){$("#add_product").hide(); $("#adm-ord-addprod").hide(); $("#col5top_1").empty();});
    $('#btn_add_cancel').click(function(){$("#add_block_add").hide();});

    $('#btn_prod_add').click(AddProductInOrder);
    $('#btn_add-show-img_block').click(ShowBlockAddingImg);
    $('#btn_end-create-img').click(ClouseBlockAddingImg);
    $('#btn_cancel-del-img').click(ClouseBlockDeleteImg);
    $('#btn_cancel_add_fabric').click(CancelAddFabric);
    $('#btn_mini_fabric_new').click(AddFabric);
    $('#btn_cancel_add_prod_cat').click(CancelAddProdCat);
    $('#btn_mini_cat_new').click(AddingProductCat);


    //(Orders) <!--Resets the order number in the session-->
    function sessionfalse(e) {
        $("#order_ord").val("");
        // $(".input_order_ord").empty();
        // console.log(document.getElementById('order_ord').value);
        var data = {};
        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            type: "POST",
            url: "sessionFalse/",
            data: data,
            success: function (arv) {
                location.reload()
                // console.log(document.getElementById('order_ord').value);
            }
        })
    }

    //(Orders) <!--Adding New Order and show #add_block_add in orders.html-->
    function AddingNewOrder(){
        $("#add_block_add").show();
    }

    //(Orders) <!--Final adding product to the order-->
    function AddProductToOrder() {
        var data = {};
        data['order_ord'] = document.getElementById('order_ord').value;
        data['product_id'] = document.getElementById('id-prod-id').value;
        data['product_id'] = document.getElementById('id-prod-id').value;
        data['nmb'] = document.getElementById('id-ord-prod-nmb').value;
        data['price_per_item'] = document.getElementById('id-ord-price_per_item').value;
        data['size'] = document.getElementById('id-ord-sizes').value;
        $("#add_product").hide();
        console.log(data);

        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            type: "POST",
            url: "adding_product_in_order/",
            data: data,

            success: function (arv) {
                console.log(arv);
                Ordlogicfunction(arv)
            }
        })
    }

    //(Orders)  <!-- Collect the data to find the product you need to add to the order.(#btn_prod_filter)-->
    function ProductFind(){
        $("#adm-ord-addprod").hide();
        $("#col5top_1").empty();
        var data = {};
        data.article = document.getElementById('id_field_filter_article').value;
        data.prod = document.getElementById('id_field_filter_prod').value;
        data.product = $(this).attr('data-prod_id');

        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            type: "POST",
            url: "ord_find_product/",
            data: data,

            success: function (arv) {
                FilterPositionInOrder(arv);
            }
        })
    }

    //(Orders) <!--Displaying a filtered list of products(ProductFind())-->
    function FilterPositionInOrder(arv) {
        var json_dict = JSON.parse(arv);
        if (json_dict == false) {
            console.log("Нет такой позиции")
        } else {
            console.log("Заказ № ", document.getElementById('order_ord').value);
            $('.tbl_ord_add_prod > tbody ').empty();
            for (i = 0; i < json_dict.length; i++) {
                var img = "<img src='/media/" + json_dict[i].image + "' class='img-responsive-in-list-mini'>";
                $('.tbl_ord_add_prod > tbody ').append(
              '<tr><td><a class="A12345" href="javascript:" data-product_id="' + json_dict[i].product + '"' +
                                                          ' data-product_img="/media/' + json_dict[i].image + '"' +
                                                          ' data-product_article="' + json_dict[i].product__article + '"' +
                                                          ' data-product_name="' + json_dict[i].product__name + '"' +
                                                          ' data-product_price="' + json_dict[i].product__price + '"' +
                                                          ' data-product_discount="' + json_dict[i].product__discount + '"' +
                                                          ' >' + img + '</a></td><td>'
                    + '<a class="A12345" href="javascript:" data-product_id="' + json_dict[i].product + '" ' +
                                                            ' data-product_img="/media/' + json_dict[i].image + '"'+
                                                            ' data-product_article="' + json_dict[i].product__article + '"' +
                                                            ' data-product_name="' + json_dict[i].product__name + '"' +
                                                            ' data-product_price="' + json_dict[i].product__price + '"' +
                                                            ' data-product_discount="' + json_dict[i].product__discount + '"' +
                                                            '>' + json_dict[i].product__article + '</a></td><td width="350">'
                    + '<a class="A12345" href="javascript:" data-product_id="' + json_dict[i].product + '" ' +
                                                            ' data-product_img="/media/' + json_dict[i].image + '"'+
                                                            ' data-product_article="' + json_dict[i].product__article + '"' +
                                                            ' data-product_name="' + json_dict[i].product__name + '"' +
                                                            ' data-product_price="' + json_dict[i].product__price + '"' +
                                                            ' data-product_discount="' + json_dict[i].product__discount + '"' +
                                                            '>' + json_dict[i].product__name + '</a></td><td>'
                    + '<a class="A12345" href="javascript:" data-product_id="' + json_dict[i].product + '" ' +
                                                            ' data-product_img="/media/' + json_dict[i].image + '"'+
                                                            ' data-product_article="' + json_dict[i].product__article + '"' +
                                                            ' data-product_name="' + json_dict[i].product__name + '"' +
                                                            ' data-product_price="' + json_dict[i].product__price + '"' +
                                                            ' data-product_discount="' + json_dict[i].product__discount + '"' +
                                                            '>' + json_dict[i].product__price + '</a></td><td>'
                    + '<a class="A12345" href="javascript:" data-product_id="' + json_dict[i].product + '" ' +
                                                            ' data-product_img="/media/' + json_dict[i].image + '"'+
                                                            ' data-product_article="' + json_dict[i].product__article + '"' +
                                                            ' data-product_name="' + json_dict[i].product__name + '"' +
                                                            ' data-product_price="' + json_dict[i].product__price + '"' +
                                                            ' data-product_discount="' + json_dict[i].product__discount + '"' +
                                                            '>' + json_dict[i].product__discount + '</a></td></tr>'
                )
            }
            $('.A12345').click(SelectedIdProduct);
        }
    }

    //(Orders) <!--Display of the found product(.A12345, .href_on_prod)-->
    function SelectedIdProduct() {
        var data = {};
        var prod_id = $(this).attr('data-product_id');
        var product_img =$(this).attr('data-product_img');
        var product_article = $(this).attr('data-product_article');
        var product_name =$(this).attr('data-product_name');
        var product_price = $(this).attr('data-product_price');
        var product_discount =$(this).attr('data-product_discount');

        product_price = +product_price;
        $('#id-prod-id').val(prod_id);
        $('#id-price-id').val(product_price);
        $('#id-discount-id').val(product_discount);

        $('.tbl_ord_add_prod > tbody ').empty();
        var pic = "<img src='" + product_img + "' class='img-responsive-in-list-mini'>";
        $('.tbl_ord_add_prod > tbody ').append(
            '<tr><td>' + pic + '</td><td>'+
             product_article + '</td><td>'+
             product_name + '</td><td>'+
             product_price + '</td><td>'+
             product_discount + '</td></tr>'
        );
        data.prod_id = prod_id;
         var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        // Request for a list of available sizes of product
        $.ajax({
            type: "POST",
            url: "size_for_product/",
            data: data,

            success: function (arv) {
                var json_dict = JSON.parse(arv);
                $('#id-ord-sizes').empty();
                $('#id-ord-sizes').append(
                        '<option></option>'
                    );
                for (i=0; i < json_dict.length; i++){

                    $('#id-ord-sizes').append(
                        '<option>'+json_dict[i].name_size+'</option>'
                    );

                }
                var price = document.getElementById('id-price-id').value;
                var discount = document.getElementById('id-discount-id').value;
                $('#id-ord-price_per_item').val((price / 100 * (100-discount)).toFixed(2));

                // $('#id_sizes').val(document.getElementById('id-ord-sizes').value);
                console.log(price, discount, price/100);
            }
        });

        // <!--Request for description a product-->
        $.ajax({
            type: "POST",
            url: "description_for_product/",
            data: data,

            success: function (arv) {
                $('#col5top_1').empty();
                console.log(arv);
                $('#col5top_1').append('<p style="word-break:break-all;color:darkorange;font-size:1vw;' +
                    'width:24vw;height:59vh;white-space:pre-wrap;overflow-y:auto;padding:1vw; text-align: left">'+arv+'</p>');
            }
        });

        $("#adm-ord-addprod").show();
    }

    //(Orders) <!--Recalculate the final cost of the order -->
    function OrderRecount() {
        var data = {};
        data.order_ord = document.getElementById('order_ord').value;

        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            type: "POST",
            url: "order_recount/",
            data: data,

            success: function (arv) {
                if (arv == false){
                    console.log("Не выбран заказ")
                }else{
                    $('#id_total_price').val(arv);
                }
            }
        })
    }

    //(Orders)<!--Displaying of products in the order-->
    function AddBlockListShow(){
        var data = {};
        data['order_ord'] = document.getElementById('order_ord').value;

        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        // var csrf_token = $('#form_adding_prod [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            type: "POST",
            url: "ord_editing_list/",
            data: data,

            success: function (arv) {
                Ordlogicfunction(arv)
            }
        })
    }

    //(Orders) <!--Removes product from order -->
    function DelFromBasket(){
        var data = {};
        data.product = $(this).attr('data-prod_in_bask');
        console.log(data.product, data.temp);
        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        $.ajax({
            type: "POST",
            url: "ord_del_product/",
            data: data,

            success: function (arv) {
                Ordlogicfunction(arv)
            }
        })
    }

    //(Orders) <!--Edit product from order -->
    function EditFromBasket(){
        var data = {};
        data.product = $(this).attr('data-prod_in_bask');
        var oldnmb = $(this).attr('data-old_nmb');
        var oldprice = $(this).attr('data-old_price');
        var amount = oldnmb * oldprice;
        var count = document.getElementById('id_total_price').value;


        var nmb_id = "prod_nmb_"+data.product;
        var price_prod = "prod_price_"+data.product;
        var size_prod = "prod_size_"+data.product;
        var btn_id = "id_btn1_"+data.product;


        $("#"+btn_id+"").hide();

        data.nmb = document.getElementById(nmb_id).value;
        data.price = document.getElementById(price_prod).value;
        data.size = document.getElementById(size_prod).value;
        var new_amout = data.price * data.nmb;
        // console.log(count, amount, new_amout);
        $('#id_total_price').val(count - amount + new_amout);


        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            type: "POST",
            url: "ord_edit_product/",
            data: data,
            cache: false,

            success: function (arv) {
            Ordlogicfunction(arv)
            }
        })
    }

    //(Orders) <!--Processes received requests from functions(AddBlockListShow, EditFromBasket, DelFromBasket ) -->
    function Ordlogicfunction(arv) {
        var json_dict = JSON.parse(arv);
            console.log(json_dict);
            if (json_dict.length == 0){
                $("#add_block_list").show();
                // json_dict = true
            }
            else if (json_dict == false){
                // alert("Не выбран заказ, или заказ пустой (ну нет там товара)");
                console.log(json_dict);
                // location.reload()
            }else{
            // $('#id_sizes').val(document.getElementById('select-size').value);

            $("#add_block_list").show();
            $('.table_prod_in_ord > tbody ').empty();
            $('#block_button').empty();
            var vh = -2;
            var vw = 0;
            var dvh = 3;
            var dvw = 0;
            for (i=0; i < json_dict.length; i++){
                // vh += 10;
                // dvh += 10;
                var img = "<img src='/media/" + json_dict[i].image + "' class='img-responsive-in-list-mini'>";
                var id_nmb_prod = "prod_nmb_"+json_dict[i].product__productinbasket;
                var id_price_prod = "prod_price_"+ json_dict[i].product__productinbasket;
                var id_size_prod = "prod_size_"+ json_dict[i].product__productinbasket;
                var id_btn1 = "id_btn1_"+ json_dict[i].product__productinbasket;
                var id_btn2 = "id_btn2_"+ json_dict[i].product__productinbasket;
                var id_check = "id_check_"+ json_dict[i].product__productinbasket;

                console.log(id_nmb_prod);
                $('.table_prod_in_ord > tbody ').append(
                    '<tr><td>'+img+'</td><td>'
                   + json_dict[i].product__article +'</td><td style="width:20vw; height: 10vh">'
                    + json_dict[i].product__name + '(price: '+json_dict[i].product__price+')'+'</td><td>'
                    // + json_dict[i].product__productinbasket__nmb +'</td><td>'
                    + '<input id="'+id_nmb_prod+'" onchange="delHide('+id_btn1+', '+id_btn2+', '+id_check+')" style="width:3vw; height:3vh" type="number" min="0" value="'+ json_dict[i].product__productinbasket__nmb +'"></td><td>'
                    + '<input id="'+id_price_prod+'" step="0.01" pattern="\d+(\.\d{2})?" onchange="delHide('+id_btn1+', '+id_btn2+', '+id_check+')" style="width:5vw; height:3vh" type="number" min="0" value="'+ json_dict[i].product__productinbasket__price_per_item +'"></td><td>'
                    // + json_dict[i].product__productinbasket__sizes +'</td><td>' +
                    + '<select style="height:3vh" onchange="delHide('+id_btn1+', '+id_btn2+', '+id_check+')" id="'+id_size_prod+'">'
                    + '<option value="'+json_dict[i].product__productinbasket__sizes +'" selected>'+json_dict[i].product__productinbasket__sizes +'</option>'
                    + '<option value="XXXL">XXXL</option>'
                    + '<option value="XXL">XXL</option>'
                    + '<option value="XL">XL</option>'
                    + '<option value="L">L</option>'
                    + '<option value="M">M</option>'
                    + '<option value="S">S</option>'
                    + '<option value="XS">XS</option>'
                    + '<option value="XXS">XXS</option>'
                    + '</select></td><td>'
                    + '<input type="checkbox" id="'+id_check+'" onchange="delHide2('+id_btn2+', '+id_btn1+')" style="width:20px;height:20px;"></td><td width="0">'
                    + '<button style="position: relative; top: '+vh+'vh; right: '+vw+'vw; height: 4vh" type="button" class="btn btn-outline my-2 my-sm-0 edit-prod hidediv" id="'+id_btn1+'" href="javascript:" ' +
                        'data-prod_in_bask="'+json_dict[i].product__productinbasket+'" ' +
                        'data-old_nmb="'+json_dict[i].product__productinbasket__nmb+'" ' +
                        'data-old_price="'+json_dict[i].product__productinbasket__price_per_item+'">Изменить</button>'+
                        '<button style="position: relative; top: '+dvh+'vh; right: '+dvw+'vw; height: 4vh" type="button" class="btn btn-outline my-2 my-sm-0 del-prod hidediv" id="'+id_btn2+'" href="javascript:" ' +
                        'data-prod_in_bask="'+json_dict[i].product__productinbasket+'">Удалить</button></td></tr>'
                );
                // $('#block_button ').append(
                //     '<button style="position: relative; top: '+vh+'vh; right: 0vw; height: 4vh" type="button" class="btn btn-outline my-2 my-sm-0 edit-prod hidediv" id="'+id_btn1+'" href="javascript:" ' +
                //         'data-prod_in_bask="'+json_dict[i].product__productinbasket+'" ' +
                //         'data-old_nmb="'+json_dict[i].product__productinbasket__nmb+'" ' +
                //         'data-old_price="'+json_dict[i].product__productinbasket__price_per_item+'">Изменить</button>'+
                //     '<button style="position: relative; top: '+dvh+'vh; right: 0vw; height: 4vh" type="button" class="btn btn-outline my-2 my-sm-0 del-prod hidediv" id="'+id_btn2+'" href="javascript:" ' +
                //         'data-prod_in_bask="'+json_dict[i].product__productinbasket+'">Удалить</button>'
                // );
            }
            $('.del-prod').click(DelFromBasket);
            $('.edit-prod').click(EditFromBasket);
            }
    }

    //(Orders) <!--Show the hidden div fir adding product in order(modulWindow2) -->
    function AddProductInOrder() {
        $("#id_field_filter_article").val('');
        ProductFind();
        $("#add_product").show();
    }

    //(Orders) <!-- Заполняет данные в форму при выборе заказа из таблицы -->
    function ord_filter() {
        var data = {};
        data.order = $(this).attr('data-ord_id');

        var csrf_token = $('#ord_editing [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            type: "POST",
            url: "ord_editing/",
            data: data,
            cache: false,

            success: function (datavada) {
                var json_dict = JSON.parse(datavada);
                $('#id_user').val(json_dict[0][0]);
                $('#id_total_price').val(json_dict[0][1]);
                $('#id_customer_name').val(json_dict[0][2]);
                $('#id_customer_phone').val(json_dict[0][3]);
                $('#id_data_completed').val(json_dict[0][5]);
                $('#id_customer_address').val(json_dict[0][6]);
                $('#id_comments').val(json_dict[0][7]);
                $('#id_status_ord').val(json_dict[0][4]);
                $('#order_ord').val(json_dict[0][8]);
                $('#order_ord_del').val(json_dict[0][8]);
                $('#ord_number_info h2').text("Заказ № "+json_dict[0][8]);
                $('#ord_number_info h5').text("от "+json_dict[0][9]);
            }
        })
    }


    var prodImgList = {};

    //(Products)(landing) <!-- Fills the price of the product with all the discounts in the purchase form when sending it (us_product.html) -->
    var form = $('#form_buying_product');
    form.on('submit', function (e) {
        // e.preventDefault();
        var submit_btn = $('#btn-by');
        var product_price = +submit_btn.data("price_per_itm").replace(/,/,'.');
        $('#id_price_per_item').val(product_price);
        $('#id_sizes').val(document.getElementById('select-size').value);
        return true
    });

    //(Admin_product) <!-- Show div "div-adding_fabric".
    function CancelAddFabric() {
        $("#div-adding_fabric").hide();
    }

    function AddFabric() {
        $("#div-adding_fabric").show();
    }

    //(Admin_product) <!-- Show div "div-adding_product_category".
    function AddingProductCat() {
        $("#div-adding_product_category").show();
    }
    function CancelAddProdCat() {
        $("#div-adding_product_category").hide();
    }


    //(Admin_product) <!-- Show div "div-prod-form-img".
    function ShowBlockAddingImg() {
        $('#div-prod-form-img').show();
    }
    function ClouseBlockAddingImg() {
        $('#div-prod-form-img').hide();
        // $('#btn_add-show-img_block').show();
    }

    //(Admin_product) <!-- Fills out the form to change the product data.
    function AutoProductList() {
        $('#change-product').show();
        $('#btn_add-show-img_block').show();
        $('#btn_adding-product').hide();
        var data = {};
        // data.name = $(this).attr('data-productname');
        data.article = $(this).attr('data-article');
        // data.price = $(this).attr('data-price');
        // data.discount = $(this).attr('data-discount');
        // data.category = $(this).attr('data-category');
        // data.short_description = $(this).attr('data-short_description');
        // data.description = $(this).attr('data-description');
        // data.manufacturer = $(this).attr('data-manufacturer');
        // data.year_model = $(this).attr('data-year_model');
        // data.status_sale = $(this).attr('data-status_sale');
        // data.status_new = $(this).attr('data-status_new');
        // data.prod_active = $(this).attr('data-prod_active');
        // data.fabric = $(this).attr('data-fabric');
        // data.sizes = $(this).attr('data-sizes');
        // data.sizes2 = document.adm_product_form.sizes;
        // console.log(data.sizes);
        // for (var n=0; n<data.sizes.length; n++){
        //     console.log(data.sizes.options[n].text)
        // }


        var csrf_token = $('#form_product_change [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        $.ajax({
            type: "POST",
            url: "adm_new_products/",
            data: data,

            success: function (arv) {
                AdmEditFormProduct(arv)
            }
        });

        $.ajax({
            type: "POST",
            url: "adm_sizes_for_new_products/",
            data: data,

            success: function (arv) {
                AdmEditFormProductSizes(arv)
            }
        });

    }

    //(Admin_product) <!-- SELECT MULTIPLE Fills sizes of product on the form to change the product data.(js:AutoProductList)
    function AdmEditFormProductSizes(arv) {
        var json_dict = JSON.parse(arv);

        // name form, name Select field
        var select_form = document.adm_product_form.sizes;

        // clear select field
        for (var s0=0; s0<select_form.length; s0++){
            select_form.options[s0].selected=false
        }
        // Fill select field
        for (var s=0; s<json_dict.length; s++){
            select_form.options[(json_dict[s].id)-1].selected=true
        }
    }

    //(Admin_product) <!-- Fills out the form to change the product data.(js:AutoProductList)
    function AdmEditFormProduct(arv) {

        var json_dict = JSON.parse(arv);
        console.log(json_dict);

            if (json_dict[0].product__status_sale) {
                $('#id_status_sale').prop('checked', true);
            } else {
                $('#id_status_sale').prop('checked', false);
            }
            if (json_dict[0].product__status_new) {
                $('#id_status_new').prop('checked', true);
            } else {
                $('#id_status_new').prop('checked', false);
            }
            if (json_dict[0].product__prod_active) {
                $('#id_prod_active').prop('checked', true);
            } else {
                $('#id_prod_active').prop('checked', false);
            }
            if (json_dict[0].product__second_hands) {
                $('#id_second_hands').prop('checked', true);
            } else {
                $('#id_second_hands').prop('checked', false);
            }

            $('#id_product').val(json_dict[0].product__name);
            $('#id_name').val(json_dict[0].product__name);
            $('#id_article').val(json_dict[0].product__article);
            $('#id_discount').val(json_dict[0].product__discount);
            $('#id_category').val(json_dict[0].product__category__name);
            $('#id_fabric').val(json_dict[0].product__fabric__name);
            $('#id_short_description').val(json_dict[0].product__short_description);
            $('#id_description').val(json_dict[0].product__description);
            $('#id_year_model').val(json_dict[0].product__year_model);
            $('#id_price').val(json_dict[0].product__price);
            // $('#id_sizes').val(data.sizes);

            $('#id_img-adm').empty();
            if (json_dict[0].image){
            for (var im = 0; im < json_dict.length; im++) {
                var url_img = "javascript:";
                var img = "<img src='/media/" + json_dict[im].image + "' class='img-adm' id=" + json_dict[im].id + ">";

                $('#id_img-adm').append("<a href=" + url_img + " class='img_id_for_del' data-id_img = '" + json_dict[im].id + "' " +
                    "data-img = '" + json_dict[im].image + "' >" + img + "</a><br>");
                if (json_dict[im].is_main) {
                    $('#id_img-adm').append("<input type='checkbox' checked class='img-adm-ck ' id='" + json_dict[im].id + "_id_main'>is_main <br>");
                } else {
                    $('#id_img-adm').append("<input type='checkbox' class='img-adm-ck ' id='" + json_dict[im].id + "_id_main'>is main <br>");
                }
                if (json_dict[im].is_active) {
                    $('#id_img-adm').append("<input type='checkbox' checked class='img-adm-ck ' id='" + json_dict[im].id + "_id_active'>is active<br>");
                } else {
                    $('#id_img-adm').append("<input type='checkbox' class='img-adm-ck ' id='" + json_dict[im].id + "_id_active'>is active<br>");
                }
            }
            $('.img_id_for_del').click(ImageDelete);
            }else {
                alert("Нет ни одного фото для "+ document.getElementById('id_product').value);
                ShowBlockAddingImg()
            }

    }

    //(Admin_product) <!-- delete image (js:AutoProductList : ajax)
    function ImageDelete() {
        $('#show_img_for_del').empty();
        $('#div-del-img').show();

        var data = {};
        data.id_img = $(this).attr('data-id_img');
        data.img = $(this).attr('data-img');
        // data.name = document.getElementById('id_name').value;
        $('#id_img_for_del').val(data.id_img);
        // $('#id_prod_name').val(data.name);
        $('#show_img_for_del').append("<img src='" + data.img + "' class='img_for_del' >");
        console.log(data.id_img, data.name)
    }

    function ClouseBlockDeleteImg() {
        $('#div-del-img').hide();
    }

    //(Admin_product) <!-- Sends data to change the product data.
    //Образец отправки и js JSON объект
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
                // data = {};
                // data.article = document.getElementById('id_article').value;
                // data.description = document.getElementById('id_description').value;
                // data.short_description = document.getElementById('id_short_description').value;
                // data.description = document.getElementById('id_description').value;
                // data.year_model = document.getElementById('id_year_model').value;
                // data.price = document.getElementById('id_price').value;
                // data.fabric = document.getElementById('id_fabric').value;
                // data.category = document.getElementById('id_category').value;
                // data.discount = document.getElementById('id_discount').value;
                // data.name = document.getElementById('id_name').value;
                // data.status_sale = document.getElementById('id_status_sale').checked;
                // data.status_new = document.getElementById('id_status_new').checked;
                // data.prod_active = document.getElementById('id_prod_active').checked;
                console.log("Save end")
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

        // console.log("ajax ->" + data.username + "pass1 ->" + data.password1);

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

    // <!-- (Account) Displaying all orders of the selected user -->
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

    // <!-- (Account) Displaying all product of the selected order -->
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

    // <!-- (Account) Displaying info about selected product -->
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

    // <!-- (Account) Sends data for changing user data -->
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
