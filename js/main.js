const WHATSAPP_NUMBER = "2250759471517";

// Menu mobile
const navToggle = document.getElementById("navToggle");
const nav = document.getElementById("nav");

function setMenu(open) {
  nav.classList.toggle("is-open", open);
  navToggle.classList.toggle("is-open", open);
  navToggle.setAttribute("aria-expanded", open);
}

navToggle.addEventListener("click", () => setMenu(!nav.classList.contains("is-open")));
nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setMenu(false)));

// Ombre de l'en-tête au défilement
const header = document.getElementById("header");
const updateHeader = () => header.classList.toggle("is-scrolled", window.scrollY > 10);
window.addEventListener("scroll", updateHeader, { passive: true });
updateHeader();

// Formulaire de devis -> message WhatsApp
const form = document.getElementById("quoteForm");

if (form) {
  const formError = document.getElementById("formError");

  form.addEventListener("input", (event) => event.target.classList.remove("is-invalid"));

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    let valid = true;
    form.querySelectorAll("[required]").forEach((field) => {
      const empty = !field.value.trim();
      field.classList.toggle("is-invalid", empty);
      if (empty) valid = false;
    });
    formError.hidden = valid;
    if (!valid) return;

    const data = new FormData(form);
    const value = (name) => (data.get(name) || "").trim();
    const date = value("date") ? value("date").split("-").reverse().join("/") : "";

    const fields = [
      ["Nom", value("nom")],
      ["Téléphone / WhatsApp", value("tel")],
      ["Email", value("email")],
      ["Type d'événement", value("evenement")],
      ["Date", date],
      ["Nombre d'invités", value("invites")],
      ["Lieu", value("lieu")],
      ["Services souhaités", data.getAll("services").join(", ")],
      ["Projet", value("message")],
    ];
    const lines = [
      "Bonjour Les Ateliers de Earland, je souhaite échanger sur mon projet événementiel.",
      "",
      ...fields.filter(([, v]) => v).map(([label, v]) => `${label} : ${v}`),
    ];

    const url = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(lines.join("\n"))}`;
    window.open(url, "_blank", "noopener");
  });
}

// Filtres des réalisations
const filters = document.querySelectorAll(".filter");
const projects = document.querySelectorAll(".project");

filters.forEach((button) =>
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;
    filters.forEach((b) => {
      b.classList.toggle("is-active", b === button);
      b.setAttribute("aria-pressed", b === button);
    });
    projects.forEach((project) => {
      const cats = project.dataset.cat.split(" ");
      project.hidden = filter !== "all" && !cats.includes(filter);
    });
    if (window.ScrollTrigger) ScrollTrigger.refresh();
  })
);

// Visionneuse de la galerie
const lightbox = document.getElementById("lightbox");

if (lightbox) {
  const galleryItems = [...document.querySelectorAll("#gallery .gallery__item")];
  const lightboxImg = lightbox.querySelector("img");
  const lightboxCaption = lightbox.querySelector("figcaption");
  let current = 0;

  const showPhoto = (index) => {
    current = (index + galleryItems.length) % galleryItems.length;
    const img = galleryItems[current].querySelector("img");
    lightboxImg.src = img.src;
    lightboxImg.alt = img.alt;
    lightboxCaption.textContent = img.alt;
  };

  const openLightbox = (index) => {
    showPhoto(index);
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
    lightbox.querySelector(".lightbox__close").focus();
  };

  const closeLightbox = () => {
    lightbox.hidden = true;
    document.body.style.overflow = "";
    galleryItems[current].focus();
  };

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
}

document.getElementById("year").textContent = new Date().getFullYear();
