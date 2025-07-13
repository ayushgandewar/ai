document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ Script loaded and DOM is ready");

  // ✅ 1. Load stored leads on page load
  const savedLeads = JSON.parse(localStorage.getItem("leads")) || [];
  const table = document.getElementById("leadTableBody");

  savedLeads.forEach(lead => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${lead.email}</td>
      <td>${lead.initial_score}</td>
      <td>${lead.reranked_score}</td>
      <td>${lead.comments}</td>
    `;
    table.appendChild(row);
  });

  // ✅ 2. Handle form submit
  document.getElementById("lead-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    console.log("📩 Form submitted");

    const email = document.getElementById("email").value;
    const creditScore = document.getElementById("creditScore").value;
    const ageGroup = document.getElementById("ageGroup").value;
    const familyStatus = document.getElementById("family").value;
    const income = document.getElementById("income").value;
    const comments = document.getElementById("comments").value;
    const consent = document.getElementById("consent").checked;

    if (!consent) {
      alert("Please provide consent to proceed.");
      return;
    }

    const leadData = {
      email,
      phone: "0000000000", // Dummy phone since input is missing in form
      creditScore: Number(creditScore),
      ageGroup,
      familyStatus,
      income: Number(income),
      comments,
    };

    console.log("📤 Sending data:", leadData);

    try {
      const response = await fetch("https://ai-2-zzcx.onrender.com/score", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(leadData),
      });

      if (!response.ok) {
        const errorMsg = await response.text();
        throw new Error(`HTTP ${response.status}: ${errorMsg}`);
      }

      const result = await response.json();
      console.log("✅ Received result:", result);

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${email}</td>
        <td>${result.initial_score}</td>
        <td>${result.reranked_score}</td>
        <td>${comments}</td>
      `;
      table.appendChild(row);

      // ✅ Save to localStorage
      savedLeads.push({
        email,
        initial_score: result.initial_score,
        reranked_score: result.reranked_score,
        comments
      });
      localStorage.setItem("leads", JSON.stringify(savedLeads));

    } catch (error) {
      console.error("❌ Error submitting data:", error);
      alert("Failed to submit data. Check backend or API.");
    }
  });
});
