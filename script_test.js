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
    this.logEntry = document.createElement('p');
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
      let currentTime = new Date().toLocaleTimeString('en-GB', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
      });
      this.logEntry.textContent = this.dropDownValue + ": " + this.number + " euros added. (" + currentTime + ").";
      this.postingLogInfo()
      this.logArea.prepend(this.logEntry);
    }

    this.okButton.setAttribute('type', 'button');
    this.okButton.textContent = 'OK';
    this.okButton.onclick = () => {this.modal.style.display = 'none'};
    this.yesNoButtonArea.appendChild(this.okButton);
  }

  postingLogInfo() {
    const data = { logString: this.logEntry.textContent };
    fetch('http://localhost:5000/save-log', {
      method: 'POST', 
      headers: {
      'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }
}

document.addEventListener('DOMContentLoaded', function() {
  fetchingLogInfo()
  document.getElementById('inputForm').addEventListener('submit', function(event) {
    event.preventDefault();

    let submitInstance = new firstSubmitFollow();
    submitInstance.structure();
  });
});



// To fetch the past transactions data from the csv
function fetchingLogInfo() {
  fetch('http://localhost:5000/get-logs')
  .then(response => response.json())
  .then(data => {
    const logsContainer = document.getElementById('logNumberInput');
    data.forEach(log => {
      const logElement = document.createElement('p');
      logElement.textContent = log['0'];
      logsContainer.prepend(logElement);
    });
  })
  .catch(error => console.error('Error:', error));
}

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
    let dropdowns = document.getElementsByClassName("dropdown-content");
    for (let i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}