// Simple script for the dashboard page.
//
// Ensures that an authenticated JWT is present and wires up the logout
// button to clear the token and redirect back to the login page.

// Redirect to the login page if no token is present.
if (!localStorage.getItem('token')) {
  window.location.href = 'index.html';
}

// Bind the logout button to clear the JWT and redirect to the login page.
document.getElementById('logout').addEventListener('click', () => {
  localStorage.removeItem('token');
  window.location.href = 'index.html';
});