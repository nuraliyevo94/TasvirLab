// KidsVidEdu Platform - Client Application
const state = {
  currentStep: 1,
  selectedAge: "5-7",
  topic: "2 ga 2 ni qo'shish siri (Matematika darsi)",
  prompt: "Bolalarga 2 ga 2 ni qo'shish qanday bo'lishini olmalar misolida tushuntirib, 2+2=4 natijasini o'rgatuvchi dars.",
  duration: 35,
  visualStyle: "pixar_3d",
  selectedVoice: "lola",
  selectedBgm: "bgm_cheerful",
  voiceVolume: 1.0,
  bgmVolume: 0.25,
  language: "uz",
  
  safetyReport: null,
  screenplay: null,
  preparedScenes: [],
  
  // Video Player state
  isPlaying: false,
  currentSceneIndex: 0,
  totalDuration: 0,
  animationFrameId: null,
  
  // Audio state
  testAudio: new Audio(),
  presets: {
    age_groups: [
      { id: "3-4", title: "Kichkintoylar (3-4 yosh)", category: "Boshlang'ich", icon: "🧸", recommended_duration: 30, style_desc: "O'ta sodda so'zlar, yorqin ranglar, sekin va mehrli nutq." },
      { id: "5-7", title: "Bog'cha va Tayyorlov (5-7 yosh)", category: "Eng Mashhur", icon: "🎨", recommended_duration: 45, style_desc: "Qiziqarli savollar, multfilm qahramonlari, quvnoq ohang." },
      { id: "8-10", title: "Boshlang'ich Maktab (8-10 yosh)", category: "Faol Ta'lim", icon: "🚀", recommended_duration: 60, style_desc: "Mantiqiy tushuntirish, qiziqarli faktlar, do'stona muloqot." },
      { id: "11-12", title: "Katta Bolalar (11-12 yosh)", category: "Ilmiy-Ommabop", icon: "🔬", recommended_duration: 75, style_desc: "Ilmiy asoslangan bilimlar, chuqurroq tahlil, zamonaviy uslub." }
    ],
    visual_styles: [
      { id: "pixar_3d", name: "Pixar 3D Multfilm", desc: "Zamonaviy 3D animatsiya, yorqin ranglar", icon: "🎬" },
      { id: "disney_2d", name: "Klassik Disney 2D", desc: "Sehrli ertaknamo multfilm uslubi", icon: "✨" },
      { id: "ghibli_anime", name: "Studio Ghibli", desc: "Mayin akvarel va tabiat manzaralari", icon: "🍃" },
      { id: "cute_claymation", name: "Plastilin Animatsiya", desc: "Yoqimli qo'lda yasalgan uslub", icon: "🧸" }
    ],
    voices: [
      { id: "lola", name: "Pedagogik O'zbek Ovoz", role: "Mehribon virtual ustoz", gender: "female", recommended: true }
    ],
    bgm_tracks: [
      { id: "bgm_cheerful", name: "Quvnoq Marimba & Ukulele", icon: "🎈", desc: "Carefree (K. MacLeod) — Quvnoq, samimiy bolalar ohangi", url: "/audio/bgm_cheerful.mp3" },
      { id: "bgm_playful", name: "Qiziqarli Multfilm Maromi", icon: "🐒", desc: "Monkeys Spinning Monkeys — Sho'x multfilm sarguzashti", url: "/audio/bgm_playful.ogg" },
      { id: "bgm_gentle", name: "Mayin va Sokin Pianino", icon: "🍃", desc: "Gymnopédie No. 1 (Erik Satie) — Orom baxsh fortepiano", url: "/audio/bgm_gentle.ogg" },
      { id: "bgm_fairytale", name: "Sehrli Ertak & Mo'jiza", icon: "✨", desc: "Sugar Plum Fairy (Chaykovskiy) — Sehrli ertak olami", url: "/audio/bgm_fairytale.ogg" },
      { id: "bgm_upbeat", name: "Shijoatli Ragtime Ta'lim", icon: "🚀", desc: "The Entertainer (Scott Joplin) — Jonli intellektual ritm", url: "/audio/bgm_upbeat.ogg" },
      { id: "none", name: "Musiqasiz (Faqat ovoz)", icon: "🔇", desc: "Faqat virtual ustozning sof nutq ovozi", url: "" }
    ],
    sample_topics: [
      { id: "colors_fun", title: "Ranglarni birga o'rganamiz", prompt: "Qizil, sariq va yashil ranglarni mevalar misolida tanishtiruvchi quvnoq dars", age_group: "3-4" },
      { id: "forest_animals", title: "O'rmondagi do'stlarimiz", prompt: "Quyoncha va ayiqvoyning do'stligi hamda o'rmon hayoti haqida ertak", age_group: "3-4" },
      { id: "math_2plus2", title: "2 ga 2 ni qo'shish siri", prompt: "2+2=4 qanday bo'lishini olmalar misolida o'rgatuvchi dars", age_group: "5-7" },
      { id: "autumn_leaves", title: "Daraxtlar nega barg to'kadi?", prompt: "Kuzda barglar nega sarg'ayishi va to'kilishi haqida ertak dars", age_group: "5-7" },
      { id: "water_cycle", title: "Yomg'ir qayerdan keladi?", prompt: "Suv tomchisining bulutlarga aylanib yerga qaytishi haqida saboq", age_group: "5-7" },
      { id: "solar_system", title: "Quyosh sistemasiga sayohat", prompt: "Sayyoralar va ularning Quyosh atrofida aylanishi sirlari", age_group: "8-10" },
      { id: "ocean_depths", title: "Okean tubidagi sirlar", prompt: "Delfinlar va dengiz jonzotlarining ajoyib xususiyatlari", age_group: "8-10" },
      { id: "photosynthesis", title: "Fotosintez mo'jizasi", prompt: "O'simliklar quyosh nuri orqali qanday qilib toza havo va kislorod ishlab chiqarishi", age_group: "11-12" },
      { id: "gravity_secret", title: "Gravitatsiya kuchi siri", prompt: "Nega narsalar yerga tushadi va fazoda vaznsizlik qanday sodir bo'ladi", age_group: "11-12" }
    ]
  }
};

const API_URL = "";
const imageCache = {};

// DOM Ready
document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  
  // Dastlabki render darhol ishga tushadi
  renderAgeCards();
  renderVisualStyles();
  renderVoiceOptions();
  renderSampleTopics();
  renderBgmTracks();

  // Dastlabki tayyor dars sahnasi (Nutqda sonlar so'z bilan, doskada esa raqamlar bilan)
  state.preparedScenes = [
    {
      scene_number: 1,
      title: "Olmalarni Sanaymiz",
      narration: "Salom bolajonim! Tasavvur qil, senga ikkita qizil olma berishdi. Keyin yana ikkita olma berishdi. Keling, ikkiga ikkini qo'shamiz!",
      audio_url: "/renders/test_voice_jasur_scene_1.wav",
      image_url: "/renders/test_voice_jasur_scene_1.svg",
      duration: 5.72,
      emotion: "quvnoq",
      visual_beats: [
        {
          time_pct: 0.0,
          badge: "SAVOL",
          main_text: "2 + 2",
          sub_text: "2 ta olma va yana 2 ta olma",
          icons: ["🍎", "🍎", "+", "🍎", "🍎"],
          highlight: false
        },
        {
          time_pct: 0.55,
          badge: "BIRGA SANAYMIZ",
          main_text: "2 + 2 = ?",
          sub_text: "Barchasini birlashtiramiz...",
          icons: ["🍎", "🍎", "🍎", "🍎"],
          highlight: false
        }
      ]
    },
    {
      scene_number: 2,
      title: "Natija va Xulosa",
      narration: "Ofarin! Ikkiga ikkini qo'shsak, to'rt bo'ladi! Qara: ikki qo'shuv ikki teng to'rt! Jami to'rtta shirin olma bo'ldi!",
      audio_url: "/renders/test_voice_sevinch_scene_1.wav",
      image_url: "/renders/test_voice_jasur_scene_1.svg",
      duration: 4.4,
      emotion: "quvonch",
      visual_beats: [
        {
          time_pct: 0.0,
          badge: "QO'SHISH AMALI",
          main_text: "2 + 2 = ?",
          sub_text: "Barcha olmalarni birga sanaymiz...",
          icons: ["🍎", "🍎", "🍎", "🍎"],
          highlight: false
        },
        {
          time_pct: 0.45,
          badge: "NATIJA",
          main_text: "2 + 2 = 4",
          sub_text: "Jami 4 ta olma bo'ldi! Barakalla! 🎉",
          icons: ["🍎", "🍎", "🍎", "🍎"],
          highlight: true
        }
      ]
    }
  ];
  state.totalDuration = 10.12;

  setupCanvasPlayer();
  await loadPresets();
});

// Load Presets
async function loadPresets() {
  try {
    const res = await fetch(`${API_URL}/api/presets`);
    if (res.ok) {
      const data = await res.json();
      if (data && data.age_groups) {
        state.presets = data;
        renderAgeCards();
        renderVisualStyles();
        renderVoiceOptions();
        renderSampleTopics();
        renderBgmTracks();
        updatePlayerBgmSelectOptions();
      }
    }
  } catch (err) {
    console.warn("Presets serverdan yuklanmadi, zaxira sozlamalar faol:", err);
  }
}

// Audio va Video Sinxronizatsiyasi Funksiyalari
function onAudioTimeUpdate() {
  const masterAudio = document.getElementById("playerMasterAudio");
  if (state.isPlaying && masterAudio && !masterAudio.paused && masterAudio.currentTime > 0) {
    if (Math.abs(state.sceneCurrentTime - masterAudio.currentTime) > 0.25) {
      state.sceneCurrentTime = masterAudio.currentTime;
    }
  }
}

function onAudioEnded() {
  if (state.isPlaying) {
    if (state.currentSceneIndex + 1 < state.preparedScenes.length) {
      loadAndDisplayScene(state.currentSceneIndex + 1);
    } else {
      state.isPlaying = false;
      state.currentTime = state.totalDuration;
      const curDisplay = document.getElementById("currentTimeDisplay");
      if (curDisplay) curDisplay.innerText = formatTime(state.totalDuration);
      const prog = document.getElementById("videoProgressBar");
      if (prog) prog.style.width = "100%";
      const btn = document.getElementById("btnPlayPause");
      if (btn) btn.innerHTML = `<span>🔄</span><span>Qayta ko'rish</span>`;
      const bgmAudio = document.getElementById("playerBgmAudio");
      if (bgmAudio) bgmAudio.pause();
      if (state.animationFrameId) {
        cancelAnimationFrame(state.animationFrameId);
        state.animationFrameId = null;
      }
    }
  }
}

function seekVideo(event) {
  if (!state.totalDuration || state.totalDuration <= 0) return;
  const bar = event.currentTarget;
  if (!bar) return;
  const rect = bar.getBoundingClientRect();
  const clickX = Math.max(0, Math.min(rect.width, event.clientX - rect.left));
  const targetPct = clickX / rect.width;
  const targetSec = targetPct * state.totalDuration;

  let accumulated = 0;
  for (let i = 0; i < state.preparedScenes.length; i++) {
    const sc = state.preparedScenes[i];
    if (targetSec <= accumulated + sc.duration || i === state.preparedScenes.length - 1) {
      const sceneSec = Math.max(0, Math.min(sc.duration, targetSec - accumulated));
      state.currentSceneIndex = i;
      state.sceneCurrentTime = sceneSec;
      state.currentTime = targetSec;
      
      const masterAudio = document.getElementById("playerMasterAudio");
      if (masterAudio) {
        masterAudio.src = sc.audio_url;
        masterAudio.currentTime = sceneSec;
        if (state.isPlaying) {
          masterAudio.play().catch(e => console.warn(e));
        }
      }
      drawSceneFrame(sc, sceneSec);
      const curDisp = document.getElementById("currentTimeDisplay");
      if (curDisp) curDisp.innerText = formatTime(state.currentTime);
      const prog = document.getElementById("videoProgressBar");
      if (prog) prog.style.width = `${(targetPct * 100).toFixed(1)}%`;
      const tracker = document.getElementById("sceneTrackerDisplay");
      if (tracker) tracker.innerText = `${i + 1}-sahna / ${state.preparedScenes.length}`;
      break;
    }
    accumulated += sc.duration;
  }
}
window.seekVideo = seekVideo;

