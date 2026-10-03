// Chandra Asri Manufacturing Knowledge Hub - Frontend Logic (Gemini & DCS Theme)

let activeTab = "assistant";
let isChatMode = false;
let selectedConflictId = null;
let recognition = null;
let isRecording = false;
let selectedDatasetId = localStorage.getItem("ca-dataset-id") || "dataset_01";
let availableDatasets = [];

// Multimodal Image Attachment State
let attachedImageData = null;
let attachedImageName = "";

let currentUser = {
  name: "Plant Engineer",
  shortName: "Engineer",
  title: "Authenticated User",
  unit: "Polyethylene Plant",
  initials: "PE"
};

document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide) lucide.createIcons();
  setupAuth();
  setupTabs();
  setupQueryHandler();
  setupDatasetSelector();
  setupSpeechRecognition();
  setupQuarantine();
  setupTelemetry();
  initTelemetryChart();

  // Load initial graph and quarantine data
  loadGraphData();
  loadQuarantineData();
});

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

async function loadAssetSuggestions() {
  try {
    const response = await fetch("/api/assets");
    const assets = await response.json();
    const suggestions = assets.filter(asset => asset.dataset_id === selectedDatasetId);
    const container = document.getElementById("hero-sample-chips");
    if (!container) return;
    container.innerHTML = suggestions.map(asset => `
      <button class="asset-suggestion pro-btn-secondary px-3.5 py-1.5 rounded-full text-[11px] transition flex items-center gap-1.5 shadow-sm" data-tag="${escapeHtml(asset.tag)}">
        <i data-lucide="factory" class="w-3 h-3"></i><span>${escapeHtml(asset.tag)}</span>
      </button>
    `).join("");
    container.querySelectorAll(".asset-suggestion").forEach(button => {
      button.addEventListener("click", () => {
        const asset = assets.find(item => item.tag === button.dataset.tag);
        const query = `What information and documents are available for ${asset?.tag} (${asset?.name || "equipment"})?`;
        document.getElementById("query-input").value = query;
        submitQuery(query);
      });
    });
    if (window.lucide) lucide.createIcons();
  } catch (error) {
    console.error("Failed to load asset suggestions:", error);
  }
}

// ---------------------------------------------------------------------------
// 1. Authentication & Role Switcher
// ---------------------------------------------------------------------------
function setupAuth() {
  const loginScreen = document.getElementById("login-screen");
  const mainApp = document.getElementById("main-app");
  const directLoginBtn = document.getElementById("direct-login-btn");
  const logoutBtn = document.getElementById("logout-btn");
  const idField = document.getElementById("login-id");
  const passwordField = document.getElementById("login-pass");

  const login = () => {
    if (directLoginBtn.disabled) return;
    const idInput = idField.value.trim();
    if (!idInput || !passwordField.value) {
      (idInput ? passwordField : idField).reportValidity();
      return;
    }

    const shortName = idInput.split("@")[0];
    currentUser = {
      name: idInput,
      shortName,
      title: "Authenticated Operator",
      unit: "Polyethylene Plant",
      initials: shortName.slice(0, 2).toUpperCase()
    };
    applyUserProfile();

    directLoginBtn.disabled = true;
    enterApp();
  };

  directLoginBtn.addEventListener("click", login);
  idField.addEventListener("keydown", event => {
    if (event.key === "Enter") {
      event.preventDefault();
      passwordField.focus();
    }
  });
  passwordField.addEventListener("keydown", event => {
    if (event.key === "Enter") {
      event.preventDefault();
      login();
    }
  });

  logoutBtn.addEventListener("click", () => {
    exitChatMode();
    mainApp.classList.add("hidden");
    directLoginBtn.disabled = false;
    loginScreen.classList.remove("hidden");
  });
}

function applyUserProfile() {
  document.getElementById("user-name-display").innerText = currentUser.name;
  document.getElementById("user-role-display").innerText = currentUser.title;
  document.getElementById("user-avatar").innerText = currentUser.initials;
  const heroName = document.getElementById("hero-user-name");
  if (heroName) heroName.innerText = currentUser.shortName;

  const modalSme = document.getElementById("modal-sme-name");
  if (modalSme) modalSme.value = `${currentUser.name} (${currentUser.title})`;
}

function enterApp() {
  const loginScreen = document.getElementById("login-screen");
  const mainApp = document.getElementById("main-app");

  loginScreen.classList.add("hidden");
  mainApp.classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

// ---------------------------------------------------------------------------
// 2. Tab Navigation & Menu Shortcuts
// ---------------------------------------------------------------------------
function setupTabs() {
  const tabs = document.querySelectorAll(".clean-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const target = tab.getAttribute("data-tab");
      switchTab(target);
    });
  });

  // Shortcut menu chips on hero
  document.querySelectorAll(".menu-shortcut-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-target-tab");
      switchTab(target);
    });
  });

}

function switchTab(target) {
  if (!target) return;

  document.querySelectorAll(".clean-tab").forEach(t => {
    t.classList.remove("active");
    if (t.getAttribute("data-tab") === target) t.classList.add("active");
  });

  document.querySelectorAll(".tab-content").forEach(tc => tc.classList.remove("active"));
  const content = document.getElementById(`tab-${target}`);
  if (content) content.classList.add("active");

  activeTab = target;

  const backHomeBtn = document.getElementById("back-to-home-btn");
  if (backHomeBtn) {
    if (target !== "assistant" || isChatMode) {
      backHomeBtn.classList.remove("hidden");
      backHomeBtn.classList.add("flex");
    } else {
      backHomeBtn.classList.add("hidden");
      backHomeBtn.classList.remove("flex");
    }
  }

  if (target === "graph") loadGraphData();
  if (target === "quarantine") loadQuarantineData();
  if (target === "telemetry") {
    setTimeout(() => {
      initTelemetryChart();
    }, 60);
  }
  if (window.lucide) lucide.createIcons();
}

// ---------------------------------------------------------------------------
// 3. Web Speech API (Microphone Voice Search)
// ---------------------------------------------------------------------------
function setupSpeechRecognition() {
  const micBtn = document.getElementById("mic-btn");
  const statusToast = document.getElementById("mic-status-toast");
  const input = document.getElementById("query-input");

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    micBtn.title = "Voice search is not supported in this browser (use Chrome or Edge)";
    micBtn.addEventListener("click", () => {
      alert("Web Speech API is not supported in this browser. Please use Google Chrome or Microsoft Edge for voice input.");
    });
    return;
  }

  recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = "en-US";

  recognition.onstart = () => {
    isRecording = true;
    micBtn.classList.add("mic-recording");
    statusToast.classList.remove("hidden");
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    if (transcript) {
      input.value = transcript;
      submitQuery(transcript);
    }
  };

  recognition.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
    stopRecording();
  };

  recognition.onend = () => {
    stopRecording();
  };

  micBtn.addEventListener("click", () => {
    if (isRecording) {
      recognition.stop();
      stopRecording();
    } else {
      try {
        recognition.start();
      } catch (err) {
        console.error("Speech recognition start failed:", err);
      }
    }
  });

  function stopRecording() {
    isRecording = false;
    micBtn.classList.remove("mic-recording");
    statusToast.classList.add("hidden");
  }
}

// ---------------------------------------------------------------------------
// 4. Query Execution, Chat Mode & Conversation History
// ---------------------------------------------------------------------------
function setupQueryHandler() {
  const input = document.getElementById("query-input");
  const runBtn = document.getElementById("run-query-btn");
  const backHomeBtn = document.getElementById("back-to-home-btn");

  // Sample chips
  document.querySelectorAll(".sample-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.getAttribute("data-query");
      if (input) input.value = q;
      submitQuery(q);
    });
  });

  if (runBtn) {
    runBtn.addEventListener("click", () => {
      if (input) submitQuery(input.value);
    });
  }

  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        submitQuery(input.value);
      }
    });
  }

  if (backHomeBtn) {
    backHomeBtn.addEventListener("click", () => {
      backToHome();
    });
  }

  window.backToHome = function() {
    switchTab("assistant");
    exitChatMode();
  };

  setupImageAttachment();
}

function setupImageAttachment() {
  const attachLabel = document.getElementById("image-attach-label");
  const attachBtn = document.getElementById("image-attach-btn");
  const fileInput = document.getElementById("image-file-input");
  const removeBtn = document.getElementById("remove-image-btn");
  const askBarContainer = document.getElementById("ask-bar-container");
  const queryInput = document.getElementById("query-input");

  if (fileInput) {
    fileInput.addEventListener("change", (e) => {
      const file = e.target.files && e.target.files[0];
      if (file) handleSelectedImage(file);
    });
  }

  if (removeBtn) {
    removeBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      clearAttachedImage();
    });
  }

  // Full-Window Drag and Drop for documents and images from Windows Explorer
  window.addEventListener("dragenter", (e) => {
    if (e.dataTransfer && e.dataTransfer.types && Array.from(e.dataTransfer.types).includes("Files")) {
      e.preventDefault();
      const overlay = document.getElementById("global-drag-overlay");
      if (overlay) {
        overlay.classList.remove("hidden");
        overlay.style.display = "flex";
      }
    }
  });

  window.addEventListener("dragover", (e) => {
    e.preventDefault();
    if (e.dataTransfer) e.dataTransfer.dropEffect = "copy";
  });

  window.addEventListener("dragleave", (e) => {
    if (e.clientX <= 0 || e.clientY <= 0 || e.clientX >= window.innerWidth || e.clientY >= window.innerHeight) {
      const overlay = document.getElementById("global-drag-overlay");
      if (overlay) {
        overlay.classList.add("hidden");
        overlay.style.display = "none";
      }
    }
  });

  window.addEventListener("drop", (e) => {
    e.preventDefault();
    const overlay = document.getElementById("global-drag-overlay");
    if (overlay) {
      overlay.classList.add("hidden");
      overlay.style.display = "none";
    }
    if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleSelectedImage(e.dataTransfer.files[0]);
    }
  });

  // Local drag and drop onto ask bar container as well
  if (askBarContainer) {
    askBarContainer.addEventListener("dragover", (e) => {
      e.preventDefault();
      askBarContainer.classList.add("ring-2", "ring-sky-500");
    });
    askBarContainer.addEventListener("dragleave", () => {
      askBarContainer.classList.remove("ring-2", "ring-sky-500");
    });
    askBarContainer.addEventListener("drop", (e) => {
      e.preventDefault();
      e.stopPropagation();
      askBarContainer.classList.remove("ring-2", "ring-sky-500");
      if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        handleSelectedImage(e.dataTransfer.files[0]);
      }
    });
  }

  // Clipboard paste support in input (image or document)
  if (queryInput) {
    queryInput.addEventListener("paste", (e) => {
      const items = (e.clipboardData || window.clipboardData).items;
      if (!items) return;
      for (let i = 0; i < items.length; i++) {
        if (items[i].kind === "file") {
          const file = items[i].getAsFile();
          if (file) handleSelectedImage(file);
          break;
        }
      }
    });
  }
}

function handleSelectedImage(file) {
  if (!file) return;
  const supported = /\.(png|jpe?g|webp|tiff?|bmp|pdf|docx|xlsx|xlsm|zip|txt|csv|md)$/i.test(file.name);
  if (!supported) {
    alert("Unsupported file format. Use an image, PDF, DOCX, XLSX, ZIP, TXT, CSV, or Markdown file.");
    return;
  }
  if (file.size > 50 * 1024 * 1024) {
    alert("Maximum file size is 50 MB.");
    return;
  }
  attachedImageName = file.name || "dokumen_skema";
  const isImage = file.type && file.type.startsWith("image/");
  const isPdf = (file.type && file.type.includes("pdf")) || attachedImageName.toLowerCase().endsWith(".pdf");

  const reader = new FileReader();
  reader.onload = (event) => {
    attachedImageData = event.target.result;
    const previewChip = document.getElementById("image-preview-chip");
    const previewThumb = document.getElementById("image-preview-thumb");
    const previewIcon = document.getElementById("image-preview-icon");
    const previewName = document.getElementById("image-preview-name");

    if (previewName) previewName.innerText = attachedImageName;

    if (isImage && previewThumb) {
      previewThumb.src = attachedImageData;
      previewThumb.classList.remove("hidden");
      if (previewIcon) previewIcon.classList.add("hidden");
    } else {
      if (previewThumb) previewThumb.classList.add("hidden");
      if (previewIcon) {
        previewIcon.classList.remove("hidden");
        previewIcon.innerText = isPdf ? "PDF" : "DOC";
      }
    }

    if (previewChip) {
      previewChip.classList.remove("hidden");
      previewChip.classList.add("flex");
    }

    // Always bring user to assistant search view if dropped from elsewhere
    switchTab("assistant");

    const input = document.getElementById("query-input");
    if (input && !input.value.trim()) input.value = `Analyze the contents of ${attachedImageName} using relevant knowledge base sources.`;
    if (input) input.focus();
    if (window.lucide) lucide.createIcons();
  };
  reader.readAsDataURL(file);
}

