function get_date(duration = null, type = null,booking_type=null) {
    var currentDate = new Date();
    duration=parseInt(duration)
    if(booking_type){
        if(booking_type=='1'){
            type="daily"; 
        }
        if (booking_type == '2'){
            type = 'yearly'
        }
        if (booking_type == '3'){
            type = 'monthly'
        }   
        duration = parseInt($("#id_duration").val()) ||  parseInt($("#id_durations").val())
    }
    if (duration && type === 'yearly') {
        currentDate.setFullYear(currentDate.getFullYear() + duration);
    }
    else if (type ==='monthly'){
        currentDate.setMonth(currentDate.getMonth()+duration);
    }
    else if (type === 'daily') {
        currentDate.setDate(currentDate.getDate() + duration);
    }
    var day = ('0' + currentDate.getDate()).slice(-2);
    var month = ('0' + (currentDate.getMonth() + 1)).slice(-2);
    var year = currentDate.getFullYear();
    var hours = ('0' + currentDate.getHours()).slice(-2);
    var minutes = ('0' + currentDate.getMinutes()).slice(-2);
    // var seconds = ('0' + currentDate.getSeconds()).slice(-2);
    // console.log(seconds)


    var formattedDateTimeForInput = year + '-' + month + '-' + day + 'T' + hours + ':' + minutes ;
    console.log(formattedDateTimeForInput)

    return formattedDateTimeForInput;
}

function calculateDuration(checkIn, checkOut, bookingType) {
    var checkInDate = new Date(checkIn);
    var checkOutDate = new Date(checkOut);

    switch (bookingType) {
        case 'Daily':
            var diffTime = Math.abs(checkOutDate - checkInDate);
            var durationInHours = diffTime / (1000 * 60 * 60);
            // If the stay exceeds 24 hours by even 1 hour, it's considered an extra day
            return Math.ceil(durationInHours / 24);

        case 'Monthly':
            var monthsDiff = checkOutDate.getMonth() - checkInDate.getMonth() + 
                             (12 * (checkOutDate.getFullYear() - checkInDate.getFullYear()));
            if (checkOutDate.getDate() > checkInDate.getDate() || 
                (checkOutDate.getDate() === checkInDate.getDate() && checkOutDate.getHours() >= checkInDate.getHours())) {
                monthsDiff++;
            }
            return monthsDiff;

        case 'Yearly':
            var yearsDiff = checkOutDate.getFullYear() - checkInDate.getFullYear();
            if (checkOutDate.getMonth() > checkInDate.getMonth() || 
                (checkOutDate.getMonth() === checkInDate.getMonth() && checkOutDate.getDate() > checkInDate.getDate()) ||
                (checkOutDate.getMonth() === checkInDate.getMonth() && checkOutDate.getDate() === checkInDate.getDate() && checkOutDate.getHours() >= checkInDate.getHours())) {
                yearsDiff++;
            }
            return yearsDiff;

        default:
            return 0;
    }
}

function convertDate(inputDateTime) {
    var months = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
        "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
        "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    };

    // Split the input datetime string into date and time parts
    var parts = inputDateTime.split(", ");
    var dateParts = parts[0].split(" ");
    var timePart = parts[2];
    var year = parts[1];
    var month = months[dateParts[0].substring(0, 3)];
    var day = dateParts[1];

    // Ensure day is two digits
    day = day.length === 1 ? '0' + day : day;

    // Adjust time format
    var timeSplit = timePart.split(" ");
    var time = timeSplit[0];
    var ampm = timeSplit[1];

    if (ampm) {
        ampm = ampm.toUpperCase();

        if (ampm.includes('P.M.')) {
            ampm = 'PM';
        } else if (ampm.includes('A.M.')) {
            ampm = 'AM';
        }

        // Handle time format variations
        var [hours, minutes = '00', seconds = '00'] = time.split(':');
        hours = parseInt(hours, 10);

        // Convert to 24-hour format if needed
        if (ampm === 'PM' && hours < 12) {
            hours += 12;
        } else if (ampm === 'AM' && hours === 12) {
            hours = 0;
        }

        // Ensure hours and minutes are two digits
        hours = ('0' + hours).slice(-2);
        minutes = ('0' + minutes).slice(-2);
        seconds = ('0' + seconds).slice(-2);

        // Combine into new format
        return year + '-' + month + '-' + day + 'T' + hours + ':' + minutes + ':' + seconds;
    }

    return 'Invalid Date Time Format';
}
// var convertedDateTime = convertDate("Dec. 24, 2023, 9:05 p.m.");


// convertDate()

// function daysBetween(date1, date2) {
//     // Parse the dates
//     var d1 = new Date(date1);
//     var d2 = new Date(date2);

//     console.log(d1,d2)

//     // Calculate the difference in milliseconds
//     var difference = Math.abs(d2 - d1);

//     // Convert milliseconds to days
//     var days = difference / (1000 * 60 * 60 * 24);

//     console.log(Math.round(days))

//     // if (Math.round(days) > 1)
//         return Math.round(days);
//     // else return 0
// }

