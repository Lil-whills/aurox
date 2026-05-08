// Hamburger Menu Functionality

document.addEventListener('DOMContentLoaded', function() {
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  const menuOverlay = document.getElementById('menuOverlay');
  const menuLinks = mobileMenu.querySelectorAll('a');

  // Toggle menu
  hamburgerBtn.addEventListener('click', function() {
    toggleMenu();
  });

  // Close menu when clicking overlay
  menuOverlay.addEventListener('click', function() {
    closeMenu();
  });

  // Close menu when clicking any link
  menuLinks.forEach(link => {
    link.addEventListener('click', function() {
      closeMenu();
    });
  });

  // Close menu on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      closeMenu();
    }
  });

  function toggleMenu() {
    const isOpen = mobileMenu.classList.contains('mobile-menu-visible');
    if (isOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  function openMenu() {
    mobileMenu.classList.add('mobile-menu-visible');
    hamburgerBtn.classList.add('active');
    menuOverlay.classList.add('visible');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    mobileMenu.classList.remove('mobile-menu-visible');
    hamburgerBtn.classList.remove('active');
    menuOverlay.classList.remove('visible');
    document.body.style.overflow = '';
  }

  // Reinitialize Lucide icons after page load
  if (window.lucide) {
    lucide.createIcons();
  }
});