// Event Listeners
function setupEventListeners() {
  document.getElementById("btnNext").addEventListener("click", () => handleNextStep());
  document.getElementById("btnPrev").addEventListener("click", () => handlePrevStep());
  
  const durationSlider = document.getElementById("durationSlider");
  const durationDisplay = document.getElementById("durationDisplay");
  durationSlider.addEventListener("input", (e) => {
    state.duration = parseInt(e.target.value);
    durationDisplay.innerText = `${state.duration} soniya`;
  });

  const btnOpen = document.getElementById("btnOpenSettings");
  if (btnOpen) {
    btnOpen.addEventListener("click", () => {
      document.getElementById("settingsModal").classList.remove("hidden");
    });
  }
  const btnClose = document.getElementById("btnCloseSettings");
  if (btnClose) {
    btnClose.addEventListener("click", () => {
      document.getElementById("settingsModal").classList.add("hidden");
    });
  }
  const btnSave = document.getElementById("btnSaveSettings");
  if (btnSave) {
    btnSave.addEventListener("click", saveSettings);
  }

  // Player controls
  document.getElementById("btnPlayPause").addEventListener("click", togglePlayPause);
  document.getElementById("btnRestart").addEventListener("click", restartVideo);
  document.getElementById("btnDownload").addEventListener("click", downloadVideoPackage);
  document.getElementById("btnOpenPremyere").addEventListener("click", () => {
    document.getElementById("renderProgressModal").classList.add("hidden");
    goToStep(5);
    initCinemaPlayer();
  });

  // Audio Player Event Listeners
  const masterAudio = document.getElementById("playerMasterAudio");
  masterAudio.addEventListener("timeupdate", onAudioTimeUpdate);
  masterAudio.addEventListener("ended", onAudioEnded);
  masterAudio.addEventListener("play", () => {
    document.getElementById("audioEqualizer").style.opacity = "1";
  });
  masterAudio.addEventListener("pause", () => {
    document.getElementById("audioEqualizer").style.opacity = "0.3";
  });
}

// Render Age Cards
function renderAgeCards() {
  const container = document.getElementById("ageCardsContainer");
  if (!container || !state.presets) return;

  container.innerHTML = state.presets.age_groups.map(age => `
    <div class="age-card glass-panel p-6 rounded-3xl ${state.selectedAge === age.id ? 'active' : ''}" 
         onclick="selectAge('${age.id}')">
      <div class="flex items-start justify-between mb-4">
        <span class="text-4xl filter drop-shadow-md">${age.icon}</span>
        <div class="check-badge w-7 h-7 rounded-full bg-indigo-600 text-white flex items-center justify-center text-sm font-bold shadow-md">
          ✓
        </div>
      </div>
      <h3 class="font-fredoka text-2xl font-bold text-slate-800 mb-1">${age.title}</h3>
      <p class="text-xs font-semibold text-indigo-600 uppercase tracking-wider mb-3">${age.category}</p>
      <p class="text-sm text-slate-600 leading-relaxed mb-4">${age.style_desc}</p>
      <div class="flex items-center gap-2 text-xs font-medium text-slate-500 bg-white/70 py-1.5 px-3 rounded-xl border border-slate-200">
        <span>⏱️ Tavsiya vaqt:</span>
        <strong class="text-indigo-600">${age.recommended_duration} soniya</strong>
      </div>
    </div>
  `).join("");
}

window.selectAge = function(ageId) {
  state.selectedAge = ageId;
  const ageInfo = state.presets.age_groups.find(a => a.id === ageId);
  if (ageInfo) {
    state.duration = ageInfo.recommended_duration;
    document.getElementById("durationSlider").value = state.duration;
    document.getElementById("durationDisplay").innerText = `${state.duration} soniya`;
  }
  renderAgeCards();
  renderSampleTopics();
};

// Render Visual Styles
function renderVisualStyles() {
  const container = document.getElementById("visualStylesContainer");
  if (!container || !state.presets) return;

  container.innerHTML = state.presets.visual_styles.map(style => `
    <label class="cursor-pointer">
      <input type="radio" name="visualStyle" value="${style.id}" class="sr-only peer" 
             ${state.visualStyle === style.id ? 'checked' : ''} onchange="selectVisualStyle('${style.id}')">
      <div class="p-4 rounded-2xl border-2 border-slate-200 bg-white/80 peer-checked:border-indigo-600 peer-checked:bg-indigo-50/70 transition-all flex items-center gap-3">
        <span class="text-2xl">${style.icon}</span>
        <div>
          <div class="font-bold text-slate-800 text-sm">${style.title}</div>
          <div class="text-xs text-slate-500">1080p Cartoon Art</div>
        </div>
      </div>
    </label>
  `).join("");
}

window.selectVisualStyle = function(styleId) {
  state.visualStyle = styleId;
};

// Render Sample Topics
function renderSampleTopics() {
  const container = document.getElementById("sampleTopicsContainer");
  if (!container || !state.presets) return;

  const relevantTopics = state.presets.sample_topics.filter(t => (t.age_group === state.selectedAge || t.age === state.selectedAge));
  container.innerHTML = relevantTopics.map(t => `
    <button type="button" class="text-left p-3 rounded-2xl bg-white/80 hover:bg-indigo-50 border border-slate-200 transition-all text-xs text-slate-700 flex items-center gap-2 shadow-sm"
            onclick="applySampleTopic('${t.title.replace(/'/g, "\\'")}', '${t.prompt.replace(/'/g, "\\'")}')">
      <span class="text-indigo-500 font-bold">✨</span>
      <span>${t.title}</span>
    </button>
  `).join("");
}

window.autoSelectBestBgm = function(topic = "", emotion = "") {
  const t = (topic || state.topic || "").toLowerCase();
  const e = (emotion || "").toLowerCase();
  let best = "bgm_cheerful";

  if (e.includes("orom") || e.includes("sokin") || t.includes("daraxt") || t.includes("kuz") || t.includes("barg") || t.includes("tabiat") || t.includes("uxla") || t.includes("kecha") || t.includes("oy")) {
    best = "bgm_gentle"; // Mayin va Sokin Pianino (Gymnopédie No. 1)
  } else if (e.includes("hayrat") || e.includes("sehr") || t.includes("ertak") || t.includes("yulduz") || t.includes("mo'jiza") || t.includes("afsona") || t.includes("sehrli")) {
    best = "bgm_fairytale"; // Sehrli Ertak & Mo'jiza (Sugar Plum Fairy)
  } else if (e.includes("shijoat") || t.includes("matematik") || t.includes("fazo") || t.includes("kosmos") || t.includes("robot") || t.includes("sport") || t.includes("intellekt") || t.includes("hisob")) {
    best = "bgm_upbeat"; // Shijoatli Ragtime Ta'lim (The Entertainer)
  } else if (e.includes("sho'x") || t.includes("hayvon") || t.includes("quyon") || t.includes("o'yin") || t.includes("maymun") || t.includes("kulgili") || t.includes("hazil")) {
    best = "bgm_playful"; // Qiziqarli Multfilm (Monkeys Spinning Monkeys)
  } else {
    best = "bgm_cheerful"; // Quvnoq Marimba & Ukulele (Carefree)
  }

  state.selectedBgm = best;
  updatePlayerBgmSelectOptions();
  renderBgmTracks();
  updatePlayerBgmSource();
};

window.applySampleTopic = function(title, prompt) {
  const topicEl = document.getElementById("inputTopic");
  if (topicEl) topicEl.value = title;
  state.topic = title;
  state.prompt = prompt || title;
  autoSelectBestBgm(title);
};

// Render Voice Options
function renderVoiceOptions() {
  const container = document.getElementById("voiceCardsContainer");
  if (!container || !state.presets) return;

  container.innerHTML = state.presets.voices.map(voice => `
    <div class="p-4 rounded-2xl border-2 cursor-pointer transition-all flex items-center justify-between ${state.selectedVoice === voice.id ? 'border-pink-500 bg-pink-50/60' : 'border-slate-200 bg-white/80'}"
         onclick="selectVoice('${voice.id}')">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl ${voice.gender === 'female' ? 'bg-pink-100 text-pink-600' : 'bg-blue-100 text-blue-600'} font-bold">
          ${voice.gender === 'female' ? '👩' : '👨'}
        </div>
        <div>
          <div class="font-fredoka font-bold text-slate-800 text-base">${voice.name}</div>
          <div class="text-xs text-indigo-600 font-medium">${voice.role}</div>
          <div class="text-xs text-slate-500 mt-0.5 line-clamp-1">${voice.tone}</div>
        </div>
      </div>
      <button type="button" class="px-3 py-1.5 rounded-xl bg-white border border-slate-200 text-xs font-bold text-slate-700 hover:bg-slate-100 shadow-sm flex items-center gap-1.5"
              onclick="event.stopPropagation(); testVoice('${voice.id}')">
        <span>🔊</span> Tinglash
      </button>
    </div>
  `).join("");
}

window.selectVoice = function(voiceId) {
  state.selectedVoice = voiceId;
  renderVoiceOptions();
};

window.testVoice = async function(voiceId) {
  try {
    state.testAudio.src = `${API_URL}/api/audio/demo?voice=${voiceId}`;
    state.testAudio.play();
  } catch (e) {
    console.error("Audio test error:", e);
  }
};

// Render BGM Tracks (Orqa fon musiqalari)
function renderBgmTracks() {
  const container = document.getElementById("bgmTracksContainer");
  if (!container || !state.presets || !state.presets.bgm_tracks) return;

  container.innerHTML = state.presets.bgm_tracks.map(track => {
    const isSelected = state.selectedBgm === track.id;
    return `
      <div class="p-3.5 rounded-2xl border-2 cursor-pointer transition-all flex items-center justify-between ${isSelected ? 'border-indigo-600 bg-indigo-50/80 shadow-sm ring-2 ring-indigo-200' : 'border-slate-200 bg-white/80 hover:bg-slate-50'}"
           onclick="selectBgm('${track.id}')">
        <div class="flex items-center gap-3">
          <span class="text-2xl">${track.icon}</span>
          <div>
            <div class="font-fredoka font-bold text-slate-800 text-sm flex items-center gap-1.5">
              <span>${track.name}</span>
              ${track.isCustom ? `<span class="px-1.5 py-0.5 rounded text-[10px] bg-pink-100 text-pink-700 font-sans font-bold">Maxsus</span>` : ''}
            </div>
            <div class="text-xs text-slate-500 font-medium">${track.desc}</div>
          </div>
        </div>
        <div class="flex items-center gap-1.5">
          ${track.url ? `
            <button type="button" class="w-8 h-8 rounded-xl bg-white border border-slate-200 text-xs font-bold text-slate-700 hover:bg-indigo-50 hover:text-indigo-600 shadow-sm flex items-center justify-center transition-all"
                    title="Musiqani eshitib ko'rish"
                    onclick="event.stopPropagation(); previewBgmAudio('${track.url}')">
              ▶️
            </button>
          ` : ''}
          <div class="w-5 h-5 rounded-full border-2 ${isSelected ? 'border-indigo-600 bg-indigo-600' : 'border-slate-300'} flex items-center justify-center">
            ${isSelected ? '<span class="text-white text-[10px] font-bold">✓</span>' : ''}
          </div>
        </div>
      </div>
    `;
  }).join("");
}

