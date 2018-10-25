function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev, close_id) {
    ev.dataTransfer.setData("text", ev.target.id);
    document.getElementById(close_id).innerHTML="x";
}

function drop(ev) {
    var data = ev.dataTransfer.getData("text");
    var x = document.getElementById(data);
    ev.target.appendChild(x);
    ev.preventDefault(x);
}

function add(id, obj) {
    var bbox = document.getElementById("bottom-box");
    var node = obj.parentNode;
    document.getElementById(id).innerHTML="x";
    bbox.appendChild(obj.parentNode);
    return false;
}
