$(function(){
    var loadForm = function(){
        $.ajax({
            url : btn.attr('data-url'),
            type : 'get',
            dataType : 'json',
            beforeSend: function(){
                $('#modalProduct').modal('show');
            },
            success: function(data) {
                $('#modalProduct .modalContent').html(data.html)
            }
        });
    }

    var saveForm = function(){
        var form = $(this);
        $.ajax({
            url : from.attr('action'),
            data : form.serialize(),
            type : from.attr('method'),
            dataType : 'json',
            success : function(data) {
                if (data.is_valid) {
                    $('#vendorDetail tbody').html(data.html_vendor);
                    #('#modalProduct').modal('hide');
                } else {
                    $('#modalProduct .modalContent').html(data.html)
                }
            }
        });
        return false;
    }

    $('.add-product').click(loadForm);
    $('#modalProduct').on("submit", ".product-add", saveForm);
    
})