/* YourRoom | script.js */
document.addEventListener("DOMContentLoaded", function () {
    var navToggle = document.getElementById("nav-toggle");
  var navMenu = document.getElementById("nav-menu");
  var navClose = document.getElementById("nav-close");

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", function () {
      var isOpen = navMenu.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", isOpen);
    });
  }
  if (navClose && navMenu && navToggle) {
    navClose.addEventListener("click", function () {
      navMenu.classList.remove("is-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  }
  if (navMenu && navToggle) {
    navMenu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navMenu.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }
 
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
      var name = prompt("Full name for the booking:");
      if (!name) return;
      var phone = prompt("Mobile money phone number (e.g. +2567XXXXXXXX):");
      if (!phone) return;
// This line below reads the value of the unit_type and primary key in the button
      var unitType = book.dataset.unitType;
      var unitId = book.dataset.unitId;
      var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

      book.disabled = true;
      book.textContent = "Processing...";

// This line creates a form for the data of name and phone obtained from the user
      var formData = new FormData();
      formData.append("name", name);
      formData.append("phone_number", phone);

      fetch("/book/" + unitType + "/" + unitId + "/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: formData,
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.status === "success") {
            alert("Payment successful! Booking confirmed. Transaction: " + data.transaction_id);
          } else {
            alert("Payment failed or was not approved. Please try again.");
          }
        })
        .catch(function (err) {
          console.error(err);
          alert("Something went wrong. Please try again.");
        })
        .finally(function () {
          book.disabled = false;
          book.textContent = "Book Now";
        });
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