function clearAttachedImage() {
  attachedImageData = null;
  attachedImageName = "";
  const fileInput = document.getElementById("image-file-input");
  if (fileInput) fileInput.value = "";
  const previewChip = document.getElementById("image-preview-chip");
  if (previewChip) {
    previewChip.classList.add("hidden");
    previewChip.classList.remove("flex");
  }
}

async function setupDatasetSelector() {
  const options = document.getElementById("dataset-picker-options");
  const picker = document.getElementById("dataset-picker");
  if (!options || !picker) return;

  try {
    const response = await fetch("/api/datasets");
    if (!response.ok) throw new Error("Dataset catalog unavailable");
    availableDatasets = await response.json();
    if (!availableDatasets.some(dataset => dataset.dataset_id === selectedDatasetId)) {
      selectedDatasetId = "dataset_01";
    }

    const render = () => {
      const selected = availableDatasets.find(dataset => dataset.dataset_id === selectedDatasetId);
      const label = document.getElementById("dataset-selection-label");
      const count = document.getElementById("dataset-availability-count");
      if (label && selected) {
        label.innerText = `Dataset ${String(selected.dataset_number).padStart(2, "0")} · ${selected.equipment_tag}`;
      }
      if (count) count.innerText = `${availableDatasets.length} available`;
      options.innerHTML = availableDatasets.map(dataset => {
        const isSelected = dataset.dataset_id === selectedDatasetId;
        return `
          <button type="button" data-dataset-id="${escapeHtml(dataset.dataset_id)}" aria-pressed="${isSelected}" class="w-full text-left rounded-lg border ${isSelected ? "pro-btn-primary" : "dcs-card app-border"} px-3 py-2.5 flex items-center gap-3 transition">
            <span class="w-7 h-7 rounded-full border app-border flex items-center justify-center text-[10px] font-mono shrink-0">${String(dataset.dataset_number).padStart(2, "0")}</span>
            <span class="min-w-0 flex-1">
              <span class="block text-xs font-semibold truncate">${escapeHtml(dataset.dataset_name)}</span>
              <span class="block text-[10px] app-text-muted truncate">${escapeHtml(dataset.equipment_tag)} · ${escapeHtml(dataset.description)}</span>
            </span>
            <span class="text-[9px] font-mono shrink-0">${isSelected ? "SELECTED" : `${dataset.document_count} SOURCES`}</span>
          </button>
        `;
      }).join("");
      if (window.lucide) lucide.createIcons();
    };

    options.addEventListener("click", event => {
      const button = event.target.closest("[data-dataset-id]");
      if (!button) return;
      selectedDatasetId = button.dataset.datasetId;
      localStorage.setItem("ca-dataset-id", selectedDatasetId);
      render();
      picker.open = false;
      loadAssetSuggestions();
    });
    render();
    loadAssetSuggestions();
  } catch (error) {
    const count = document.getElementById("dataset-availability-count");
    if (count) count.innerText = "Unavailable";
    console.error("Failed to load dataset catalog:", error);
  }
}

function setupPidValidator() {
  const openBtn = document.getElementById("open-pid-validator-btn");
  const closeBtn = document.getElementById("close-pid-validator-btn");
  const modal = document.getElementById("pid-validator-modal");
  const loadDraftBtn = document.getElementById("load-sample-pid-btn");
  const runAuditBtn = document.getElementById("run-pid-audit-btn");

  if (openBtn) openBtn.addEventListener("click", openPidValidatorModal);
  if (closeBtn) closeBtn.addEventListener("click", closePidValidatorModal);

  window.openPidValidatorModal = function() {
    if (modal) modal.classList.remove("hidden");
    if (window.lucide) lucide.createIcons();
  };

  window.closePidValidatorModal = function() {
    if (modal) modal.classList.add("hidden");
  };

  if (loadDraftBtn) {
    loadDraftBtn.addEventListener("click", () => {
      document.getElementById("pid-drawing-title").value = "P&ID Schematic Draft (Feed Pump GA-1201A/B)";
      document.getElementById("pid-drawing-author").value = "Junior Process Engineer (Draft Rev 0.1)";
      const resultsDiv = document.getElementById("pid-audit-results");
      resultsDiv.innerHTML = `
        <div class="p-4 dcs-card rounded-xl border app-border space-y-2">
          <div class="flex items-center gap-2 font-bold app-text-primary text-xs">
            <i data-lucide="check-circle" class="w-4 h-4"></i> Junior Engineer Draft Loaded
          </div>
          <p class="text-xs app-text-secondary leading-relaxed">
            This schematic draft shows a 30 kW centrifugal pump without an FV-1201 minimum-flow bypass, uses a single 1oo1 suction pressure switch, and does not include an API Plan 11 seal flush.
          </p>
          <div class="text-[11px] app-text-secondary font-semibold font-mono">
            Click the "Audit P&amp;ID" button above to compare it against the Senior PE Golden Master.
          </div>
        </div>
      `;
      if (window.lucide) lucide.createIcons();
    });
  }

  if (runAuditBtn) {
    runAuditBtn.addEventListener("click", async () => {
      const resultsDiv = document.getElementById("pid-audit-results");
      resultsDiv.innerHTML = `
        <div class="p-8 text-center text-xs app-text-muted space-y-3">
          <span class="inline-block animate-spin text-2xl font-mono">⚙</span>
          <p class="font-mono">Running a deterministic rule audit against TJC-LLD-PID-1201 Rev 2.0 &amp; SEQ-1201 Rev 3.0...</p>
        </div>
      `;

      try {
        const title = document.getElementById("pid-drawing-title").value;
        const author = document.getElementById("pid-drawing-author").value;

        const res = await fetch("/api/validate-pid", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ drawing_title: title, drawing_author: author })
        });
        const data = await res.json();
        renderPidAuditReport(resultsDiv, data);
      } catch (err) {
        console.error("PID audit error:", err);
        resultsDiv.innerHTML = `<div class="p-4 app-text-primary text-xs dcs-panel border app-border">P&amp;ID audit failed. Make sure the backend is running.</div>`;
      }
    });
  }
}

function renderPidAuditReport(container, data) {
  const isFailed = data.status.includes("FAILED");
  const statusColor = isFailed ? "pro-badge border-2" : "pro-badge";

  let tableRows = data.discrepancies.map((d) => {
    let sevBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold pro-badge font-mono">${d.severity}</span>`;

    return `
      <tr class="hover:bg-slate-500/10 transition border-b app-border text-[11px]">
        <td class="p-3 font-mono font-bold app-text-primary align-top">${d.tag} <br/><span class="text-[10px] app-text-muted font-mono font-normal">${d.item}</span></td>
        <td class="p-3 align-top">${sevBadge}</td>
        <td class="p-3 app-text-primary align-top font-mono font-medium">${d.draft_finding}</td>
        <td class="p-3 app-text-primary align-top font-mono font-medium">${d.golden_standard}</td>
        <td class="p-3 app-text-secondary align-top">
          <div class="font-semibold mb-1 app-text-primary">Hazard: ${d.hazard_impact}</div>
          <div class="font-bold app-text-primary">Required Replacement/Addition: ${d.required_correction}</div>
        </td>
      </tr>
    `;
  }).join("");

  container.innerHTML = `
    <div class="space-y-4">
      <!-- Status Card -->
      <div class="dcs-card p-4 rounded-xl border ${statusColor} flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        <div>
          <div class="font-bold text-xs uppercase tracking-wider font-mono flex items-center gap-1.5">
            <i data-lucide="shield-alert" class="w-4 h-4"></i> ${data.status}
          </div>
          <div class="text-xs app-text-primary font-semibold mt-0.5">
            ${data.discrepancy_count} design discrepancies found against Senior Process Engineer standards.
          </div>
          <div class="text-[10px] app-text-muted">Referensi Golden Master: ${data.golden_master_ref}</div>
        </div>
        <div class="text-right">
          <div class="text-2xl font-black font-mono app-text-primary">${data.compliance_score}%</div>
          <div class="text-[10px] app-text-muted">Safety Compliance Score</div>
        </div>
      </div>

      <!-- Commentary -->
      <div class="p-3.5 dcs-panel rounded-xl border app-border text-xs leading-relaxed app-text-secondary">
        <strong class="text-sky-400">Rekomendasi Senior PE:</strong> ${data.summary_commentary}
      </div>

      <!-- Discrepancy Comparison Table -->
      <div class="overflow-x-auto rounded-xl border app-border">
        <table class="w-full text-left">
          <thead class="app-subtle-bg app-text-muted uppercase tracking-wider text-[10px] border-b app-border font-mono">
            <tr>
              <th class="p-3">Komponen / Tag</th>
              <th class="p-3">Severity</th>
              <th class="p-3">Skema Engineer Junior</th>
              <th class="p-3">Standar Senior PE (Master)</th>
              <th class="p-3">Dampak Bahaya & Solusi Perbaikan</th>
            </tr>
          </thead>
          <tbody class="divide-y app-border">
            ${tableRows}
          </tbody>
        </table>
      </div>
    </div>
  `;

  if (window.lucide) lucide.createIcons();
}

window.openKeywordGuideModal = function() {
  const modal = document.getElementById("keyword-guide-modal");
  if (modal) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    modal.style.setProperty("display", "flex", "important");
  }
  if (window.lucide) lucide.createIcons();
};

window.closeKeywordGuideModal = function() {
  const modal = document.getElementById("keyword-guide-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    modal.style.setProperty("display", "none", "important");
  }
};

window.askFromGuide = function(question) {
  if (!question) return;
  window.closeKeywordGuideModal();
  switchTab("assistant"); // Switch to assistant / query view
  const input = document.getElementById("query-input");
  if (input) {
    input.value = question;
    input.dispatchEvent(new Event("input", { bubbles: true }));
  }
  submitQuery(question);
};

function setupKeywordGuide() {
  const openBtn = document.getElementById("open-guide-btn");
  const closeBtn = document.getElementById("close-guide-modal-btn");
  const modal = document.getElementById("keyword-guide-modal");

  if (openBtn) {
    openBtn.onclick = () => window.openKeywordGuideModal();
  }

  if (closeBtn) {
    closeBtn.onclick = () => window.closeKeywordGuideModal();
  }

  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        window.closeKeywordGuideModal();
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      window.closeKeywordGuideModal();
    }
  });

  document.querySelectorAll(".guide-ask-btn").forEach(btn => {
    btn.onclick = (e) => {
      e.stopPropagation();
      const q = btn.getAttribute("data-ask");
      window.askFromGuide(q);
    };
  });
}

// ---------------------------------------------------------------------------
// 4B. Dedicated Multimodal Document & P&ID Upload Feature
// ---------------------------------------------------------------------------
let pendingModalFileData = null;
let pendingModalFileName = "";
let pendingModalFileType = "";

window.openUploadModal = function() {
  const modal = document.getElementById("upload-dialog-modal");
  if (modal) {
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    modal.style.display = "flex";
  }
  if (window.lucide) lucide.createIcons();
};

