// check for saved 'darkMode' in localStorage
let darkMode = localStorage.getItem('darkMode'); 

const darkModeToggle = document.querySelector('#dark-mode-toggle');
const themeStyleSheet = document.getElementById('theme');

const enableDarkMode = () => {
  //themeStyleSheet.href = '{% static \'css/dark-theme.css\' %}';
  //Add the class to the body
  document.body.classList.add('darkmode');
  console.log("dark mode on");

  //Update darkMode in localStorage
  localStorage.setItem('darkMode', 'enabled');

   //change the name of the label
  //darkModeToggle.textContent = "Dark Mode: ON";
};

const disableDarkMode = () => {
  //themeStyleSheet.href = '{% static \'css/light-theme.css\' %}';
  //Remove the class from the body
  document.body.classList.remove('darkmode');
  console.log("dark mode off");

  //Update darkMode in localStorage
  localStorage.setItem('darkMode', null);

   //change the name of the label
  //darkModeToggle.textContent = "Dark Mode: OFF";
};
 
// If the user already visited and enabled darkMode
// start things off with it on
if (darkMode === 'enabled') {
  enableDarkMode();
}

// When someone clicks the button
darkModeToggle.addEventListener('click', () => {
  // get their darkMode setting
  darkMode = localStorage.getItem('darkMode'); 
  
  // if it not current enabled, enable it
  if (darkMode !== 'enabled') {
    enableDarkMode();
  // if it has been enabled, turn it off  
  } else {  
    disableDarkMode(); 
  }
});
