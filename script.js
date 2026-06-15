// SmartLoan – script.js

// ── Setup page: live loan calculation preview ──────────────────────────────
(function setupCalcPreview() {
  const fields = ["loan_amount", "interest_rate", "deduction_pct", "duration_months"];
  const preview = document.getElementById("calcPreview");
  if (!preview) return;

  function fmt(n) {
    return "₹" + Number(n).toLocaleString("en-IN", { maximumFractionDigits: 2 });
  }

  function update() {
    const loan = parseFloat(document.getElementById("loan_amount")?.value) || 0;
    const rate = parseFloat(document.getElementById("interest_rate")?.value) || 0;
    const ded = parseFloat(document.getElementById("deduction_pct")?.value) || 0;
    const months = parseFloat(document.getElementById("duration_months")?.value) || 0;

    if (!loan || !rate || !ded || !months) {
      preview.style.display = "none";
      return;
    }

    const interest = loan * (rate / 100) * (months / 12);
    const total = loan + interest;
    const deductionPerThousand = 1000 * (ded / 100);

    document.getElementById("previewInterest").textContent = fmt(interest);
    document.getElementById("previewTotal").textContent = fmt(total);
    document.getElementById("previewDeduction").textContent = fmt(deductionPerThousand);
    preview.style.display = "flex";
  }

  fields.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("input", update);
  });

  update(); // run on load if values exist
})();


// ── Merchant page: live split preview ─────────────────────────────────────
(function splitPreview() {
  const input = document.getElementById("paymentAmount");
  const preview = document.getElementById("splitPreview");
  if (!input || !preview) return;

  const dedPct = parseFloat(
    document.querySelector(".qr-main")?.dataset.deductionPct
  ) || 10;

  function fmt(n) {
    return "₹" + Number(n).toLocaleString("en-IN", { maximumFractionDigits: 2 });
  }

  input.addEventListener("input", function () {
    const amount = parseFloat(this.value) || 0;
    if (!amount) { preview.style.display = "none"; return; }

    const loanShare = amount * (dedPct / 100);
    const youShare = amount - loanShare;
    const youPct = (youShare / amount) * 100;

    document.getElementById("previewYou").textContent = fmt(youShare);
    document.getElementById("previewLoan").textContent = fmt(loanShare);
    document.getElementById("splitFill").style.width = youPct + "%";
    preview.style.display = "block";
  });
})();


// ── Dashboard: animate progress bar on load ────────────────────────────────
(function animateProgress() {
  const fill = document.querySelector(".progress-fill");
  if (!fill) return;
  const target = fill.style.width;
  fill.style.width = "0%";
  setTimeout(() => { fill.style.width = target; }, 200);
})();
