// Interactivity for the tables page.
//
// Handles listing existing tables, creating new tables, toggling the
// availability status and deleting tables.  Uses simple fetch calls
// against the backend API.

// Require authentication.
if (!localStorage.getItem('token')) {
  window.location.href = 'index.html';
}

async function loadTables() {
  const response = await fetch('http://localhost:8000/tables');
  const tables = await response.json();
  const list = document.getElementById('table-list');
  list.innerHTML = '';
  tables.forEach((table) => {
    const li = document.createElement('li');
    li.textContent = `${table.name} – capacity: ${table.capacity}, status: ${table.status}`;
    // Button to toggle the status between available/occupied.
    const toggleBtn = document.createElement('button');
    toggleBtn.textContent = 'Toggle Status';
    toggleBtn.style.backgroundColor = '#17a2b8';
    toggleBtn.style.color = 'white';
    toggleBtn.onclick = () => toggleStatus(table);
    // Button to delete the table.
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.onclick = () => deleteTable(table.id);
    li.appendChild(toggleBtn);
    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

async function createTable() {
  const name = document.getElementById('table-name').value;
  const capacity = parseInt(document.getElementById('table-capacity').value);
  const status = document.getElementById('table-status').value;
  const response = await fetch('http://localhost:8000/tables', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, capacity, status })
  });
  if (response.ok) {
    await loadTables();
    document.getElementById('table-form').reset();
    document.getElementById('table-capacity').value = 2;
  } else {
    const data = await response.json();
    alert(data.detail || 'Error creating table');
  }
}

async function deleteTable(id) {
  if (!confirm('Delete this table?')) return;
  const response = await fetch(`http://localhost:8000/tables/${id}`, {
    method: 'DELETE'
  });
  if (response.status === 204) {
    await loadTables();
  } else {
    const data = await response.json();
    alert(data.detail || 'Error deleting table');
  }
}

async function toggleStatus(table) {
  const newStatus = table.status === 'available' ? 'occupied' : 'available';
  const response = await fetch(`http://localhost:8000/tables/${table.id}?status=${newStatus}`, {
    method: 'PATCH'
  });
  if (response.ok) {
    await loadTables();
  } else {
    const data = await response.json();
    alert(data.detail || 'Error updating table');
  }
}

document.getElementById('table-form').addEventListener('submit', (event) => {
  event.preventDefault();
  createTable();
});

loadTables();