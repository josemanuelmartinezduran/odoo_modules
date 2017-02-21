var tpv_window_lib = new Object();

tpv_window_lib.popup_counter = 0;


//función general para mandar mensaje
tpv_window_lib.show_popup = function (innerWidth, innerHeight, tipo, funcion) {
    
    tpv_window_lib.heightClient = window.innerHeight;
    
    body = document.body
    cortina = document.createElement("div");
    cortina.style.backgroundColor = "#000";
    cortina.style.width = "100%";
    cortina.style.height = tpv_window_lib.heightClient + "px";
    cortina.style.top = 0;
    cortina.style.left = 0;
    cortina.style.position = "fixed";
    cortina.style.opacity = "0.3";
    cortina.zIndex = 10000 + tpv_window_lib.popup_counter;
    cortina.id = 10000 + tpv_window_lib.popup_counter;
    cortina.style.display = "block";
    body.appendChild(cortina);
    
    popup = document.createElement("div");
    popup.style.width = "100%";
    popup.style.height = tpv_window_lib.heightClient + "px";
    popup.style.top = 0;
    popup.style.left = 0;
    popup.style.position = "absolute";
    popup.style.textAlign = "center";
    popup.zIndex = 10001 + tpv_window_lib.popup_counter;
    popup.id = 10001 + tpv_window_lib.popup_counter;
    popup.style.display = "block";
    body.appendChild(popup);
    
    contenido = document.createElement("div");
    contenido.style.width = innerWidth;
    contenido.style.height = innerHeight;
    contenido.style.margin = "0 auto";
    contenido.style.backgroundColor = "#FFF";
    
    if (tipo == "popup") {
        contenido.style.marginTop = "20%";
    }
    if (tipo == "ventana") {
        contenido.style.marginTop = "5%";
    }
    contenido.id = 10002 + tpv_window_lib.popup_counter;
    contenido.innerHTML = "<div style='width:auto; height:25px;text-align:right;padding-right:5px; cursor:pointer' onclick='tpv_window_lib.hide_popup("+tpv_window_lib.popup_counter+")'><span class='order-button square'><i class='fa fa-check'></i></span></div>";
    contenido.style.borderRadius = "5px";
    //contenido.style.boxShadow = "4px 4px 10px #555";
    //contenido.style.backgroundColor = "#CCC";
    contenido.style.overflow = "auto";
    popup.appendChild(contenido);
    
    tpv_window_lib.popup_counter++;
    
    eval(funcion);
    
}

tpv_window_lib.hide_popup = function (id) {
    contenido = document.getElementById(10001+id);
    document.body.removeChild(contenido);
    cortina = document.getElementById(10000+id);
    document.body.removeChild(cortina);
    
}

