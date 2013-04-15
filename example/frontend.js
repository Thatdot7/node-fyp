function xml_http_post(url, data, callback) {
    var req = false;
    try {
        // Firefox, Opera 8.0+, Safari
        req = new XMLHttpRequest();
    }
    catch (e) {
        // Internet Explorer
        try {
            req = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            try {
                req = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }
    }
    req.open("POST", url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            callback(req);
        }
    }
    req.send(data);
}

window.onload = function test_button() {
	setInterval(function() {
    var data = document.test_form.test_text.value;           
    xml_http_post("frontend.html", data, test_handle)},400);
}

function test_handle(req) {
    var elem = document.getElementById('test_result')
    elem.innerHTML =  req.responseText
}
