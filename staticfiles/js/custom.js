document.addEventListener('DOMContentLoaded', () => {
    const html = document.documentElement;
    const toggle = document.getElementById('themeToggle');
    let theme = html.getAttribute('data-theme') || 'dark';
  
    // Set icon
    function setIcon() {
      toggle.innerHTML = theme === 'dark'
        ? '<i class="bi bi-sun-fill"></i>'
        : '<i class="bi bi-moon-fill"></i>';
    }
    setIcon();
  
    toggle.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', theme);
      // Persist in cookie for 1 year
      document.cookie = `theme=${theme};path=/;max-age=${60*60*24*365}`;
      setIcon();
    });
  });
  