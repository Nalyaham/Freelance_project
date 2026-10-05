/* YourRoom staff dashboard | list page helpers */
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("list-form");
  if (!form) return;

  // Mark rows you have changed, and rows you have ticked for deletion.
  form.querySelectorAll("tbody tr").forEach(function (row) {
    function markDirty() { row.classList.add("is-dirty"); }
    row.addEventListener("input", markDirty);
    row.addEventListener("change", markDirty);

    var del = row.querySelector("input[type=checkbox][name$='-DELETE']");
    if (del) {
      del.addEventListener("change", function () {
        row.classList.toggle("is-deleting", del.checked);
      });
    }
  });

  // Ask before deleting anything.
  form.addEventListener("submit", function (e) {
    var n = form.querySelectorAll("input[name$='-DELETE']:checked").length;
    if (n && !window.confirm("Delete " + n + (n === 1 ? " unit" : " units") +
        "? Their photos and video records are removed too.")) {
      e.preventDefault();
    }
  });
});
