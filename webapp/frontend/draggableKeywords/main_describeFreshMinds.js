var words = ['Could You Create A New Internet Of Things Application For Your Local Transit System?', 
            'If You Had A Smart Home, What Sequences Of Tasks Would You Automate To Better Your Life?',
            'How Would Citizens Use An App To Report Public Safety Incidents?'];

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev, id) {
    ev.dataTransfer.setData("text", ev.target.id);
    if(document.getElementById(id).innerHTML=="x") {
        document.getElementById(id).innerHTML="+";
    }
    else {
        document.getElementById(id).innerHTML="x";
    }
}

function drop(ev) {
    var data = ev.dataTransfer.getData("text");
    var x = document.getElementById(data);
    ev.target.appendChild(x);
    ev.preventDefault(x);
}

function add(parent, close_id) {
    var bot_box = document.getElementById("bottom-box");
    var big_box = document.getElementById("big-box");
    if(document.getElementById(close_id).innerHTML=="x") {
        document.getElementById(close_id).innerHTML="+";
        big_box.appendChild(parent);
    }
    else { // if +
        document.getElementById(close_id).innerHTML="x";
        bot_box.appendChild(parent);
    }
    return false;
}

function setRandomColor() {
    words.forEach(function(element) {
        document.getElementById(element).style.background = getRandomColor(); // Setting the random color on your div element.
    });
}

function getRandomColor() {
    var colors = ['#6eba7f', '#ae90b0', '#eca0be', '#ea6763', '#f79960', '#fdd25a', '#3c9ccc'];
    return colors[Math.floor(Math.random() * Math.floor(colors.length))];
}

function search() { 
    var frm = document.getElementById('searchForm');
    var name = frm.elements["searchItem"].value; 
    frm.reset();
    name = name.trim();
    if(name == "") {
        return;
    }
    var name_lower = name.toLowerCase();
    var name_use = name.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
    name_use = name_use.replace(/\s+/g,' ').trim();
    if(name_use.charAt(name_use.length-1) != '?') {
        name_use += '?';
    }
    if(words.includes(name_use)) {
        addFromSearch(name_use);
    }
    else {
        $('#bottom-box').append("<div class='draggableItem' id='tmp' draggable='false'>ymp</div>");
        document.getElementById('tmp').id = name_use;
        var node = document.getElementById(name_use);
        node.innerHTML = "<span id=" + 'add'+name_use.replace(/ +/g, "") + ">+</span>" + "   " + name_use;
        var click = "add(this, 'add" + name_use.replace(/ +/g, "") +"')";
        var dragstart = "drag(event, 'add" + name_use.replace(/ +/g, "") +"')";
        node.style.background = getRandomColor();
        node.setAttribute("onclick", click);
        node.setAttribute("ondragstart", dragstart);
        words.push(name_use);
        // if(name_use.includes(" ")) {
        //     document.getElementById('tmp')
        // }
        addFromSearch(name_use);
    }
}

function addFromSearch(id) {
    var parent = document.getElementById(id);
    var bot_box = document.getElementById("bottom-box");
    var big_box = document.getElementById("big-box");
    var id_no_space = id.replace(/ +/g, "");
    if(document.getElementById('add' + id_no_space).innerHTML=="+") {
        document.getElementById('add' + id_no_space).innerHTML="x";
        bot_box.appendChild(parent);
    }
    return false;
}



