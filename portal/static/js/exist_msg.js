document.getElementById('myForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission to handle the input check with AJAX
    
    const inputValue = document.getElementById('receipt').value;
  
    // Make an AJAX request to the server to check if the input exists in the database
    fetch('/checkInput', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ input: inputValue })
    })
    .then(response => response.json())
    .then(data => {
      // Display the message above the input field based on the response from the server
      const messageContainer = document.getElementById('messageContainer');
      if (data.exists) {
        messageContainer.textContent = 'Input already exists!';
      } else {
        messageContainer.textContent = '';
      }
    })
    .catch(error => {
      console.error('Error occurred:', error);
    });
  });
  