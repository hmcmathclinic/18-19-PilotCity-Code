// Copyright 2016, Google, Inc.
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

$(function(){
  // This is the host for the backend.
  // TODO: When running Firenotes locally, set to http://localhost:8081. Before
  // deploying the application to a live production environment, change to
  // https://backend-dot-<PROJECT_ID>.appspot.com as specified in the
  // backend's app.yaml file.
  //var backendHostUrl = 'https://backend-dot-silver-osprey-217701.appspot.com';
  var backendHostUrl = 'http://localhost:8081';

  // [START gae_python_firenotes_config]
  // Obtain the following from the "Add Firebase to your web app" dialogue
  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyATvZ71rmui_33x_XJDEw0dZm6Tt2iItTA",
    authDomain: "users-94e00.firebaseapp.com",
    databaseURL: "https://users-94e00.firebaseio.com",
    projectId: "users-94e00",
    storageBucket: "users-94e00.appspot.com",
    messagingSenderId: "1022626447098"
  };
  // [END gae_python_firenotes_config]

  // This is passed into the backend to authenticate the user.
  var userIdToken = null;

  // Firebase log-in
  
  function configureFirebaseLogin() {

    firebase.initializeApp(config);

    // [START gae_python_state_change]
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        $('#logged-out').hide();
        var name = user.displayName;

        /* If the provider gives a display name, use the name for the
        personal welcome message. Otherwise, use the user's email. */
        var welcomeName = name ? name : user.email;

        user.getToken().then(function(idToken) {
          userIdToken = idToken;

          createUserEntryInDb()
          $('#user').text(welcomeName);
          $('#logged-in').show();

        });

      } else {
        $('#logged-in').hide();
        $('#logged-out').show();

      }
    // [END gae_python_state_change]

    });

  }

  // [START configureFirebaseLoginWidget]
  // Firebase log-in widget
  function configureFirebaseLoginWidget() {
    var uiConfig = {
      'signInSuccessUrl': '/',
      'signInOptions': [
        // Leave the lines as is for the providers you want to offer your users.
        firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        firebase.auth.FacebookAuthProvider.PROVIDER_ID,
        firebase.auth.EmailAuthProvider.PROVIDER_ID
      ],
      // Terms of service url
      'tosUrl': '<your-tos-url>',
    };

    var ui = new firebaseui.auth.AuthUI(firebase.auth());
    ui.start('#firebaseui-auth-container', uiConfig);
  }
  // [END gae_python_firebase_login

  function createUserEntryInDb() {
    $.ajax(backendHostUrl + '/user/data/onboarding', {
      /* Set header for the XMLHttpRequest to get data from the web server
      associated with userIdToken */
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      }
    }).then(function(data){
      fetchUserData()
    });
  }

  function fetchUserData() {
    $.ajax(backendHostUrl + '/user/data', {
      /* Set header for the XMLHttpRequest to get data from the web server
      associated with userIdToken */
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      }
    }).then(function(data){
      console.log(data)
      console.log("Fetched user data successfully")
      updateFormCompletionStatus(false)
    });
  }

  function updateFormCompletionStatus(status) {
    $.ajax(backendHostUrl + '/user/data/updateformcompletionstatus', {
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      },
      method: 'POST',
      data: JSON.stringify({'completedform': status}),
      contentType : 'application/json'
    }).then(function(data){
      console.log("update form completion status successful")
      console.log(data)
    }); 
  }


  // Sign out a user
  var signOutBtn =$('#sign-out');
  signOutBtn.click(function(event) {
    event.preventDefault();

    firebase.auth().signOut().then(function() {
      console.log("Sign out successful");
    }, function(error) {
      console.log(error);
    });
  });

  // Save a teacher/employer/student response to the backend
  
    $('#save-res').click(function(event) {
      event.preventDefault();

    if ($('#radioEmployer').prop('checked')) {
      window.location = 'googleform_employer.html';
    }

    else if ($('#radioTeacher').prop('checked')) {
      window.location = 'googleform_teacher.html';
    }

  
    /*
    var noteField = $('#note-content');
    var note = noteField.val();
    noteField.val("");
    
    /* Send note data to backend, storing in database with existing data
    associated with userIdToken */
    
    $.ajax(backendHostUrl + '/notes', {
      headers: {
        'Authorization': 'Bearer ' + userIdToken
      },
      method: 'POST',
      data: JSON.stringify({'message': note}),
      contentType : 'application/json'
    }).then(function(){
      // Refresh notebook display.
      fetchNotes();
    }); 
  
  });

  configureFirebaseLogin();
  configureFirebaseLoginWidget();

});