function copyText () {
  const element = document.getElementById('copyButton')
  // Copy the text inside the text field
  const encouragementId = element.getAttribute('data-value')
  navigator.clipboard.writeText(`${window.location.protocol}//${window.location.host}?encouragement_id=${encouragementId}`)
}

// make an event listener for favorite button
function favoriteEncouragement() {
  const element = document.getElementById('favoriteEncouragement')

  const encouragementId = element.getAttribute('data-value') // Problem here, not getting the value of the button
  console.log(`this is my encouragement I'm saving ${encouragementId}`)

  fetch(`${window.location.protocol}//${window.location.host}/save-favorite`, { // this constructs the url
    method: 'POST',
    headers: {
      'Content-Type': 'application/json' // tells server this is a json request
    },
    credentials: 'include', // sends user credentials, so it knows which user is sending request
    body: JSON.stringify({ encouragement_id: encouragementId }) // takes JS object and turns it into a string
  })
    .then(function () { // anonymous function, not doing anything with response (vs code suggested this)
      console.log('success saving encouragement')
    })
    .catch((error) => { // in the case there was some error
      console.error('Error:', error) // log an error to the console
    })
}

// make an event listener for delete button
function deleteFavoriteEncouragement(encouragementId) {
  fetch(`${window.location.protocol}//${window.location.host}/delete-favorite`, { // this constructs the url
    method: 'POST',
    headers: {
      'Content-Type': 'application/json' // tells server this is a json request
    },
    credentials: 'include', // sends user credentials, so it knows which user is sending request
    body: JSON.stringify({ encouragement_id: encouragementId }) // takes JS object and turns it into a string
  })
    .then(function () { // anonymous function, not doing anything with response (vs code suggested this)
      const element = document.getElementById('encouragement-' + encouragementId) // grabs div id & encouragement_id
      element.remove() // Removes deleted encouragement from page on successful submission
    })
    .catch((error) => { // in the case there was some error
      console.error('Error:', error) // log an error to the console
    })
}

// makes an AJAX request for getting new encouragments
function getNextEncouragement() {
  let encouragementId = 0 // global variable to store encouragement id
  fetch(`${window.location.protocol}//${window.location.host}/next-encouragement`, {
    method: 'GET',
    credentials: 'include' // sends user credentials, so it knows which user is sending request
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById('encouragement-text').innerHTML = data.text

      encouragementId = data.id // not updating encouragementId
      console.log(data)
      setButtonValuesById(encouragementId)
    }) // changed this here to make an AJAX request
    .catch((error) => { // in the case there was some error
      console.error('Error:', error) // log an error to the console
    })
  document.getElementById('share-buttons').style.visibility ='visible'
  console.log(encouragementId)
  setButtonValuesById(encouragementId)
}

function shareOnFacebook() {
  const url = window.location.href
  const shareUrl = `http://www.facebook.com/sharer.php?u=${url}`
  window.open(shareUrl, '_blank')
}

function setButtonValuesById (id) {
  const favoriteEncouragementElem = document.getElementById('favoriteEncouragement')
  if (favoriteEncouragementElem) {
    favoriteEncouragementElem.setAttribute('data-value', id)
  }
  // document.getElementById("facebook")
  // document.getElementById("email").value = id;
  document.getElementById('copyButton').setAttribute('data-value', id)
}

// language selection dropdown button triggers translation of site to en or es
function selectLanguage(language) {
  fetch(`${window.location.protocol}//${window.location.host}/language/${language}`, { // changes language using variable in route
    method: 'GET',
    credentials: 'include' // sends user credentials, so it knows which user is sending request
  })
    .then(function () {
      window.location.reload() // anonymous function, not doing anything with response (vs code suggested this)
    })
}

function retryFetch(url, options, retries = 3) {
  return fetch(url, options)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      return response.json()
    })
    .catch(error => {
      console.error('Error:', error)
      if (retries > 0) {
        console.log(`Retrying fetch. ${retries} retries left.`)
        return retryFetch(url, options, retries - 1)
      } else {
        console.log('Fetch failed after all retries.')
        throw error
      }
    })
}

// make an event listener for add email for push notifications
function updateEmail() {
  // getting value of text field entered for email
  const email = document.getElementById('updateEmailId').value
  fetch(`${window.location.protocol}//${window.location.host}/profile/email`, { // this constructs the url
    method: 'POST',
    headers: {
      'Content-Type': 'application/json' // tells server this is a json request
    },
    credentials: 'include', // sends user credentials, so it knows which user is sending request
    body: JSON.stringify({ email: email }) // takes JS object and turns it into a string
  }).then(
    console.log('submitted email')
  ).catch((error) => { // in the case there was some error
    console.error('Error:', error) // log an error to the console
  })
}
