// ==================== EFEITO DE FADE-IN ====================
document.addEventListener("DOMContentLoaded", () => {
  const fadeElements = document.querySelectorAll(".fade-in");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target); // anima uma vez só
        }
      });
    },
    {
      threshold: 0.2, // começa o efeito quando 20% do elemento aparece
    }
  );

  fadeElements.forEach((el) => observer.observe(el));
});

// ==================== BOTÃO "VOLTAR AO TOPO" ====================
const btnTopo = document.getElementById("btnTopo");

window.addEventListener("scroll", () => {
  if (window.scrollY > 300) {
    btnTopo.style.display = "block";
  } else {
    btnTopo.style.display = "none";
  }
});

btnTopo.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

// ==================== MENU ATIVO AUTOMÁTICO ====================
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".menu a");
  const currentPath = window.location.pathname;

  links.forEach((link) => {
    if (link.href.includes(currentPath)) {
      link.classList.add("ativo");
    }
  });
});
