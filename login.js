const loginForm = document.getElementById('loginForm');

if (loginForm) {
  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value;
    const senha = document.getElementById('loginPassword').value;

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.message || 'Erro ao fazer login.');
        return;
      }

      localStorage.setItem('ecomapaToken', data.token);
      window.location.href = 'admin.html';
    } catch (error) {
      alert('Erro ao conectar com o servidor.');
    }
  });
}
