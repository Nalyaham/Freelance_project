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

    var csrfToken = feedback.querySelector("[name=csrfmiddlewaretoken]").value;
    var formData = new FormData(feedback);

    fetch("/feedback/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken },
      body: formData,
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.status === "success") {
          feedback.reset();
          document.getElementById("feedback-note").hidden = false;
          
          // This line is used to set the time of the message which goes off after 4 secs
          setTimeout(function () {
            note.hidden = true;
          }, 4000);
        } else {
          alert(data.message || "Something went wrong. Please try again.");
        }
      })
      .catch(function (err) {
        console.error(err);
        alert("Something went wrong. Please try again.");
      });

    
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
          if (data.status === "error") {
            alert(data.message || "Something went wrong.");
            book.disabled = false;
            book.textContent = "Book Now";
            return;
          }
          alert("Payment request sent! Check your phone to approve.");
          pollBookingStatus(data.reference);
          });
        function pollBookingStatus(reference) {
      var interval = setInterval(function () {
        fetch("/booking-status/" + reference + "/")
          .then(function (res) { return res.json(); })
          .then(function (data) {
            if (data.status === "successful") {
              clearInterval(interval);
              alert("Booking confirmed! 🎉");
              book.disabled = false;
              book.textContent = "Book Now";
            } else if (data.status === "failed" || data.status === "cancelled") {
              clearInterval(interval);
              alert("Payment " + data.status + (data.failure_reason ? ": " + data.failure_reason : ""));
              book.disabled = false;
              book.textContent = "Book Now";
            }
            // "pending"/"processing" → keep polling, no action needed
          });
      }, 3000); // every 3 seconds// stop after 5 min
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
  }
});