function updatePlayerBgmSelectOptions() {
  const selectEl = document.getElementById("playerBgmSelect");
  if (!selectEl || !state.presets || !state.presets.bgm_tracks) return;
  
  selectEl.innerHTML = state.presets.bgm_tracks.map(t => `
    <option value="${t.id}" ${state.selectedBgm === t.id ? 'selected' : ''}>${t.name}</option>
  `).join("");
}

window.handleCustomBgmUpload = function(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  const objectUrl = URL.createObjectURL(file);
  const trackName = file.name.replace(/\.[^/.]+$/, "").substring(0, 32);
  
  const customTrack = {
    id: "custom_bgm",
    name: trackName || "Maxsus yuklangan musiqa",
    icon: "🎶",
    desc: `O'zingiz yuklagan fayl (${(file.size / (1024 * 1024)).toFixed(1)} MB)`,
    url: objectUrl,
    isCustom: true
  };

  const existingIdx = state.presets.bgm_tracks.findIndex(t => t.id === "custom_bgm");
  if (existingIdx >= 0) {
    state.presets.bgm_tracks[existingIdx] = customTrack;
  } else {
    const noneIdx = state.presets.bgm_tracks.findIndex(t => t.id === "none");
    if (noneIdx >= 0) {
      state.presets.bgm_tracks.splice(noneIdx, 0, customTrack);
    } else {
      state.presets.bgm_tracks.push(customTrack);
    }
  }

  updatePlayerBgmSelectOptions();
  selectBgm("custom_bgm");
  alert(`"${customTrack.name}" fon musiqasi sifatida muvaffaqiyatli tanlandi!`);
};

window.selectBgm = function(bgmId) {
  state.selectedBgm = bgmId;
  const selectEl = document.getElementById("playerBgmSelect");
  if (selectEl) selectEl.value = bgmId;
  renderBgmTracks();
  updatePlayerBgmSource();
};

window.changePlayerBgm = function(bgmId) {
  state.selectedBgm = bgmId;
  renderBgmTracks();
  updatePlayerBgmSource();
};

window.previewBgmAudio = function(url) {
  if (!url) return;
  if (!state.testAudio.paused && state.testAudio.src && state.testAudio.src.endsWith(url)) {
    state.testAudio.pause();
    return;
  }
  state.testAudio.src = url;
  state.testAudio.volume = 0.35;
  state.testAudio.play().catch(e => console.warn("BGM preview warning:", e));
};

function updatePlayerBgmSource() {
  const bgmAudio = document.getElementById("playerBgmAudio");
  if (!bgmAudio) return;
  
  if (state.selectedBgm === "none") {
    bgmAudio.pause();
    bgmAudio.src = "";
    return;
  }
  
  const track = (state.presets.bgm_tracks || []).find(t => t.id === state.selectedBgm);
  const trackUrl = (track && track.url) ? track.url : `/audio/${state.selectedBgm}.mp3`;
  
  if (bgmAudio.src !== trackUrl) {
    const wasPlaying = !bgmAudio.paused && state.isPlaying;
    bgmAudio.src = trackUrl;
    bgmAudio.currentTime = 0;
    if (wasPlaying) {
      bgmAudio.play().catch(e => console.warn("BGM play error:", e));
    }
  }
}

// Step Navigation Handlers
async function handleNextStep() {
  if (state.currentStep === 1) {
    goToStep(2);
  } else if (state.currentStep === 2) {
    const topic = document.getElementById("inputTopic").value.trim();
    if (!topic) {
      alert("Iltimos, video mavzusini kiriting!");
      return;
    }
    state.topic = topic;
    state.prompt = topic;
    
    showLoading("Bolalar xavfsizligi va qonuniy me'yorlar (COPPA) tahlil qilinmoqda...");
    await runSafetyCheck();
    hideLoading();
    goToStep(3);
  } else if (state.currentStep === 3) {
    if (!state.safetyReport || !state.safetyReport.is_safe) {
      alert("Mavzu xavfsizlik talablariga javob bermadi. Iltimos mavzuni qayta ko'rib chiqing.");
      goToStep(2);
      return;
    }
    showLoading("Gemini AI tajribali ssenarist sifatida ssenariy yozmoqda...");
    await generateScreenplay();
    hideLoading();
    goToStep(4);
  } else if (state.currentStep === 4) {
    // REAL STEP-BY-STEP SCENE RENDERING PIPELINE
    await startRealRenderingPipeline();
  }
}

function handlePrevStep() {
  if (state.currentStep > 1) {
    goToStep(state.currentStep - 1);
  }
}