function updatetotal(){
    //calculate total price
    var rate = $('#id_rate').val()
    var duration = $('#id_duration').val()
    console.log(rate,duration)
    var numericRate = parseFloat(rate);
    var numericDuration = parseInt(duration, 10);
    var result = (!isNaN(numericRate) && !isNaN(numericDuration)) ? numericRate * numericDuration : 'Invalid input';

    return result

}

function calculate_total(rate,duration){

var numericRate = parseFloat(rate);
    var numericDuration = parseInt(duration, 10);
    if (!isNaN(numericRate) && !isNaN(numericDuration)) {
        var result = numericRate * numericDuration;
        return result.toFixed(2); // Call toFixed only if result is a number
    } else {
        return 'Invalid input';
    }
}



function calculateTotal(){
    //calculate total price
    var rate = $('#id_rate').val()
    var duration = $('#id_duration').val()
    console.log(rate,duration)
    var numericRate = parseFloat(rate);
    var numericDuration = parseInt(duration, 10);
    var result = (!isNaN(numericRate) && !isNaN(numericDuration)) ? numericRate * numericDuration : 'Invalid input';

    return result

}

function calculation_Summary(){
    var amount = calculate_total($('#id_rates').val(),$('#id_durations').val())
    var discount = parseFloat($('#id_discounts').val()) 
    var total =  amount-discount
    var advance = parseFloat($('#advance').text())
    var net_total = total-advance
    $('#totalinput').val(total)
    $('#id_checkout_anount').val(net_total)
    $('#id_total_amount').text(calculate_total($('#id_rates').val(),$('#id_durations').val()))
    $('#total').text(total.toFixed(2))
    $('#net_total').text(net_total.toFixed(2))
}

$('#id_rate').on('change',function(){
    $('#id_total_amount').val(updatetotal().toFixed(2))
    $('#id_discount').val(0.0)
})

$('#id_discounts').on('input',function(){
    $('#discount').text($(this).val())
    calculation_Summary()
})


$('#id_rates').on('input',function(){
   calculation_Summary()

})

$('#id_discount').on('change',function(){
    var discount = parseFloat($(this).val())
    var total = updatetotal().toFixed(2) - discount
    $('#id_total_amount').val(total.toFixed(2))

})

$('#id_duration').on('input',function(){
    var type = $('#id_booking_type').val()
    $('#id_expected_checkout_date').val(get_date($(this).val(),null,type)); 
    $('#id_total_amount').val(updatetotal().toFixed(2))
    $('#id_discount').val(0.0)
})



$(document).ready(function(){
    var convertedDateTime = convertDate("Dec. 24, 2023, 9:05 p.m.");
    console.log(convertedDateTime);
    var duration = $('#id_durations').val()
    console.log(duration)
    // console.log($('#id_check_in_date').val().toString().length)
    if($('#id_check_in_date').val()<1){
        $('#id_check_in_date').val(get_date())

    }

    var expected_date = convertDate($('#id_expcheck_out_dates').val())
    
        $('#id_check_out_dates').val(get_date())

    // console.log( $('#id_check_in_date').val(get_date()),'qq')
    // $('#id_check_out_dates').val(get_date(duration,null,'1'));
$('#id_check_in_dates').val(convertDate($('#check_in').text()))
var exoected=$('#id_check_outt_date').val()
$('#id_check_outt_date').val(convertDate(exoected))
    var type = $('#id_booking_types').val()
    $('#id_durations').val(calculateDuration($('#id_check_in_dates').val(),$('#id_check_out_dates').val(),type))
    calculation_Summary()
    console.log($('#id_checkout_anount').val())

})



$('#id_check_out_dates').on('change',function(){

    var type = $('#id_booking_types').val()
    $('#id_durations').val(calculateDuration($('#id_check_in_dates').val(),$('#id_check_out_dates').val(),type))
    calculation_Summary()

})

$('#filter_btn').on('click',function(){
    var url = $(this).data('url')
    var start_date =$('#start_date').val()
    var end_date = $('#end_date').val()
    if(start_date && end_date)
       window.location=url+"?start="+start_date+"&end="+end_date;
})



$('#id_booking_type').on('change',function(){
    var value = $(this).val()
        var url = window.location.href
        if (value != "") {
            $.ajax({
                type: 'GET',
                url: url,
                data: {
                    'type': value
                },
                success: function (response) {
                    $('#id_rate').val(response.room_rate)
                    var duration =parseInt($('#id_duration').val(), 10);
                    if(value=='1'){
                        $('#id_expected_checkout_date').val(get_date(duration,'daily')); 
                    }
                    if (value == '2'){
                        $('#id_expected_checkout_date').val(get_date(duration,'yearly')); 
                    }
                    if (value == '3'){
                        $('#id_expected_checkout_date').val(get_date(duration,'monthly')); 
                    }
                    $('#id_discount').val(0.0)
                    $('#id_total_amount').val(updatetotal().toFixed(2))
                    // console.log(response)
                },
                error: function (xhr, status, error) {
                    console.error(xhr.responseText);
                }
            });
        }
})