// Handle registration and login for the CoffeeKing frontend.

const registerForm = document.getElementById('register-form');
const loginForm = document.getElementById('login-form');

// Register a new user via the API.
registerForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = document.getElementById('reg-username').value;
  const password = document.getElementById('reg-password').value;
  const regMsg = document.getElementById('register-message');
  regMsg.textContent = '';
  try {
    const response = await fetch('http://localhost:8000/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (response.ok) {
      regMsg.textContent = 'Registration successful. Please log in.';
      registerForm.reset();
    } else {
      const data = await response.json();
      regMsg.textContent = 'Error: ' + (data.detail || 'Registration failed');
    }
  } catch (err) {
    regMsg.textContent = 'Error: ' + err.message;
  }
});

// Authenticate a user and store the returned JWT in localStorage.
loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const email = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;
  const loginMsg = document.getElementById('login-message');
  loginMsg.textContent = '';
  try {
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username: email, password })
    });
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      // Redirect to the dashboard after a successful login.
      window.location.href = 'dashboard.html';
    } else {
      const data = await response.json();
      loginMsg.textContent = 'Error: ' + (data.detail || 'Login failed');
    }
  } catch (err) {
    loginMsg.textContent = 'Error: ' + err.message;
  }
});