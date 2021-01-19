const menuBtn = document.querySelector('.menu-btn');
const hamburger = document.querySelector('.menu-btn__burger');
const menuNav = document.querySelector('.menu-nav');
const navNames = document.querySelectorAll('.nav_name');

let showMenu = false;

menuBtn.addEventListener('click', toggleMenu);

function toggleMenu() {
  if(!showMenu) {
    hamburger.classList.add('open');
    menuNav.classList.add('open');
    navNames.forEach(item => item.classList.add('open'));

    showMenu = true;
  } else {
    hamburger.classList.remove('open');
    menuNav.classList.remove('open');
    navNames.forEach(item => item.classList.remove('open'));

    showMenu = false;
  }
}