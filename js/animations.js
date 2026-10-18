// Animations GSAP (le site reste entièrement lisible si GSAP ne se charge pas)
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

    // Apparition au défilement, en cascade
    const revealOnScroll = (targets, vars = {}, trigger) => {
      const els = gsap.utils.toArray(targets);
      if (!els.length) return;
      gsap.from(els, {
        autoAlpha: 0,
        y: 40,
        duration: 0.9,
        ease: "power3.out",
        stagger: 0.12,
        onComplete: withoutCssTransition(els),
        ...vars,
        scrollTrigger: { trigger: trigger || els[0], start: "top 85%", once: true },
      });
    };

    // ===== Accueil =====
    const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });
    heroTl
      .from(".hero__pattern", { xPercent: 30, rotate: 20, autoAlpha: 0, duration: 1.4, ease: "power2.out" })
      .from(".hero__plate", { scale: 0.6, rotate: -25, autoAlpha: 0, duration: 1.2, ease: "back.out(1.6)" }, 0.2)
      .from(".hero .script", { x: -30, autoAlpha: 0, duration: 0.8 }, 0.4)
      .from(".hero h1", { y: 50, autoAlpha: 0, duration: 1 }, 0.5)
      .from(".hero__lead", { y: 30, autoAlpha: 0, duration: 0.8 }, 0.7)
      .from(".hero__actions .btn", {
        y: 20, autoAlpha: 0, duration: 0.6, stagger: 0.12,
        onComplete: withoutCssTransition(".hero__actions .btn"),
      }, 0.85)
      .from(".hero__badges li", { y: 15, autoAlpha: 0, duration: 0.5, stagger: 0.08 }, 1);

    // Le plateau flotte doucement
    gsap.to(".hero__plate", {
      y: -14, duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: -1, delay: 1.4,
    });

    // Parallaxe du motif wax
    gsap.to(".hero__pattern", {
      yPercent: 12, ease: "none",
      scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true },
    });

    // ===== Titres de section =====
    gsap.utils.toArray(".section__head").forEach((head) =>
      revealOnScroll(head.children, { stagger: 0.1 }, head)
    );

    // ===== L'Atelier =====
    gsap.from(".about__visual", {
      clipPath: "inset(100% 0 0 0 round 18px)", duration: 1.3, ease: "power4.out",
      scrollTrigger: { trigger: ".about", start: "top 80%", once: true },
    });
    gsap.fromTo(".about__visual img", { scale: 1.25 }, {
      scale: 1, ease: "none",
      scrollTrigger: { trigger: ".about", start: "top bottom", end: "bottom top", scrub: true },
    });
    revealOnScroll(".about__text > *", { stagger: 0.1 }, ".about__text");

    const percent = document.querySelector(".about__stats strong");
    if (percent && percent.textContent.trim() === "100%") {
      const counter = { value: 0 };
      gsap.to(counter, {
        value: 100, duration: 1.6, ease: "power2.out",
        onUpdate: () => (percent.textContent = `${Math.round(counter.value)}%`),
        scrollTrigger: { trigger: ".about__stats", start: "top 90%", once: true },
      });
    }

    // ===== Prestations =====
    revealOnScroll(".service", { y: 60 }, ".services");
    gsap.from(".service__icon", {
      scale: 0, rotate: -90, duration: 0.7, ease: "back.out(2)", stagger: 0.12, delay: 0.3,
      scrollTrigger: { trigger: ".services", start: "top 85%", once: true },
    });
    revealOnScroll(".steps", {}, ".steps");
    gsap.from(".steps li", {
      x: -30, autoAlpha: 0, duration: 0.7, ease: "power3.out", stagger: 0.2, delay: 0.2,
      scrollTrigger: { trigger: ".steps", start: "top 80%", once: true },
    });

    // ===== Offres =====
    revealOnScroll(".offer", { y: 50, rotateX: -15, transformPerspective: 800, transformOrigin: "top center" }, ".offers__grid");
    revealOnScroll(".offers__cta", {}, ".offers__cta");

    // ===== Galerie =====
    revealOnScroll(".gallery__item", { y: 0, scale: 0.85, duration: 0.8, stagger: 0.08 }, ".gallery");

    // ===== Avis et devis =====
    revealOnScroll(".review", {}, ".reviews");
    revealOnScroll(".quote__info > *", { stagger: 0.08 }, ".quote");
    revealOnScroll(".quote__form", { x: 40, y: 0 }, ".quote");

    // ===== Bouton WhatsApp =====
    gsap.from(".wa-float", {
      scale: 0, duration: 0.6, ease: "back.out(2)", delay: 1.6,
      onComplete: withoutCssTransition(".wa-float"),
    });
  });
}
