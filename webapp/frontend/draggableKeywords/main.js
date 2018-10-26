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

function add(id, obj) {
    var bbox = document.getElementById("bottom-box");
    var parent = obj.parentNode;
    if(document.getElementById(id).innerHTML=="x") {
        document.getElementById(id).innerHTML="+";
        // document.getElementById(parent).style.visibility = "visible";
    }
    else {
        document.getElementById(id).innerHTML="x";
    }
    bbox.appendChild(parent);
    return false;
}

function setRandomColor() {
    var words = ['Drones', 'Robotics', 'Space', 'Sustainability', 'Gaming', 'Healthcare', 'Data', 
    'Artificial Intelligence', 'Bioprinting', 'Automotive'];
    words.forEach(function(element) {
        document.getElementById(element).style.background = getRandomColor(); // Setting the random color on your div element.
    });
}

function getRandomColor() {
    var colors = ['#6eba7f', '#ae90b0', '#eca0be', '#ea6763', '#f79960', '#fdd25a', '#3c9ccc'];
    return colors[Math.floor(Math.random() * Math.floor(colors.length))];
}


