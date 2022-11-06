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
    fetch(`${window.location.protocol}//${window.location.host}/delete-favorite`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({encouragement_id: encouragement_id})
    })
    .then((response) => {
      console.log(response);
      const element = document.getElementById("encouragement-"+ encouragement_id);
      element.remove(); // Removes deleted encouragement from page on successful submission
    })
    .catch((error)=> {
      console.error('Error:', error);
    });
  }