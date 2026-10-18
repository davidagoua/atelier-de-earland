const WHATSAPP_NUMBER = "2250759471517";

// Menu mobile
const navToggle = document.getElementById("navToggle");
const nav = document.getElementById("nav");

navToggle.addEventListener("click", () => {
  const open = nav.classList.toggle("is-open");
  navToggle.classList.toggle("is-open", open);
  navToggle.setAttribute("aria-expanded", open);
});

nav.querySelectorAll("a").forEach((link) =>
  link.addEventListener("click", () => {
    nav.classList.remove("is-open");
    navToggle.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
  })
);

// Ombre de l'en-tête au défilement
const header = document.getElementById("header");
window.addEventListener("scroll", () => {
  header.classList.toggle("is-scrolled", window.scrollY > 10);
});

// Pré-sélection de la prestation depuis les cartes
const serviceSelect = document.getElementById("service");
document.querySelectorAll("[data-service]").forEach((link) =>
  link.addEventListener("click", () => {
    const wanted = link.dataset.service;
    const option = [...serviceSelect.options].find((o) => o.text.startsWith(wanted));
    if (option) serviceSelect.value = option.value || option.text;
  })
);

// Formulaire de devis -> message WhatsApp
const form = document.getElementById("quoteForm");
const formError = document.getElementById("formError");

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const required = form.querySelectorAll("[required]");
  let valid = true;
  required.forEach((field) => {
    const empty = !field.value.trim();
    field.classList.toggle("is-invalid", empty);
    if (empty) valid = false;
  });
  formError.hidden = valid;
  if (!valid) return;

  const data = new FormData(form);
  const value = (name) => data.get(name).trim();
  const date = value("date") ? value("date").split("-").reverse().join("/") : "";

  const fields = [
    ["Nom", value("nom")],
    ["Téléphone", value("tel")],
    ["Prestation", value("service")],
    ["Événement", value("evenement")],
    ["Date", date],
    ["Nombre d'invités", value("invites")],
    ["Lieu", value("lieu")],
    ["Message", value("message")],
  ];
  const lines = [
    "Bonjour Les Ateliers de Earland, je souhaite un devis :",
    "",
    ...fields.filter(([, v]) => v).map(([label, v]) => `${label} : ${v}`),
  ];

  const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(lines.join("\n"))}`;
  window.open(url, "_blank", "noopener");
});

// Visionneuse de la galerie
const galleryItems = [...document.querySelectorAll("#gallery .gallery__item")];
const lightbox = document.getElementById("lightbox");
const lightboxImg = lightbox.querySelector("img");
const lightboxCaption = lightbox.querySelector("figcaption");
let current = 0;

function showPhoto(index) {
  current = (index + galleryItems.length) % galleryItems.length;
  const img = galleryItems[current].querySelector("img");
  lightboxImg.src = img.src;
  lightboxImg.alt = img.alt;
  lightboxCaption.textContent = img.alt;
}

function openLightbox(index) {
  showPhoto(index);
  lightbox.hidden = false;
  document.body.style.overflow = "hidden";
  lightbox.querySelector(".lightbox__close").focus();
}

function closeLightbox() {
  lightbox.hidden = true;
  document.body.style.overflow = "";
  galleryItems[current].focus();
}

galleryItems.forEach((item, index) => item.addEventListener("click", () => openLightbox(index)));
lightbox.querySelector(".lightbox__close").addEventListener("click", closeLightbox);
lightbox.querySelector(".lightbox__nav--prev").addEventListener("click", () => showPhoto(current - 1));
lightbox.querySelector(".lightbox__nav--next").addEventListener("click", () => showPhoto(current + 1));
lightbox.addEventListener("click", (event) => {
  if (event.target === lightbox) closeLightbox();
});
document.addEventListener("keydown", (event) => {
  if (lightbox.hidden) return;
  if (event.key === "Escape") closeLightbox();
  if (event.key === "ArrowLeft") showPhoto(current - 1);
  if (event.key === "ArrowRight") showPhoto(current + 1);
});

// Apparition des blocs au défilement
const revealTargets = document.querySelectorAll(
  ".section__head, .service, .offer, .gallery__item, .review, .about__visual, .about__text, .quote__info, .quote__form"
);
revealTargets.forEach((el) => el.classList.add("reveal"));

const observer = new IntersectionObserver(
  (entries) =>
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    }),
  { threshold: 0.12 }
);
revealTargets.forEach((el) => observer.observe(el));

document.getElementById("year").textContent = new Date().getFullYear();
