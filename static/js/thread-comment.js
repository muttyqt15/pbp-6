$(document).ready(() => {
    function getCSRFToken() {
        const csrfToken = document.cookie
          .split("; ")
          .find((row) => row.startsWith("csrftoken="))
          ?.split("=")[1];
        return csrfToken || "";
      }
    window.deleteComment = function (commentId) {
      $.ajax({
        url: `/thread/delete/comment/${commentId}/`,
        method: "POST",
        headers: {
          "X-CSRFToken": "{{ csrf_token }}",
        },
        success: function (data) {
          if (data.success) {
            $(`#comment-${commentId}`).remove();
          }
        },
        error: function (xhr, status, error) {
          console.error("Error:", error);
        },
      });
    };
    window.toggleCommentLike = function (commentId) {
      const likeButton = document.getElementById(
        `like-button-comment-${commentId}`
      );
      const originalText = likeButton.textContent;

      likeButton.textContent = "Liking...";
      likeButton.disabled = true;

      fetch(`/thread/like/comment/${commentId}/`, {
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
  });