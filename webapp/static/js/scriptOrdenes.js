$('[data-toggle=confirmation]').confirmation({
  rootSelector: '[data-toggle=confirmation]',
});

$(document).ready(function(){

  var nombre;
  var tipo;
  var id;
  var uniqueProducts = function(prod){
    var max = parseInt($('#cant_productos').val());
    var value;
    var seenOnce = false;
    for (var i = 1; i <= max; i++) {
      value = $('#select'+i).val();
      if (!isNaN(value) && value.length !== 0) {
        if (parseInt(value) == prod){
          if (seenOnce){
            return false;
          } else {
            seenOnce = true;
          }
        }
      }
    }
    return true;
  };

  $('#select1').selectize({
    valueField: 'id',
    labelField: 'nombre',
    searchField: 'nombre',
    preload: true,
    options: [],
    load: function(query, callback) {
    $.ajax({
        url: "/productos/get_products",
        type: 'GET',
        dataType: 'json',
        error: function() {
            callback();
        },
        success: function(res) {
          callback(res);
        }
      });
    },
    create: function(input, callback){
      $('#confirm1').confirmation('show');
      nombre = input;
      callback({ value: id, text: input })
      },
    dropdownParent: 'body',
    sortField: {
      field: 'text',
      direction: 'asc'
    },
    onChange: function (value) {
      if(!uniqueProducts(value)){
        $(this)[0].clear();
        $.notify({
          icon: 'mdi mdi-cancel',
          title: "Error",
          message: "No se permite repetir productos."
          },{
          element: '#tablaProductos',
          type: "danger",
          clickToHide: true,
          autoHide: true,
          autoHideDelay: 100,
          showAnimation: 'slideDown',
          showDuration: 400,
          hideAnimation: 'slideUp',
          hideDuration: 200
        });
      };
    }
  });

  $('body').on('click', 'a.product_remove', function(){
    var id_remove = $(this).attr("data-remove");
    console.log("Al menos pesca esto: "+id_remove);
    $('#tablaProductos tr#'+id_remove).remove();
  });

  $("[data-toggle='confirmation']").on('confirmed.bs.confirmation', function(){
    $.ajax({
        url:"/productos/insertar_producto_get_id",
        method:"post",
        data: {nombre: nombre,
              tipo: "Insumo"},
        success:function(data){
          id = data;
        },
        error: function(){
          alert("Ha ocurrido un error :(");
        }
      });
  });
  $("[data-toggle='confirmation']").on('canceled.bs.confirmation', function(){
    $.ajax({
        url:"/productos/insertar_producto_get_id",
        method:"post",
        data: {nombre: nombre,
              tipo: "Activo"},
        success:function(data){
          id = data;
        },
        error: function(){
          alert("Ha ocurrido un error :(");
        }
      });
  });


  $(document).keyup(function() {
    $('tr').each(function(){
      var result = 1;
      $(this).find('.count').each(function () {
        var data = $(this).val();
        if (!isNaN(data) && data.length !== 0) {
          result = result * parseFloat(data);
        } else {
          result = 0;
        }
      });
      $('.count-sum', this).html("$ " + result);

    });
    var total = 0
    $(this).find('.count-sum').each(function () {
      var data = Number($(this).html().replace(/[^0-9\.-]+/g,""));
      total += data;
    });
    $('.count-sum-total').html("$ "+total);
    $('#total-sum').val(total);

    var impuesto = parseFloat($('#impuesto').val());
    var descuento = parseFloat($('#descuento').val());
    $('.total-impuesto').html("$ "+Math.round(impuesto*(total - descuento)));
    var final = Math.round((1+impuesto)*(total - descuento));
    $('.count-sum-total-final').html("$ "+final);
  });

 });
