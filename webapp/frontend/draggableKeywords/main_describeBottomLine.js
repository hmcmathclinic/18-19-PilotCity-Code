var words1 = ['Client Acquisition', 'Use Cases', 'Building Community', 'Training Talent'];
var words2 = ['Social Media Marketing', 'Manual Recruitment', 'Attending Conferences'];

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

function add1(parent, close_id) {
    var bot_box = document.getElementById("bottom-box-1");
    var big_box = document.getElementById("big-box-1");
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

function add2(parent, close_id) {
    var bot_box = document.getElementById("bottom-box-2");
    var big_box = document.getElementById("big-box-2");
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
    words1.forEach(function(element) {
        document.getElementById(element).style.background = getRandomColor(); // Setting the random color on your div element.
    });
    words2.forEach(function(element) {
        document.getElementById(element).style.background = getRandomColor(); // Setting the random color on your div element.
    });
}

function getRandomColor() {
    var colors = ['#6eba7f', '#ae90b0', '#eca0be', '#ea6763', '#f79960', '#fdd25a', '#3c9ccc'];
    return colors[Math.floor(Math.random() * Math.floor(colors.length))];
}

function search1() { 
    var frm = document.getElementById('searchForm-1');
    var name = frm.elements["searchItem-1"].value; 
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
    if(words1.includes(name_use)) {
        addFromSearch1(name_use);
    }
    else {
        $('#bottom-box-1').append("<div class='draggableItem' id='tmp' draggable='false'>ymp</div>");
        document.getElementById('tmp').id = name_use;
        var node = document.getElementById(name_use);
        node.innerHTML = "<span id=" + 'add'+name_use.replace(/ +/g, "") + ">+</span>" + "   " + name_use;
        var click = "add(this, 'add" + name_use.replace(/ +/g, "") +"')";
        var dragstart = "drag(event, 'add" + name_use.replace(/ +/g, "") +"')";
        node.style.background = getRandomColor();
        node.setAttribute("onclick", click);
        node.setAttribute("ondragstart", dragstart);
        words1.push(name_use);
        // if(name_use.includes(" ")) {
        //     document.getElementById('tmp')
        // }
        addFromSearch1(name_use);
    }
}

function addFromSearch1(id) {
    var parent = document.getElementById(id);
    var bot_box = document.getElementById("bottom-box-1");
    var big_box = document.getElementById("big-box-1");
    var id_no_space = id.replace(/ +/g, "");
    if(document.getElementById('add' + id_no_space).innerHTML=="+") {
        document.getElementById('add' + id_no_space).innerHTML="x";
        bot_box.appendChild(parent);
    }
    return false;
}

function addFromSearch2(id) {
    var parent = document.getElementById(id);
    var bot_box = document.getElementById("bottom-box-2");
    var big_box = document.getElementById("big-box-2");
    var id_no_space = id.replace(/ +/g, "");
    if(document.getElementById('add' + id_no_space).innerHTML=="+") {
        document.getElementById('add' + id_no_space).innerHTML="x";
        bot_box.appendChild(parent);
    }
    return false;
}

function autocomplete(inp, arr, one) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) {x[currentFocus].click(); currentFocus = -1;}
        }
        else{
            closeAllLists();
            console.log(one);
            if(one == "1")
              {
                search1();
              }
            else
            {
              console.log("here");
              search2();
            }
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
    });
}


function search2() { 
    var frm = document.getElementById('searchForm-2');
    var name = frm.elements["searchItem-2"].value; 
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
    if(words2.includes(name_use)) {
        addFromSearch2(name_use);
    }
    else {
        $('#bottom-box-2').append("<div class='draggableItem' id='tmp' draggable='false'>ymp</div>");
        document.getElementById('tmp').id = name_use;
        var node = document.getElementById(name_use);
        node.innerHTML = "<span id=" + 'add'+name_use.replace(/ +/g, "") + ">+</span>" + "   " + name_use;
        var click = "add(this, 'add" + name_use.replace(/ +/g, "") +"')";
        var dragstart = "drag(event, 'add" + name_use.replace(/ +/g, "") +"')";
        node.style.background = getRandomColor();
        node.setAttribute("onclick", click);
        node.setAttribute("ondragstart", dragstart);
        words2.push(name_use);
        // if(name_use.includes(" ")) {
        //     document.getElementById('tmp')
        // }
        addFromSearch2(name_use);
    }
}

  function main() {
    setRandomColor();
    /*initiate the autocomplete function on the "searchItem" element, and pass along the words array as possible autocomplete values:*/
    autocomplete(document.getElementById("searchItem-1"), words1, "1");
    autocomplete(document.getElementById("searchItem-2"), words2, "2");
}