window.closeUploadModal = function() {
  const modal = document.getElementById("upload-dialog-modal");
  if (modal) {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    modal.style.display = "none";
  }
};

window.clearModalFile = function() {
  pendingModalFileData = null;
  pendingModalFileName = "";
  pendingModalFileType = "";
  const box = document.getElementById("modal-selected-file-box");
  if (box) {
    box.classList.add("hidden");
    box.classList.remove("flex");
  }
  const input = document.getElementById("modal-file-upload-input");
  if (input) input.value = "";
};

window.loadSampleFileToModal = function(type) {
  const box = document.getElementById("modal-selected-file-box");
  const nameEl = document.getElementById("modal-file-name");
  const iconEl = document.getElementById("modal-file-icon");
  const queryEl = document.getElementById("modal-upload-query");

  if (type === "pid") {
    pendingModalFileName = "TJC-LLD-PID-1201_Draft_Junior_Rev0.1.png";
    pendingModalFileType = "image/png";
    pendingModalFileData = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==";
    if (nameEl) nameEl.innerText = pendingModalFileName;
    if (iconEl) iconEl.innerText = "PNG";
    if (queryEl) queryEl.value = "Compare and verify this P&ID schematic draft against Golden Master TJC-LLD-PID-1201 Rev 2.0 and SEQ-1201.";
  } else if (type === "seal") {
    pendingModalFileName = "OPL-01_Mechanical_Seal_Flush_Inspection.jpg";
    pendingModalFileType = "image/jpeg";
    pendingModalFileData = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==";
    if (nameEl) nameEl.innerText = pendingModalFileName;
    if (iconEl) iconEl.innerText = "JPG";
    if (queryEl) queryEl.value = "Analyze the Plan 11/62 mechanical seal inspection photo and hexane leak prevention according to OPL-01.";
  } else if (type === "datasheet") {
    pendingModalFileName = "TJC-LLD-DS-GA-1201A_Datasheet_Pompa.pdf";
    pendingModalFileType = "application/pdf";
    pendingModalFileData = "data:application/pdf;base64,JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmoKPDwvTGVuZ3RoIDM2L0ZpbHRlci9GbGF0ZURlY29kZT4+c3RyZWFtCnicM1QwUIhQMlQI0LMw0LPQM1IwNNczgXBAyAglAK1TBpUKZW5kc3RyZWFtCmVuZG9iag==";
    if (nameEl) nameEl.innerText = pendingModalFileName;
    if (iconEl) iconEl.innerText = "PDF";
    if (queryEl) queryEl.value = "Verify the 18 m3/h flow and NPSHa versus NPSHr hydraulic parameters for pump GA-1201A against the datasheet.";
  }

  if (box) {
    box.classList.remove("hidden");
    box.classList.add("flex");
  }
  if (window.lucide) lucide.createIcons();
};

window.submitModalUpload = function() {
  const queryInput = document.getElementById("modal-upload-query");
  const q = (queryInput && queryInput.value.trim()) ? queryInput.value.trim() : "Compare and verify this file against the Train A P&ID Golden Master standards.";

  if (pendingModalFileData) {
    attachedImageData = pendingModalFileData;
    attachedImageName = pendingModalFileName;

    const previewChip = document.getElementById("image-preview-chip");
    const previewThumb = document.getElementById("image-preview-thumb");
    const previewIcon = document.getElementById("image-preview-icon");
    const previewName = document.getElementById("image-preview-name");

    if (previewName) previewName.innerText = attachedImageName;

    const isImage = pendingModalFileType.startsWith("image/");
    if (isImage && previewThumb) {
      previewThumb.src = attachedImageData;
      previewThumb.classList.remove("hidden");
      if (previewIcon) previewIcon.classList.add("hidden");
    } else {
      if (previewThumb) previewThumb.classList.add("hidden");
      if (previewIcon) {
        previewIcon.classList.remove("hidden");
        previewIcon.innerText = pendingModalFileType.includes("pdf") ? "PDF" : "DOC";
      }
    }

    if (previewChip) {
      previewChip.classList.remove("hidden");
      previewChip.classList.add("flex");
    }
  }

  window.closeUploadModal();
  switchTab("assistant");

  const mainInput = document.getElementById("query-input");
  if (mainInput) mainInput.value = q;
  submitQuery(q);
};

