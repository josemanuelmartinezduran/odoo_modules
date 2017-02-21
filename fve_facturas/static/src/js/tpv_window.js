var tpv_window = new Object();


tpv_window.ver_web = function(agrupador) {
    agrupador = 10002+agrupador;
    div_agrupador = document.getElementById(agrupador);
    iframe = document.createElement("iframe");
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    iframe.src = "http://odoo.com";
    div_agrupador.appendChild(iframe);
}

tpv_window.ver_contenido = function(agrupador) {
    agrupador = 10002+agrupador;
    div_agrupador = document.getElementById(agrupador);
    mi_contenido = document.createElement("div");
    mi_contenido.innerHTML = "Mi contenido";
    div_agrupador.appendChild(mi_contenido);
}

tpv_window.ver_usuarios = function(agrupador) {
    agrupador = 10002+agrupador;
    div_agrupador = document.getElementById(agrupador);
    mi_contenido = document.createElement("div");
    mi_contenido.innerHTML = "Usuarios en Odoo";
    
    var Users = new openerp.Model('res.users');
    
    Users.query(['name'])
    .filter([['active', '=', true]])
    .all().then(function (users) {
        for (i in users) {
            mi_contenido.innerHTML = mi_contenido.innerHTML + "<br><br>" + users[i].name;
        }
    });    
    
    div_agrupador.appendChild(mi_contenido);
}

tpv_window.ventana1 = function() {
    tpv_window_lib.show_popup("80%", "80%","ventana","tpv_window.ver_web("+tpv_window_lib.popup_counter+")");
}

tpv_window.ventana2 = function() {
    tpv_window_lib.show_popup("50%", "50%","popup","tpv_window.ver_contenido("+tpv_window_lib.popup_counter+")");
}

tpv_window.ventana3 = function() {
    tpv_window_lib.show_popup("50%", "50%","popup","tpv_window.ver_usuarios("+tpv_window_lib.popup_counter+")");
}

tpv_window.ventana4 = function() {
    var Users = new openerp.Model('tpv_window');
    mi_dato = "hola";
    Users.call('accion', [mi_dato]).then(function (result) {
        alert("La función se ha ejecutado.");
    });     
}


function init() {
    /*Agregando dos botones abajo del panel izquierdo order*/
    order = $(".order-scroller");
    order.append("<div><button onclick='tpv_window.ventana1()'>Ver página web</button></div>");
    order.append("<div><button onclick='tpv_window.ventana2()'>Ver mi contenido</button></div>");
    /*Agregando botoenes que interacturan con python*/
    order.append("<div><button onclick='tpv_window.ventana3()'>Ver usuarios</button></div>");
    order.append("<div><button onclick='tpv_window.ventana4()'>Ejecutar función</button></div>");
    
}

/* Lanzando la funcion inicial */
window.setTimeout("init()", 10000);



