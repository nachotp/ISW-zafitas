var cant_productos = 1;

$(document).ready(function(){
  var uniqueProducts = function(prod){
    var value;
    var seenOnce = false;
    for (var i = 0; i <= cant_productos; i++) {
      value = $('#id_form-'+i+'-producto').val();
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
      for (var i = 0; i <= cant_productos; i++) {
        $('#id_form-'+i+'-obra').val(value);
    }}
  });

  $('#id_form-0-producto').selectize({
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

  $('.add_product').click(function(){
    var idt = parseInt($('#tablaProductos tr:last').attr('id')) + 1;
    console.log(idt);
    var lastTotal = $('#tablaProductos').find('tr:last').find("cant").val();
    console.log(lastTotal);

      $('#tablaProductos tr:last').after(`
      <tr id="`+idt+`">
    <td>
        <select name="form-`+idt+`-producto" id="id_form-`+idt+`-producto" </select>
    </td>
    <td>
        <input type="number" name="form-`+idt+`-cantidad" min="1" id="id_form-`+idt+`-cantidad" class="form-control cant">
    </td>
    <td>
        <input type="hidden" name="form-`+idt+`-obra" id="id_form-`+idt+`-obra" value="`+$('#selectObra').val()+`">
    </td>
    <td>

    </td>
    </tr>
      `);
      $('#id_form-'+idt+'-producto').selectize({
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

      var cantRows = parseInt($('#id_form-TOTAL_FORMS').val());
      $('#id_form-TOTAL_FORMS').val(cantRows + 1);
  });

 });
