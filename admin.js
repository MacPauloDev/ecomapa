const token = localStorage.getItem('ecomapaToken');
const form = document.getElementById('pointForm');
const adminPointsList = document.getElementById('adminPointsList');
const logoutButton = document.getElementById('logoutButton');
const cancelEditButton = document.getElementById('cancelEdit');

const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;'
})[character]);

const safeSourceUrl = (source) => {
  try {
    const url = new URL(source);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
  } catch (error) {
    return '';
  }
};

if (!token) {
  window.location.href = 'index.html';
}

const readForm = () => ({
  id: document.getElementById('pointId').value,
  nome: document.getElementById('nome').value,
  endereco: document.getElementById('endereco').value,
  latitude: document.getElementById('latitude').value,
  longitude: document.getElementById('longitude').value,
  materiais_aceitos: document.getElementById('materiaisAceitos').value,
  horario_funcionamento: document.getElementById('horario').value,
  contato: document.getElementById('contato').value,
  fonte_url: document.getElementById('fonteUrl').value,
  observacoes: document.getElementById('observacoes').value
});

const loadPoints = async () => {
  const response = await fetch('/api/pontos');
  const points = await response.json();

  adminPointsList.innerHTML = '';

  if (!points.length) {
    adminPointsList.innerHTML = '<p>Nenhum ponto cadastrado.</p>';
    return;
  }

  points.forEach((point) => {
    const item = document.createElement('article');
    item.className = 'admin-point-item';
    const sourceUrl = safeSourceUrl(point.fonte_url);
    item.innerHTML = `
      <div>
        <h3>${escapeHtml(point.nome)}</h3>
        <p>${escapeHtml(point.endereco)}</p>
        <small>${escapeHtml(point.materiais_aceitos.join(', ') || 'Sem material')}</small>
        ${point.observacoes ? `<p>${escapeHtml(point.observacoes)}</p>` : ''}
        ${sourceUrl ? `<a href="${escapeHtml(sourceUrl)}" target="_blank" rel="noopener noreferrer">Abrir fonte</a>` : ''}
      </div>
      <div class="admin-actions">
        <button class="button button-secondary" data-action="edit" data-id="${Number(point.id)}" type="button">Editar</button>
        <button class="button button-primary" data-action="delete" data-id="${Number(point.id)}" type="button">Excluir</button>
      </div>
    `;
    adminPointsList.appendChild(item);
  });
};

const fillForm = (point) => {
  document.getElementById('pointId').value = point.id;
  document.getElementById('nome').value = point.nome;
  document.getElementById('endereco').value = point.endereco;
  document.getElementById('latitude').value = point.latitude;
  document.getElementById('longitude').value = point.longitude;
  document.getElementById('materiaisAceitos').value = point.materiais_aceitos.join(', ');
  document.getElementById('horario').value = point.horario_funcionamento;
  document.getElementById('contato').value = point.contato || '';
  document.getElementById('fonteUrl').value = point.fonte_url || '';
  document.getElementById('observacoes').value = point.observacoes || '';
};

const resetForm = () => {
  form.reset();
  document.getElementById('pointId').value = '';
};

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const payload = readForm();
  const method = payload.id ? 'PUT' : 'POST';
  const url = payload.id ? `/api/pontos/${payload.id}` : '/api/pontos';

  const response = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  const result = await response.json();

  if (!response.ok) {
    alert(result.message || 'Erro ao salvar ponto.');
    return;
  }

  resetForm();
  alert(payload.id ? 'Ponto atualizado com sucesso.' : 'Ponto cadastrado com sucesso.');
  loadPoints();
});

adminPointsList.addEventListener('click', async (event) => {
  const button = event.target.closest('button');
  if (!button) return;

  const { action, id } = button.dataset;
  if (!id) return;

  const response = await fetch(`/api/pontos/${id}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const point = await response.json();

  if (!response.ok) {
    alert(point.message || 'Erro ao carregar o ponto.');
    return;
  }

  if (action === 'edit') {
    fillForm(point);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  if (action === 'delete') {
    const confirmed = window.confirm('Deseja excluir este ponto?');
    if (!confirmed) return;

    const deleteResponse = await fetch(`/api/pontos/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });

    const deleteResult = await deleteResponse.json();

    if (!deleteResponse.ok) {
      alert(deleteResult.message || 'Erro ao excluir ponto.');
      return;
    }

    alert('Ponto excluído com sucesso.');
    loadPoints();
  }
});

logoutButton.addEventListener('click', () => {
  localStorage.removeItem('ecomapaToken');
  window.location.href = 'index.html';
});

cancelEditButton.addEventListener('click', resetForm);

loadPoints();
