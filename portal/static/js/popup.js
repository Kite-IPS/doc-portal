// Function to show the popup div and background overlay when the submit button is clicked
function showPopup() {
    var popup = document.getElementById("popupDiv");
    var overlay = document.querySelector(".overlay");

    popup.style.display = "block";
    overlay.style.display = "block";
  }

  // Function to hide the popup div and background overlay
  function hidePopup() {
    var popup = document.getElementById("popupDiv");
    var overlay = document.querySelector(".overlay");

    popup.style.display = "none";
    overlay.style.display = "none";
  }

  // Add a click event listener to the submit button
  var submitButton = document.getElementById("submit");
  submitButton.addEventListener("click", showPopup);

  // Add a click event listener to the document to handle hiding the popup when clicking outside it
  document.addEventListener("click", function(event) {
    var popup = document.getElementById("popupDiv");
    if (!popup.contains(event.target) && event.target !== submitButton) {
      hidePopup();
    }
  });