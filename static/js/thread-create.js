
$(document).ready(function () {
    
    const $textarea = $("#content");
    const $charCount = $("#char-count");
    const $imageInput = $("#image");
    const $imagePreview = $("#image-preview");

    $textarea.on("input", function () {
      const remaining = 456 - $textarea.val().length;
      $charCount.text(`${remaining} characters remaining`);
      if (remaining < 0) {
        $charCount.text("You've exceeded the limit!");
      }
    });

    $imageInput.on("change", function () {
      const file = $imageInput[0].files[0]; // Get the uploaded file
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          $imagePreview.attr("src", e.target.result); // Set the preview source
          $imagePreview.removeClass("hidden"); // Show the preview

          // Limit the image preview size
          $imagePreview.css({
            maxWidth: "48px",
            maxHeight: "48px"
          });

          // Reset the image preview size on error
          $imagePreview.on("error", function () {
            $imagePreview.css({
              maxWidth: "none",
              maxHeight: "none"
            });
            $imagePreview.attr("src", ""); // Clear the source
          });
        };
        reader.readAsDataURL(file); // Read the file as a data URL
      } else {
        $imagePreview.addClass("hidden"); // Hide the preview if no file
      }
    });
  });