function setupUploadModal() {
  const fileInput = document.getElementById("modal-file-upload-input");
  if (fileInput) {
    fileInput.addEventListener("change", (e) => {
      const file = e.target.files && e.target.files[0];
      if (!file) return;
      pendingModalFileName = file.name;
      pendingModalFileType = file.type || "application/octet-stream";

      const reader = new FileReader();
      reader.onload = (ev) => {
        pendingModalFileData = ev.target.result;
        const box = document.getElementById("modal-selected-file-box");
        const nameEl = document.getElementById("modal-file-name");
        const iconEl = document.getElementById("modal-file-icon");

        if (nameEl) nameEl.innerText = file.name;
        if (iconEl) {
          iconEl.innerText = file.type.startsWith("image/") ? "IMG" : (file.name.toLowerCase().endsWith(".pdf") ? "PDF" : "DOC");
        }
        if (box) {
          box.classList.remove("hidden");
          box.classList.add("flex");
        }
        if (window.lucide) lucide.createIcons();
      };
      reader.readAsDataURL(file);
    });
  }

  const uploadModal = document.getElementById("upload-dialog-modal");
  if (uploadModal) {
    uploadModal.addEventListener("click", (e) => {
      if (e.target === uploadModal) {
        window.closeUploadModal();
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      window.closeUploadModal();
    }
  });
}

function enterChatMode() {
  if (isChatMode) return;
  isChatMode = true;

  const heroWrapper = document.getElementById("hero-wrapper");
  const resultsFeed = document.getElementById("results-feed");
  const stickyBottomBar = document.getElementById("sticky-bottom-bar");
  const askBar = document.getElementById("ask-bar-container");
  const stickyMount = document.getElementById("sticky-bar-mount");
  const backHomeBtn = document.getElementById("back-to-home-btn");
  const modeDropdown = document.getElementById("mode-dropdown");

  // Hide hero landing elements
  if (heroWrapper) heroWrapper.classList.add("hidden");

  // Move search bar to bottom sticky container
  if (stickyMount && askBar) {
    stickyMount.appendChild(askBar);
  }
  if (stickyBottomBar) stickyBottomBar.classList.remove("hidden");

  // Adjust dropdown positioning when docked at bottom: open UPWARDS!
  if (modeDropdown) {
    modeDropdown.classList.remove("top-11");
    modeDropdown.classList.add("bottom-full", "mb-3");
  }

  // Show conversation feed & Back button
  if (resultsFeed) resultsFeed.classList.remove("hidden");
  if (backHomeBtn) {
    backHomeBtn.classList.remove("hidden");
    backHomeBtn.classList.add("flex");
  }

  if (window.lucide) lucide.createIcons();
}

function exitChatMode() {
  if (!isChatMode) return;
  isChatMode = false;

  const heroWrapper = document.getElementById("hero-wrapper");
  const resultsFeed = document.getElementById("results-feed");
  const stickyBottomBar = document.getElementById("sticky-bottom-bar");
  const askBar = document.getElementById("ask-bar-container");
  const backHomeBtn = document.getElementById("back-to-home-btn");
  const modeDropdown = document.getElementById("mode-dropdown");
  const input = document.getElementById("query-input");

  // Clear feed history
  if (resultsFeed) {
    resultsFeed.innerHTML = "";
    resultsFeed.classList.add("hidden");
  }

  // Move search bar back to hero center
  if (heroWrapper && askBar) {
    heroWrapper.insertBefore(askBar, document.getElementById("hero-menu-chips"));
  }
  if (stickyBottomBar) stickyBottomBar.classList.add("hidden");

  // Adjust dropdown positioning when in hero: open DOWNWARDS!
  if (modeDropdown) {
    modeDropdown.classList.remove("bottom-full", "mb-3");
    modeDropdown.classList.add("top-11");
  }

  // Restore hero layout
  if (heroWrapper) heroWrapper.classList.remove("hidden");
  if (backHomeBtn) {
    backHomeBtn.classList.add("hidden");
    backHomeBtn.classList.remove("flex");
  }

  if (input) {
    input.value = "";
    input.focus();
  }
  if (window.lucide) lucide.createIcons();
}

async function submitQuery(queryText) {
  const currentAttachedImage = attachedImageData;
  const currentAttachedImageName = attachedImageName;
  const cleanQuery = (queryText || "").trim() || (currentAttachedImage
    ? `Extract and analyze ${currentAttachedImageName} using relevant knowledge base sources.`
    : "");
  if (!cleanQuery) return;
  const input = document.getElementById("query-input");
  if (input) input.value = "";

  clearAttachedImage();

  // Trigger chat mode layout on first query
  enterChatMode();

  // Keep focus on input for fast follow-up typing
  if (input) setTimeout(() => input.focus(), 60);

  const resultsFeed = document.getElementById("results-feed");
  if (!resultsFeed) return;

  // 1. Create Turn Container & Append User Question Bubble
  const turnId = "turn-" + Date.now();
  const turnDiv = document.createElement("div");
  turnDiv.id = turnId;
  turnDiv.className = "w-full max-w-5xl mx-auto space-y-4";

  const isAttachedImage = /\.(png|jpe?g|webp|tiff?|bmp)$/i.test(currentAttachedImageName);
  const attachmentHtml = currentAttachedImage ? `
    <div class="mt-2.5 p-1.5 rounded-xl bg-slate-900/60 border border-white/20 overflow-hidden inline-block text-left">
      <div class="text-[10px] text-sky-300 font-mono flex items-center gap-1.5 px-2 py-0.5 mb-1">
        <i data-lucide="${isAttachedImage ? "image" : "file-text"}" class="w-3.5 h-3.5"></i> <span>${escapeHtml(currentAttachedImageName)}</span>
      </div>
      ${isAttachedImage ? `<img src="${currentAttachedImage}" alt="Uploaded drawing" class="max-w-xs md:max-w-sm max-h-60 rounded-lg object-contain border border-white/10" />` : ""}
    </div>
  ` : '';

  turnDiv.innerHTML = `
    <!-- User Bubble -->
    <div class="flex items-start justify-end gap-3">
      <div class="bg-sky-600 text-white px-4 py-3 rounded-2xl rounded-tr-sm max-w-xl text-sm shadow-sm font-medium">
        <div>${escapeHtml(cleanQuery)}</div>
        <div class="mt-1 text-[10px] opacity-80 font-mono">Dataset ${String(availableDatasets.find(dataset => dataset.dataset_id === selectedDatasetId)?.dataset_number || 1).padStart(2, "0")} · General</div>
        ${attachmentHtml}
      </div>
      <div class="w-8 h-8 rounded-full bg-sky-100 text-sky-800 font-bold text-xs flex items-center justify-center border border-sky-200 flex-shrink-0 shadow-sm">
        ${currentUser.initials}
      </div>
    </div>

    <!-- Assistant Skeleton Loading State -->
    <div class="assistant-response-container flex items-start gap-3">
      <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-sky-600 to-blue-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 shadow-sm">
        CA
      </div>
      <div class="flex-1 dcs-panel ai-thinking-panel is-thinking p-6 space-y-3 border app-border shadow-sm">
        <div class="flex items-center gap-2 text-xs app-text-muted font-mono">
          <span class="inline-block animate-spin">⚙</span>
          <span>Extracting the attachment, retrieving relevant documents, and preparing an answer with citations...</span>
        </div>
        <div class="space-y-2">
          <div class="h-4 skeleton-shimmer w-3/4"></div>
          <div class="h-4 skeleton-shimmer w-full"></div>
          <div class="h-4 skeleton-shimmer w-5/6"></div>
        </div>
      </div>
    </div>
  `;

  resultsFeed.appendChild(turnDiv);
  resultsFeed.scrollTo({ top: resultsFeed.scrollHeight, behavior: "smooth" });
  if (window.lucide) lucide.createIcons();

  // 2. Fetch API Data
  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: cleanQuery,
        image_data: currentAttachedImage,
        image_name: currentAttachedImageName,
        dataset_id: selectedDatasetId,
      })
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${data.detail || "Request failed"}`);

    // 3. Render Assistant Response into this specific turn
    const responseContainer = turnDiv.querySelector(".assistant-response-container");
    renderAssistantTurn(responseContainer, data);
    resultsFeed.scrollTo({ top: resultsFeed.scrollHeight, behavior: "smooth" });

    if (window.lucide) lucide.createIcons();
  } catch (err) {
    console.error("Query API error:", err);
    const responseContainer = turnDiv.querySelector(".assistant-response-container");
    const errorMessage = err instanceof TypeError
      ? "Could not connect to the backend. Make sure the Knowledge Hub server is running."
      : err.message;
    responseContainer.innerHTML = `
      <div class="w-8 h-8 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0">!</div>
      <div class="dcs-panel p-4 text-red-500 text-xs flex-1 border border-red-500/30">
        ${escapeHtml(errorMessage)}
      </div>
    `;
  }
}

function renderAssistantTurn(container, data) {
  // If Guardrail blocked
  if (data.status === "REJECTED_BY_GUARDRAIL") {
    container.innerHTML = `
      <div class="w-8 h-8 rounded-full bg-red-600 text-white font-bold text-xs flex items-center justify-center flex-shrink-0 shadow-sm">
        !
      </div>
      <div class="flex-1 dcs-panel p-6 border-red-500/30 bg-red-500/10 space-y-3 shadow-sm">
        <div class="flex items-center justify-between pb-2 border-b border-red-500/20">
          <div class="flex items-center gap-2 text-red-500 font-bold text-xs">
            <span class="w-2.5 h-2.5 rounded-full bg-red-600 inline-block"></span>
            ${data.answer.summary}
          </div>
          <span class="px-2.5 py-0.5 rounded-full bg-red-500/15 text-red-500 font-mono text-[10px] font-bold border border-red-500/25">GUARDRAIL BLOCKED (0%)</span>
        </div>
        <p class="text-xs text-red-400 leading-relaxed">${data.answer.explanation}</p>
        <div class="text-[11px] font-bold app-text-primary pt-2 border-t app-border">In-Domain Chemical Plant Topics:</div>
        <ul class="list-disc pl-5 text-xs app-text-muted space-y-1">
          ${data.answer.suggested_topics.map(t => `<li class="cursor-pointer hover:underline transition" onclick="document.getElementById('query-input').value='${t}'; submitQuery('${t}');">${t}</li>`).join("")}
        </ul>
      </div>
    `;
    return;
  }

  // Formatting strings
  let summaryHtml = data.answer.summary;
  if (window.marked) {
    summaryHtml = marked.parse(summaryHtml);
  } else {
    summaryHtml = summaryHtml.replace(/\*\*(.*?)\*\*/g, '<strong class="app-text-primary font-bold">$1</strong>').replace(/\n/g, '<br/>');
  }
  const tacticalHtml = data.answer.tactical_action
    .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold">$1</strong>')
    .replace(/\n/g, '<br/>');

  const tb = data.trust_badge;
  const scores = data.fusion_breakdown.source_scores;
  const topSrc = data.sources && data.sources.length > 0 ? data.sources[0] : null;

  // Build downstream chain HTML
  let chainHtml = `<span class="px-2 py-0.5 pro-badge rounded font-mono font-semibold">${escapeHtml(data.primary_entity || "Plant Knowledge Base")}</span>`;
  if (data.downstream_impacts && data.downstream_impacts.length > 0) {
    data.downstream_impacts.forEach(ds => {
      chainHtml += `<span class="app-text-muted">&rarr;</span><span class="px-2 py-0.5 dcs-card border app-border app-text-secondary rounded font-mono">${ds.impacted_asset} (${ds.asset_type})</span>`;
    });
  }

  // Multimodal Image Analysis Card (if image was uploaded/compared)
  let imageAuditHtml = "";
  if (data.image_analysis) {
    const ia = data.image_analysis;
    const statusBadge = `<span class="px-2.5 py-1 rounded-full text-xs font-bold pro-badge border app-border font-mono">${escapeHtml(ia.verdict)}</span>`;

    const discRows = ia.discrepancies.map(d => {
      const sevBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold pro-badge font-mono">${d.severity}</span>`;

      return `
        <tr class="hover:bg-slate-500/10 transition border-b app-border text-[11px]">
          <td class="p-3 font-mono font-bold app-text-primary align-top">${escapeHtml(d.tag)} <br/><span class="text-[10px] app-text-muted font-normal">${escapeHtml(d.item)}</span></td>
          <td class="p-3 align-top">${sevBadge}</td>
          <td class="p-3 app-text-primary align-top font-mono font-medium">${escapeHtml(d.draft_finding)}</td>
          <td class="p-3 app-text-primary align-top font-mono font-medium">${escapeHtml(d.golden_standard)}</td>
          <td class="p-3 app-text-secondary align-top">${d.location?.length ? d.location.map(position => `Page ${escapeHtml(position.page ?? "?")} · ${escapeHtml(JSON.stringify(position.bbox || []))}`).join("<br/>") : "Not located by OCR; inspect the full drawing."}</td>
          <td class="p-3 app-text-secondary align-top">
            <div class="font-semibold mb-1 app-text-primary">Catatan: ${escapeHtml(d.hazard_impact)}</div>
            <div class="font-bold app-text-primary">Tindak lanjut: ${escapeHtml(d.required_correction)}</div>
          </td>
        </tr>
      `;
    }).join("");

    const matchedHtml = (ia.matched_tags || []).map(tag =>
      `<span class="px-2.5 py-1 rounded-lg pro-badge text-[11px] font-mono flex items-center gap-1.5"><i data-lucide="check" class="w-3.5 h-3.5"></i> ${escapeHtml(tag)}</span>`
    ).join("");
    const locationEntries = Object.entries(ia.tag_locations || {}).slice(0, 100);
    const locationRows = locationEntries.map(([tag, positions]) => `
      <tr class="border-b app-border text-[11px]">
        <td class="p-2.5 font-mono font-semibold">${escapeHtml(tag)}</td>
        <td class="p-2.5 font-mono">${positions.map(position => {
          const box = Array.isArray(position.bbox) ? JSON.stringify(position.bbox) : "box unavailable";
          const page = position.page ? `Page ${position.page}` : "Page unknown";
          const confidence = Number.isFinite(position.confidence) ? ` · ${Math.round(position.confidence * 100)}%` : "";
          return `${escapeHtml(page)} · ${escapeHtml(box)}${confidence}`;
        }).join("<br/>")}</td>
      </tr>
    `).join("");
    const masterRefsHtml = (ia.master_sources || []).map(source =>
      `<span class="px-2 py-1 rounded-lg dcs-card border app-border text-[10px] font-mono">${escapeHtml(source.doc_id)} · ${escapeHtml(source.approval_status)}</span>`
    ).join("");

    imageAuditHtml = `
      <!-- Multimodal P&ID & Drawing Audit Card -->
      <div class="dcs-panel p-5 rounded-2xl border app-border space-y-4 shadow-md">
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3 pb-3 border-b app-border">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 rounded-lg pro-badge flex items-center justify-center font-bold">
                <i data-lucide="scan-line" class="w-4 h-4"></i>
              </div>
              <h4 class="text-sm font-bold app-text-primary">OCR tag comparison</h4>
              <span class="text-[10px] px-2 py-0.5 rounded pro-badge font-mono font-semibold">${escapeHtml(ia.source_name || "Uploaded file")}</span>
            </div>
            <p class="text-xs app-text-muted">Aset: <strong class="app-text-primary font-mono">${escapeHtml(ia.detected_equipment || "not resolved")}</strong></p>
          </div>
          <div class="flex items-center gap-3">
            <div class="text-right">
              <div class="text-2xl font-black font-mono app-text-primary">${(ia.matched_tags || []).length}</div>
              <div class="text-[10px] app-text-muted">Matched tags</div>
            </div>
            ${statusBadge}
          </div>
        </div>

        <!-- Matched Components Detected -->
        <div class="space-y-1.5">
          <div class="text-[11px] font-bold app-text-muted uppercase tracking-wider font-mono">OCR tags matched in master:</div>
          <div class="flex flex-wrap gap-1.5">
            ${matchedHtml || '<span class="text-xs app-text-muted">No matching tags detected.</span>'}
          </div>
        </div>

        <details class="dcs-card rounded-xl border app-border">
          <summary class="p-3 text-[11px] font-bold app-text-primary cursor-pointer">Detected tag positions (${locationEntries.length}) · page and pixel bounding boxes</summary>
          <div class="max-h-64 overflow-auto border-t app-border">
            <table class="w-full text-left">
              <thead class="app-subtle-bg app-text-muted uppercase text-[10px] font-mono"><tr><th class="p-2.5">Tag</th><th class="p-2.5">OCR location</th></tr></thead>
              <tbody class="divide-y app-border">
                ${locationRows || '<tr><td class="p-3 app-text-muted" colspan="2">No OCR bounding boxes were returned.</td></tr>'}
              </tbody>
            </table>
          </div>
        </details>

        <!-- Discrepancy Matrix -->
        <div class="space-y-1.5">
          <div class="text-[11px] font-bold app-text-primary uppercase tracking-wider font-mono flex items-center gap-1.5">
            <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i>
            Master tags not detected (${(ia.discrepancies || []).length}):
          </div>
          <div class="overflow-x-auto rounded-xl border app-border">
            <table class="w-full text-left">
              <thead class="app-subtle-bg app-text-muted uppercase tracking-wider text-[10px] border-b app-border font-mono">
                <tr>
                  <th class="p-3">Item / Tag</th>
                  <th class="p-3">Severity</th>
                  <th class="p-3">OCR finding</th>
                  <th class="p-3">Retrieved master evidence</th>
                  <th class="p-3">OCR location</th>
                  <th class="p-3">Review note</th>
                </tr>
              </thead>
              <tbody class="divide-y app-border">
                ${discRows || '<tr><td class="p-3 app-text-muted" colspan="6">No missing master tags detected by OCR. This is not a full connectivity or safety-logic validation.</td></tr>'}
              </tbody>
            </table>
          </div>
        </div>

        <!-- Senior PE Summary Box -->
        <div class="p-3.5 rounded-xl dcs-card border app-border text-xs app-text-secondary leading-relaxed font-sans">
          <strong class="app-text-primary font-mono">${escapeHtml(ia.message || "Comparison summary")}</strong>
          <div class="mt-2">Scope: ${escapeHtml(ia.comparison_scope || "OCR tag presence only; manual drawing review is still required.")}</div>
          <div class="mt-2 flex flex-wrap gap-1.5">Retrieved master sources: ${masterRefsHtml || "No matching master sources."}</div>
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="w-8 h-8 rounded-full pro-btn-primary text-xs font-bold font-mono flex items-center justify-center flex-shrink-0 shadow-sm">
      CA
    </div>
    <div class="flex-1 space-y-4">
      
      <!-- Prepend Image Audit Card if available -->
      ${imageAuditHtml}

      <!-- Main Synthesized Guidance Card -->
      <div class="dcs-panel p-6 space-y-4 border app-border shadow-sm">
        
        <!-- Header & Trust Badge -->
        <div class="flex items-center justify-between pb-3 border-b app-border">
          <div>
            <h4 class="text-sm font-bold app-text-primary flex items-center gap-2">
              <i data-lucide="check-circle" class="w-4 h-4"></i> Synthesized Technical Assessment
            </h4>
            <p class="text-[11px] app-text-muted font-mono">Entity: ${data.primary_entity} &bull; Polyethylene Train A</p>
          </div>
          <div class="px-3 py-1 rounded-full text-xs font-bold font-mono flex items-center gap-1.5 pro-badge">
            <span class="w-2 h-2 rounded-full inline-block bg-current opacity-80"></span>
            <span>${tb.ui_label} (${tb.confidence_percentage}%)</span>
          </div>
        </div>

        <!-- Synthesis Body -->
        <div class="text-xs md:text-sm app-text-secondary leading-relaxed space-y-2 prose prose-invert prose-sm max-w-none">
          ${summaryHtml}
        </div>

        <!-- Tactical Action Box -->
        <div class="p-3.5 rounded-xl tactical-box space-y-1.5">
          <div class="text-[11px] font-bold uppercase tracking-wider flex items-center gap-1.5 font-mono">
            <i data-lucide="alert-triangle" class="w-3.5 h-3.5"></i> Tactical Action Mandate
          </div>
          <div class="text-xs leading-relaxed">
            ${tacticalHtml}
          </div>
        </div>

        <!-- Normalized Multi-Source Scores -->
        <div class="pt-3 border-t app-border">
          <div class="flex items-center justify-between text-[11px] app-text-muted mb-2 font-mono">
            <span>Explainable Multi-Source Normalized Fusion:</span>
            <span class="app-text-primary font-bold font-mono">Fused: ${data.fusion_breakdown.fused_score.toFixed(3)}</span>
          </div>
          <div class="grid grid-cols-3 gap-2 text-xs font-mono">
            <div class="dcs-card p-2.5 rounded-lg border app-border">
              <div class="app-text-muted text-[10px]">Graph Hop Decay</div>
              <div class="app-text-primary font-bold">${(scores.graph || 0).toFixed(3)}</div>
            </div>
            <div class="dcs-card p-2.5 rounded-lg border app-border">
              <div class="app-text-muted text-[10px]">Normalized Cosine (0-1)</div>
              <div class="app-text-primary font-bold">${(scores.semantic || 0).toFixed(3)}</div>
            </div>
            <div class="dcs-card p-2.5 rounded-lg border app-border">
              <div class="app-text-muted text-[10px]">Trip Proximity Ratio</div>
              <div class="app-text-primary font-bold">${(scores.structured || 0).toFixed(3)}</div>
            </div>
          </div>
        </div>

      </div>

      <!-- Verified Citation & XAI Highlighting Card -->
      ${topSrc ? `
      <div class="dcs-card p-4 space-y-3 shadow-sm border app-border">
        <div class="flex items-center justify-between pb-2 border-b app-border">
          <div class="flex items-center gap-2">
            <i data-lucide="file-check" class="w-4 h-4"></i>
            <span class="text-xs font-bold app-text-primary">${topSrc.doc_id} &bull; ${topSrc.title}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="doc-approved-stamp">${topSrc.approval_status}</span>
            <span class="text-[10px] px-2 py-0.5 rounded pro-badge font-mono">
              ${(topSrc.similarity_score * 100).toFixed(0)}% Match
            </span>
          </div>
        </div>

        <div class="doc-highlight text-xs leading-relaxed font-sans">
          "${topSrc.content}"
        </div>

        <div class="flex justify-between items-center text-[10px] app-text-muted pt-1 font-mono">
          <span>Authority Sign-off: <strong class="app-text-primary">${topSrc.approved_by}</strong></span>
          <div class="flex items-center gap-1 app-text-muted">${chainHtml}</div>
        </div>
      </div>
      ` : ''}

    </div>
  `;
}

