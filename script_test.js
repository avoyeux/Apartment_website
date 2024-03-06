// File with the test scripts for the html file
class firstSubmitFollow {
  constructor() {
    this.modal = document.getElementById('myModal');
    this.dropDownValue = document.getElementById('dropdownButton').textContent;
    this.isValidDropDown = this.dropDownValue !== "Select an option";
    this.number = document.getElementById('numberInput').value; 
    this.yesNoButtonArea = document.getElementById('buttonAreaNumberInput');
    this.yesButton = document.createElement('button');
    this.noButton = document.createElement('button');
    this.closeButton = document.querySelector('.close');
    this.okButton = document.createElement('button');
    this.displayQuestion = document.getElementById('displayNumberInput');
    this.logArea = document.getElementById('logNumberInput');
    this.logEntry = document.createElement('div');
  }

  structure() {
    this.displayQuestion.textContent = '';

    if (this.isValidDropDown) {
      this.modal.style.display = 'flex';
      document.getElementById('inputForm').reset();

      this.yesNoButtonArea.innerHTML = '';
      this.yesButton.setAttribute('type', 'button');
      this.noButton.setAttribute('type', 'button');
      this.yesButton.textContent = 'YES';
      this.noButton.textContent = 'NO';
      this.displayQuestion.textContent =  "You want to pay " + this.number + " euros for " + this.dropDownValue + ". Is this right?";

      this.closeButton.onclick = () => {this.modal.style.display = 'none'};
      this.yesButton.onclick = () => {this.yesNoFunctions(true, this.dropDownValue + ': paid ' + this.number + ' euros.');};
      this.noButton.onclick = () => {this.yesNoFunctions(false, 'Cancelled transaction.');};

      this.yesNoButtonArea.appendChild(this.yesButton);
      this.yesNoButtonArea.appendChild(this.noButton);
    } else {
      alert("Please select an option for the Dropdown.");
    }
  }

  yesNoFunctions(yesBool, message) {
    this.yesNoButtonArea.innerHTML = '';
    this.displayQuestion.textContent = message;

    if (yesBool) {
      var currentTime = new Date().toLocaleTimeString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour12: false,
        minute: '2-digit',
        second: '2-digit'
      });
      this.logEntry.textContent = this.dropDownValue + ": " + this.number + " euros added. (" + currentTime + ").";
      this.logArea.prepend(this.logEntry);
    }

    this.okButton.setAttribute('type', 'button');
    this.okButton.textContent = 'OK';
    this.okButton.onclick = () => {this.modal.style.display = 'none'};
    this.yesNoButtonArea.appendChild(this.okButton);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault();

    var submitInstance = new firstSubmitFollow();
    submitInstance.structure();
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