
(() => {
  function getCSRFToken() {
    const csrfToken = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      ?.split("=")[1];
    return csrfToken || "";
  }
// Flag to track edit mode
  let isEditMode = false;
  let originalContent = ""; // Store original content globally
  console.log("Thread.js loaded");
  // Toggle edit mode for a specific thread
  window.toggleEditMode = function (threadId, e) {
    const contentContainer = $(`#content-container-${threadId}`);
    const editButtons = $(`#edit-buttons-${threadId}`);
    if (!isEditMode) {
      // Save original content when entering edit mode
      originalContent = contentContainer.find("p").text();

      contentContainer.html(`
          <textarea id="edit-content-${threadId}" class="w-full p-2 border border-gray-300 rounded mb-4 z-50">${originalContent}</textarea>
        `);
      // Add click handler to prevent propagation on the textarea
      $(`#edit-content-${threadId}`).on("click", function (e) {
        e.stopPropagation();
      });

      editButtons.html(`
          <button class="text-coyote hover:text-lion duration-300 ease-in-out transition text-sm z-50" onclick="submitEdit(${threadId})" id="save-${threadId}">Save</button>
          <button class="text-gray-500 hover:text-raisin duration-300 ease-in-out transition text-sm z-50" onclick="cancelEdit(${threadId})" id="cancel-${threadId}">Cancel</button>
        `);

      $(`#edit-content-${threadId}`).focus();
    } else {
      cancelEdit(threadId);
    }

    isEditMode = !isEditMode;
  };

  // Submit edited content for a specific thread
  window.submitEdit = function (threadId, e) {
    const updatedContent = $(`#edit-content-${threadId}`).val();

    $.ajax({
      url: `/thread/edit/${threadId}/`,
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
        "Content-Type": "application/json",
      },
      data: JSON.stringify({ content: updatedContent }),
      success: function (data) {
        if (data.success) {
          const contentContainer = $(`#content-container-${threadId}`);
          contentContainer.html(
            `<p class="text-gray-800 mb-4 cursor-pointer"
                onclick="window.location.href = '/thread/${threadId}/';"
            >${data.data.content || updatedContent}</p>`
          );

          const editButtons = $(`#edit-buttons-${threadId}`);
          editButtons.html(`
              <button class="text-gray-600 font-bold hover:text-coyote duration-300 transition text-sm" onclick="toggleEditMode(${threadId})">Edit</button>
              <button class="text-gray-600 font-bold hover:text-red-500 duration-300 transition text-sm" onclick="deleteThread(${threadId})">Delete</button>
            `);

          isEditMode = false;
        }
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  };

  // Cancel edit mode and restore original content
  window.cancelEdit = function (threadId, e) {
    const contentContainer = $(`#content-container-${threadId}`);
    const editButtons = $(`#edit-buttons-${threadId}`);

    // Restore the original content without saving
    contentContainer.html(
      `<p class="text-gray-800 mb-4">${originalContent}</p>`
    );

    // Reset buttons
    editButtons.html(`
        <button class="text-gray-600 font-bold hover:text-coyote duration-300 transition text-sm" onclick="toggleEditMode(${threadId})">Edit</button>
        <button class="text-gray-600 font-bold hover:text-red-500 duration-300 transition text-sm" onclick="deleteThread(${threadId})">Delete</button>
      `);

    isEditMode = false;
  };

  // Delete a specific thread
  window.deleteThread = function (threadId, e) {
    $.ajax({
      url: `/thread/delete/${threadId}/`,
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
      success: function (data) {
        if (data.success) {
          $(`#thread-${threadId}`).remove();
        }
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  };

  // Toggle like for a specific thread
  window.toggleLike = function (threadId, e) {
    const likeButton = document.getElementById(`like-button-${threadId}`);
    const originalText = likeButton.textContent;
    console.log("Liking thread:", threadId);
    console.log("csrf", getCSRFToken());
    likeButton.textContent = "Liking...";
    likeButton.disabled = true;

    fetch(`/thread/like/${threadId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCSRFToken(),
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        likeButton.textContent = `${data.likes ?? 0} Likes`;

        if (data.liked) {
          likeButton.classList.add("text-[#910101]");
          likeButton.classList.remove("text-blue-500");
        } else {
          likeButton.classList.add("text-blue-500");
          likeButton.classList.remove("text-[#910101]");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        likeButton.textContent = originalText;
      })
      .finally(() => {
        likeButton.disabled = false;
      });
  };
})();
