(() => {
    const slidesContainer = document.getElementById("slides-container");
    const slides = document.querySelectorAll(".slide");
    const prevButton = document.getElementById("slide-arrow-prev");
    const nextButton = document.getElementById("slide-arrow-next");
  
    // Check if elements are selected correctly
    console.log(slidesContainer, slides, prevButton, nextButton);
  
    if (!slidesContainer || slides.length === 0 || !prevButton || !nextButton) {
      console.error("One or more elements are not found!");
      return; // Exit if elements are not found
    }
  
    nextButton.addEventListener("click", () => {
      console.log("Next button clicked"); // For debugging
      if (slides.length > 0) {
        const slideWidth = slides[0].clientWidth; // Use the width of the first slide
        slidesContainer.scrollLeft += slideWidth; // Scroll right
      }
    });
  
    prevButton.addEventListener("click", () => {
      console.log("Previous button clicked"); // For debugging
      if (slides.length > 0) {
        const slideWidth = slides[0].clientWidth; // Use the width of the first slide
        slidesContainer.scrollLeft -= slideWidth; // Scroll left
      }
    });
  })();
  