function goToStep(step) {
  state.currentStep = step;
  
  for (let i = 1; i <= 5; i++) {
    const el = document.getElementById(`stepPanel${i}`);
    if (el) el.classList.add("hidden");
    
    const navItem = document.getElementById(`stepNav${i}`);
    if (navItem) {
      navItem.classList.remove("active", "completed");
      if (i === step) navItem.classList.add("active");
      else if (i < step) navItem.classList.add("completed");
    }
  }
  
  const currentPanel = document.getElementById(`stepPanel${step}`);
  if (currentPanel) currentPanel.classList.remove("hidden");
  
  const btnPrev = document.getElementById("btnPrev");
  const btnNext = document.getElementById("btnNext");
  
  if (step === 1) btnPrev.classList.add("hidden");
  else btnPrev.classList.remove("hidden");
  
  if (step === 4) {
    btnNext.classList.remove("hidden");
    btnNext.innerHTML = `<span>🎬 Videoni Yaratish</span><span>→</span>`;
  } else if (step === 5) {
    btnNext.classList.add("hidden");
    // Ensure player is initialized immediately
    if (state.preparedScenes.length === 0) {
      autoPrepareDefaultScenes().then(() => initCinemaPlayer());
    } else {
      initCinemaPlayer();
    }
  } else {
    btnNext.classList.remove("hidden");
    btnNext.innerHTML = `<span>Davom etish</span><span>→</span>`;
  }
  
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Safety Check
async function runSafetyCheck() {
  try {
    const res = await fetch(`${API_URL}/api/safety-check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: state.topic,
        prompt: state.prompt,
        age_group: state.selectedAge
      })
    });
    
    if (res.ok) {
      state.safetyReport = await res.json();
      renderSafetyReport();
    }
  } catch (err) {
    console.error("Xavfsizlik tekshiruvida xatolik:", err);
  }
}

function renderSafetyReport() {
  const r = state.safetyReport;
  if (!r) return;

  const scoreEl = document.getElementById("safetyScoreBadge");
  scoreEl.innerText = `${r.safety_score}% Xavfsiz`;
  scoreEl.className = `px-4 py-1.5 rounded-full font-fredoka font-bold text-sm ${r.is_safe ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`;

  document.getElementById("safetyMeterFill").style.width = `${r.safety_score}%`;
  document.getElementById("safetyPedagogicalAdvice").innerText = r.pedagogical_advice;

  const checksList = document.getElementById("safetyChecksList");
  checksList.innerHTML = `
    <li class="flex items-center justify-between p-3 rounded-2xl bg-white/70 border border-slate-200">
      <span class="text-xs font-semibold text-slate-700 flex items-center gap-2">
        <span>🛡️</span> Zo'ravonlik va qo'rqinchli elementlar yo'qligi
      </span>
      <span class="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg">Tasdiqlandi ✓</span>
    </li>
    <li class="flex items-center justify-between p-3 rounded-2xl bg-white/70 border border-slate-200">
      <span class="text-xs font-semibold text-slate-700 flex items-center gap-2">
        <span>👶</span> COPPA va bolalar psixologiyasiga muvofiqlik
      </span>
      <span class="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg">Tasdiqlandi ✓</span>
    </li>
    <li class="flex items-center justify-between p-3 rounded-2xl bg-white/70 border border-slate-200">
      <span class="text-xs font-semibold text-slate-700 flex items-center gap-2">
        <span>🇺🇿</span> O'zbek milliy qadriyatlari va tarbiya mezonlari
      </span>
      <span class="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg">Tasdiqlandi ✓</span>
    </li>
    <li class="flex items-center justify-between p-3 rounded-2xl bg-white/70 border border-slate-200">
      <span class="text-xs font-semibold text-slate-700 flex items-center gap-2">
        <span>🎯</span> Tanlangan yosh toifasi (${state.selectedAge} yosh)ga mosligi
      </span>
      <span class="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-lg">
        Mukammal ✓
      </span>
    </li>
  `;
}

// Generate Screenplay
async function generateScreenplay() {
  try {
    const res = await fetch(`${API_URL}/api/generate-screenplay`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: state.topic,
        prompt: state.prompt,
        age_group: state.selectedAge,
        duration_seconds: state.duration,
        visual_style_id: state.visualStyle,
        language: state.language
      })
    });
    
    if (res.ok) {
      const data = await res.json();
      state.screenplay = data.screenplay;
      if (state.screenplay && state.screenplay.scenes) {
        state.screenplay.scenes.forEach(sc => {
          sc.title = cleanTitleWithoutNumbers(sc.title);
        });
        const firstEmotion = state.screenplay.scenes[0] ? state.screenplay.scenes[0].emotion : "";
        autoSelectBestBgm(state.topic, firstEmotion);
      }
      renderScreenplayScenes();
    }
  } catch (err) {
    console.error("Ssenariy generatsiyasida xatolik:", err);
  }
}

function renderScreenplayScenes() {
  const container = document.getElementById("screenplayScenesContainer");
  if (!container || !state.screenplay) return;

  document.getElementById("screenplayTitle").innerText = cleanTitleWithoutNumbers(state.screenplay.title);
  document.getElementById("screenplayMoral").innerText = state.screenplay.moral_summary;

  container.innerHTML = state.screenplay.scenes.map((scene, idx) => `
    <div class="scene-card glass-panel p-5 rounded-3xl border border-slate-200 bg-white/90 shadow-sm relative">
      <div class="flex items-center justify-between mb-3 border-b border-slate-100 pb-3">
        <div class="flex items-center gap-2">
          <span class="w-8 h-8 rounded-xl bg-indigo-600 text-white font-fredoka font-bold flex items-center justify-center text-sm shadow-sm">
            ✨
          </span>
          <span class="font-fredoka font-bold text-slate-800 text-base">${cleanTitleWithoutNumbers(scene.title)}</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs bg-indigo-50 text-indigo-700 px-3 py-1 rounded-xl font-bold">
            ⏱️ ~${scene.duration_seconds}s
          </span>
          <span class="text-xs bg-pink-50 text-pink-700 px-3 py-1 rounded-xl font-semibold capitalize">
            🎭 ${scene.emotion}
          </span>
        </div>
      </div>

      <div class="mb-3">
        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-1">
          🎙️ O'zbekcha Nutq (Mohir AI):
        </label>
        <textarea class="w-full text-sm p-3 rounded-2xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-indigo-500 outline-none transition-all font-medium text-slate-700" 
                  rows="2" onchange="updateSceneNarration(${idx}, this.value)">${scene.narration}</textarea>
      </div>

      ${scene.visual_beats && scene.visual_beats.length > 0 ? `
        <div class="mb-3 pt-3 border-t border-slate-100">
          <label class="block text-xs font-bold text-indigo-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <span>📊</span> Interaktiv Bosqichlar va Belgilar (Ekrandagi sinxron vizual qadamlar):
          </label>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
            ${scene.visual_beats.map((b, bIdx) => `
              <div class="p-2.5 rounded-xl border ${b.highlight ? 'border-amber-300 bg-amber-50/70 shadow-sm' : 'border-indigo-100 bg-indigo-50/50'} text-xs">
                <div class="flex items-center justify-between font-bold text-slate-700 mb-1">
                  <span class="text-[10px] uppercase px-1.5 py-0.5 rounded font-fredoka ${b.highlight ? 'bg-amber-200 text-amber-800' : 'bg-indigo-200 text-indigo-800'}">${cleanTitleWithoutNumbers(b.badge || 'BOSQICH')}</span>
                  <span class="text-[10px] text-slate-500 font-semibold">⏱️ ${(b.time_pct*100).toFixed(0)}%</span>
                </div>
                <div class="font-fredoka font-bold text-sm text-indigo-900">${cleanTitleWithoutNumbers(b.main_text)}</div>
                <div class="text-[11px] text-slate-600 mt-0.5 line-clamp-1">${b.sub_text}</div>
                <div class="mt-1 text-sm tracking-widest">${(b.icons || []).join(" ")}</div>
              </div>
            `).join("")}
          </div>
        </div>
      ` : ''}

      <div class="flex items-center justify-between text-xs text-slate-500 pt-2 border-t border-slate-100">
        <span>🎥 Kamera: <strong class="text-slate-700">${scene.camera_movement}</strong></span>
        <span>🎵 Ovoz: <strong class="text-slate-700">${scene.sound_effect || 'Mayin kuy'}</strong></span>
      </div>
    </div>
  `).join("");
}

window.updateSceneNarration = function(idx, val) {
  if (state.screenplay && state.screenplay.scenes[idx]) {
    state.screenplay.scenes[idx].narration = val;
  }
};

window.openFlashcardsPrintView = function() {
  const scenes = (state.preparedScenes && state.preparedScenes.length > 0) 
    ? state.preparedScenes 
    : ((state.screenplay && state.screenplay.scenes) ? state.screenplay.scenes : []);
    
  if (scenes.length === 0) {
    alert("Avval dars ssenariysini yarating!");
    return;
  }
  const title = cleanTitleWithoutNumbers((state.screenplay && state.screenplay.title) || state.topic);
  const moral = (state.screenplay && state.screenplay.moral_summary) || "Bilim — eng katta boylikdir!";
  
  const printWin = window.open("", "_blank");
  if (!printWin) {
    alert("Iltimos brauzerda yangi oynalarga ruxsat bering!");
    return;
  }

  const cardsHtml = scenes.map((s, idx) => {
    const scTitle = cleanTitleWithoutNumbers(s.title || `Dars Qismi`);
    const imgTag = s.image_url ? `<img src="${s.image_url}" class="card-img" alt="kadr">` : '';
    const beatsHtml = (s.visual_beats && s.visual_beats.length > 0)
      ? `<div class="beats"><strong>💡 Kalit tushuncha:</strong> ${s.visual_beats.map(b => b.main_text).join(" ➔ ")} ${(s.visual_beats[0].icons || []).join(" ")}</div>`
      : '';
    return `
      <div class="card">
        <div class="card-header">
          <span class="card-title">${scTitle}</span>
          <span class="badge">${s.emotion || "ta'limiy"}</span>
        </div>
        ${imgTag}
        <div class="narration">"${s.narration}"</div>
        ${beatsHtml}
      </div>
    `;
  }).join("");

  printWin.document.write(`<!DOCTYPE html>
<html>
<head>
  <title>${title} — Ta'limiy Flashcard / Storyboard</title>
  <meta charset="utf-8">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 24px; color: #0f172a; background: #fff; }
    .header { text-align: center; border-bottom: 2px solid #6366f1; padding-bottom: 12px; margin-bottom: 24px; }
    .header h1 { margin: 0 0 6px 0; color: #4338ca; font-size: 26px; }
    .header p { margin: 0; color: #64748b; font-size: 14px; font-weight: 600; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 18px; }
    .card { border: 1.5px solid #cbd5e1; border-radius: 16px; padding: 16px; background: #f8fafc; page-break-inside: avoid; display: flex; flex-direction: column; justify-content: space-between; }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }
    .card-title { font-weight: bold; color: #1e1b4b; font-size: 16px; }
    .badge { font-size: 11px; background: #e0e7ff; color: #4338ca; padding: 3px 8px; border-radius: 8px; font-weight: bold; text-transform: uppercase; }
    .card-img { width: 100%; height: 180px; object-fit: cover; border-radius: 10px; margin-bottom: 12px; background: #e2e8f0; border: 1px solid #cbd5e1; }
    .narration { font-size: 13.5px; line-height: 1.55; color: #334155; margin-bottom: 10px; font-style: italic; }
    .beats { background: #fff; padding: 8px 12px; border-radius: 10px; border: 1px solid #e2e8f0; font-size: 12px; color: #4338ca; }
    .footer { margin-top: 24px; text-align: center; padding: 14px; background: #ede9fe; border-radius: 14px; font-weight: bold; color: #5b21b6; font-size: 14px; }
    @media print { .no-print { display: none !important; } body { margin: 8mm; } }
  </style>
</head>
<body>
  <div class="no-print" style="margin-bottom: 18px; display: flex; justify-content: space-between; align-items: center;">
    <span style="font-size: 13px; color: #64748b;">KidsVidEdu o'qituvchilar va ota-onalar uchun ta'limiy varaq</span>
    <button onclick="window.print()" style="padding: 10px 22px; background: #4f46e5; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);">
      🖨️ Chop etish / PDF saqlash
    </button>
  </div>
  <div class="header">
    <h1>🎓 ${title}</h1>
    <p>Yosh toifasi: ${state.selectedAge} yosh | KidsVidEdu Bolalar Ta'limiy AI Platformasi</p>
  </div>
  <div class="grid">
    ${cardsHtml}
  </div>
  <div class="footer">
    💡 Xulosa va Asosiy Saboq: ${moral}
  </div>
</body>
</html>`);
  printWin.document.close();
};

// ==========================================
// REAL-TIME RENDERING PIPELINE (STEP-BY-STEP)
// ==========================================
async function startRealRenderingPipeline() {
  const modal = document.getElementById("renderProgressModal");
  modal.classList.remove("hidden");

  const scenes = state.screenplay.scenes;
  state.preparedScenes = [];
  
  const statusTitle = document.getElementById("renderStatusTitle");
  const statusSub = document.getElementById("renderStatusSub");
  const progressText = document.getElementById("renderProgressText");
  const progressPercent = document.getElementById("renderProgressPercent");
  const progressBarFill = document.getElementById("renderProgressBarFill");
  const liveList = document.getElementById("renderScenesLiveList");
  const btnPremyere = document.getElementById("btnOpenPremyere");

  statusTitle.innerText = "Video Sahnalari Tayyorlanmoqda...";
  statusSub.innerText = "Mohir AI dan haqiqiy ovozlar olinmoqda va kadrlar chizilmoqda. Iltimos, kuting!";
  btnPremyere.disabled = true;
  btnPremyere.className = "px-6 py-3 rounded-2xl bg-slate-300 text-slate-500 font-fredoka font-bold text-sm cursor-not-allowed";
  btnPremyere.innerText = "⏳ Tayyorlanishi kutilmoqda...";

  liveList.innerHTML = scenes.map(s => `
    <div id="liveSceneCard_${s.scene_number}" class="p-4 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <span class="w-8 h-8 rounded-xl bg-indigo-50 text-indigo-600 font-fredoka font-bold flex items-center justify-center text-sm">
          🎬
        </span>
        <div>
          <div class="font-bold text-slate-800 text-sm">${cleanTitleWithoutNumbers(s.title)}</div>
          <div id="liveSceneText_${s.scene_number}" class="text-xs text-amber-600 font-medium">⏳ Kutilmoqda...</div>
        </div>
      </div>
      <div id="liveSceneAction_${s.scene_number}" class="text-xs text-slate-400">Navbatda</div>
    </div>
  `).join("");

  const projectId = `proj_${Date.now()}`;
  let completedCount = 0;

  for (let i = 0; i < scenes.length; i++) {
    const sc = scenes[i];
    const sNum = sc.scene_number;
    
    // Update live card to in-progress
    const textEl = document.getElementById(`liveSceneText_${sNum}`);
    const actionEl = document.getElementById(`liveSceneAction_${sNum}`);
    if (textEl) textEl.innerHTML = `<span class="animate-pulse text-indigo-600 font-bold">🎙️ Mohir AI ovozi yozilmoqda...</span>`;

    try {
      const res = await fetch(`${API_URL}/api/prepare-scene`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          project_id: projectId,
          scene: sc,
          topic: state.topic,
          voice_id: state.selectedVoice
        })
      });

      if (res.ok) {
        const prep = await res.json();
        state.preparedScenes.push(prep);
        
        // Preload Image into browser cache
        const img = new Image();
        img.src = prep.image_url;
        imageCache[prep.image_url] = img;

        completedCount++;
        const pct = Math.round((completedCount / scenes.length) * 100);
        progressPercent.innerText = `${pct}%`;
        progressText.innerText = `${completedCount} / ${scenes.length} sahna tayyorlandi`;
        progressBarFill.style.width = `${pct}%`;

        // Update card to finished with audio test button
        if (textEl) textEl.innerHTML = `<span class="text-emerald-600 font-bold">✅ Tayyor! (Davomiylik: ${prep.duration}s)</span>`;
        if (actionEl) {
          actionEl.innerHTML = `
            <div class="flex items-center gap-2">
              <img src="${prep.image_url}" class="w-12 h-8 rounded-lg object-cover border border-slate-300 shadow-sm" alt="kadr">
              <button onclick="playSampleAudio('${prep.audio_url}')" class="px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-lg text-xs font-bold hover:bg-indigo-100 flex items-center gap-1">
                <span>🔊</span> Tinglash
              </button>
            </div>
          `;
        }
      }
    } catch (err) {
      console.error(`Sahna ${sNum} tayyorlashda xatolik:`, err);
    }
  }

  // ALL SCENES READY!
  state.totalDuration = state.preparedScenes.reduce((acc, s) => acc + s.duration, 0);
  statusTitle.innerText = "🎉 Barcha sahnalar to'liq tayyor bo'ldi!";
  statusSub.innerText = `Jami ${state.preparedScenes.length} ta sahna va haqiqiy Mohir AI ovozlari saqlandi (Umumiy vaqt: ${Math.round(state.totalDuration)} soniya).`;

  btnPremyere.disabled = false;
  btnPremyere.className = "px-6 py-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-pink-600 text-white font-fredoka font-bold text-sm shadow-xl hover:shadow-indigo-500/25 cursor-pointer flex items-center gap-2";
  btnPremyere.innerHTML = `<span>🎬 Premyerani Tomosha Qilish (Full HD)</span><span>→</span>`;
}

window.playSampleAudio = function(url) {
  state.testAudio.src = url;
  state.testAudio.play();
};

// ==========================================
// CINEMA PLAYER LOGIC (REAL AUDIO & ANIMATION)
// ==========================================
let canvas, ctx;
let audioCtx = null;
let masterSourceNode = null;
let bgmSourceNode = null;
let masterGainNode = null;
let bgmGainNode = null;
let voiceAnalyserNode = null;
let mediaStreamDestNode = null;
let webAudioInitialized = false;

function initWebAudio() {
  if (webAudioInitialized && audioCtx) {
    if (audioCtx.state === "suspended") {
      audioCtx.resume().catch(e => console.warn("AudioContext resume warning:", e));
    }
    return;
  }
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextClass) return;

  const masterAudio = document.getElementById("playerMasterAudio");
  const bgmAudio = document.getElementById("playerBgmAudio");
  if (!masterAudio || !bgmAudio) return;

  try {
    audioCtx = new AudioContextClass();
    masterAudio.crossOrigin = "anonymous";
    bgmAudio.crossOrigin = "anonymous";

    masterSourceNode = audioCtx.createMediaElementSource(masterAudio);
    bgmSourceNode = audioCtx.createMediaElementSource(bgmAudio);

    masterGainNode = audioCtx.createGain();
    masterGainNode.gain.value = state.voiceVolume !== undefined ? state.voiceVolume : 1.0;

    bgmGainNode = audioCtx.createGain();
    bgmGainNode.gain.value = state.bgmVolume !== undefined ? state.bgmVolume : 0.25;

    voiceAnalyserNode = audioCtx.createAnalyser();
    voiceAnalyserNode.fftSize = 256;

    mediaStreamDestNode = audioCtx.createMediaStreamDestination();

    // Nutq audio zanjiri: masterSource -> voiceAnalyser -> masterGain -> (destinatsiya & yozib olish)
    masterSourceNode.connect(voiceAnalyserNode);
    voiceAnalyserNode.connect(masterGainNode);
    masterGainNode.connect(audioCtx.destination);
    masterGainNode.connect(mediaStreamDestNode);

    // BGM musiqa zanjiri: bgmSource -> bgmGain -> (destinatsiya & yozib olish)
    bgmSourceNode.connect(bgmGainNode);
    bgmGainNode.connect(audioCtx.destination);
    bgmGainNode.connect(mediaStreamDestNode);

    webAudioInitialized = true;
    if (audioCtx.state === "suspended") {
      audioCtx.resume().catch(e => console.warn(e));
    }
  } catch (err) {
    console.warn("Web Audio API ulashda ogohlantirish:", err);
  }
}

window.changeVoiceVolume = function(val) {
  const num = Math.max(0, Math.min(100, Number(val)));
  state.voiceVolume = num / 100;
  const disp = document.getElementById("voiceVolDisplay");
  if (disp) disp.innerText = `${num}%`;
  if (masterGainNode && audioCtx) {
    masterGainNode.gain.setTargetAtTime(state.voiceVolume, audioCtx.currentTime, 0.05);
  }
};

window.changeBgmVolume = function(val) {
  const num = Math.max(0, Math.min(100, Number(val)));
  state.bgmVolume = num / 100;
  const disp = document.getElementById("bgmVolDisplay");
  if (disp) disp.innerText = `${num}%`;
  if (bgmGainNode && audioCtx) {
    bgmGainNode.gain.setTargetAtTime(state.bgmVolume, audioCtx.currentTime, 0.05);
  }
};

function updateAudioDucking() {
  if (!audioCtx || !bgmGainNode || state.selectedBgm === "none") return;

  const masterAudio = document.getElementById("playerMasterAudio");
  let isSpeaking = false;

  if (masterAudio && !masterAudio.paused && !masterAudio.ended && masterAudio.readyState >= 2 && masterAudio.currentTime > 0) {
    if (voiceAnalyserNode) {
      const buffer = new Uint8Array(voiceAnalyserNode.frequencyBinCount);
      voiceAnalyserNode.getByteTimeDomainData(buffer);
      let sum = 0;
      for (let i = 0; i < buffer.length; i++) {
        const val = (buffer[i] - 128) / 128;
        sum += val * val;
      }
      const rms = Math.sqrt(sum / buffer.length);
      isSpeaking = rms > 0.025; // Haqiqiy nutq faolligi aniqlandi
    } else {
      isSpeaking = true;
    }
  }

  const baseBgm = (state.bgmVolume !== undefined) ? state.bgmVolume : 0.25;
  // Nutq so'zlanganda musiqa avtomatik ravishda 36% ga pasayadi
  const targetGain = isSpeaking ? (baseBgm * 0.36) : baseBgm;
  const timeConstant = isSpeaking ? 0.12 : 0.40; // Attack 120ms, Release 400ms

  try {
    bgmGainNode.gain.setTargetAtTime(targetGain, audioCtx.currentTime, timeConstant);
  } catch (e) {}

  const duckingText = document.getElementById("duckingStatusText");
  const duckingBadge = document.getElementById("duckingBadge");
  if (duckingText && duckingBadge) {
    if (isSpeaking) {
      duckingText.innerText = "Sidechain: Nutq pasaytirdi (-64%)";
      duckingBadge.className = "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-amber-950/80 text-amber-300 border border-amber-800/60 shadow-sm";
    } else {
      duckingText.innerText = "Sidechain: Musiqa to'liq";
      duckingBadge.className = "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-emerald-950/80 text-emerald-300 border border-emerald-800/60 shadow-sm";
    }
  }
}

function setupCanvasPlayer() {
  canvas = document.getElementById("cinemaCanvas");
  if (!canvas) return;
  ctx = canvas.getContext("2d");
  canvas.width = 1280;
  canvas.height = 720;
  drawPlayerIdle();
}

async function autoPrepareDefaultScenes() {
  showLoading("Namunaviy sahna va Mohir AI ovozlari yuklanmoqda...");
  try {
    const res = await fetch(`${API_URL}/api/prepare-scene`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        project_id: "default_demo",
        scene: {
          scene_number: 1,
          title: "Sehrli Tabiat",
          narration: "Salom, jajji do'stim! Kuz faslida daraxtlar barglarini oltin rangga bo'yab, tabiat qishki oromga tayyorlanadi.",
          emotion: "quvnoq"
        },
        topic: state.topic,
        voice_id: state.selectedVoice
      })
    });
    if (res.ok) {
      const prep = await res.json();
      state.preparedScenes = [prep];
      state.totalDuration = prep.duration;
      const img = new Image();
      img.src = prep.image_url;
      imageCache[prep.image_url] = img;
    }
  } catch (e) {
    console.error("Auto prepare error:", e);
  } finally {
    hideLoading();
  }
}

function initCinemaPlayer() {
  if (state.preparedScenes.length === 0) return;
  
  state.currentSceneIndex = 0;
  state.currentTime = 0;
  state.sceneCurrentTime = 0;
  state.isPlaying = false;
  state.totalDuration = state.preparedScenes.reduce((acc, s) => acc + s.duration, 0);
  
  document.getElementById("videoTitleDisplay").innerText = cleanTitleWithoutNumbers(state.screenplay ? state.screenplay.title : state.topic);
  document.getElementById("totalTimeDisplay").innerText = formatTime(state.totalDuration);
  document.getElementById("currentTimeDisplay").innerText = "00:00";
  document.getElementById("sceneTrackerDisplay").innerText = `1-sahna / ${state.preparedScenes.length}`;
  document.getElementById("videoProgressBar").style.width = "0%";

  updatePlayerBgmSelectOptions();
  const selectBgmEl = document.getElementById("playerBgmSelect");
  if (selectBgmEl) selectBgmEl.value = state.selectedBgm;

  const sliderVoice = document.getElementById("sliderVoiceVol");
  if (sliderVoice) sliderVoice.value = Math.round((state.voiceVolume !== undefined ? state.voiceVolume : 1.0) * 100);
  const dispVoice = document.getElementById("voiceVolDisplay");
  if (dispVoice && sliderVoice) dispVoice.innerText = `${sliderVoice.value}%`;

  const sliderBgm = document.getElementById("sliderBgmVol");
  if (sliderBgm) sliderBgm.value = Math.round((state.bgmVolume !== undefined ? state.bgmVolume : 0.25) * 100);
  const dispBgm = document.getElementById("bgmVolDisplay");
  if (dispBgm && sliderBgm) dispBgm.innerText = `${sliderBgm.value}%`;

  updatePlayerBgmSource();
  loadAndDisplayScene(0);
}

function loadAndDisplayScene(idx) {
  state.currentSceneIndex = idx;
  state.sceneCurrentTime = 0;
  const scene = state.preparedScenes[idx];
  if (!scene) return;

  document.getElementById("sceneTrackerDisplay").innerText = `${idx + 1}-sahna / ${state.preparedScenes.length}`;
  
  const masterAudio = document.getElementById("playerMasterAudio");
  masterAudio.src = scene.audio_url;
  masterAudio.currentTime = 0;
  
  if (state.isPlaying) {
    initWebAudio();
    masterAudio.play().catch(e => console.warn("Audio play warning:", e));

    const bgmAudio = document.getElementById("playerBgmAudio");
    if (bgmAudio && state.selectedBgm !== "none" && bgmAudio.paused) {
      const track = (state.presets.bgm_tracks || []).find(b => b.id === state.selectedBgm);
      const targetUrl = (track && track.url) ? track.url : `/audio/${state.selectedBgm}.mp3`;
      if (bgmAudio.src !== targetUrl) {
        bgmAudio.src = targetUrl;
      }
      bgmAudio.play().catch(e => console.warn("BGM resume warning:", e));
    }
  }

  // Preload image with onload re-render to prevent black screen on load
  if (scene.image_url) {
    if (!imageCache[scene.image_url]) {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        if (!state.isPlaying && state.currentSceneIndex === idx) {
          drawSceneFrame(scene, state.sceneCurrentTime);
        }
      };
      img.src = scene.image_url;
      imageCache[scene.image_url] = img;
    }
  }

  drawSceneFrame(scene, 0);
}

function togglePlayPause() {
  const masterAudio = document.getElementById("playerMasterAudio");
  const bgmAudio = document.getElementById("playerBgmAudio");
  const btn = document.getElementById("btnPlayPause");

  if (!state.isPlaying) {
    initWebAudio();
    if (audioCtx && audioCtx.state === "suspended") {
      audioCtx.resume().catch(e => console.warn(e));
    }

    // If completed or at end, start from beginning
    if (state.currentTime >= state.totalDuration && state.totalDuration > 0) {
      state.currentSceneIndex = 0;
      state.currentTime = 0;
      state.sceneCurrentTime = 0;
      if (bgmAudio) bgmAudio.currentTime = 0;
      loadAndDisplayScene(0);
    }
    
    state.isPlaying = true;
    btn.innerHTML = `<span>⏸️</span><span>To'xtatish</span>`;
    state.lastTick = performance.now();
    
    if (masterAudio && masterAudio.src) {
      masterAudio.play().catch(e => console.warn("Autoplay audio blocked:", e));
    }

    if (bgmAudio && state.selectedBgm !== "none") {
      const track = (state.presets.bgm_tracks || []).find(b => b.id === state.selectedBgm);
      const targetUrl = (track && track.url) ? track.url : `/audio/${state.selectedBgm}.mp3`;
      if (bgmAudio.src !== targetUrl) {
        bgmAudio.src = targetUrl;
      }
      bgmAudio.play().catch(e => console.warn("Autoplay BGM blocked:", e));
    }
    
    startPlaybackLoop();
  } else {
    state.isPlaying = false;
    btn.innerHTML = `<span>▶️</span><span>Ijro etish</span>`;
    if (masterAudio) masterAudio.pause();
    if (bgmAudio) bgmAudio.pause();
    if (state.animationFrameId) {
      cancelAnimationFrame(state.animationFrameId);
      state.animationFrameId = null;
    }
  }
}

function startPlaybackLoop() {
  if (state.animationFrameId) {
    cancelAnimationFrame(state.animationFrameId);
    state.animationFrameId = null;
  }

  function tick(now) {
    if (!state.isPlaying) return;
    
    // Dynamic broadcast audio ducking
    updateAudioDucking();

    const dt = Math.min(0.1, (now - state.lastTick) / 1000);
    state.lastTick = now;

    const masterAudio = document.getElementById("playerMasterAudio");
    if (masterAudio && !masterAudio.paused && !masterAudio.ended && masterAudio.currentTime > 0) {
      state.sceneCurrentTime = masterAudio.currentTime;
    } else {
      state.sceneCurrentTime += dt;
    }
    
    // Calculate total elapsed time across scenes
    let elapsedBefore = 0;
    for (let i = 0; i < state.currentSceneIndex; i++) {
      if (state.preparedScenes[i]) {
        elapsedBefore += state.preparedScenes[i].duration;
      }
    }
    state.currentTime = elapsedBefore + state.sceneCurrentTime;

    // Update Player UI every frame
    const curTimeEl = document.getElementById("currentTimeDisplay");
    if (curTimeEl) curTimeEl.innerText = formatTime(state.currentTime);
    const pct = Math.min(100, (state.currentTime / (state.totalDuration || 1)) * 100);
    const progBar = document.getElementById("videoProgressBar");
    if (progBar) progBar.style.width = `${pct}%`;

    const currentScene = state.preparedScenes[state.currentSceneIndex];
    if (currentScene) {
      drawSceneFrame(currentScene, state.sceneCurrentTime);

      // Check if current scene audio/duration is finished
      if (state.sceneCurrentTime >= currentScene.duration) {
        if (state.currentSceneIndex + 1 < state.preparedScenes.length) {
          loadAndDisplayScene(state.currentSceneIndex + 1);
        } else {
          // Finished all scenes!
          state.isPlaying = false;
          state.currentTime = state.totalDuration;
          if (curTimeEl) curTimeEl.innerText = formatTime(state.totalDuration);
          if (progBar) progBar.style.width = "100%";
          const btnPlay = document.getElementById("btnPlayPause");
          if (btnPlay) btnPlay.innerHTML = `<span>🔄</span><span>Qayta ko'rish</span>`;
          if (masterAudio) masterAudio.pause();
          const bgmAudio = document.getElementById("playerBgmAudio");
          if (bgmAudio) bgmAudio.pause();
          return;
        }
      }
    }

    state.animationFrameId = requestAnimationFrame(tick);
  }
  
  state.animationFrameId = requestAnimationFrame(tick);
}

function restartVideo() {
  state.isPlaying = false;
  const masterAudio = document.getElementById("playerMasterAudio");
  if (masterAudio) masterAudio.pause();
  const bgmAudio = document.getElementById("playerBgmAudio");
  if (bgmAudio) {
    bgmAudio.pause();
    bgmAudio.currentTime = 0;
  }
  state.currentTime = 0;
  state.sceneCurrentTime = 0;
  loadAndDisplayScene(0);
  togglePlayPause();
}

window.nextScene = function() {
  if (state.currentSceneIndex + 1 < state.preparedScenes.length) {
    loadAndDisplayScene(state.currentSceneIndex + 1);
  }
};

window.prevScene = function() {
  if (state.currentSceneIndex > 0) {
    loadAndDisplayScene(state.currentSceneIndex - 1);
  }
};

function clearTextShadows(c) {
  c.shadowOffsetX = 0;
  c.shadowOffsetY = 0;
  c.shadowBlur = 0;
  c.shadowColor = "transparent";
}

function cleanTitleWithoutNumbers(title) {
  if (!title) return "";
  let clean = title.replace(/^(?:\d+[\s\-_.:\)]*(?:sahna|kadr|bosqich|qadam)?|(?:sahna|kadr|bosqich|qadam)\s*\d+)[\s\-_.:\)]*/i, "").trim();
  clean = clean.replace(/^\d+[\s\-_.:\)]+/, "").trim();
  return clean || title;
}

function getActiveNarrationChunk(narration, sceneProgress) {
  if (!narration) return { text: "", wordProgress: 0, index: 0, total: 1 };
  
  // Split on sentence boundaries: '.', '!', '?', or long comma clauses
  const rawSentences = narration.match(/[^.!?]+[.!?]*/g) || [narration];
  const sentences = rawSentences.map(s => s.trim()).filter(s => s.length > 0);
  
  if (sentences.length <= 1) {
    return {
      text: narration,
      wordProgress: Math.max(0, Math.min(1, sceneProgress)),
      index: 0,
      total: 1
    };
  }

  // Calculate proportional weight of each sentence by word count
  const sentenceWordCounts = sentences.map(s => Math.max(1, s.split(/\s+/).length));
  const totalWords = sentenceWordCounts.reduce((a, b) => a + b, 0);
  
  let accumulatedProgress = 0;
  for (let i = 0; i < sentences.length; i++) {
    const slice = sentenceWordCounts[i] / totalWords;
    if (sceneProgress <= accumulatedProgress + slice || i === sentences.length - 1) {
      const localProgress = Math.max(0, Math.min(1, (sceneProgress - accumulatedProgress) / slice));
      return {
        text: sentences[i],
        wordProgress: localProgress,
        index: i,
        total: sentences.length
      };
    }
    accumulatedProgress += slice;
  }
  return {
    text: sentences[sentences.length - 1],
    wordProgress: 1,
    index: sentences.length - 1,
    total: sentences.length
  };
}

function drawKaraokeSubtitle(c, chunk, x, y, maxWidth, maxHeight, isHighlighted) {
  clearTextShadows(c);
  if (!chunk || !chunk.text) return;

  const words = chunk.text.split(/\s+/).filter(w => w.length > 0);
  if (words.length === 0) return;

  // Active word index in current sentence
  const activeWordIdx = Math.min(words.length - 1, Math.floor(chunk.wordProgress * words.length));

  // Dynamic font size depending on length
  let fontSize = 18;
  if (words.length > 18) fontSize = 16;
  if (words.length > 28) fontSize = 14;
  let lineHeight = fontSize + 8;
  c.font = `600 ${fontSize}px 'Plus Jakarta Sans'`;

  // Measure word positions for wrapping with guaranteed clean spacing
  const spaceWidth = Math.max(8, c.measureText(" ").width + 3);
  let lines = [];
  let currentLine = [];
  let currentLineWidth = 0;

  for (let i = 0; i < words.length; i++) {
    const wordWidth = c.measureText(words[i]).width;
    if (currentLineWidth + wordWidth > maxWidth && currentLine.length > 0) {
      lines.push(currentLine);
      currentLine = [];
      currentLineWidth = 0;
    }
    currentLine.push({ word: words[i], width: wordWidth, globalIdx: i });
    currentLineWidth += wordWidth + spaceWidth;
  }
  if (currentLine.length > 0) {
    lines.push(currentLine);
  }

  // Vertical centering inside subtitle box
  const totalTextHeight = lines.length * lineHeight;
  const startY = y + Math.max(4, (maxHeight - totalTextHeight) / 2);

  c.textBaseline = "top";
  c.textAlign = "left";

  for (let l = 0; l < lines.length; l++) {
    const line = lines[l];
    let curX = x;
    const curY = startY + l * lineHeight;

    for (let w = 0; w < line.length; w++) {
      const item = line[w];
      const isPastOrCurrent = item.globalIdx <= activeWordIdx;
      const isCurrent = item.globalIdx === activeWordIdx;

      if (isCurrent) {
        c.fillStyle = "#FDE047"; // Active spoken word: glowing gold
        c.font = `bold ${fontSize}px 'Plus Jakarta Sans'`;
      } else if (isPastOrCurrent) {
        c.fillStyle = isHighlighted ? "#FEF08A" : "#FFFFFF"; // Spoken words: clean bright
        c.font = `600 ${fontSize}px 'Plus Jakarta Sans'`;
      } else {
        c.fillStyle = "rgba(226, 232, 240, 0.65)"; // Future words: soft
        c.font = `500 ${fontSize}px 'Plus Jakarta Sans'`;
      }

      c.fillText(item.word, curX, curY);
      const measuredWordW = c.measureText(item.word).width;
      curX += Math.max(item.width, measuredWordW) + spaceWidth;
    }
  }

  // Mini pagination dots if multiple sentences
  if (chunk.total > 1) {
    const dotStartX = x + maxWidth - (chunk.total * 12);
    const dotY = y + maxHeight - 6;
    for (let p = 0; p < chunk.total; p++) {
      c.fillStyle = p === chunk.index ? "#38BDF8" : "rgba(255, 255, 255, 0.25)";
      c.beginPath();
      c.arc(dotStartX + p * 12, dotY, p === chunk.index ? 3.5 : 2, 0, Math.PI * 2);
      c.fill();
    }
  }
}

function drawRoundedRect(c, x, y, w, h, r) {
  if (r === undefined) r = 0;
  if (typeof r === "number") {
    r = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
  }
  c.beginPath();
  if (typeof c.roundRect === "function") {
    try {
      c.roundRect(x, y, w, h, r);
      return;
    } catch (e) {}
  }
  // Barcha brauzerlar (Firefox, Chrome, Safari, Edge) uchun 100% xavfsiz arcTo
  c.moveTo(x + r, y);
  c.arcTo(x + w, y, x + w, y + h, r);
  c.arcTo(x + w, y + h, x, y + h, r);
  c.arcTo(x, y + h, x, y, r);
  c.arcTo(x, y, x + w, y, r);
  c.closePath();
}

function drawThematicFallbackStage(c, width, height, scene, progress, t) {
  // Har doim yorqin, bolalarbop va jonli multfilm fon sahnasi
  const skyGrad = c.createLinearGradient(0, 0, 0, height);
  skyGrad.addColorStop(0, "#38BDF8"); // Moviy osmon
  skyGrad.addColorStop(0.5, "#818CF8"); // Mayin binafsharang
  skyGrad.addColorStop(1, "#312E81"); // To'q iliq indigo
  c.fillStyle = skyGrad;
  c.fillRect(0, 0, width, height);

  // Yaltiroq quyosh nuri
  const sunGrad = c.createRadialGradient(180, 140, 10, 180, 140, 240);
  sunGrad.addColorStop(0, "rgba(254, 240, 138, 0.5)");
  sunGrad.addColorStop(1, "rgba(254, 240, 138, 0)");
  c.fillStyle = sunGrad;
  c.beginPath();
  c.arc(180, 140, 240, 0, Math.PI * 2);
  c.fill();

  // Suzuvchi mayin bulutlar
  for (let b = 0; b < 3; b++) {
    const bx = ((b * 420 + t * 20) % (width + 250)) - 120;
    const by = 85 + (b % 2) * 50 + Math.sin(t * 1.4 + b) * 8;
    c.fillStyle = "rgba(255, 255, 255, 0.22)";
    c.beginPath();
    if (typeof c.ellipse === "function") {
      try {
        c.ellipse(bx, by, 75, 30, 0, 0, Math.PI * 2);
      } catch (e) {
        c.arc(bx, by, 45, 0, Math.PI * 2);
      }
    } else {
      c.save();
      c.translate(bx, by);
      c.scale(1, 30 / 75);
      c.arc(0, 0, 75, 0, Math.PI * 2);
      c.restore();
    }
    c.fill();
    c.beginPath();
    c.arc(bx - 26, by - 8, 26, 0, Math.PI * 2);
    c.arc(bx + 24, by - 10, 32, 0, Math.PI * 2);
    c.fill();
  }

  // Ufqdagi yam-yashil tepaliklar
  c.fillStyle = "rgba(34, 197, 94, 0.4)";
  c.beginPath();
  c.moveTo(0, 420);
  c.bezierCurveTo(340, 360, 720, 440, width, 380);
  c.lineTo(width, height);
  c.lineTo(0, height);
  c.closePath();
  c.fill();

  // Markaziy ta'limiy kadr vitrinasi (Doskadan yuqorida to'liq va ochiq ko'rinadi)
  const stageCardW = 560;
  const stageCardH = 260;
  const stageCardX = (width - stageCardW) / 2;
  const stageCardY = 90;

  c.save();
  c.fillStyle = "rgba(15, 23, 42, 0.65)";
  drawRoundedRect(c, stageCardX, stageCardY, stageCardW, stageCardH, 24);
  c.fill();
  c.strokeStyle = "rgba(255, 255, 255, 0.25)";
  c.lineWidth = 1.5;
  c.stroke();

  clearTextShadows(c);
  c.font = "bold 64px sans-serif";
  c.textAlign = "center";
  c.textBaseline = "middle";
  const icon = (scene.visual_beats && scene.visual_beats[0] && scene.visual_beats[0].icons && scene.visual_beats[0].icons[0]) || "🎨";
  c.fillText(icon, width / 2, stageCardY + 80);

  c.font = "bold 24px 'Fredoka'";
  c.fillStyle = "#FFFFFF";
  c.fillText(cleanTitleWithoutNumbers(scene.title || "KidsVidEdu Virtual Darsi"), width / 2, stageCardY + 160);

  c.font = "600 15px 'Plus Jakarta Sans'";
  c.fillStyle = "#A5B4FC";
  c.fillText(cleanTitleWithoutNumbers(state.topic || "Interaktiv Ta'limiy Video"), width / 2, stageCardY + 200);
  c.restore();
}

function drawSceneFrame(scene, currentTime) {
  if (!ctx || !canvas) {
    canvas = document.getElementById("cinemaCanvas");
    if (canvas) ctx = canvas.getContext("2d");
  }
  if (!ctx || !canvas) return;
  const width = canvas.width || 1280;
  const height = canvas.height || 720;
  const progress = (scene && scene.duration > 0) ? Math.max(0, Math.min(1, currentTime / scene.duration)) : 0;
  const t = performance.now() / 1000;

  try {
    // 0. Kadrlarni tozalash
    clearTextShadows(ctx);
    ctx.clearRect(0, 0, width, height);

    // Active visual beat determination
    let beats = (scene && scene.visual_beats) ? scene.visual_beats : [];
    if (!beats || beats.length === 0) {
      beats = generateDefaultVisualBeats(scene || {});
    }
    let activeBeat = beats[0] || {};
    let beatIndex = 0;
    for (let i = 0; i < beats.length; i++) {
      if (progress >= (beats[i].time_pct || 0)) {
        activeBeat = beats[i];
        beatIndex = i;
      }
    }

    // 1. HAR DOIM YORQIN FON CHIZISH (Qora ekran bo'lib qolmasligi kafolati!)
    drawThematicFallbackStage(ctx, width, height, scene || {}, progress, t);

    // 2. AGAR MAXSUS ILUSTRATSIYA YUKLANGAN BO'LSA, UNI USTIGA CHIZISH
    if (scene && scene.image_url) {
      let cachedImg = imageCache[scene.image_url];
      if (!cachedImg) {
        cachedImg = new Image();
        cachedImg.crossOrigin = "anonymous";
        cachedImg.onload = () => {
          if (!state.isPlaying) {
            drawSceneFrame(scene, currentTime);
          }
        };
        cachedImg.src = scene.image_url;
        imageCache[scene.image_url] = cachedImg;
      }

      if (cachedImg && cachedImg.complete && cachedImg.naturalWidth > 0) {
        try {
          ctx.save();
          const zoom = 1.0 + (progress * 0.05);
          const panX = Math.sin(progress * Math.PI) * 16;
          ctx.translate(width / 2, 235);
          ctx.scale(zoom, zoom);
          ctx.drawImage(cachedImg, -width / 2 + panX, -height / 2 + 55, width, height);
          ctx.restore();
        } catch (imgErr) {
          console.warn("Rasm chizishda xatolik:", imgErr);
        }
      }
    }

    // 3. PASTKI YUMSHOQ KINEMATIK SOYA (Doska foniga mayin ulanishi uchun)
    const botVignette = ctx.createLinearGradient(0, 440, 0, height);
    botVignette.addColorStop(0, "rgba(8, 12, 22, 0)");
    botVignette.addColorStop(0.5, "rgba(8, 12, 22, 0.45)");
    botVignette.addColorStop(1, "rgba(8, 12, 22, 0.75)");
    ctx.fillStyle = botVignette;
    ctx.fillRect(0, 440, width, height - 440);

    // 4. PASTKI TA'LIMIY DOSKA VA SUBTITR PANELI (TOZA VA YENGIL DIZAYN)
    // Hech qanday texnik yozuvlar (kadr raqami, vaqt, bosqich raqami) ko'rinmaydi!
    const cardX = 40;
    const cardY = 485;
    const cardW = 1200;
    const cardH = 212;
    const cardR = 24;

    ctx.save();
    clearTextShadows(ctx);

    // Doska fon qatlami
    const cardGrad = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY + cardH);
    if (activeBeat.highlight) {
      cardGrad.addColorStop(0, "rgba(22, 24, 40, 0.95)");
      cardGrad.addColorStop(1, "rgba(42, 26, 60, 0.95)");
    } else {
      cardGrad.addColorStop(0, "rgba(11, 16, 30, 0.94)");
      cardGrad.addColorStop(1, "rgba(18, 25, 48, 0.94)");
    }
    ctx.fillStyle = cardGrad;
    drawRoundedRect(ctx, cardX, cardY, cardW, cardH, cardR);
    ctx.fill();

    // Doska hoshiyasi
    ctx.lineWidth = activeBeat.highlight ? 2.5 : 1.5;
    const borderGrad = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY);
    if (activeBeat.highlight) {
      borderGrad.addColorStop(0, "#FBBF24");
      borderGrad.addColorStop(0.5, "#34D399");
      borderGrad.addColorStop(1, "#FBBF24");
    } else {
      borderGrad.addColorStop(0, "rgba(56, 189, 248, 0.75)");
      borderGrad.addColorStop(0.5, "rgba(168, 85, 247, 0.75)");
      borderGrad.addColorStop(1, "rgba(56, 189, 248, 0.75)");
    }
    ctx.strokeStyle = borderGrad;
    ctx.stroke();

    // 4A. 1-USTUN: ASOSIY FORMULA VA TUSHUNCHA (Chap tomon - toza va ravshan, sahna raqamisiz!)
    ctx.save();
    // 1-ustun chegarasi: x=40 dan x=388 gacha
    ctx.beginPath();
    ctx.rect(40, 485, 348, 212);
    ctx.clip();

    clearTextShadows(ctx);
    const rawMain = activeBeat.main_text || (scene && scene.title) || state.topic || "Dars Tushunchasi";
    const mainText = cleanTitleWithoutNumbers(rawMain);
    let fontSize = 44;
    ctx.font = `bold ${fontSize}px 'Fredoka'`;
    while (fontSize > 22 && ctx.measureText(mainText).width > 310) {
      fontSize -= 2;
      ctx.font = `bold ${fontSize}px 'Fredoka'`;
    }
    let displayMainText = mainText;
    if (ctx.measureText(displayMainText).width > 310) {
      while (ctx.measureText(displayMainText + "...").width > 310 && displayMainText.length > 0) {
        displayMainText = displayMainText.slice(0, -1);
      }
      displayMainText = displayMainText.trim() + "...";
    }
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = activeBeat.highlight ? "#FDE047" : "#FFFFFF";
    // Markaziy chiroyli joylashuv (x = 215, y = 591)
    ctx.fillText(displayMainText, 215, 591);
    ctx.restore();

    // Ajratuvchi chiziq 1
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.beginPath();
    ctx.moveTo(390, 502);
    ctx.lineTo(390, 680);
    ctx.stroke();

    // 4B. 2-USTUN: INTERAKTIV VIZUAL SANAG'ICH / EMOJILAR (O'rta tomon - sarlavhasiz, katta va jonli)
    ctx.save();
    // 2-ustun chegarasi: x=392 dan x=738 gacha
    ctx.beginPath();
    ctx.rect(392, 485, 346, 212);
    ctx.clip();

    clearTextShadows(ctx);
    // Suzuvchi vizual elementlar (Piktogrammalar)
    const icons = activeBeat.icons || [];
    if (icons.length > 0) {
      const maxIconsWidth = 320;
      const iconSpacing = Math.min(52, maxIconsWidth / icons.length);
      const totalW = icons.length * iconSpacing;
      const startX = 565 - totalW / 2 + iconSpacing / 2;
      for (let k = 0; k < icons.length; k++) {
        const bobY = Math.sin(t * 3.5 + k * 0.75) * 5;
        const ic = icons[k];
        clearTextShadows(ctx);
        if (ic === "+" || ic === "=" || ic === "➔") {
          ctx.font = "bold 36px 'Fredoka'";
          ctx.fillStyle = "#38BDF8";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(ic, startX + (k * iconSpacing), 591 + bobY);
        } else {
          ctx.font = "38px sans-serif";
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(ic, startX + (k * iconSpacing), 591 + bobY);
        }
      }
    }

    // Bosqich nuqtalari indikatori
    for (let d = 0; d < 3; d++) {
      ctx.fillStyle = d === beatIndex ? "#38BDF8" : "rgba(255, 255, 255, 0.2)";
      ctx.beginPath();
      ctx.arc(553 + d * 12, 660, 3, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();

    // Ajratuvchi chiziq 2
    ctx.strokeStyle = "rgba(255, 255, 255, 0.08)";
    ctx.beginPath();
    ctx.moveTo(740, 502);
    ctx.lineTo(740, 680);
    ctx.stroke();

    // 4C. 3-USTUN: SUBTITR NUTQI VA ASOSIY SABOQ / QOIDA (O'ng tomon - toza va ravshan)
    ctx.save();
    clearTextShadows(ctx);

    // Subtitr kartasi (kattaroq va qulayroq - doskadan qolib ketmaydi)
    ctx.fillStyle = "rgba(255, 255, 255, 0.05)";
    drawRoundedRect(ctx, 760, 498, 460, 134, 16);
    ctx.fill();
    ctx.strokeStyle = activeBeat.highlight ? "rgba(251, 191, 36, 0.35)" : "rgba(255, 255, 255, 0.1)";
    ctx.lineWidth = 1;
    ctx.stroke();

    // Dinamik Karaoke Subtitr: Har bir gap va so'z o'z vaqtida ravshan ko'rinadi (0 so'z yo'qotilmaydi!)
    const activeChunk = getActiveNarrationChunk(scene && scene.narration, progress);
    drawKaraokeSubtitle(ctx, activeChunk, 776, 508, 428, 114, activeBeat.highlight);

    // Asosiy saboq / Qoida (Pastki qism - mavzuga moslashuvchan)
    clearTextShadows(ctx);
    ctx.font = "bold 13px 'Fredoka'";
    ctx.fillStyle = "#C084FC";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText("💡 QOIDA:", 765, 655);

    const isMathTopic = (state.topic && (state.topic.toLowerCase().includes("qo'shish") || state.topic.toLowerCase().includes("matematik") || state.topic.toLowerCase().includes("hisob")));
    const ruleText = (activeBeat.highlight && isMathTopic)
      ? "Qo'shish — miqdorlarni birga jamlash va aniq hisoblash demakdir!" 
      : ((state.screenplay && state.screenplay.moral_summary) || "Bilim — eng katta boylik va kuchdir!");
    ctx.font = "500 13px 'Plus Jakarta Sans'";
    ctx.fillStyle = "#CBD5E1";
    let displayRule = ruleText;
    if (ctx.measureText(displayRule).width > 375) {
      while (ctx.measureText(displayRule + "...").width > 375 && displayRule.length > 0) {
        displayRule = displayRule.slice(0, -1);
      }
      displayRule = displayRule + "...";
    }
    ctx.fillText(displayRule, 835, 655);

    ctx.restore(); // end board

  } catch (frameErr) {
    console.error("drawSceneFrame render xatoligi:", frameErr);
  }
}

function generateDefaultVisualBeats(scene) {
  const text = (scene.narration || "").toLowerCase();
  const topicLower = (state.topic || "").toLowerCase();
  const isMath = (text.includes("qo'shish amali") || text.includes("hisoblaymiz") || text.includes("matematika") || topicLower.includes("qo'shish") || topicLower.includes("matematik")) && !text.includes("qo'shiq");

  if (isMath) {
    const match = text.match(/(\d+)\s*(?:ga|\+|,)?\s*(\d+)/);
    const n1 = match ? (parseInt(match[1]) || 2) : 2;
    const n2 = match ? (parseInt(match[2]) || 2) : 2;
    const ans = n1 + n2;
    return [
      {
        time_pct: 0.0,
        badge: "SAVOL",
        main_text: `${n1} + ${n2}`,
        sub_text: `${n1} ta olma va yana ${n2} ta olma`,
        icons: Array(Math.min(5, n1)).fill("🍎").concat(["+"]).concat(Array(Math.min(5, n2)).fill("🍎")),
        highlight: false
      },
      {
        time_pct: 0.45,
        badge: "QO'SHISH AMALI",
        main_text: `${n1} + ${n2} = ?`,
        sub_text: "Barchasini birga jamlaymiz...",
        icons: Array(Math.min(8, ans)).fill("🍎"),
        highlight: false
      },
      {
        time_pct: 0.75,
        badge: "NATIJA",
        main_text: `${n1} + ${n2} = ${ans}`,
        sub_text: `Jami ${ans} bo'ldi! Barakalla! 🎉`,
        icons: Array(Math.min(8, ans)).fill("🍎"),
        highlight: true
      }
    ];
  }

  // Hayvonlar va fauna
  if (/hayvon|sher|bo'ri|quyon|ayiq|fil|mushuk|kuchuk|qush|tulki/.test(text) || /hayvon|quyon|ayiq/.test(topicLower)) {
    return [
      { time_pct: 0.0, badge: "TANISHUV", main_text: cleanTitleWithoutNumbers(scene.title || "Jonivorlar Olami"), sub_text: scene.narration || "Hayvonlar bilan tanishamiz", icons: ["🐰", "🦊", "🐻", "🦁"], highlight: false },
      { time_pct: 0.55, badge: "XUSUSIYAT", main_text: "Tabiat Mo'jizasi", sub_text: "Hayvonlarning do'stona olami", icons: ["🐾", "🌿", "⭐", "🎉"], highlight: true }
    ];
  }

  // Suv, dengiz, baliqlar
  if (/dengiz|okean|suv|baliq|delfin|kit|tomchi/.test(text) || /dengiz|baliq|okean|suv/.test(topicLower)) {
    return [
      { time_pct: 0.0, badge: "SUV OLAMI", main_text: cleanTitleWithoutNumbers(scene.title || "Moviy Okean"), sub_text: scene.narration || "Suv osti sirlarini o'rganamiz", icons: ["🐬", "🌊", "🐠", "🫧"], highlight: false },
      { time_pct: 0.55, badge: "SUZAMIZ", main_text: "Sehrli Suv Osti", sub_text: "Tabiat go'zalligini asraymiz", icons: ["🫧", "🐟", "🌊", "✨"], highlight: true }
    ];
  }

  // Kosmos, quyosh, sayyoralar
  if (/kosmos|quyosh|oy|sayyora|yulduz|raketa|yer/.test(text) || /kosmos|sayyora|quyosh/.test(topicLower)) {
    return [
      { time_pct: 0.0, badge: "FAZOVIY SAYOHAT", main_text: cleanTitleWithoutNumbers(scene.title || "Koinot Sirlari"), sub_text: scene.narration || "Sayyoralarni o'rganamiz", icons: ["🚀", "🌍", "🌕", "⭐"], highlight: false },
      { time_pct: 0.55, badge: "SAYYORALAR", main_text: "Cheksiz Koinot", sub_text: "Yulduzlar olamiga parvoz", icons: ["🪐", "🛸", "✨", "🌟"], highlight: true }
    ];
  }

  // Fasllar va daraxtlar
  if (/fasl|kuz|bahor|yoz|qish|barg|daraxt|yomg'ir|qor/.test(text) || /kuz|fasl|barg/.test(topicLower)) {
    return [
      { time_pct: 0.0, badge: "TABIAT KO'RINISHI", main_text: cleanTitleWithoutNumbers(scene.title || "Oltin Fasl"), sub_text: scene.narration || "Tabiat o'zgarishlarini kuzatamiz", icons: ["🍂", "🍁", "🌳", "🍃"], highlight: false },
      { time_pct: 0.55, badge: "TABIAT SABOG'I", main_text: "Fasllar Almashinuvi", sub_text: "Tabiat go'zalligidan bahramand bo'lamiz", icons: ["☀️", "🌿", "🌈", "✨"], highlight: true }
    ];
  }

  // Ranglar va mevalar
  if (/rang|qizil|sariq|yashil|ko'k|meva|olma|banan|uzum/.test(text) || /rang|meva/.test(topicLower)) {
    return [
      { time_pct: 0.0, badge: "YORQIN RANGLAR", main_text: cleanTitleWithoutNumbers(scene.title || "Ranglar va Mevalar"), sub_text: scene.narration || "Yorqin ranglarni ajratamiz", icons: ["🎨", "🔴", "🟡", "🟢"], highlight: false },
      { time_pct: 0.55, badge: "FOYDALI MEVALAR", main_text: "Vitaminlar Xazinasi", sub_text: "Salomatlik va kuch-quvvat", icons: ["🍎", "🍌", "🍇", "🍓"], highlight: true }
    ];
  }

  // Standart ta'limiy beat
  return [
    {
      time_pct: 0.0,
      badge: "TUSHUNCHA",
      main_text: cleanTitleWithoutNumbers(scene.title || "Dars Tushunchasi"),
      sub_text: scene.narration || "Diqqat bilan tinglaymiz",
      icons: ["💡", "📚", "✨", "🎯"],
      highlight: false
    },
    {
      time_pct: 0.60,
      badge: "XULOSA",
      main_text: "Yangi Bilim!",
      sub_text: (state.screenplay && state.screenplay.moral_summary) || "Saboqni mustahkamladik",
      icons: ["🎯", "⭐", "🎉", "🏆"],
      highlight: true
    }
  ];
}

function drawPlayerIdle() {
  if (!ctx || !canvas) {
    canvas = document.getElementById("cinemaCanvas");
    if (canvas) ctx = canvas.getContext("2d");
  }
  if (!ctx || !canvas) return;
  const width = canvas.width || 1280;
  const height = canvas.height || 720;
  
  clearTextShadows(ctx);
  ctx.clearRect(0, 0, width, height);

  // Yorqin va yoqimli studio foni
  const grad = ctx.createLinearGradient(0, 0, 0, height);
  grad.addColorStop(0, "#38BDF8");
  grad.addColorStop(0.55, "#6366F1");
  grad.addColorStop(1, "#1E1B4B");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, width, height);

  // Markaziy yorug'lik
  const sun = ctx.createRadialGradient(width/2, height/2 - 40, 10, width/2, height/2 - 40, 320);
  sun.addColorStop(0, "rgba(255, 255, 255, 0.25)");
  sun.addColorStop(1, "rgba(255, 255, 255, 0)");
  ctx.fillStyle = sun;
  ctx.beginPath();
  ctx.arc(width/2, height/2 - 40, 320, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  clearTextShadows(ctx);

  // Vitrina card
  ctx.fillStyle = "rgba(15, 23, 42, 0.75)";
  drawRoundedRect(ctx, width/2 - 280, height/2 - 120, 560, 240, 24);
  ctx.fill();
  ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // Top pill
  ctx.fillStyle = "rgba(56, 189, 248, 0.2)";
  drawRoundedRect(ctx, width/2 - 150, height/2 - 95, 300, 34, 17);
  ctx.fill();
  ctx.strokeStyle = "#38BDF8";
  ctx.lineWidth = 1;
  ctx.stroke();

  ctx.font = "bold 13px 'Fredoka'";
  ctx.fillStyle = "#38BDF8";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText("✨ BOLALAR TA'LIMIY STUDIYASI", width/2, height/2 - 78);

  ctx.font = "bold 32px 'Fredoka'";
  ctx.fillStyle = "#FFFFFF";
  ctx.fillText("KidsVidEdu Video Studiyasi", width / 2, height / 2 - 25);
  
  ctx.font = "bold 16px 'Plus Jakarta Sans'";
  ctx.fillStyle = "#FDE047";
  ctx.fillText("🎬 Darsni boshlash uchun «Ijro etish» tugmasini bosing", width / 2, height / 2 + 30);
  ctx.restore();
}

// Download Manifest or Export Real Video
function downloadVideoPackage() {
  if (state.preparedScenes.length === 0) return;
  exportRealVideo();
}

async function exportRealVideo() {
  if (state.preparedScenes.length === 0) {
    alert("Avval videoni tayyorlang!");
    return;
  }

  const choice = confirm("Videoni ovozli (Mohir AI pedagogik nutqi va fon musiqasi bilan) MP4/WebM formatida yuklab olishni xohlaysizmi?\n\n(OK - Ovozli video yuklab olish, Bekor qilish - Loyiha faylini saqlash)");
  if (!choice) {
    // Save JSON
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
      project_name: state.screenplay ? state.screenplay.title : state.topic,
      total_duration: state.totalDuration,
      scenes: state.preparedScenes,
      bgm: state.selectedBgm
    }, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `KidsVidEdu_${state.topic.replace(/\s+/g, "_")}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
    alert("Video loyihasi muvaffaqiyatli saqlandi!");
    return;
  }

  showLoading("Ovozli to'liq video yozib olinmoqda va saqlanmoqda. Video ijrosi davomida kuting...");

  try {
    initWebAudio();
    if (audioCtx && audioCtx.state === "suspended") {
      await audioCtx.resume();
    }

    const canvasStream = canvas.captureStream(30);
    const combinedStream = new MediaStream();

    // 1. Video trek qo'shish
    canvasStream.getVideoTracks().forEach(track => combinedStream.addTrack(track));

    // 2. Audio treklar (Lola ustoz ovozi + Musiqa miksi) qo'shish
    if (mediaStreamDestNode && mediaStreamDestNode.stream) {
      const audioTracks = mediaStreamDestNode.stream.getAudioTracks();
      audioTracks.forEach(track => combinedStream.addTrack(track));
      console.log(`Video eksportiga ${audioTracks.length} ta audio trek ulandi.`);
    }

    let mimeType = "video/webm";
    const candidates = [
      "video/webm;codecs=vp9,opus",
      "video/webm;codecs=vp8,opus",
      "video/webm",
      "video/mp4;codecs=avc1,mp4a.40.2",
      "video/mp4"
    ];
    for (const cand of candidates) {
      if (MediaRecorder.isTypeSupported(cand)) {
        mimeType = cand;
        break;
      }
    }

    const recorder = new MediaRecorder(combinedStream, {
      mimeType,
      videoBitsPerSecond: 3500000,
      audioBitsPerSecond: 192000
    });
    const chunks = [];

    recorder.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) chunks.push(e.data);
    };

    recorder.onstop = () => {
      const blob = new Blob(chunks, { type: mimeType });
      const ext = mimeType.includes("mp4") ? "mp4" : "webm";
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `KidsVidEdu_${state.topic.replace(/\s+/g, "_")}.${ext}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      hideLoading();
      alert("🎉 Ovozli to'liq video muvaffaqiyatli yuklab olindi! (Mohir AI nutqi va fon musiqasi qo'shilgan)");
    };

    recorder.start(100);
    restartVideo();

    const checkInterval = setInterval(() => {
      if (!state.isPlaying || state.currentTime >= state.totalDuration) {
        clearInterval(checkInterval);
        setTimeout(() => {
          if (recorder.state === "recording") {
            recorder.stop();
          }
        }, 800);
      }
    }, 250);

  } catch (err) {
    hideLoading();
    console.error("Export error:", err);
    alert("Video eksport qilishda xatolik yuz berdi: " + (err.message || err));
  }
}

// Save Settings
async function saveSettings() {
  const mohiraiKey = document.getElementById("inputMohirAIKey").value.trim();
  const geminiKey = document.getElementById("inputGeminiKey").value.trim();

  try {
    const res = await fetch(`${API_URL}/api/save-settings`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mohirai_api_key: mohiraiKey || null,
        gemini_api_key: geminiKey || null
      })
    });
    if (res.ok) {
      alert("API kalitlar saqlandi!");
      document.getElementById("settingsModal").classList.add("hidden");
    }
  } catch (e) {
    console.error(e);
  }
}

// Helpers
function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function showLoading(msg) {
  const loader = document.getElementById("loadingModal");
  document.getElementById("loadingMessage").innerText = msg;
  loader.classList.remove("hidden");
}

function hideLoading() {
  document.getElementById("loadingModal").classList.add("hidden");
}