// ---------------------------------------------------------------------------
// 5. Topological Knowledge Graph Visualization (Interactive SVG)
// ---------------------------------------------------------------------------
let activeGraphAsset = localStorage.getItem("ca-graph-asset") || "GA-1201A";

async function loadGraphData() {
  const svg = document.getElementById("graph-svg");
  if (!svg) return;

  try {
    const assetRes = await fetch("/api/assets");
    const assets = await assetRes.json();
    const selector = document.getElementById("graph-asset-select");
    if (selector) {
      selector.innerHTML = assets.map(asset => `<option value="${escapeHtml(asset.tag)}">${escapeHtml(asset.tag)} - ${escapeHtml(asset.name)}</option>`).join("");
      if (!assets.some(asset => asset.tag === activeGraphAsset) && assets.length) activeGraphAsset = assets[0].tag;
      selector.value = activeGraphAsset;
      selector.onchange = () => {
        activeGraphAsset = selector.value;
        localStorage.setItem("ca-graph-asset", activeGraphAsset);
        loadGraphData();
      };
    }

    const res = await fetch(`/api/graph?asset_tag=${encodeURIComponent(activeGraphAsset)}`);
    const data = await res.json();
    renderGraph(svg, data);
  } catch (err) {
    console.error("Failed to load graph:", err);
  }
}

function renderGraph(svg, data) {
  const nodes = data.nodes || [];
  const edges = data.edges || [];
  const root = nodes.find(node => node.id === data.root_asset) || nodes.find(node => node.type === "asset");
  if (!root) {
    svg.innerHTML = "";
    return;
  }

  const positions = new Map([[root.id, { x: 620, y: 320 }]]);
  const flowEdges = edges.filter(edge => edge.type === "FEEDS");
  const flowDistance = new Map([[root.id, 0]]);
  for (let pass = 0; pass < nodes.length; pass++) {
    let changed = false;
    flowEdges.forEach(edge => {
      if (flowDistance.has(edge.target) && !flowDistance.has(edge.source)) {
        flowDistance.set(edge.source, flowDistance.get(edge.target) - 1);
        changed = true;
      } else if (flowDistance.has(edge.source) && !flowDistance.has(edge.target)) {
        flowDistance.set(edge.target, flowDistance.get(edge.source) + 1);
        changed = true;
      }
    });
    if (!changed) break;
  }
  const flowGroups = new Map();
  flowDistance.forEach((distance, id) => {
    if (!flowGroups.has(distance)) flowGroups.set(distance, []);
    flowGroups.get(distance).push(id);
  });
  const minDistance = Math.min(...flowGroups.keys());
  const maxDistance = Math.max(...flowGroups.keys());
  flowGroups.forEach((ids, distance) => {
    ids.forEach((id, index) => {
      const x = minDistance === maxDistance ? 620 : 620 + distance * (420 / Math.max(Math.abs(minDistance), Math.abs(maxDistance), 1));
      const y = 320 + (index - (ids.length - 1) / 2) * 110;
      positions.set(id, { x: Math.max(130, Math.min(1110, x)), y });
    });
  });

  const parameters = nodes.filter(node => node.type === "parameter");
  parameters.forEach((node, index) => {
    positions.set(node.id, { x: 100 + index * (1040 / Math.max(1, parameters.length - 1)), y: 105 });
  });
  const documents = nodes.filter(node => node.type === "document");
  documents.forEach((node, index) => {
    positions.set(node.id, { x: 70 + index * (1100 / Math.max(1, documents.length - 1)), y: 555 });
  });
  const otherNodes = nodes.filter(node => !positions.has(node.id));
  otherNodes.forEach((node, index) => {
    positions.set(node.id, { x: 270 + index * (700 / Math.max(1, otherNodes.length - 1)), y: 455 });
  });

  let svgContent = `
    <defs>
      <marker id="graph-arrow-flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#0284c7" />
      </marker>
      <marker id="graph-arrow-reference" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8" />
      </marker>
    </defs>
    <text x="180" y="38" fill="var(--text-muted)" font-size="13" font-family="Poppins, sans-serif" text-anchor="middle">UPSTREAM</text>
    <text x="620" y="38" fill="var(--text-muted)" font-size="13" font-family="Poppins, sans-serif" text-anchor="middle">SELECTED ASSET</text>
    <text x="1010" y="38" fill="var(--text-muted)" font-size="13" font-family="Poppins, sans-serif" text-anchor="middle">DOWNSTREAM</text>
    <text x="620" y="80" fill="var(--text-muted)" font-size="12" font-family="Poppins, sans-serif" text-anchor="middle">PROCESS SIGNALS / PARAMETERS</text>
    <text x="620" y="610" fill="var(--text-muted)" font-size="12" font-family="Poppins, sans-serif" text-anchor="middle">LINKED DOCUMENTS / FAILURE MEMORY</text>
  `;

  edges.forEach(edge => {
    const start = positions.get(edge.source);
    const end = positions.get(edge.target);
    if (!start || !end) return;
    const flow = edge.type === "FEEDS";
    const color = flow ? "#0284c7" : "#94a3b8";
    const marker = flow ? "graph-arrow-flow" : "graph-arrow-reference";
    const dash = flow ? "" : "stroke-dasharray='5 5'";
    const midX = (start.x + end.x) / 2;
    const midY = (start.y + end.y) / 2;
    svgContent += `
      <g class="graph-edge" opacity="0.88">
        <line x1="${start.x}" y1="${start.y}" x2="${end.x}" y2="${end.y}" stroke="${color}" stroke-width="${flow ? 3 : 1.5}" ${dash} marker-end="url(#${marker})" />
        <text x="${midX}" y="${midY - 7}" fill="var(--text-muted)" font-size="9" font-family="Poppins, sans-serif" text-anchor="middle">${escapeHtml(edge.type)}</text>
      </g>`;
  });

  nodes.forEach(node => {
    const point = positions.get(node.id);
    const color = node.type === "asset" ? "#168f96" : node.type === "parameter" ? "#d28a18" : node.type === "incident" ? "#b84b42" : "#718096";
    const selected = node.id === root.id;
    const radius = selected ? 26 : node.type === "asset" ? 20 : 15;
    const fullLabel = node.label || node.id;
    const label = fullLabel.length > 19 ? `${fullLabel.slice(0, 16)}...` : fullLabel;
    svgContent += `
      <g class="graph-node" data-node-id="${escapeHtml(node.id)}" tabindex="0" role="button" aria-label="${escapeHtml(fullLabel)}">
        <title>${escapeHtml(node.name || fullLabel)}</title>
        <circle cx="${point.x}" cy="${point.y}" r="${radius}" fill="${color}" stroke="${selected ? '#0f766e' : 'var(--bg-surface)'}" stroke-width="${selected ? 4 : 2}" />
        <text x="${point.x}" y="${point.y + radius + 16}" fill="var(--graph-node-text)" font-family="Poppins, sans-serif" font-size="10" font-weight="700" text-anchor="middle">${escapeHtml(label)}</text>
      </g>`;
  });

  svg.innerHTML = svgContent;
  window.graphNodesData = nodes;
  window.graphEdgesData = edges;
  svg.querySelectorAll(".graph-node").forEach(group => {
    const inspect = () => window.inspectNode(group.dataset.nodeId);
    group.addEventListener("click", inspect);
    group.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") inspect();
    });
  });
}

window.inspectNode = function(nodeId) {
  const inspector = document.getElementById("graph-node-inspector");
  const nodes = window.graphNodesData || [];
  const node = nodes.find(n => n.id === nodeId);
  if (!node) return;

  inspector.classList.remove("hidden");
  document.getElementById("inspector-title").innerText = node.label || node.id;
  const badgeType = node.doc_type === "one_point_lesson" ? "ONE POINT LESSON" : (node.type || "node").toUpperCase();
  document.getElementById("inspector-badge").innerText = badgeType;
  document.getElementById("inspector-desc").innerText = node.name || "";

  let details = "";
  if (node.criticality) details += `<div>Criticality: <span class="font-bold app-text-primary font-mono">${node.criticality}</span></div>`;
  if (node.unit) details += `<div>Unit: <span class="font-bold app-text-primary font-mono">${node.unit} (Trip: ${node.trip || 'N/A'})</span></div>`;
  if (node.normal) details += `<div>Normal: <span class="font-bold app-text-primary font-mono">${node.normal} ${node.unit || ''}</span></div>`;
  if (node.alarm) details += `<div>Alarm: <span class="font-bold app-text-primary font-mono">${node.alarm} ${node.unit || ''}</span></div>`;
  if (node.version) details += `<div>Governance: <span class="font-bold app-text-primary font-mono">${node.version} (${node.approval_status})</span></div>`;
  if (node.doc_type === "one_point_lesson") details += `<div class="app-text-secondary font-medium font-sans">Standard Operating Knowledge Base (OPL)</div>`;
  if (node.root_cause) details += `<div class="app-text-secondary font-medium font-sans">RCA: ${node.root_cause}</div>`;

  document.getElementById("inspector-details").innerHTML = details;

  const relations = (window.graphEdgesData || []).filter(edge => edge.source === nodeId || edge.target === nodeId);
  const relationMarkup = relations.map(edge => {
    const outgoing = edge.source === nodeId;
    const other = outgoing ? edge.target : edge.source;
    return `<div><span class="font-mono">${outgoing ? "OUT" : "IN"}</span> <strong>${escapeHtml(edge.type)}</strong> ${outgoing ? "&rarr;" : "&larr;"} <span class="font-mono app-text-primary">${escapeHtml(other)}</span></div>`;
  }).join("");
  document.getElementById("inspector-relations").innerHTML = relationMarkup || "No linked relationships in this view.";
};

