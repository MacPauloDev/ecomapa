const materialMeta = {
  todos: { label: 'Todos', color: '#1d8b4d' },
  pilhas: { label: 'Pilhas', color: '#2fbe72' },
  oleo: { label: 'Óleo', color: '#f59e0b' },
  eletronicos: { label: 'Eletrônicos', color: '#3b82f6' },
  vidro: { label: 'Vidro', color: '#9f7aea' },
  plastico: { label: 'Plástico', color: '#ef4444' },
  papel: { label: 'Papel', color: '#eab308' },
  metais: { label: 'Metais', color: '#64748b' },
  lampadas: { label: 'Lâmpadas', color: '#a855f7' },
  toners: { label: 'Toners', color: '#ec4899' },
  eletrodomesticos_grandes: { label: 'Eletrodomésticos Grandes', color: '#f97316' }
};

const filtersContainer = document.getElementById('materialFilters');
const pointList = document.getElementById('pointList');
const locationButton = document.getElementById('useLocation');

let points = [];
let pointsLoaded = false;
let selectedMaterial = 'todos';
let map;
let markersLayer;
let userCoordinates = null;
let showAllPoints = false;

const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;'
})[character]);

const toMapPoint = (point) => ({
  ...point,
  id: Number(point.id),
  lat: Number(point.latitude),
  lng: Number(point.longitude),
  materials: Array.isArray(point.materiais_aceitos) ? point.materiais_aceitos : [],
  hours: point.horario_funcionamento || 'Horário não informado',
  contact: point.contato || 'Contato não informado',
  source: point.fonte_url || '',
  notes: point.observacoes || ''
});

function createFilterButtons() {
  Object.entries(materialMeta).forEach(([key, meta]) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `material-filter ${selectedMaterial === key ? 'active' : ''}`;
    button.dataset.material = key;

    const label = document.createElement('span');
    label.className = 'label';
    label.textContent = meta.label;

    const dot = document.createElement('span');
    dot.className = 'dot';
    dot.style.backgroundColor = meta.color;

    button.append(label, dot);
    button.addEventListener('click', () => {
      selectedMaterial = key;
      updateFilters();
      if (pointsLoaded) renderVisiblePoints();
    });

    filtersContainer.appendChild(button);
  });
}

function updateFilters() {
  filtersContainer.querySelectorAll('.material-filter').forEach((button) => {
    button.classList.toggle('active', button.dataset.material === selectedMaterial);
  });
}

function getDistanceKm(from, to) {
  const radians = (degrees) => (degrees * Math.PI) / 180;
  const deltaLat = radians(to.lat - from.lat);
  const deltaLng = radians(to.lng - from.lng);
  const a = Math.sin(deltaLat / 2) ** 2 +
    Math.cos(radians(from.lat)) * Math.cos(radians(to.lat)) * Math.sin(deltaLng / 2) ** 2;
  return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function getFilteredPoints() {
  const filtered = selectedMaterial === 'todos'
    ? [...points]
    : points.filter((point) => point.materials.includes(selectedMaterial));

  if (userCoordinates) {
    filtered.sort((a, b) => getDistanceKm(userCoordinates, a) - getDistanceKm(userCoordinates, b));
  }

  return filtered;
}

function getVisiblePoints() {
  const filtered = getFilteredPoints();
  if (showAllPoints || !userCoordinates) {
    return filtered;
  }
  return filtered.slice(0, 5);
}

function renderVisiblePoints() {
  const visible = getVisiblePoints();
  renderPointList(visible);
  markersLayer.clearLayers();

  visible.forEach((point) => {
    const marker = L.marker([point.lat, point.lng]).addTo(markersLayer);
    marker.options.pointId = point.id;
    const safeSource = getSafeSourceUrl(point.source);
    marker.bindPopup(`
      <strong>${escapeHtml(point.nome)}</strong><br>
      ${escapeHtml(point.endereco)}<br>
      <small>${escapeHtml(point.hours)}</small><br>
      <strong>Materiais:</strong> ${escapeHtml(point.materials.map((item) => materialMeta[item]?.label || item).join(', ') || 'Não informado')}<br>
      <strong>Contato:</strong> ${escapeHtml(point.contact)}<br>
      ${point.notes ? `<small>${escapeHtml(point.notes)}</small><br>` : ''}
      ${safeSource ? `<a href="${escapeHtml(safeSource)}" target="_blank" rel="noopener noreferrer">Fonte do local</a><br>` : ''}
      <a href="https://www.google.com/maps/dir/?api=1&destination=${point.lat},${point.lng}" target="_blank" rel="noopener noreferrer">Abrir rota</a>
    `);
  });

  if (userCoordinates) {
    L.circleMarker([userCoordinates.lat, userCoordinates.lng], {
      radius: 8,
      color: '#fff',
      weight: 2,
      fillColor: '#2563eb',
      fillOpacity: 1
    }).bindPopup('Sua localização').addTo(markersLayer);
  }

  if (visible.length) {
    const bounds = visible.map((point) => [point.lat, point.lng]);
    if (userCoordinates) bounds.push([userCoordinates.lat, userCoordinates.lng]);
    map.fitBounds(bounds, { padding: [30, 30], maxZoom: 14 });
  } else if (userCoordinates) {
    map.flyTo([userCoordinates.lat, userCoordinates.lng], 13);
  }
}

function createPointCard(point) {
  const card = document.createElement('article');
  card.className = 'point-card';

  const title = document.createElement('h4');
  title.textContent = point.nome;

  const address = document.createElement('small');
  address.textContent = point.endereco;

  const tags = document.createElement('span');
  tags.className = 'tag';
  tags.textContent = point.materials.map((key) => materialMeta[key]?.label || key).join(', ') || 'Material não informado';

  card.append(title, address, tags);

  if (userCoordinates) {
    const distance = document.createElement('small');
    distance.className = 'distance-label';
    distance.textContent = `${getDistanceKm(userCoordinates, point).toFixed(1)} km em linha reta`;
    card.appendChild(distance);
  }

  if (point.notes) {
    const note = document.createElement('small');
    note.className = 'point-note';
    note.textContent = point.notes;
    card.appendChild(note);
  }

  const directions = document.createElement('a');
  directions.className = 'point-directions';
  directions.href = `https://www.google.com/maps/dir/?api=1&destination=${point.lat},${point.lng}`;
  directions.target = '_blank';
  directions.rel = 'noopener noreferrer';
  directions.textContent = 'Abrir rota';
  directions.addEventListener('click', (event) => event.stopPropagation());
  card.appendChild(directions);

  card.tabIndex = 0;
  card.setAttribute('role', 'button');
  card.addEventListener('click', () => focusPoint(point));
  card.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      focusPoint(point);
    }
  });

  return card;
}

