// Interactivity for the matches page.
//
// Fetches available tables and existing matches.  Users can host a new
// match by selecting a table and can join any match that does not
// already have a guest.

if (!localStorage.getItem('token')) {
  window.location.href = 'index.html';
}

const tokenMatch = localStorage.getItem('token');

async function loadMatches() {
  const response = await fetch('http://localhost:8000/matches');
  const matches = await response.json();
  const list = document.getElementById('match-list');
  list.innerHTML = '';
  matches.forEach((match) => {
    const li = document.createElement('li');
    li.textContent = `Match ${match.id} on table ${match.table_id} – host: ${match.host_id}, guest: ${match.guest_id ?? 'none'}, status: ${match.status}`;
    // Only allow joining if there is no guest yet.
    if (!match.guest_id) {
      const joinBtn = document.createElement('button');
      joinBtn.textContent = 'Join';
      joinBtn.style.backgroundColor = '#28a745';
      joinBtn.style.color = 'white';
      joinBtn.onclick = () => joinMatch(match.id);
      li.appendChild(joinBtn);
    }
    list.appendChild(li);
  });
}

async function loadTables() {
  const response = await fetch('http://localhost:8000/tables');
  const tables = await response.json();
  const select = document.getElementById('match-table');
  tables.forEach((table) => {
    const opt = document.createElement('option');
    opt.value = table.id;
    opt.textContent = `${table.name} (${table.status})`;
    select.appendChild(opt);
  });
}

async function createMatch() {
  const table_id = parseInt(document.getElementById('match-table').value);
  const response = await fetch('http://localhost:8000/matches', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + tokenMatch
    },
    body: JSON.stringify({ host_id: 0, table_id })
  });
  if (response.ok) {
    await loadMatches();
  } else {
    const data = await response.json();
    alert(data.detail || 'Error creating match');
  }
}

async function joinMatch(match_id) {
  const response = await fetch(`http://localhost:8000/matches/${match_id}/join`, {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + tokenMatch }
  });
  if (response.ok) {
    await loadMatches();
  } else {
    const data = await response.json();
    alert(data.detail || 'Error joining match');
  }
}

document.getElementById('match-form').addEventListener('submit', (event) => {
  event.preventDefault();
  createMatch();
});

loadTables();
loadMatches();