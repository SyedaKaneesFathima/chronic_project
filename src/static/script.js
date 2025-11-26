// static/script.js

// -----------------------------
// CHATBOT & FORM HELPERS
// -----------------------------
function toggleChat() {
  const cb = document.getElementById('chatbot');
  cb.classList.toggle('show');
}

function sendMsg() {
  const input = document.getElementById("chatMsg");
  const text = input.value.trim();
  if (!text) return;

  const chatBody = document.getElementById("chatBody");
  chatBody.innerHTML += `<div class="user-msg">${escapeHtml(text)}</div>`;
  chatBody.scrollTop = chatBody.scrollHeight;
  input.value = "";

  fetch("/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
  })
  .then(res => res.json())
  .then(data => {
      chatBody.innerHTML += `<div class="bot-msg">${escapeHtml(data.reply)}</div>`;
      chatBody.scrollTop = chatBody.scrollHeight;
  })
  .catch(() => {
      chatBody.innerHTML += `<div class="bot-msg">❌ Error connecting to AI.</div>`;
      chatBody.scrollTop = chatBody.scrollHeight;
  });
}

// small helper to avoid broken HTML when injecting user text
function escapeHtml(str) {
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

// -----------------------------
// RANGES SIDEBAR LOGIC
// -----------------------------
const RANGES = {
  "Age": "0 – 120 years (adult typical: 18–65).",
  "BMI": "18.5 – 24.9 kg/m² (Normal); 25–29.9 overweight; ≥30 obese.",
  "SystolicBP": "90 – 120 mmHg (normal); ≥130 high.",
  "DiastolicBP": "60 – 80 mmHg (normal); ≥80 high.",
  "SerumCreatinine": "Men: 0.7–1.3 mg/dL, Women: 0.6–1.1 mg/dL (lab-specific).",
  "GFR": "≥90 normal; 60–89 mild; 45–59 stage 3a; 30–44 stage 3b; 15–29 stage 4; <15 stage 5.",
  "HemoglobinLevels": "Men: 13.8–17.2 g/dL; Women: 12.1–15.1 g/dL.",
  "ProteinInUrine": "0–30 mg/dL (trace); >30 abnormal.",
  "FastingBloodSugar": "70–99 mg/dL normal; 100–125 prediabetes.",
  "HbA1c": "<5.7% normal; 5.7–6.4% prediabetes; ≥6.5% diabetes."
};

// Map input name attributes → keys used in RANGES
const INPUT_TO_FEATURE = {
  "age": "Age",
  "bmi": "BMI",
  "systolic_bp": "SystolicBP",
  "diastolic_bp": "DiastolicBP",
  "creatinine": "SerumCreatinine",
  "gfr": "GFR",
  "hemoglobin": "HemoglobinLevels",
  "protein": "ProteinInUrine",
  "sugar": "FastingBloodSugar",
  "hba1c": "HbA1c"
};

function buildRangesList(){
  const container = document.getElementById("rangeList");
  if(!container) return;
  container.innerHTML = "";
  for(const [feature, range] of Object.entries(RANGES)){
    const div = document.createElement("div");
    div.className = "range-item";
    div.dataset.feature = feature;
    div.innerHTML = `<div class="label">${feature}</div><div class="values">${range}</div>`;
    container.appendChild(div);
  }
}

function highlightFeature(featureKey){
  const items = document.querySelectorAll(".range-item");
  items.forEach(it => {
    if(featureKey && it.dataset.feature === featureKey){
      it.classList.add("highlight");
      it.scrollIntoView({behavior: "smooth", block: "nearest"});
    } else {
      it.classList.remove("highlight");
    }
  });
}

function wireInputFocus(){
  Object.keys(INPUT_TO_FEATURE).forEach(inputName => {
    const el = document.querySelector(`[name="${inputName}"]`);
    if(!el) return;
    el.addEventListener("focus", () => {
      const feature = INPUT_TO_FEATURE[inputName];
      highlightFeature(feature);
      const sidebar = document.getElementById("rangeSidebar");
      if (sidebar && sidebar.classList.contains('hidden')) {
        // don't automatically show, just highlight if open; optionally open:
        // sidebar.classList.remove('hidden');
      }
    });
    el.addEventListener("blur", () => {
      // keep highlight for a short time, then clear
      setTimeout(() => highlightFeature(null), 300);
    });
  });
}

// Sidebar toggle wiring
document.addEventListener("DOMContentLoaded", () => {
  buildRangesList();
  wireInputFocus();

  const sidebar = document.getElementById("rangeSidebar");
  const toggle = document.getElementById("rangeToggle");
  const closeBtn = document.getElementById("closeRanges");

  if(toggle){
    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("hidden");
    });
  }
  if(closeBtn){
    closeBtn.addEventListener("click", () => {
      sidebar.classList.add("hidden");
    });
  }
});