// ---------------------------------------------------------------------------
// 6. Industrial Data Ops & HITL Quarantine
// ---------------------------------------------------------------------------
function setupQuarantine() {
  document.getElementById("refresh-quarantine-btn").addEventListener("click", loadQuarantineData);
  document.getElementById("modal-cancel-btn").addEventListener("click", closeModal);
  document.getElementById("modal-approve-btn").addEventListener("click", () => submitResolution("APPROVE"));
  document.getElementById("modal-reject-btn").addEventListener("click", () => submitResolution("REJECT"));
}

async function loadQuarantineData() {
  try {
    const res = await fetch("/api/quarantine");
    const data = await res.json();

    document.getElementById("kpi-total-sources").innerText = data.metrics.total_ingested_sources;
    document.getElementById("kpi-clean-chunks").innerText = data.metrics.clean_active_chunks;
    document.getElementById("kpi-quarantined").innerText = data.metrics.quarantined_conflicts;
    document.getElementById("kpi-health-score").innerText = `${data.metrics.data_health_score}%`;

    const tbody = document.getElementById("quarantine-tbody");
    tbody.innerHTML = data.records.map(r => {
      let sevClass = "px-2 py-0.5 rounded pro-badge font-mono text-[10px]";
      let statusClass = r.status === "QUARANTINED" ? "app-text-primary font-mono font-bold" : "app-text-muted font-mono font-medium";

      let actionBtn = r.status === "QUARANTINED" ? `
        <button onclick="openModal('${r.conflict_id}')" class="px-3 py-1 pro-btn-primary rounded-lg text-[11px] font-semibold transition shadow-sm cursor-pointer">
          Review &amp; Resolve
        </button>
      ` : `<span class="app-text-muted text-[11px] font-mono font-medium">${r.status}</span>`;

      return `
        <tr class="hover:bg-slate-500/10 transition">
          <td class="p-3 font-mono font-bold app-text-primary">${r.conflict_id}</td>
          <td class="p-3 font-semibold app-text-primary">${r.source_system} <br/><span class="text-[10px] app-text-muted font-mono">${r.document_ref}</span></td>
          <td class="p-3 app-text-secondary">${r.conflict_type}</td>
          <td class="p-3"><span class="${sevClass}">${r.severity}</span></td>
          <td class="p-3 max-w-xs app-text-muted truncate" title="${r.issue_description}">${r.issue_description}</td>
          <td class="p-3 ${statusClass}">${r.status}</td>
          <td class="p-3 text-right">${actionBtn}</td>
        </tr>
      `;
    }).join("");

    window.quarantineRecords = data.records;
  } catch (err) {
    console.error("Failed to load quarantine data:", err);
  }
}

window.openModal = function(conflictId) {
  selectedConflictId = conflictId;
  const records = window.quarantineRecords || [];
  const rec = records.find(r => r.conflict_id === conflictId);
  if (!rec) return;

  document.getElementById("sme-modal").classList.remove("hidden");
  document.getElementById("modal-title").innerText = `SME Review: ${rec.conflict_id} (${rec.conflict_type})`;
  document.getElementById("modal-desc").innerText = rec.issue_description;
};

window.closeModal = function() {
  document.getElementById("sme-modal").classList.add("hidden");
  selectedConflictId = null;
};

async function submitResolution(action) {
  if (!selectedConflictId) return;

  const smeName = document.getElementById("modal-sme-name").value;
  const notes = document.getElementById("modal-notes").value;

  try {
    await fetch("/api/quarantine/resolve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        conflict_id: selectedConflictId,
        action: action,
        sme_name: smeName,
        notes: notes
      })
    });
    closeModal();
    loadQuarantineData();
  } catch (err) {
    console.error("Failed to resolve quarantine record:", err);
  }
}

// ---------------------------------------------------------------------------
// 7. Live Telemetry & Event-Driven Proactive Push (Oscilloscope Strip-Chart)
// ---------------------------------------------------------------------------
const SENSORS = {
  "PT-1201": {
    name: "Suction Sensor PT-1201",
    desc: "Inlet Header to Hexane Feed Pump GA-1201A",
    paramLabel: "Live Suction Pressure",
    unit: "barg",
    normalVal: 1.20,
    normalText: "1.20 barg",
    warnText: "< 0.80 barg",
    tripText: "< 0.50 barg",
    legendWarn: "— Alarm (<0.8)",
    legendTrip: "— Trip (<0.5)",
    defaultVal: 1.18,
    minY: 0.0,
    maxY: 1.60,
    warnThresh: 0.80,
    tripThresh: 0.50,
    warnIsLower: true,
    canSimulate: true
  },
  "PDT-1201": {
    name: "Diff Pressure Sensor PDT-1201",
    desc: "Suction Strainer Y-1201 Choke Indicator",
    paramLabel: "Strainer Differential Pressure",
    unit: "bar",
    normalVal: 0.15,
    normalText: "0.15 bar",
    warnText: "> 0.45 bar",
    tripText: "> 0.60 bar",
    legendWarn: "— Alarm (>0.45)",
    legendTrip: "— Trip (>0.60)",
    defaultVal: 0.18,
    minY: 0.0,
    maxY: 1.0,
    warnThresh: 0.45,
    tripThresh: 0.60,
    warnIsLower: false,
    canSimulate: false
  },
  "TT-1201": {
    name: "Bearing Temp Sensor TT-1201",
    desc: "GA-1201A Drive-End (DE) Bearing Thermocouple",
    paramLabel: "DE Bearing Temperature",
    unit: "°C",
    normalVal: 55.0,
    normalText: "55.0 °C",
    warnText: "> 75.0 °C",
    tripText: "> 85.0 °C",
    legendWarn: "— Alarm (>75)",
    legendTrip: "— Trip (>85)",
    defaultVal: 54.8,
    minY: 20.0,
    maxY: 100.0,
    warnThresh: 75.0,
    tripThresh: 85.0,
    warnIsLower: false,
    canSimulate: false
  },
  "VT-1201": {
    name: "Vibration Sensor VT-1201",
    desc: "GA-1201A Radial Bearing Vibration (ISO 10816)",
    paramLabel: "Overall Vibration Velocity",
    unit: "mm/s",
    normalVal: 2.10,
    normalText: "2.10 mm/s",
    warnText: "> 4.50 mm/s",
    tripText: "> 7.10 mm/s",
    legendWarn: "— Alarm (>4.5)",
    legendTrip: "— Trip (>7.1)",
    defaultVal: 2.15,
    minY: 0.0,
    maxY: 10.0,
    warnThresh: 4.50,
    tripThresh: 7.10,
    warnIsLower: false,
    canSimulate: false
  }
};

let currentSensor = "PT-1201";
let telemetryHistory = [];
const MAX_TELEMETRY_POINTS = 60;
let currentPressure = 1.18;
let isSimulating = false;
let isLiveStreaming = false; // Standby by default, not running automatically
let telemetryAnimationId = null;
let telemetryHeartbeatTimer = null;
let simulationInterval = null;

function initTelemetryChart() {
  const canvas = document.getElementById("telemetry-live-chart");
  if (!canvas) return;

  const parent = canvas.parentElement;
  if (parent && parent.clientWidth > 0) {
    canvas.width = parent.clientWidth;
    canvas.height = parent.clientHeight || 144;
  } else {
    canvas.width = 500;
    canvas.height = 144;
  }

  // Pre-fill history with steady baseline if empty
  if (!telemetryHistory || telemetryHistory.length < MAX_TELEMETRY_POINTS) {
    resetHistoryToSensorDefault();
  }

  // Draw initial static frame immediately
  drawTelemetryFrame();

  // Start display loop for smooth animation
  if (!telemetryAnimationId) {
    startTelemetryCanvasLoop();
  }
}

function resetHistoryToSensorDefault() {
  const s = SENSORS[currentSensor] || SENSORS["PT-1201"];
  telemetryHistory = [];
  for (let i = 0; i < MAX_TELEMETRY_POINTS; i++) {
    telemetryHistory.push(s.defaultVal);
  }
}

function startTelemetryCanvasLoop() {
  function loop() {
    if (activeTab === "telemetry") {
      drawTelemetryFrame();
    }
    telemetryAnimationId = requestAnimationFrame(loop);
  }
  telemetryAnimationId = requestAnimationFrame(loop);
}

// ---------------------------------------------------------------------------
// Sensor Selector & Live Feed Toggle
// ---------------------------------------------------------------------------
window.selectTelemetrySensor = function(tag) {
  if (!SENSORS[tag]) return;
  currentSensor = tag;
  const s = SENSORS[tag];

  // Update UI buttons
  const buttons = document.querySelectorAll("#telemetry-sensor-chips button");
  buttons.forEach(btn => {
    btn.className = "px-3 py-1.5 rounded-xl text-xs font-mono font-medium transition pro-btn-secondary flex items-center gap-1.5 cursor-pointer";
    const dot = btn.querySelector("span");
    if (dot) dot.className = "w-2 h-2 rounded-full bg-current opacity-50";
  });

  const activeBtn = document.getElementById(`sensor-chip-${tag}`);
  if (activeBtn) {
    activeBtn.className = "px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition pro-btn-primary shadow-sm flex items-center gap-1.5 cursor-pointer";
    const dot = activeBtn.querySelector("span");
    if (dot) dot.className = "w-2 h-2 rounded-full bg-current opacity-90";
  }

  // Update UI card texts
  const titleEl = document.getElementById("telemetry-sensor-title");
  const descEl = document.getElementById("telemetry-sensor-desc");
  const paramLabelEl = document.getElementById("telemetry-param-label");
  const unitEl = document.getElementById("live-pressure-unit");
  const valEl = document.getElementById("live-pressure-val");
  const threshNorm = document.getElementById("thresh-normal-val");
  const threshWarn = document.getElementById("thresh-warn-val");
  const threshTrip = document.getElementById("thresh-trip-val");
  const chartTitle = document.getElementById("telemetry-chart-title");
  const legNorm = document.getElementById("legend-normal-text");
  const legWarn = document.getElementById("legend-warn-text");
  const legTrip = document.getElementById("legend-trip-text");
  const statusPill = document.getElementById("telemetry-live-status-pill");

  if (titleEl) titleEl.innerHTML = `<i data-lucide="activity" class="w-4 h-4"></i> ${s.name}`;
  if (descEl) descEl.innerText = s.desc;
  if (paramLabelEl) paramLabelEl.innerText = s.paramLabel;
  if (unitEl) unitEl.innerText = s.unit;
  if (valEl) valEl.innerText = s.defaultVal.toFixed(2);
  if (threshNorm) threshNorm.innerText = s.normalText;
  if (threshWarn) threshWarn.innerText = s.warnText;
  if (threshTrip) threshTrip.innerText = s.tripText;
  if (chartTitle) {
    chartTitle.innerHTML = `<span id="telemetry-live-dot" class="w-2 h-2 rounded-full ${isLiveStreaming ? 'bg-current animate-pulse' : 'bg-slate-400'}"></span> Waveform Monitor (${tag})`;
  }
  if (legNorm) legNorm.innerHTML = `&mdash; Normal`;
  if (legWarn) legWarn.innerHTML = s.legendWarn;
  if (legTrip) legTrip.innerHTML = s.legendTrip;

  if (statusPill) {
    statusPill.innerText = "NORMAL";
    statusPill.className = "px-3 py-1 rounded-full text-xs font-mono font-bold pro-badge";
  }

  // Reset telemetry waveform history for selected sensor
  currentPressure = s.defaultVal;
  resetHistoryToSensorDefault();
  drawTelemetryFrame();
  fetchTelemetry(tag);
  if (window.lucide) lucide.createIcons();
};

