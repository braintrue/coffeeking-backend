// Interactivity for the orders page.
//
// Loads available tables and menu items and allows the user to construct
// an order by selecting a table and quantities for each menu item.  The
// created order is submitted to the backend with the JWT attached.

if (!localStorage.getItem('token')) {
  window.location.href = 'index.html';
}

let menus = [];
let tables = [];
const token = localStorage.getItem('token');

async function loadData() {
  // Fetch menus
  const menuRes = await fetch('http://localhost:8000/menus');
  menus = await menuRes.json();
  // Fetch tables
  const tableRes = await fetch('http://localhost:8000/tables');
  tables = await tableRes.json();
  const tableSelect = document.getElementById('order-table');
  tables.forEach((table) => {
    const opt = document.createElement('option');
    opt.value = table.id;
    opt.textContent = `${table.name} (${table.status})`;
    tableSelect.appendChild(opt);
  });
  const itemsDiv = document.getElementById('order-items');
  menus.forEach((menu) => {
    const div = document.createElement('div');
    const label = document.createElement('label');
    label.textContent = `${menu.name} ($${menu.price.toFixed(2)})`;
    const qty = document.createElement('input');
    qty.type = 'number';
    qty.min = 0;
    qty.value = 0;
    qty.dataset.menuId = menu.id;
    qty.style.marginLeft = '10px';
    div.appendChild(label);
    div.appendChild(qty);
    itemsDiv.appendChild(div);
  });
}

async function createOrder() {
  const table_id = parseInt(document.getElementById('order-table').value);
  const items = [];
  document.querySelectorAll('#order-items input').forEach((input) => {
    const qty = parseInt(input.value);
    if (qty > 0) {
      items.push({ menu_id: parseInt(input.dataset.menuId), quantity: qty });
    }
  });
  if (items.length === 0) {
    alert('Please select at least one item.');
    return;
  }
  const response = await fetch('http://localhost:8000/orders', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    },
    body: JSON.stringify({ table_id, items })
  });
  if (response.ok) {
    const order = await response.json();
    alert('Order created: ID ' + order.id + ', total $' + order.total_amount.toFixed(2));
    // Reset form
    document.getElementById('order-form').reset();
    document.querySelectorAll('#order-items input').forEach((input) => {
      input.value = 0;
    });
  } else {
    const data = await response.json();
    alert(data.detail || 'Error creating order');
  }
}

document.getElementById('order-form').addEventListener('submit', (event) => {
  event.preventDefault();
  createOrder();
});

loadData();