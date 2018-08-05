var cant_productos = 1;

$(document).ready(function(){
  var uniqueProducts = function(prod){
    var value;
    var seenOnce = false;
    for (var i = 1; i <= cant_productos; i++) {
      value = $('#select'+i).val();
      if (!isNaN(value) && value.length !== 0) {
        if (parseInt(value) === prod){
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

  $('#selectObra').selectize({
    valueField: 'id',
    searchField: 'nombre',
    labelField: 'nombre',
    preload: true,
    create: false,
    options: [],
    load: function(query, callback) {
    $.ajax({
        url: "api/getobras",
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
    onChange: function (value) {
      for (var i = 1; i <= cant_productos; i++) {
        $('#obra'+i).val(value);
    }}
  });

  $('#select1').selectize({
    valueField: 'id',
    labelField: 'nombre',
    searchField: 'nombre',
    preload: true,
    create: false,
    options: [],
    load: function(query, callback) {
    $.ajax({
        url: "api/getprods",
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
      }
    }
  });

  $('body').on('click', 'a.product_remove', function(){
    var id_remove = $(this).attr("data-remove");
    console.log("Al menos pesca esto: "+id_remove);
    $('#tablaProductos tr#'+id_remove).remove();
  });

 });
