const express = require('express');
const fs = require('fs');
const path = require('path');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const initSqlJs = require('sql.js');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'ecomapa-secret-araiguma';
const DB_PATH = path.join(__dirname, 'ecomapa.db');

let db;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname)));

const saveDatabase = () => {
  if (!db) return;
  const data = db.export();
  fs.writeFileSync(DB_PATH, Buffer.from(data));
};

const normalizeMaterials = (input) => {
  if (Array.isArray(input)) return input.map((item) => String(item).trim().toLowerCase()).filter(Boolean);
  if (typeof input === 'string') return input.split(',').map((item) => item.trim().toLowerCase()).filter(Boolean);
  return [];
};

const normalizeSourceUrl = (input) => {
  if (!input) return null;

  try {
    const url = new URL(String(input).trim());
    return ['http:', 'https:'].includes(url.protocol) ? url.toString() : null;
  } catch (error) {
    return null;
  }
};

const queryAll = (sql, params = []) => {
  const result = db.exec(sql, params);
  if (!result.length) return [];
  const [first] = result;
  return first.values.map((row) =>
    Object.fromEntries(first.columns.map((column, index) => [column, row[index]]))
  );
};

const initializeDatabase = async () => {
  const SQL = await initSqlJs();

  if (fs.existsSync(DB_PATH)) {
    const fileBuffer = fs.readFileSync(DB_PATH);
    db = new SQL.Database(new Uint8Array(fileBuffer));
  } else {
    db = new SQL.Database();
  }

  db.run(`
    CREATE TABLE IF NOT EXISTS usuario_admin (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      email TEXT UNIQUE NOT NULL,
      senha_hash TEXT NOT NULL
    );
  `);

  db.run(`
    CREATE TABLE IF NOT EXISTS ponto_descarte (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      nome TEXT NOT NULL,
      endereco TEXT NOT NULL,
      latitude REAL NOT NULL,
      longitude REAL NOT NULL,
      materiais_aceitos TEXT NOT NULL,
      horario_funcionamento TEXT NOT NULL,
      contato TEXT,
      fonte_url TEXT,
      observacoes TEXT
    );
  `);

  const pointColumns = queryAll('PRAGMA table_info(ponto_descarte)');
  if (!pointColumns.some((column) => column.name === 'fonte_url')) {
    db.run('ALTER TABLE ponto_descarte ADD COLUMN fonte_url TEXT');
  }
  if (!pointColumns.some((column) => column.name === 'observacoes')) {
    db.run('ALTER TABLE ponto_descarte ADD COLUMN observacoes TEXT');
  }

  const adminRows = queryAll('SELECT COUNT(*) as total FROM usuario_admin');
  if (!adminRows.length || Number(adminRows[0].total) === 0) {
    const hash = bcrypt.hashSync('admin123', 10);
    db.run('INSERT INTO usuario_admin (nome, email, senha_hash) VALUES (?, ?, ?)', [
      'Administrador',
      'admin@ecomapa.com',
      hash
    ]);
  }

  db.run(`
    DELETE FROM ponto_descarte
    WHERE nome IN (
      'Ecoponto da Escola',
      'Ponto Verde do Bairro',
      'Coleta Comum do Mercado',
      'Recicla Tech',
      'Ponto Teste Araiguma'
    )
  `);

  const verifiedPoints = [
    {
      nome: 'PEV do Parque Municipal do Mindu',
      endereco: 'Rua Dom João, 247 - Parque Dez de Novembro, Manaus - AM',
      latitude: -3.0783863,
      longitude: -60.0079453,
      materiais: 'plastico,papel,vidro,metais',
      horario: 'Consulte o local antes da visita',
      contato: '(92) 99270-0985',
      fonte: 'https://www.google.com/maps/place/Ponto+de+Entrega+Volunt%C3%A1ria-+PEV+(Parque+do+Mindu)/@-3.0783863,-60.0079453,17z/',
      observacoes: 'Ponto de entrega voluntária listado no Parque do Mindu. Confirme no local quais materiais estão sendo recebidos e o horário atualizado.'
    },
    {
      nome: 'Ecoponto Zona Sul - Educandos',
      endereco: 'Avenida Lourenço da Silva Braga, s/n - Educandos, Manaus - AM',
      latitude: -3.1367217,
      longitude: -60.0096817,
      materiais: 'eletronicos',
      horario: 'Consulte o local antes da visita',
      contato: null,
      fonte: 'https://www.google.com/maps/place/Ecoponto+zona+sul/@-3.1367217,-60.0096817,17z/',
      observacoes: 'A Prefeitura divulgou ações de coleta de eletrônicos neste Ecoponto. Confirme no local a operação e os materiais recebidos antes de levar resíduos.'
    }
  ];

  for (const point of verifiedPoints) {
    const existing = queryAll('SELECT id FROM ponto_descarte WHERE nome = ?', [point.nome]);
    if (!existing.length) {
      db.run(
        `INSERT INTO ponto_descarte
          (nome, endereco, latitude, longitude, materiais_aceitos, horario_funcionamento, contato, fonte_url, observacoes)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
        [
          point.nome,
          point.endereco,
          point.latitude,
          point.longitude,
          point.materiais,
          point.horario,
          point.contato,
          point.fonte,
          point.observacoes
        ]
      );
    }
  }

  saveDatabase();
};

const authenticateToken = (req, res, next) => {
  const authHeader = req.headers.authorization;
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) {
    return res.status(401).json({ message: 'Token ausente.' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    return next();
  } catch (error) {
    return res.status(403).json({ message: 'Token inválido ou expirado.' });
  }
};

app.get('/api/health', (_, res) => {
  res.json({ ok: true, app: 'EcoMapa', group: 'Araiguma', timestamp: new Date().toISOString() });
});

app.post('/api/login', (req, res) => {
  const { email, senha } = req.body;

  if (!email || !senha) {
    return res.status(400).json({ message: 'Email e senha são obrigatórios.' });
  }

  const user = queryAll('SELECT * FROM usuario_admin WHERE email = ?', [String(email).trim().toLowerCase()])[0];

  if (!user) {
    return res.status(401).json({ message: 'Credenciais inválidas.' });
  }

  const senhaValida = bcrypt.compareSync(String(senha), user.senha_hash);
  if (!senhaValida) {
    return res.status(401).json({ message: 'Credenciais inválidas.' });
  }

  const token = jwt.sign({ id: user.id, email: user.email, nome: user.nome }, JWT_SECRET, { expiresIn: '8h' });

  return res.json({
    token,
    user: { id: user.id, nome: user.nome, email: user.email }
  });
});

app.get('/api/pontos', (req, res) => {
  try {
    const rows = queryAll('SELECT * FROM ponto_descarte ORDER BY id ASC');
    const normalizedRows = rows.map((row) => ({
      ...row,
      materiais_aceitos: String(row.materiais_aceitos || '').split(',').map((item) => item.trim()).filter(Boolean)
    }));
    return res.json(normalizedRows);
  } catch (error) {
    return res.status(500).json({ message: 'Erro ao buscar pontos.', error: error.message });
  }
});

app.get('/api/pontos/:id', authenticateToken, (req, res) => {
  const { id } = req.params;
  const rows = queryAll('SELECT * FROM ponto_descarte WHERE id = ?', [Number(id)]);

  if (!rows.length) {
    return res.status(404).json({ message: 'Ponto não encontrado.' });
  }

  const point = rows[0];
  return res.json({
    ...point,
    materiais_aceitos: String(point.materiais_aceitos || '').split(',').map((item) => item.trim()).filter(Boolean)
  });
});

app.post('/api/pontos', authenticateToken, (req, res) => {
  const { nome, endereco, latitude, longitude, materiais_aceitos, horario_funcionamento, contato, fonte_url, observacoes } = req.body;

  if (!nome || !endereco || latitude === undefined || longitude === undefined || !horario_funcionamento) {
    return res.status(400).json({ message: 'Nome, endereço, latitude, longitude e horário de funcionamento são obrigatórios.' });
  }

  if (!Number.isFinite(Number(latitude)) || Number(latitude) < -90 || Number(latitude) > 90 ||
      !Number.isFinite(Number(longitude)) || Number(longitude) < -180 || Number(longitude) > 180) {
    return res.status(400).json({ message: 'Latitude ou longitude inválida.' });
  }

  const materiais = normalizeMaterials(materiais_aceitos);
  const sourceUrl = normalizeSourceUrl(fonte_url);
  if (fonte_url && !sourceUrl) {
    return res.status(400).json({ message: 'A fonte deve ser uma URL HTTP ou HTTPS válida.' });
  }

  try {
    db.run(
      `INSERT INTO ponto_descarte
        (nome, endereco, latitude, longitude, materiais_aceitos, horario_funcionamento, contato, fonte_url, observacoes)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        String(nome).trim(),
        String(endereco).trim(),
        Number(latitude),
        Number(longitude),
        materiais.join(','),
        String(horario_funcionamento).trim(),
        contato ? String(contato).trim() : null,
        sourceUrl,
        observacoes ? String(observacoes).trim() : null
      ]
    );

    saveDatabase();

    const createdRows = queryAll('SELECT * FROM ponto_descarte ORDER BY id DESC LIMIT 1');
    const created = createdRows[0];

    return res.status(201).json({
      ...created,
      materiais_aceitos: String(created.materiais_aceitos || '').split(',').map((item) => item.trim()).filter(Boolean)
    });
  } catch (error) {
    return res.status(400).json({ message: 'Erro ao criar ponto.', error: error.message });
  }
});

