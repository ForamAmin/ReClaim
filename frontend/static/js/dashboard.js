function openTab(evt, tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.classList.add('active');
  }

  function scrollToFeed() {
    document.getElementById('feed-section').scrollIntoView({ behavior: 'smooth' });
  }
  

  
  const toggle  = document.getElementById('pw-toggle');
  const pwInput = document.getElementById('password');
  const pwIcon  = document.getElementById('pw-icon');

  toggle.addEventListener('click', () => {
    const hidden = pwInput.type === 'password';
    pwInput.type  = hidden ? 'text' : 'password';
    pwIcon.className = hidden ? 'fas fa-eye-slash' : 'fas fa-eye';
  });
  
  