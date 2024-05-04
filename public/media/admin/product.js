



$(function(){
    var btn1 = `<div> <button  id="calculate-btn-normal">Calculate</button> </div>`;
    $('.form-row.field-normal_price.field-normal_discount_percenatage .flex-container.form-multiline').append(btn1)

    var btn2 = `<div> <button id="calculate-btn-prime">Calculate</button> </div>`;
    $('.form-row.field-prime_price.field-prime_discount_percenatage .flex-container.form-multiline').append(btn2)

    var btn3 = `<div> <button  id="calculate-btn-dealer">Calculate</button> </div>`;
    $('.form-row.field-dealer_price.field-dealer_discount_percenatage .flex-container.form-multiline').append(btn3)

    var btn4 = `<span> <button id="clear-btn">Clear All</button> </span>`;
    $('.form-row.field-mrp .flex-container').append(btn4)

});


$(document).on('click', '#clear-btn', function(event) {
    event.preventDefault();
    $( '#id_mrp, #id_normal_price, #id_normal_discount_percenatage, #id_prime_price, #id_prime_discount_percenatage, #id_dealer_price, #id_dealer_discount_percenatage').val('')
})


function calculate_discount(mrp, price){
    return (((mrp - price)/mrp)*100);
};


function calculate_price(mrp, discount){
    return (mrp - ((discount * mrp) / 100));
};

$(document).on('click', '#calculate-btn-normal', function(event) {

    event.preventDefault();
    var normal_price = parseFloat($('#id_normal_price').val());
    var mrp = parseFloat($('#id_mrp').val());
    var normal_discount = parseFloat($('#id_normal_discount_percenatage').val());


    try{
        if(normal_price){
            var result = Math.round(calculate_discount(mrp, normal_price));
            $('#id_normal_discount_percenatage').val(result);
        }
        else if(normal_discount){
            var result = Math.round(calculate_price(mrp, normal_discount));
            $('#id_normal_price').val(result);
        }
        else{
            alert('Write Proper Values')
        }
    } catch(error){
        alert(`write proper values ${error}`)
    }

})

$(document).on('click', '#calculate-btn-prime', function(event) {

    event.preventDefault();
    var prime_price = parseFloat($('#id_prime_price').val());
    var mrp = parseFloat($('#id_mrp').val());
    var prime_discount = parseFloat($('#id_prime_discount_percenatage').val());


    try{
        if(prime_price){
            var result = Math.round(calculate_discount(mrp, prime_price));
            $('#id_prime_discount_percenatage').val(result);
        }
        else if(prime_discount){
            var result = Math.round(calculate_price(mrp, prime_discount));
            $('#id_prime_price').val(result);
        }
        else{
            alert('Write Proper Values')
        }
    } catch(error){
        alert(`write proper values ${error}`)
    }
})

$(document).on('click', '#calculate-btn-dealer', function(event) {

    event.preventDefault();
    var dealer_price = parseFloat($('#id_dealer_price').val());
    var mrp = parseFloat($('#id_mrp').val());
    var dealer_discount = parseFloat($('#id_dealer_discount_percenatage').val());


    try{
        if(dealer_price){
            var result = Math.round(calculate_discount(mrp, dealer_price));
            $('#id_dealer_discount_percenatage').val(result);
        }
        else if(dealer_discount){
            var result = Math.round(calculate_price(mrp, dealer_discount));
            $('#id_dealer_price').val(result);
        }
        else{
            alert('Write Proper Values')
        }
    } catch(error){
        alert(`write proper values ${error}`)
    }
})

