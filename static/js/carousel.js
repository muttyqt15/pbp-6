document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll("[data-slides] .slide");
  const prevButton = document.querySelector('[data-carousel-button="prev"]');
  const nextButton = document.querySelector('[data-carousel-button="next"]');

  let currentIndex = 0;

  const updateSlides = () => {
    slides.forEach((slide, index) => {
      slide.removeAttribute("data-active"); // Remove active class from all slides
      slide.style.opacity = "0"; // Set opacity to 0
      slide.style.transitionDelay = "200ms"; // Delay transition for inactive slides
    });

    slides[currentIndex].setAttribute("data-active", ""); // Set current slide as active
    slides[currentIndex].style.opacity = "1"; // Set current slide opacity to 1
    slides[currentIndex].style.transitionDelay = "0ms"; // Remove delay for active slide
  };

  nextButton.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % slides.length; // Loop back to start
    updateSlides();
  });

  prevButton.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + slides.length) % slides.length; // Loop back to end
    updateSlides();
  });

  updateSlides(); // Initialize slides on load
});