window.toggleTelemetryStream = function() {
  isLiveStreaming = !isLiveStreaming;
  const toggleBtn = document.getElementById("toggle-stream-btn");
  const toggleLabel = document.getElementById("stream-toggle-label");
  const rateLabel = document.getElementById("chart-rate-label");
  const liveDot = document.getElementById("telemetry-live-dot");

  if (isLiveStreaming) {
    if (toggleLabel) toggleLabel.innerText = "Pause polling";
    if (toggleBtn) {
      toggleBtn.className = "px-3 py-1.5 rounded-xl text-xs font-semibold pro-btn-secondary transition flex items-center gap-1.5 shadow-sm cursor-pointer";
      toggleBtn.innerHTML = `<i data-lucide="pause" class="w-3.5 h-3.5"></i> <span id="stream-toggle-label">Pause polling</span>`;
    }
    if (rateLabel) {
      rateLabel.innerText = "POLLING DEMO STATE (2s)";
      rateLabel.className = "text-[10px] app-text-primary font-mono font-bold";
    }
    if (liveDot) {
      liveDot.className = "w-2 h-2 rounded-full bg-current animate-pulse";
    }

    if (telemetryHeartbeatTimer) clearInterval(telemetryHeartbeatTimer);
    telemetryHeartbeatTimer = setInterval(() => {
      if (activeTab === "telemetry") fetchTelemetry();
    }, 2000);
  } else {
    if (telemetryHeartbeatTimer) clearInterval(telemetryHeartbeatTimer);
    if (toggleLabel) toggleLabel.innerText = "Poll simulator";
    if (toggleBtn) {
      toggleBtn.className = "px-3 py-1.5 rounded-xl text-xs font-medium pro-btn-secondary transition flex items-center gap-1.5 shadow-sm cursor-pointer";
      toggleBtn.innerHTML = `<i data-lucide="play" class="w-3.5 h-3.5"></i> <span id="stream-toggle-label">Poll simulator</span>`;
    }
    if (rateLabel) {
      rateLabel.innerText = "DEMO SIMULATOR (historian offline)";
      rateLabel.className = "text-[10px] app-text-secondary font-mono font-bold";
    }
    if (liveDot) {
      liveDot.className = "w-2 h-2 rounded-full bg-slate-400";
    }
  }
  if (window.lucide) lucide.createIcons();
};

// ---------------------------------------------------------------------------
// Oscilloscope Renderer
// ---------------------------------------------------------------------------
function drawTelemetryFrame() {
  const canvas = document.getElementById("telemetry-live-chart");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const w = canvas.width || 500;
  const h = canvas.height || 144;
  const s = SENSORS[currentSensor] || SENSORS["PT-1201"];

  // Background
  ctx.fillStyle = "#030712";
  ctx.fillRect(0, 0, w, h);

  // Oscilloscope Grid Lines
  ctx.strokeStyle = "rgba(56, 189, 248, 0.12)";
  ctx.lineWidth = 1;
  ctx.setLineDash([]);
  for (let x = 0; x < w; x += 35) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }
  for (let y = 0; y < h; y += 24) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(w, y);
    ctx.stroke();
  }

  // Y Scale mapping
  const minY = s.minY;
  const maxY = s.maxY;
  function getY(val) {
    const clamped = Math.max(minY, Math.min(maxY, val));
    return h - 14 - ((clamped - minY) / (maxY - minY)) * (h - 28);
  }

  // Normal Reference line
  const yNormal = getY(s.normalVal);
  ctx.strokeStyle = "rgba(16, 185, 129, 0.65)";
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.moveTo(0, yNormal);
  ctx.lineTo(w, yNormal);
  ctx.stroke();

  // Warning Reference line
  const yWarn = getY(s.warnThresh);
  ctx.strokeStyle = "rgba(245, 158, 11, 0.75)";
  ctx.beginPath();
  ctx.moveTo(0, yWarn);
  ctx.lineTo(w, yWarn);
  ctx.stroke();

  // Trip Reference line
  const yTrip = getY(s.tripThresh);
  ctx.strokeStyle = "rgba(239, 68, 68, 0.85)";
  ctx.setLineDash([]);
  ctx.beginPath();
  ctx.moveTo(0, yTrip);
  ctx.lineTo(w, yTrip);
  ctx.stroke();

  // Threshold labels
  ctx.font = "bold 9px monospace";
  ctx.fillStyle = "#10B981";
  ctx.fillText(`${s.normalVal.toFixed(2)} NOMINAL`, 8, Math.max(12, yNormal - 4));
  ctx.fillStyle = "#F59E0B";
  ctx.fillText(`${s.warnThresh.toFixed(2)} WARN`, 8, Math.max(12, yWarn - 4));
  ctx.fillStyle = "#EF4444";
  ctx.fillText(`${s.tripThresh.toFixed(2)} TRIP PSLL`, 8, Math.max(12, yTrip - 4));

  // Determine alert status
  let isTripNow = false;
  let isWarnNow = false;
  if (s.warnIsLower) {
    isTripNow = currentPressure <= s.tripThresh;
    isWarnNow = currentPressure < s.warnThresh && !isTripNow;
  } else {
    isTripNow = currentPressure >= s.tripThresh;
    isWarnNow = currentPressure > s.warnThresh && !isTripNow;
  }

  // Draw Waveform Curve
  if (telemetryHistory && telemetryHistory.length > 1) {
    const stepX = w / (MAX_TELEMETRY_POINTS - 1);
    const strokeColor = isTripNow ? "#EF4444" : (isWarnNow ? "#F59E0B" : "#38BDF8");
    const gradient = ctx.createLinearGradient(0, 0, 0, h);
    if (isTripNow) {
      gradient.addColorStop(0, "rgba(239, 68, 68, 0.40)");
      gradient.addColorStop(1, "rgba(239, 68, 68, 0.02)");
    } else if (isWarnNow) {
      gradient.addColorStop(0, "rgba(245, 158, 11, 0.35)");
      gradient.addColorStop(1, "rgba(245, 158, 11, 0.02)");
    } else {
      gradient.addColorStop(0, "rgba(56, 189, 248, 0.35)");
      gradient.addColorStop(1, "rgba(56, 189, 248, 0.02)");
    }

    // Main line
    ctx.setLineDash([]);
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(0, getY(telemetryHistory[0]));
    for (let i = 1; i < telemetryHistory.length; i++) {
      ctx.lineTo(i * stepX, getY(telemetryHistory[i]));
    }
    ctx.stroke();

    // Area fill
    ctx.lineTo((telemetryHistory.length - 1) * stepX, h);
    ctx.lineTo(0, h);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();

    // Leading glowing dot at latest point
    const lastIdx = telemetryHistory.length - 1;
    const lastX = lastIdx * stepX;
    const lastY = getY(telemetryHistory[lastIdx]);

    ctx.beginPath();
    ctx.arc(lastX, lastY, 4, 0, Math.PI * 2);
    ctx.fillStyle = strokeColor;
    ctx.fill();

    ctx.beginPath();
    ctx.arc(lastX, lastY, 8, 0, Math.PI * 2);
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Floating live badge inside canvas top-right
    ctx.fillStyle = strokeColor;
    ctx.font = "bold 12px monospace";
    ctx.textAlign = "right";
    ctx.fillText(`${currentPressure.toFixed(2)} ${s.unit}`, w - 10, 20);
    ctx.textAlign = "left"; // reset
  }
}

function setupTelemetry() {
  const triggerBtn = document.getElementById("trigger-anomaly-btn");
  const stepBtn = document.getElementById("step-sim-btn");
  const resetBtn = document.getElementById("reset-sim-btn");
  if (triggerBtn) {
    triggerBtn.addEventListener("click", () => window.triggerPressureCollapse());
  }
  if (stepBtn) {
    stepBtn.addEventListener("click", () => window.stepTelemetrySim());
  }
  if (resetBtn) {
    resetBtn.addEventListener("click", () => window.resetTelemetrySim());
  }

  fetch("/api/telemetry/sensors")
    .then(response => response.json())
    .then(payload => {
      const sensors = payload.sensors || [];
      const container = document.getElementById("telemetry-sensor-chips");
      if (!container || !sensors.length) return;

      sensors.forEach(sensor => {
        const config = SENSORS[sensor.tag_id] || {};
        const lower = sensor.warn_is_lower;
        Object.assign(config, {
          name: sensor.name,
          desc: sensor.description,
          paramLabel: sensor.name,
          unit: sensor.unit,
          normalVal: sensor.normal,
          normalText: `${sensor.normal} ${sensor.unit}`,
          warnText: `${lower ? "<" : ">"} ${sensor.alarm} ${sensor.unit}`,
          tripText: `${lower ? "<" : ">"} ${sensor.trip} ${sensor.unit}`,
          legendWarn: `— Alarm (${lower ? "<" : ">"}${sensor.alarm})`,
          legendTrip: `— Trip (${lower ? "<" : ">"}${sensor.trip})`,
          defaultVal: sensor.current_value,
          minY: 0,
          maxY: lower ? Math.max(sensor.setpoint * 1.4, sensor.setpoint + 0.5) : Math.max(sensor.trip * 1.2, sensor.trip + 5),
          warnThresh: sensor.alarm,
          tripThresh: sensor.trip,
          warnIsLower: lower,
          collapseSteps: sensor.collapse_steps,
          sourceReference: sensor.source_reference,
        });
        SENSORS[sensor.tag_id] = config;
      });

      container.innerHTML = sensors.map(sensor => `
        <button type="button" id="sensor-chip-${escapeHtml(sensor.tag_id)}" class="px-3 py-1.5 rounded-xl text-xs font-mono font-medium transition pro-btn-secondary flex items-center gap-1.5 cursor-pointer">
          <span class="w-2 h-2 rounded-full bg-current opacity-50"></span>${escapeHtml(sensor.tag_id)} (${escapeHtml(sensor.unit)})
        </button>
      `).join("");
      container.querySelectorAll("button").forEach((button, index) => {
        button.addEventListener("click", () => window.selectTelemetrySensor(sensors[index].tag_id));
      });

      const note = document.getElementById("telemetry-source-note");
      if (note) note.innerText = payload.live_historian_connected
        ? "Live historian feed connected."
        : "DEMO SIMULATOR: no DCS/historian connection. Values and events come from the configured simulator; references are linked below.";
      currentSensor = sensors[0].tag_id;
      window.selectTelemetrySensor(currentSensor);
      if (window.lucide) lucide.createIcons();
    })
    .catch(error => console.error("Failed to load telemetry catalog:", error));
}