app.put('/api/pontos/:id', authenticateToken, (req, res) => {
  const { id } = req.params;
  const { nome, endereco, latitude, longitude, materiais_aceitos, horario_funcionamento, contato, fonte_url, observacoes } = req.body;

  if (!nome || !endereco || latitude === undefined || longitude === undefined || !horario_funcionamento) {
    return res.status(400).json({ message: 'Nome, endereço, latitude, longitude e horário de funcionamento são obrigatórios.' });
  }

  if (!Number.isFinite(Number(latitude)) || Number(latitude) < -90 || Number(latitude) > 90 ||
      !Number.isFinite(Number(longitude)) || Number(longitude) < -180 || Number(longitude) > 180) {
    return res.status(400).json({ message: 'Latitude ou longitude inválida.' });
  }

  const materiais = normalizeMaterials(materiais_aceitos);
  const sourceUrl = normalizeSourceUrl(fonte_url);
  if (fonte_url && !sourceUrl) {
    return res.status(400).json({ message: 'A fonte deve ser uma URL HTTP ou HTTPS válida.' });
  }

  try {
    db.run(
      `UPDATE ponto_descarte
       SET nome = ?, endereco = ?, latitude = ?, longitude = ?, materiais_aceitos = ?, horario_funcionamento = ?,
           contato = ?, fonte_url = ?, observacoes = ?
       WHERE id = ?`,
      [
        String(nome).trim(),
        String(endereco).trim(),
        Number(latitude),
        Number(longitude),
        materiais.join(','),
        String(horario_funcionamento).trim(),
        contato ? String(contato).trim() : null,
        sourceUrl,
        observacoes ? String(observacoes).trim() : null,
        Number(id)
      ]
    );

    if (db.getRowsModified() === 0) {
      return res.status(404).json({ message: 'Ponto não encontrado.' });
    }

    saveDatabase();

    return res.json({
      id: Number(id),
      nome,
      endereco,
      latitude: Number(latitude),
      longitude: Number(longitude),
      materiais_aceitos: materiais,
      horario_funcionamento,
      contato: contato || null,
      fonte_url: sourceUrl,
      observacoes: observacoes || null,
      fonte_url: sourceUrl,
      observacoes: observacoes || null
    });
  } catch (error) {
    return res.status(400).json({ message: 'Erro ao atualizar ponto.', error: error.message });
  }
});

app.delete('/api/pontos/:id', authenticateToken, (req, res) => {
  const { id } = req.params;

  try {
    db.run('DELETE FROM ponto_descarte WHERE id = ?', [Number(id)]);
    if (db.getRowsModified() === 0) {
      return res.status(404).json({ message: 'Ponto não encontrado.' });
    }
    saveDatabase();
    return res.json({ message: 'Ponto removido com sucesso.' });
  } catch (error) {
    return res.status(400).json({ message: 'Erro ao remover ponto.', error: error.message });
  }
});

app.get('*', (_, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

initializeDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`EcoMapa server running on http://localhost:${PORT}`);
  });
}).catch((error) => {
  console.error('Failed to initialize EcoMapa database:', error);
  process.exit(1);
});
