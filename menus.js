// Interactivity for the menus page.
//
// Fetches the list of menu items from the backend and renders them on
// the page.  Users can create new items via a form, update existing
// items via prompt dialogs, or delete items.  When an operation
// completes successfully the list is refreshed.

// Redirect if unauthenticated.
if (!localStorage.getItem('token')) {
  window.location.href = 'index.html';
}

async function loadMenus() {
  const response = await fetch('http://localhost:8000/menus');
  const menus = await response.json();
  const list = document.getElementById('menu-list');
  list.innerHTML = '';
  menus.forEach((menu) => {
    const li = document.createElement('li');
    li.textContent = `${menu.name} – $${menu.price.toFixed(2)} ${menu.is_available ? '' : '(Unavailable)'}`;
    // Button to update the menu item.
    const updateBtn = document.createElement('button');
    updateBtn.textContent = 'Update';
    updateBtn.style.backgroundColor = '#17a2b8';
    updateBtn.style.color = 'white';
    updateBtn.onclick = () => editMenu(menu);
    // Button to delete the menu item.
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = () => deleteMenu(menu.id);
    li.appendChild(updateBtn);
    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

async function createMenu() {
  const name = document.getElementById('menu-name').value;
  const description = document.getElementById('menu-description').value;
  const price = parseFloat(document.getElementById('menu-price').value);
  const is_available = document.getElementById('menu-available').checked;
  const response = await fetch('http://localhost:8000/menus', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description, price, is_available })
  });
  if (response.ok) {
    await loadMenus();
    document.getElementById('menu-form').reset();
  } else {
    const data = await response.json();
    alert(data.detail || 'Error creating menu');
  }
}

async function deleteMenu(id) {
  if (!confirm('Delete this menu item?')) return;
  const response = await fetch(`http://localhost:8000/menus/${id}`, {
    method: 'DELETE'
  });
  if (response.status === 204) {
    await loadMenus();
  } else {
    const data = await response.json();
    alert(data.detail || 'Error deleting menu');
  }
}

function editMenu(menu) {
  const name = prompt('Name', menu.name);
  if (name === null) return;
  const description = prompt('Description', menu.description || '');
  if (description === null) return;
  const priceStr = prompt('Price', menu.price);
  if (priceStr === null) return;
  const is_available = confirm('Is available? OK = yes, Cancel = no');
  const price = parseFloat(priceStr);
  fetch(`http://localhost:8000/menus/${menu.id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, description, price, is_available })
  }).then((response) => {
    if (response.ok) {
      loadMenus();
    } else {
      response.json().then((data) => {
        alert(data.detail || 'Error updating menu');
      });
    }
  });
}

// Bind the creation form handler.
document.getElementById('menu-form').addEventListener('submit', (event) => {
  event.preventDefault();
  createMenu();
});

// Load menus on initial page load.
loadMenus();