const faqs = document.querySelectorAll('.respostaduvida');

faqs.forEach(item => {
  const pergunta = item.querySelector('.perguntafaq');
  pergunta.addEventListener('click', () => {
    const texto = item.querySelector('.textchamado');
    const icone = item.querySelector('.icone');

    if (texto.style.display === "block") {
      texto.style.display = "none";
      icone.classList.remove('fa-chevron-down');
      icone.classList.add('fa-chevron-right');
    } else {
      texto.style.display = "block";
      icone.classList.remove('fa-chevron-right');
      icone.classList.add('fa-chevron-down');
    }
  });
});