function renderPointList(filteredPoints) {
  pointList.replaceChildren();

  if (!filteredPoints.length) {
    const emptyState = document.createElement('p');
    emptyState.textContent = points.length
      ? 'Nenhum ponto encontrado para esse filtro.'
      : 'Clique em "Usar minha localização" para ver os pontos de descarte mais próximos.';
    pointList.appendChild(emptyState);
    return;
  }

  filteredPoints.forEach((point) => pointList.appendChild(createPointCard(point)));
}

function buildMap() {
  map = L.map('map', {
    zoomControl: true,
    preferCanvas: true
  }).setView([-3.10, -60.02], 11);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  markersLayer = L.layerGroup().addTo(map);
}

function getSafeSourceUrl(source) {
  try {
    const url = new URL(source);
    return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
  } catch (error) {
    return '';
  }
}

function focusPoint(point) {
  map.flyTo([point.lat, point.lng], 16, { duration: 1.2 });
  const marker = markersLayer.getLayers().find((layer) => layer.options.pointId === point.id);
  if (marker) marker.openPopup();
}

async function loadPoints() {
  try {
    const response = await fetch('pontos.json');
    if (!response.ok) throw new Error(`Falha ao carregar os pontos (HTTP ${response.status}).`);

    const result = await response.json();
    points = result.map(toMapPoint).filter((point) =>
      Number.isFinite(point.lat) && Number.isFinite(point.lng)
    );
    pointsLoaded = true;
    return points;
  } catch (error) {
    console.error('Não foi possível carregar os pontos do EcoMapa:', error);
    const message = document.createElement('p');
    message.textContent = 'Não foi possível carregar pontos de descarte.';
    pointList.replaceChildren(message);
    return null;
  }
}

function useUserLocation() {
  if (!navigator.geolocation) {
    alert('Geolocalização não suportada neste navegador.');
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      userCoordinates = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };

      if (!pointsLoaded) {
        const loadedPoints = await loadPoints();
        if (!loadedPoints) return;
      }

      renderVisiblePoints();
    },
    () => {
      alert('Não foi possível acessar sua localização. Permita o uso para calcular proximidade.');
    }
  );
}

if (locationButton) locationButton.addEventListener('click', useUserLocation);

// Toggle button for showing all points
const toggleButton = document.createElement('button');
toggleButton.id = 'toggleAllPoints';
toggleButton.className = 'button button-outline full-width';
toggleButton.type = 'button';
toggleButton.textContent = 'Mostrar todos os pontos';
toggleButton.style.marginTop = '0.5rem';
if (locationButton?.parentNode) locationButton.parentNode.insertBefore(toggleButton, locationButton.nextSibling);

toggleButton.addEventListener('click', async () => {
  if (!userCoordinates) {
    alert('Use sua localização primeiro para ordenar os pontos por proximidade.');
    return;
  }

  if (!pointsLoaded) {
    const loadedPoints = await loadPoints();
    if (!loadedPoints) return;
  }

  showAllPoints = !showAllPoints;
  toggleButton.textContent = showAllPoints ? 'Mostrar apenas 5 mais próximos' : 'Mostrar todos os pontos';
  renderVisiblePoints();
});

if (filtersContainer && pointList) createFilterButtons();
if (document.getElementById('map') && typeof L !== 'undefined') buildMap();

if (pointList && map) loadPoints().then((loadedPoints) => {
  if (loadedPoints) renderVisiblePoints();
});
