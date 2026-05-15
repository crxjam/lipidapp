const API_BASE = "https://fuzzy-goldfish-v6g4p646rx553qw4-8000.app.github.dev/";

let lastResult = null;
let lastFilename = "";

function getFeatures() {
  return {
    filename: lastFilename,
    origin_peak: document.getElementById("origin_peak").checked,
    beta_increased: document.getElementById("beta_increased").checked,
    prebeta_increased: document.getElementById("prebeta_increased").checked,
    broad_beta: document.getElementById("broad_beta").checked,
    lpx_suspected: document.getElementById("lpx_suspected").checked,
    sample_quality_issue: document.getElementById("sample_quality_issue").checked,
    alpha_visible: true
  };
}

async function uploadOne() {
  const input = document.getElementById("scanInput");

  if (!input.files.length) {
    alert("Choose or take a scan photo first.");
    return;
  }

  const file = input.files[0];
  lastFilename = file.name;

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE}/upload-one`, {
    method: "POST",
    body: formData
  });

  const data = await response.json();
  document.getElementById("resultBox").textContent =
    JSON.stringify(data, null, 2);
}

async function classifyManual() {
  const features = getFeatures();

  const response = await fetch(`${API_BASE}/classify-manual`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(features)
  });

  lastResult = await response.json();

  document.getElementById("resultBox").textContent =
    JSON.stringify(lastResult, null, 2);
}

async function saveLabel() {
  const features = getFeatures();

  const payload = {
    ...features,
    suggested_classification:
      lastResult?.result?.classification || "",

    confidence:
      lastResult?.result?.confidence || "",

    confirmed_classification:
      document.getElementById("confirmed_classification").value,

    comments:
      document.getElementById("comments").value
  };

  const response = await fetch(`${API_BASE}/save-label`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  const data = await response.json();

  document.getElementById("resultBox").textContent =
    JSON.stringify(data, null, 2);
}
