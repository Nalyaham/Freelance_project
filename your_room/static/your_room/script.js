/* YourRoom | script.js */
document.addEventListener("DOMContentLoaded", function () {
  // Hero search -> search results page
 
  // Feedback form
  var feedback = document.getElementById("feedback-form");
  if (feedback) {
    feedback.addEventListener("submit", function (e) {
      e.preventDefault();
      feedback.reset();
      document.getElementById("feedback-note").hidden = false;
    });
  }

  // Show the search term on the results page
  var term = document.getElementById("search-term");
  if (term) {
    var q = new URLSearchParams(window.location.search).get("q") || "";
    term.textContent = q;
  }

  // Filter buttons toggle an active state
  document.querySelectorAll(".filter").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.classList.toggle("is-active");
      btn.style.background = btn.classList.contains("is-active") ? "var(--surface-gray)" : "";
    });
  });

  // Book now
  var book = document.getElementById("book-now");
  if (book) {
    book.addEventListener("click", function () {
      alert("Thank you! We will contact you shortly to confirm your booking.");
    });
  }
});

// This line of code helps to remove any bfcache. Any text in the search bar is removed
// once the user returns to the page. 
window.addEventListener("pageshow", function (event) {
  var searchInput = document.getElementById("search-input");
  if (searchInput && event.persisted) {
    searchInput.value = "";
  }
});