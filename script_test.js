// File with the test scripts for the html file

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('inputForm').addEventListener('submit', function(event) {
        event.preventDefault();

        var dropDownValue = document.getElementById('dropdownButton').textContent

        var input = document.getElementById('numberInput').value;
        document.getElementById('displayNumberInput').textContent = "You want to pay " + input + " euros for " + dropDownValue + ". Is this right?";

        // Clear previous button if any
        var buttonArea = document.getElementById('buttonAreaNumberInput');
        buttonArea.innerHTML = '';

        // Adding the confirmation buttons
        var yesButton = document.createElement('button');
        yesButton.setAttribute('type', 'button'); //prevents form submission when using the button
        yesButton.textContent = 'YES';
        yesButton.onclick = function() {
            document.getElementById('displayNumberInput').textContent = '';
            document.getElementById('confirmationNumberInput').textContent = dropDownValue + ': paid ' + input + ' euros.';
            buttonArea.innerHTML = '';

            var currentTime = new Date().toLocaleTimeString('en-GB', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false 
            });

            var logArea = document.getElementById('logNumberInput');
            var logEntry = document.createElement('div')
            logEntry.textContent = dropDownValue + ": " + input + " euros added. (" + currentTime + ").";
            logArea.prepend(logEntry);
        }

        var noButton = document.createElement('button');
        noButton.setAttribute('type', 'button');
        noButton.textContent = 'NO';
        noButton.onclick = function() {
            document.getElementById('displayNumberInput').textContent = '';
            document.getElementById('confirmationNumberInput').textContent = 'Cancelled transaction.';
            buttonArea.innerHTML = '';
        }

        // Append the confirmation buttons to the HTML
        buttonArea.appendChild(yesButton);
        buttonArea.appendChild(noButton);
    });
});

// Function to show/hide the dropdown
function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Function to handle dropdown item click
function chooseItem(value) {
    document.getElementById("dropdownButton").textContent = value; // Update button text
    document.getElementById("myDropdown").classList.remove("show"); // Hide the dropdown

    document.getElementById('requiredDropDownValue').value = value
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropdown button')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}