async function fetchTelemetry(tag = currentSensor) {
  try {
    const res = await fetch(`/api/telemetry?tag=${encodeURIComponent(tag)}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Telemetry unavailable");
    renderTelemetry(data);
    drawTelemetryFrame();
  } catch (err) {
    console.error("Failed to fetch telemetry:", err);
  }
}

function renderTelemetry(data) {
  const pressureValEl = document.getElementById("live-pressure-val");
  const statusPill = document.getElementById("telemetry-live-status-pill");
  const alertBox = document.getElementById("proactive-alert-box");

  currentSensor = data.tag_id || currentSensor;
  currentPressure = Number(data.current_val ?? data.current_pressure);
  if (Array.isArray(data.telemetry_history) && data.telemetry_history.length) {
    const values = data.telemetry_history.map(point => Number(point.current_val ?? point.pressure)).filter(Number.isFinite);
    telemetryHistory = values.slice(-MAX_TELEMETRY_POINTS);
    while (telemetryHistory.length < MAX_TELEMETRY_POINTS) telemetryHistory.unshift(telemetryHistory[0] ?? currentPressure);
  }
  if (pressureValEl) {
    pressureValEl.innerText = currentPressure.toFixed(2);
    pressureValEl.className = "text-6xl font-mono font-extrabold app-text-primary tracking-tight";
  }

  if (data.is_tripped) {
    if (statusPill) {
      statusPill.innerText = "TRIP INTERLOCK ACTIVATED";
      statusPill.className = "px-3 py-1 rounded-full text-xs font-mono font-bold pro-badge border-2";
    }
  } else if (data.is_pre_trip) {
    if (statusPill) {
      statusPill.innerText = "PRE-TRIP DEGRADING";
      statusPill.className = "px-3 py-1 rounded-full text-xs font-mono font-bold pro-badge";
    }
  } else {
    if (statusPill) {
      statusPill.innerText = "NORMAL";
      statusPill.className = "px-3 py-1 rounded-full text-xs font-mono font-bold pro-badge";
    }
  }

  // Proactive Alert Rendering
  if (data.proactive_alert) {
    const alt = data.proactive_alert;
    alertBox.className = "p-6 rounded-2xl dcs-panel border app-border app-text-secondary space-y-3 shadow-md";
    alertBox.innerHTML = `
        <div class="flex items-center gap-2">
          <span class="font-bold app-text-primary text-sm tracking-wide">PROACTIVE CRITICAL ADVISORY (${alt.tag})</span>
        <span class="px-2.5 py-0.5 rounded-full pro-badge font-mono text-[10px] font-bold">PRE-TRIP INTERLOCK</span>
      </div>

      <div class="text-xs leading-relaxed app-text-secondary">
        ${escapeHtml(alt.tag)} reads <strong class="app-text-primary font-mono font-bold">${escapeHtml(alt.current_val)}</strong>; configured trip threshold is <strong class="app-text-primary font-mono font-bold">${escapeHtml(alt.trip_limit)}</strong> (delta: ${escapeHtml(alt.delta_to_trip)}).
      </div>

      <div class="p-3.5 dcs-card rounded-xl border app-border space-y-1.5 shadow-sm">
        <div class="text-[11px] font-bold app-text-primary flex items-center gap-1.5">
          <i data-lucide="history" class="w-3.5 h-3.5"></i> Failure Memory: ${escapeHtml(alt.matched_incident_id)} (${Math.round((alt.similarity_score || 0) * 100)}%)
        </div>
        <p class="text-[11px] app-text-muted font-sans">${escapeHtml(alt.incident_title || "Linked incident record")}</p>
      </div>

      <div class="p-3.5 dcs-card rounded-xl border app-border space-y-1 text-xs shadow-sm">
        <div class="font-bold app-text-primary uppercase tracking-wider text-[10px] font-mono">Scheduled Mitigation Action (Proactive Push):</div>
        <p class="font-medium app-text-primary mt-1">${escapeHtml(alt.recommended_action)}</p>
        <p class="text-[10px] app-text-muted pt-1 font-mono">Reference: <strong>${escapeHtml(alt.sop_reference)}</strong></p>
      </div>

      <div class="text-[11px] app-text-muted">
        Affected assets: <span class="app-text-primary font-semibold font-mono">${(alt.affected_downstream_units || []).map(escapeHtml).join(" &bull; ")}</span>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
  } else {
    alertBox.className = "p-6 rounded-2xl dcs-card border app-border app-text-muted text-xs text-center";
    alertBox.innerHTML = `
      <p class="py-12">${escapeHtml(data.sensor_name || currentSensor)} is within its configured demo-simulator threshold. No live historian connection is available.</p>
    `;
  }
}

window.triggerPressureCollapse = async function() {
  const button = document.getElementById("trigger-anomaly-btn");
  if (button) button.disabled = true;
  try {
    const response = await fetch(`/api/telemetry/simulate-anomaly?tag=${encodeURIComponent(currentSensor)}`, { method: "POST" });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Simulator unavailable");
    renderTelemetry(data);
    drawTelemetryFrame();

    // Auto-advance simulation smoothly until it trips
    let simInterval = setInterval(async () => {
      try {
        const stepRes = await fetch(`/api/telemetry/step?tag=${encodeURIComponent(currentSensor)}`, { method: "POST" });
        const stepData = await stepRes.json();
        renderTelemetry(stepData);
        drawTelemetryFrame();
        if (stepData.is_tripped) {
          clearInterval(simInterval);
          if (button) button.disabled = false;
        }
      } catch (err) {
        clearInterval(simInterval);
        if (button) button.disabled = false;
      }
    }, 1500);

  } catch (error) {
    console.error("Telemetry anomaly API error:", error);
    if (button) button.disabled = false;
  }
};

window.stepTelemetrySim = async function() {
  const response = await fetch(`/api/telemetry/step?tag=${encodeURIComponent(currentSensor)}`, { method: "POST" });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Simulator unavailable");
  renderTelemetry(data);
  drawTelemetryFrame();
};

window.resetTelemetrySim = async function() {
  const response = await fetch(`/api/telemetry/reset?tag=${encodeURIComponent(currentSensor)}`, { method: "POST" });
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Simulator unavailable");
  renderTelemetry(data);
  drawTelemetryFrame();
};

(() => {
  const initializeLoginWater = () => {
    const canvas = document.getElementById("login-water-canvas");
    const loginScreen = document.getElementById("login-screen");
    if (!canvas || !loginScreen) return;

    const gl = canvas.getContext("webgl", { alpha: false, antialias: false });
    if (!gl) {
      console.error("Login water effect could not initialize: WebGL is unavailable.");
      return;
    }

    const vertexSource = `
      attribute vec2 a_position;
      void main() {
        gl_Position = vec4(a_position, 0.0, 1.0);
      }
    `;
    const fragmentSource = `
      precision highp float;
      uniform float u_time;
      uniform vec2 u_resolution;
      uniform vec3 u_trail[15];

      void main() {
        vec2 uv = gl_FragCoord.xy / u_resolution;
        vec2 p = uv * 2.0 - 1.0;
        p.x *= u_resolution.x / u_resolution.y;

        float ripple = 0.0;
        for (int i = 0; i < 15; i++) {
          vec2 trailPoint = u_trail[i].xy / u_resolution;
          trailPoint = trailPoint * 2.0 - 1.0;
          trailPoint.x *= u_resolution.x / u_resolution.y;
          float distanceToTrail = length(p - trailPoint);
          float age = float(i) / 15.0;
          float wave = sin(distanceToTrail * 30.0 - u_time * 8.0 - age * 8.0);
          float mask = exp(-distanceToTrail * (10.0 - age * 5.0));
          ripple += wave * mask * (1.0 - age) * u_trail[i].z * 0.7;
        }

        vec2 q = p + ripple;
        float time = u_time * 0.3;
        for (float i = 1.0; i < 6.0; i++) {
          q.x += 0.3 / i * cos(i * 2.5 * q.y + time);
          q.y += 0.3 / i * cos(i * 1.5 * q.x + time);
        }

        float surface = sin(q.x + q.y) * 0.5 + 0.5;
        vec3 color = mix(vec3(0.04, 0.16, 0.36), vec3(0.16, 0.45, 0.72), smoothstep(0.0, 0.6, surface));
        color = mix(color, vec3(0.40, 0.85, 0.95), smoothstep(0.7, 1.0, surface));
        color += pow(smoothstep(0.85, 1.0, surface), 5.0) * vec3(0.8, 0.95, 1.0);
        gl_FragColor = vec4(color, 1.0);
      }
    `;

    const compileShader = (type, source) => {
      const shader = gl.createShader(type);
      if (!shader) {
        console.error("Login water effect could not create a WebGL shader.");
        return null;
      }
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error("Login water effect shader compilation failed:", gl.getShaderInfoLog(shader));
        gl.deleteShader(shader);
        return null;
      }
      return shader;
    };

    const vertexShader = compileShader(gl.VERTEX_SHADER, vertexSource);
    const fragmentShader = compileShader(gl.FRAGMENT_SHADER, fragmentSource);
    if (!vertexShader || !fragmentShader) return;

    const program = gl.createProgram();
    if (!program) {
      console.error("Login water effect could not create a WebGL program.");
      return;
    }
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      console.error("Login water effect program linking failed:", gl.getProgramInfoLog(program));
      return;
    }
    gl.useProgram(program);

    const positionBuffer = gl.createBuffer();
    if (!positionBuffer) {
      console.error("Login water effect could not create a WebGL buffer.");
      return;
    }
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
      -1, -1, 1, -1, -1, 1,
      -1, 1, 1, -1, 1, 1
    ]), gl.STATIC_DRAW);

    const positionLocation = gl.getAttribLocation(program, "a_position");
    const timeLocation = gl.getUniformLocation(program, "u_time");
    const resolutionLocation = gl.getUniformLocation(program, "u_resolution");
    const trailLocation = gl.getUniformLocation(program, "u_trail[0]");
    if (positionLocation < 0 || !timeLocation || !resolutionLocation || !trailLocation) {
      console.error("Login water effect could not find required WebGL shader inputs.");
      return;
    }
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    const trailCount = 15;
    const trail = new Float32Array(trailCount * 3);
    let targetX = 0;
    let targetY = 0;
    let lastX = 0;
    let lastY = 0;
    let startTime = 0;
    let animationFrame = 0;

    const resizeCanvas = () => {
      const bounds = canvas.getBoundingClientRect();
      const pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
      canvas.width = Math.max(1, Math.round(bounds.width * pixelRatio));
      canvas.height = Math.max(1, Math.round(bounds.height * pixelRatio));
      gl.viewport(0, 0, canvas.width, canvas.height);
      targetX = canvas.width / 2;
      targetY = canvas.height / 2;
      lastX = targetX;
      lastY = targetY;
      for (let i = 0; i < trailCount; i++) {
        trail[i * 3] = targetX;
        trail[i * 3 + 1] = targetY;
        trail[i * 3 + 2] = 0;
      }
    };

    loginScreen.addEventListener("pointermove", event => {
      const bounds = canvas.getBoundingClientRect();
      const scaleX = canvas.width / bounds.width;
      const scaleY = canvas.height / bounds.height;
      targetX = (event.clientX - bounds.left) * scaleX;
      targetY = canvas.height - (event.clientY - bounds.top) * scaleY;
    });
    window.addEventListener("resize", resizeCanvas);

    const render = timestamp => {
      if (loginScreen.classList.contains("hidden")) {
        animationFrame = 0;
        return;
      }

      if (!startTime) startTime = timestamp;
      const deltaX = targetX - lastX;
      const deltaY = targetY - lastY;
      const strength = Math.min(Math.hypot(deltaX, deltaY) * 0.03, 1);
      lastX = targetX;
      lastY = targetY;

      trail[0] += (targetX - trail[0]) * 0.6;
      trail[1] += (targetY - trail[1]) * 0.6;
      trail[2] += (strength - trail[2]) * 0.15;
      for (let i = 1; i < trailCount; i++) {
        trail[i * 3] += (trail[(i - 1) * 3] - trail[i * 3]) * 0.45;
        trail[i * 3 + 1] += (trail[(i - 1) * 3 + 1] - trail[i * 3 + 1]) * 0.45;
        trail[i * 3 + 2] += (trail[(i - 1) * 3 + 2] - trail[i * 3 + 2]) * 0.45;
      }

      gl.uniform1f(timeLocation, (timestamp - startTime) * 0.001);
      gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
      gl.uniform3fv(trailLocation, trail);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      animationFrame = window.requestAnimationFrame(render);
    };

    const startRendering = () => {
      if (!animationFrame && !loginScreen.classList.contains("hidden")) {
        startTime = 0;
        animationFrame = window.requestAnimationFrame(render);
      }
    };

    const stopRendering = () => {
      if (animationFrame) {
        window.cancelAnimationFrame(animationFrame);
        animationFrame = 0;
      }
    };

    resizeCanvas();
    new MutationObserver(() => {
      if (loginScreen.classList.contains("hidden")) stopRendering();
      else startRendering();
    }).observe(loginScreen, { attributes: true, attributeFilter: ["class"] });
    startRendering();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeLoginWater, { once: true });
  } else {
    initializeLoginWater();
  }
})();
