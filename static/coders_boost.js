function copyText() {
    // Get the text field
    var copyText = document.getElementById("copyUrl");
  
    // Select the text field
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices
  
     // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);
  
  }

  //make an event listener for delete button
  function deleteFavoriteEncouragement(encouragement_id) {
    fetch(`${window.location.protocol}//${window.location.host}/delete-favorite`, { //this constructs the url
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', //tells server this is a json request
      },
      credentials: 'include',  //sends user credentials, so it knows which user is sending request
      body: JSON.stringify({encouragement_id: encouragement_id}) //takes JS object and turns it into a string
    })
    .then(function () {   //anonymous function, not doing anything with response (vs code suggested this)
      const element = document.getElementById("encouragement-" + encouragement_id); //grabs div id & encouragement_id
      element.remove(); // Removes deleted encouragement from page on successful submission
    })
    .catch((error)=> {  // in the case there was some error
      console.error('Error:', error); // log an error to the console
    });
  }

  //language selection dropdown button triggers translation of site to en or es
  function selectLanguage(language) {
    fetch(`${window.location.protocol}//${window.location.host}/language/${language}`, { //changes language using variable in route
      method: 'GET',
      credentials: 'include',  //sends user credentials, so it knows which user is sending request
    })
    .then(function () {   //anonymous function, not doing anything with response (vs code suggested this)
      return false
    })
  }