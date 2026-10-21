// Animations GSAP (le site reste entièrement lisible si GSAP ne se charge pas)
// Dans le HTML :
//   data-reveal        -> l'élément apparaît au défilement
//   data-stagger       -> ses enfants apparaissent en cascade
//   data-reveal-media  -> l'image se dévoile de bas en haut
if (window.gsap && window.ScrollTrigger) {
  gsap.registerPlugin(ScrollTrigger);

  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    // Les éléments ayant une transition CSS sur transform la perdent le temps de l'animation
    const withoutCssTransition = (targets) => {
      const els = gsap.utils.toArray(targets);
      gsap.set(els, { transition: "none" });
      return () => gsap.set(els, { clearProps: "transition,transform" });
    };

    const onScroll = (trigger) => ({ trigger, start: "top 85%", once: true });

    // ===== Accueil =====
    if (document.querySelector(".hero")) {
      gsap.timeline({ defaults: { ease: "power3.out" } })
        .from(".hero__bg img", { scale: 1.15, duration: 2.2, ease: "power2.out" })
        .from(".hero .script", { y: 20, autoAlpha: 0, duration: 0.9 }, 0.3)
        .from(".hero h1", { y: 50, autoAlpha: 0, duration: 1.1 }, 0.45)
        .from(".hero__tagline", { y: 30, autoAlpha: 0, duration: 0.9 }, 0.7)
        .from(".hero__lead", { y: 30, autoAlpha: 0, duration: 0.9 }, 0.85)
        .from(".hero__actions .btn", {
          y: 20, autoAlpha: 0, duration: 0.7, stagger: 0.12,
          onComplete: withoutCssTransition(".hero__actions .btn"),
        }, 1)
        .from(".hero__expertises", { scaleX: 0, transformOrigin: "left", duration: 1, ease: "power2.inOut" }, 1.1)
        .from(".hero__expertises li", { y: 10, autoAlpha: 0, duration: 0.5, stagger: 0.08 }, 1.4);

      gsap.to(".hero__bg img", {
        yPercent: -10, ease: "none",
        scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
      });
    }

    // ===== Bandeau des pages intérieures =====
    if (document.querySelector(".page-hero")) {
      gsap.timeline({ defaults: { ease: "power3.out" } })
        .from(".page-hero__bg img", { scale: 1.2, duration: 2, ease: "power2.out" })
        .from(".page-hero .container > *", { y: 40, autoAlpha: 0, duration: 0.9, stagger: 0.12 }, 0.2);
    }

    // ===== Apparitions au défilement =====
    gsap.utils.toArray("[data-reveal]").forEach((el) =>
      gsap.from(el, {
        y: 40, autoAlpha: 0, duration: 0.9, ease: "power3.out",
        onComplete: withoutCssTransition(el),
        scrollTrigger: onScroll(el),
      })
    );

    gsap.utils.toArray("[data-stagger]").forEach((group) =>
      gsap.from(group.children, {
        y: 40, autoAlpha: 0, duration: 0.9, ease: "power3.out", stagger: 0.12,
        onComplete: withoutCssTransition(group.children),
        scrollTrigger: onScroll(group),
      })
    );

    gsap.utils.toArray("[data-reveal-media]").forEach((media) => {
      gsap.from(media, {
        clipPath: "inset(100% 0% 0% 0%)", duration: 1.3, ease: "power4.out",
        scrollTrigger: { trigger: media, start: "top 85%", once: true },
      });
      const img = media.querySelector("img");
      if (img) {
        gsap.fromTo(img, { scale: 1.2 }, {
          scale: 1, ease: "none",
          scrollTrigger: { trigger: media, start: "top bottom", end: "bottom top", scrub: true },
        });
      }
    });

    // Projets du portfolio (gérés à part à cause des filtres)
    const projects = gsap.utils.toArray(".project");
    if (projects.length) {
      gsap.from(projects, {
        y: 50, autoAlpha: 0, duration: 0.9, ease: "power3.out", stagger: 0.1,
        scrollTrigger: onScroll(".projects"),
      });
    }

    // ===== Bouton WhatsApp =====
    gsap.from(".wa-float", {
      scale: 0, duration: 0.6, ease: "back.out(2)", delay: 1.2,
      onComplete: withoutCssTransition(".wa-float"),
    });
  });
}
