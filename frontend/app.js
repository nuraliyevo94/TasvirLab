// TasvirLab Platform - Client Application
const state = {
  currentStep: 1,
  selectedAge: "5-7",
  topic: "",
  prompt: "",
  duration: 45,
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
      { id: "2-4", title: "Kichkintoylar (2-4 yosh)", category: "Kichkintoylar", icon: "🧸", thumbnail: "/images/age_2_4.jpg", recommended_duration: 30, style_desc: "O'ta sodda so'zlar, yorqin ranglar, sekin va mehrli nutq." },
      { id: "5-7", title: "Bog'cha va Tayyorlov (5-7 yosh)", category: "Bog'cha va Tayyorlov", icon: "🎨", thumbnail: "/images/age_5_7.jpg", recommended_duration: 45, style_desc: "Qiziqarli savollar, multfilm qahramonlari, quvnoq ohang." },
      { id: "8-10", title: "Boshlang'ich Maktab (8-10 yosh)", category: "Boshlang'ich Maktab", icon: "🚀", thumbnail: "/images/age_8_10.jpg", recommended_duration: 60, style_desc: "Mantiqiy tushuntirish, qiziqarli faktlar, do'stona muloqot." },
      { id: "11-12", title: "Katta Bolalar (11-12 yosh)", category: "Katta Bolalar", icon: "🔬", thumbnail: "/images/age_11_12.jpg", recommended_duration: 75, style_desc: "Ilmiy asoslangan bilimlar, chuqurroq tahlil, qiziqarli saboqlar." },
      { id: "13-15", title: "O'smirlar (13-15 yosh)", category: "O'smirlar", icon: "💻", thumbnail: "/images/age_stem_13_15.jpg", recommended_duration: 150, style_desc: "Zamonaviy texnologiyalar, dasturlash va kasbga yo'naltirish." },
      { id: "16-19", title: "Yoshlar (16-19 yosh)", category: "Katta Sinf va Yoshlar", icon: "🎓", thumbnail: "/images/age_tech_16_19.jpg", recommended_duration: 180, style_desc: "Mustaqil hayot, to'g'ri kasb tanlash va kelajak rejalari." }
    ],
    visual_styles: [
      { id: "pixar_3d", name: "Yorqin 3D Multfilm", title: "Yorqin 3D Multfilm", desc: "Zamonaviy 3D animatsiya, yorqin ranglar", icon: "🎬", thumbnail: "/images/style_pixar_3d.jpg" },
      { id: "watercolor_2d", name: "Ertaknamo Mo'yqalam", title: "Ertaknamo Mo'yqalam", desc: "Sehrli kitob va ertaknamo uslub", icon: "✨", thumbnail: "/images/style_watercolor_2d.jpg" },
      { id: "ghibli_anime", name: "Mayin Tabiat va Quyosh", title: "Mayin Tabiat va Quyosh", desc: "Mayin tabiat manzaralari va quyosh nuri", icon: "🍃", thumbnail: "/images/style_ghibli_anime.jpg" },
      { id: "sci_fi_3d", name: "Koinot va Texnologiya", title: "Koinot va Texnologiya", desc: "Sayyoralar, robotlar va ilmiy kashfiyotlar", icon: "🪐", thumbnail: "/images/style_scifi_3d.jpg" },
      { id: "modern_flat", name: "Oddiy va Chiroyli Chizmalar", title: "Oddiy va Chiroyli Chizmalar", desc: "Tushunarli va yorqin tasvirlar", icon: "📊", thumbnail: "/images/style_modern_flat.jpg" }
    ],
    voices: [
      { id: "lola", name: "O'zbekcha Ovoz (Lola)", role: "Mehribon ustoz va ertakchi", gender: "female", recommended: true }
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
      // 1. Kichkintoylar (2-4 yosh)
      { id: "colors_fun", title: "Ranglarni birga o'rganamiz", prompt: "Qizil olma, sariq banan va yashil nok misolida ranglarni quvnoq o'rgatuvchi dars.", age_group: "2-4" },
      { id: "forest_animals", title: "O'rmondagi do'stlarimiz", prompt: "Quyoncha va ayiqvoyning do'stligi hamda o'rmon hayvonlari haqida mayin ertak darsi.", age_group: "2-4" },
      { id: "magic_polite_words", title: "Sehrli 'Rahmat' va 'Iltimos' so'zlari", prompt: "Kichkintoylar uchun shirin muomala, salom berish va rahmat aytish odobi haqida saboq.", age_group: "2-4" },
      { id: "morning_sunshine", title: "Quyosh uyg'ondi: Quvnoq ertalab", prompt: "Ertalab yuvinish, tishlarni tozalash va quvnoq badantarbiya haqida ertak dars.", age_group: "2-4" },
      { id: "farm_animal_sounds", title: "Uy hayvonlari va ularning ovozlari", prompt: "Kuchukcha, mushukcha va qo'zichoq ovozlarini kichkintoylarga tanishtiruvchi saboq.", age_group: "2-4" },

      // 2. Bog'cha va Tayyorlov (5-7 yosh)
      { id: "kindness_friends", title: "Do'stlik va ahillik odobi", prompt: "Bolalarga do'stlar bilan o'rtoqlashish, samimiy va ahil bo'lish haqida ibratli ertak darsi.", age_group: "5-7" },
      { id: "autumn_leaves", title: "Daraxtlar nega barg to'kadi?", prompt: "Kuz faslida daraxtlar nega barglarini oltin rangga bo'yab to'kishi va qishki uyqusi haqida samimiy dars.", age_group: "5-7" },
      { id: "water_cycle_intro", title: "Yomg'ir qayerdan keladi?", prompt: "Kichik suv tomchisining bulutlarga chiqib, yerga shifobaxsh yomg'ir bo'lib qaytishi haqida saboq.", age_group: "5-7" },
      { id: "bread_journey", title: "Non qanday dasturxonga keladi?", prompt: "Bug'doy donidan issiq va xushbo'y nonga qadar bo'lgan mashaqqatli mehnat haqida hikoya.", age_group: "5-7" },
      { id: "traffic_lights", title: "Yo'l harakati qoidalari: Svetofor", prompt: "Qizil, sariq va yashil chiroqlarning ma'nosi va ko'chani xavfsiz kesib o'tish qoidalari.", age_group: "5-7" },

      // 3. Boshlang'ich Maktab (8-10 yosh)
      { id: "solar_system", title: "Quyosh sistemasiga sayohat", prompt: "Sayyoralar, Quyosh va ularning fazoda aylanish sirlari haqida qiziqarli sayohat.", age_group: "8-10" },
      { id: "ocean_depths", title: "Okean tubidagi sirli hayot", prompt: "Moviy kitlar, rang-barang marjon riflari va dengiz mo'jizalari haqida dars.", age_group: "8-10" },
      { id: "reading_superpower", title: "Kitob o'qish qanday kuch beradi?", prompt: "Kitoblar inson tasavvurini qanday kengaytirishi va allomalar ilmi haqida suhbat.", age_group: "8-10" },
      { id: "honeybee_wonder", title: "Asalarilar uyasi va asal mo'jizasi", prompt: "Asalarilarning intizomi, tabiatni changlatishi va shirin asal tayyorlashi haqida biologik dars.", age_group: "8-10" },
      { id: "ulughbeg_astronomy", title: "Mirzo Ulug'bek va yulduzlar jadvali", prompt: "Samarqand rasadxonasida yulduzlarni xaritaga tushirgan buyuk alloma haqida tarixiy saboq.", age_group: "8-10" },

      // 4. Katta Bolalar (11-12 yosh)
      { id: "photosynthesis", title: "Fotosintez: Yaproq laboratoriyasi", prompt: "O'simliklar quyosh nuri orqali qanday toza kislorod ishlab chiqarishi va ekologiya sirlari.", age_group: "11-12" },
      { id: "gravity_secret", title: "Gravitatsiya kuchi va vaznsizlik", prompt: "Nega yer narsalarni tortadi va fazogirlar kosmosda qanday suzib yuradi?", age_group: "11-12" },
      { id: "human_brain_memory", title: "Inson miyasi qanday xotirlaydi?", prompt: "Neyronlar va xotira qanday ishlashi, bilimlarni tez va oson eslab qolish texnikasi.", age_group: "11-12" },
      { id: "electricity_basics", title: "Elektr energiyasi qanday hosil bo'ladi?", prompt: "Gidro va quyosh elektr stansiyalari, elektronlar oqimi va xavfsiz foydalanish.", age_group: "11-12" },
      { id: "ibn_sina_health", title: "Ibn Sino: Tabobat va sog'lom hayot", prompt: "Buyuk tabib Ibn Sinoning to'g'ri ovqatlanish, sport va salomatlik bo'yicha tavsiyalari.", age_group: "11-12" },

      // 5. O'smirlar (13-15 yosh)
      { id: "cyber_security", title: "Internetda xavfsizlik: Shaxsiy ma'lumotlarni asrash", prompt: "Internetda shaxsiy ma'lumotlarni asrash, firibgarlardan himoyalanish va mustahkam parollar tuzish.", age_group: "13-15" },
      { id: "ai_machine_learning", title: "Sun'iy intellekt qanday o'rganadi?", prompt: "Neyrotarmoqlar va sun'iy intellekt ma'lumotlardan qanday o'rganishi va insonlarga yordam berishi.", age_group: "13-15" },
      { id: "coding_logic_algorithms", title: "Dasturlash tili va algoritmlar", prompt: "Algoritmlar mantiqi, ketma-ketlik va kompyuterga buyruq berish san'ati.", age_group: "13-15" },
      { id: "time_management", title: "Vaqtni to'g'ri taqsimlash va unumdorlik", prompt: "O'smirlar uchun darslar va dam olishni to'g'ri rejalashtirish, vaqtni behuda sarflamaslik sirlari.", age_group: "13-15" },
      { id: "mars_space_exploration", title: "Kosmik kashfiyotlar va Marsga safar", prompt: "Mars sayyorasi, qizil tuproqdagi muz izlari va fazogirlarning kelajak rejalari.", age_group: "13-15" },

      // 6. Yoshlar (16-19 yosh)
      { id: "financial_literacy", title: "Moliyaviy savodxonlik va shaxsiy byudjet", prompt: "Pulni oqilona boshqarish, jamg'arma shakllantirish, tejash va birinchi daromadlar.", age_group: "16-19" },
      { id: "critical_thinking_media", title: "Tanqidiy fikrlash va yolg'on xabarlarni aniqlash", prompt: "Axborot oqimida ishonchli manbalarni topish, aldovlarga uchmaslik va mustaqil xulosa chiqarish.", age_group: "16-19" },
      { id: "future_careers", title: "Kelajak kasblari va to'g'ri yo'nalish tanlash", prompt: "Zamonaviy texnologiyalar davrida talab yuqori bo'lgan sohalar, hayotiy qobiliyatlar va kasbiy ko'nikmalar.", age_group: "16-19" },
      { id: "public_speaking", title: "Notiqlik san'ati va taqdimot siri", prompt: "Odamlar oldida ishonchli so'zlash, g'oyalarni chiroyli yetkazish va hayajonni yengish.", age_group: "16-19" },
      { id: "startup_innovation", title: "Yangi loyiha va foydali g'oyani boshlash", prompt: "Muammoni aniqlash, birinchi oddiy namunani yaratish va foydali loyihalarni boshlash qadamlari.", age_group: "16-19" }
    ]
  }
};

const API_URL = "";
const imageCache = {};

const AGE_THUMBNAILS = {
  "2-4": "/images/age_2_4.jpg",
  "5-7": "/images/age_5_7.jpg",
  "8-10": "/images/age_8_10.jpg",
  "11-12": "/images/age_11_12.jpg",
  "13-15": "/images/age_stem_13_15.jpg",
  "16-19": "/images/age_tech_16_19.jpg"
};

const STYLE_THUMBNAILS = {
  "pixar_3d": "/images/style_pixar_3d.jpg",
  "watercolor_2d": "/images/style_watercolor_2d.jpg",
  "disney_2d": "/images/style_watercolor_2d.jpg",
  "ghibli_anime": "/images/style_ghibli_anime.jpg",
  "sci_fi_3d": "/images/style_scifi_3d.jpg",
  "modern_flat": "/images/style_modern_flat.jpg"
};

// ==========================================
// SAHIFA BILDIRISHNOMALARI VA ESLATMALAR
// (Chrome tizim alert/dialoglari o'rnini bosuvchi qulay sahifa bildirishnomasi)
// ==========================================
window.showToast = function(message, type = "info", customTitle = null) {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const typeConfig = {
    success: {
      border: "border-emerald-200",
      bg: "bg-white",
      badge: "bg-emerald-500 text-white",
      icon: "✅",
      defaultTitle: "Muvaffaqiyatli",
      textColor: "text-emerald-950",
      subColor: "text-slate-600",
      ring: "ring-1 ring-emerald-400/30"
    },
    warning: {
      border: "border-amber-200",
      bg: "bg-white",
      badge: "bg-amber-500 text-white",
      icon: "⚠️",
      defaultTitle: "Eslatma",
      textColor: "text-amber-950",
      subColor: "text-slate-600",
      ring: "ring-1 ring-amber-400/30"
    },
    error: {
      border: "border-rose-200",
      bg: "bg-white",
      badge: "bg-rose-500 text-white",
      icon: "🚫",
      defaultTitle: "Xatolik",
      textColor: "text-rose-950",
      subColor: "text-slate-600",
      ring: "ring-1 ring-rose-400/30"
    },
    info: {
      border: "border-indigo-200",
      bg: "bg-white",
      badge: "bg-indigo-600 text-white",
      icon: "💡",
      defaultTitle: "Ma'lumot",
      textColor: "text-indigo-950",
      subColor: "text-slate-600",
      ring: "ring-1 ring-indigo-400/30"
    }
  };

  const cfg = typeConfig[type] || typeConfig.info;
  const title = customTitle || cfg.defaultTitle;

  const toast = document.createElement("div");
  toast.className = `pointer-events-auto flex items-start gap-3.5 p-4 rounded-2xl border ${cfg.border} ${cfg.bg} ${cfg.ring} shadow-xl transition-all duration-300 transform translate-x-12 opacity-0 relative overflow-hidden`;

  toast.innerHTML = `
    <span class="w-9 h-9 rounded-xl ${cfg.badge} flex items-center justify-center text-base font-bold shrink-0 shadow-sm mt-0.5">
      ${cfg.icon}
    </span>
    <div class="flex-1 pr-3">
      <div class="font-fredoka font-bold text-sm ${cfg.textColor}">${title}</div>
      <div class="text-xs ${cfg.subColor} mt-1 leading-relaxed whitespace-pre-line">${message}</div>
    </div>
    <button class="text-slate-300 hover:text-slate-500 text-base font-bold shrink-0 p-1 cursor-pointer transition-colors" onclick="this.parentElement.remove()">✕</button>
    <div class="toast-progress absolute bottom-0 left-0 right-0 h-1 bg-slate-100">
      <div class="h-full bg-gradient-to-r from-indigo-500 to-pink-500 transition-all duration-[4200ms] ease-linear w-full"></div>
    </div>
  `;

  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.remove("translate-x-12", "opacity-0");
    toast.classList.add("translate-x-0", "opacity-100");
    const bar = toast.querySelector(".toast-progress > div");
    if (bar) {
      setTimeout(() => { bar.style.width = "0%"; }, 50);
    }
  });

  const timer = setTimeout(() => {
    toast.classList.remove("translate-x-0", "opacity-100");
    toast.classList.add("translate-x-12", "opacity-0");
    setTimeout(() => { toast.remove(); }, 350);
  }, 4200);

  toast.addEventListener("mouseenter", () => clearTimeout(timer));
};

window.showNoticeModal = function(title, message, icon = "💡") {
  const modal = document.getElementById("noticeModal");
  if (!modal) return;
  document.getElementById("noticeModalTitle").innerText = title || "Eslatma";
  document.getElementById("noticeModalBody").innerText = message;
  document.getElementById("noticeModalIcon").innerText = icon;
  modal.classList.remove("hidden");
};

window.closeNoticeModal = function() {
  const modal = document.getElementById("noticeModal");
  if (modal) modal.classList.add("hidden");
};

// Chrome alert() tizim dialogini sahifa bildirishnomasiga o'tkazish
window.alert = function(msg) {
  if (!msg) return;
  const str = String(msg);
  if (str.includes("\n") || str.length > 90) {
    const icon = str.includes("🎉") ? "🎉" : (str.includes("⚠️") ? "⚠️" : "💡");
    window.showNoticeModal("Eslatma", str, icon);
  } else {
    let type = "info";
    if (str.includes("🎉") || str.includes("muvaffaqiyatli") || str.includes("saqlandi")) type = "success";
    else if (str.includes("xato") || str.includes("mos kelmadi")) type = "warning";
    else if (str.includes("Iltimos") || str.includes("kiriting")) type = "warning";
    window.showToast(str, type);
  }
};

window.toggleKeyVisibility = function(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.style.webkitTextSecurity === "none") {
    input.style.webkitTextSecurity = "disc";
    btn.innerText = "👁️";
  } else {
    input.style.webkitTextSecurity = "none";
    btn.innerText = "🙈";
  }
};

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
  await initAuthAndUser();
  updateMyVideosBadge();
});

// Load Presets
async function loadPresets() {
  try {
    const res = await fetch(`${API_URL}/api/presets`);
    if (res.ok) {
      const data = await res.json();
      if (data && data.age_groups) {
        data.age_groups.forEach(a => {
          if (!a.thumbnail) a.thumbnail = AGE_THUMBNAILS[a.id] || "/images/age_5_7.jpg";
        });
        if (data.visual_styles) {
          data.visual_styles.forEach(s => {
            if (!s.thumbnail) s.thumbnail = STYLE_THUMBNAILS[s.id] || "/images/style_pixar_3d.jpg";
          });
        }
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

  const inputTopic = document.getElementById("inputTopic");
  if (inputTopic) {
    inputTopic.addEventListener("input", (e) => {
      state.topic = e.target.value.trim();
      state.prompt = e.target.value.trim();
      renderSampleTopics();
    });
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

  container.innerHTML = state.presets.age_groups.map(age => {
    const thumbUrl = age.thumbnail || AGE_THUMBNAILS[age.id] || "/images/age_5_7.jpg";
    const isSelected = state.selectedAge === age.id;
    return `
    <div class="age-card glass-panel rounded-3xl overflow-hidden p-3.5 transition-all flex flex-col justify-between ${isSelected ? 'active ring-4 ring-indigo-200' : 'hover:shadow-lg'}" 
         onclick="selectAge('${age.id}')">
      <!-- 1. Sof, toza 3D rasm (ustida hech qanday yozuv yo'q) -->
      <div class="relative overflow-hidden rounded-2xl h-44 bg-slate-100 mb-3 shadow-inner">
        <img src="${thumbUrl}" alt="${age.title}" class="w-full h-full object-cover transition-transform duration-500 hover:scale-105" onerror="this.onerror=null; this.src='/images/age_5_7.jpg';">
      </div>

      <!-- 2. Ma'lumotlar va yozuvlar rasm ostida tartibli joylashadi -->
      <div class="space-y-2.5 flex-1 flex flex-col justify-between">
        <!-- Toifa nishoni va tanlanganlik belgisi -->
        <div class="flex items-center justify-between gap-2">
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-100 shadow-xs">
            <span>${age.icon}</span> <span>${age.category}</span>
          </span>
          <div class="check-badge w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs font-bold shadow-sm transition-transform ${isSelected ? 'scale-100 opacity-100' : 'scale-50 opacity-0'}">
            ✓
          </div>
        </div>

        <!-- Yosh sarlavhasi -->
        <h3 class="font-fredoka text-xl font-bold text-slate-900 leading-tight">
          ${age.title}
        </h3>

        <!-- Tavsif -->
        <p class="text-xs text-slate-600 leading-relaxed">
          ${age.style_desc}
        </p>

        <!-- Tavsiya etilgan davomiylik -->
        <div class="flex items-center justify-between text-xs font-semibold text-slate-500 bg-slate-50/90 py-1.5 px-3 rounded-xl border border-slate-200 mt-2">
          <span>⏱️ Tavsiya vaqt:</span>
          <strong class="text-indigo-600 font-bold">${age.recommended_duration} soniya</strong>
        </div>
      </div>
    </div>
  `;
  }).join("");
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

  container.innerHTML = state.presets.visual_styles.map(style => {
    const thumbUrl = style.thumbnail || STYLE_THUMBNAILS[style.id] || "/images/style_pixar_3d.jpg";
    const isSelected = state.visualStyle === style.id;
    return `
    <label class="cursor-pointer">
      <input type="radio" name="visualStyle" value="${style.id}" class="sr-only peer" 
             ${isSelected ? 'checked' : ''} onchange="selectVisualStyle('${style.id}')">
      <div class="style-card p-2.5 rounded-2xl border-2 border-slate-200 bg-white/95 peer-checked:border-indigo-600 peer-checked:bg-indigo-50/70 peer-checked:ring-4 peer-checked:ring-indigo-100 transition-all flex flex-col gap-2.5">
        <!-- Toza Rasm vitrinasi (ustida yozuvsiz) -->
        <div class="relative rounded-xl overflow-hidden h-32 bg-slate-100 shadow-inner">
          <img src="${thumbUrl}" alt="${style.title}" class="w-full h-full object-cover transition-transform duration-400 hover:scale-105" onerror="this.onerror=null; this.src='/images/style_pixar_3d.jpg';">
        </div>
        <!-- Rasm ostidagi matnlar -->
        <div class="px-1 pb-1">
          <div class="flex items-center justify-between gap-1 mb-0.5">
            <span class="font-fredoka font-bold text-slate-800 text-sm leading-tight">${style.title || style.name}</span>
            <span class="text-xs">${style.icon}</span>
          </div>
          <p class="text-[11px] text-slate-500 line-clamp-1">${style.desc || 'Yuqori sifatli animatsiya'}</p>
        </div>
      </div>
    </label>
  `;
  }).join("");
}

window.selectVisualStyle = function(styleId) {
  state.visualStyle = styleId;
};

// Render Sample Topics
function renderSampleTopics() {
  const container = document.getElementById("sampleTopicsContainer");
  if (!container || !state.presets) return;

  const relevantTopics = state.presets.sample_topics.filter(t => (t.age_group === state.selectedAge || t.age === state.selectedAge));
  const currentTopic = (state.topic || "").trim().toLowerCase();

  container.innerHTML = relevantTopics.map(t => {
    const isSelected = currentTopic.length > 0 && currentTopic === t.title.trim().toLowerCase();
    return `
    <button type="button" class="text-left p-3 rounded-2xl transition-all text-xs flex items-center justify-between gap-2 shadow-sm ${
      isSelected 
        ? 'bg-indigo-600 text-white font-semibold ring-2 ring-indigo-400 shadow-indigo-200' 
        : 'bg-white/80 hover:bg-indigo-50 border border-slate-200 text-slate-700 hover:border-indigo-200'
    }"
            onclick="applySampleTopic('${t.title.replace(/'/g, "\\'")}', '${t.prompt.replace(/'/g, "\\'")}')">
      <div class="flex items-center gap-2">
        <span class="${isSelected ? 'text-amber-300' : 'text-indigo-500'} font-bold">✨</span>
        <span>${t.title}</span>
      </div>
      ${isSelected ? '<span class="text-xs bg-white/20 px-2 py-0.5 rounded-lg text-white font-bold">Tanlandi ✓</span>' : ''}
    </button>
  `;
  }).join("");
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
  renderSampleTopics();
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
  showToast(`"${customTrack.name}" fon musiqasi sifatida tanlandi`, "success", "Musiqa tanlandi 🎵");
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
      showToast("Iltimos, video mavzusini yozing yoki pastdagi namunalardan birini tanlang.", "warning", "Mavzu kiritilmadi 📌");
      const inputEl = document.getElementById("inputTopic");
      if (inputEl) inputEl.focus();
      return;
    }
    state.topic = topic;
    state.prompt = topic;
    
    showLoading("Mavzu bolalar uchun tekshirilmoqda...");
    await runSafetyCheck();
    hideLoading();
    goToStep(3);
  } else if (state.currentStep === 3) {
    if (!state.safetyReport || !state.safetyReport.is_safe) {
      showToast("Mavzu bolalar xavfsizligi talablariga mos kelmadi. Iltimos, boshqa mavzu tanlang yoki yozing.", "warning", "Xavfsizlik eslatmasi 🛡️");
      goToStep(2);
      return;
    }
    showLoading("Dars uchun qiziqarli ssenariy yozilmoqda...");
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

  const lineFill = document.getElementById("stepNavLineFill");
  if (lineFill) {
    const pct = Math.max(0, Math.min(100, (step - 1) * 25));
    lineFill.style.width = `${pct}%`;
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

  const statusCard = document.getElementById("safetyStatusCard");
  const statusIcon = document.getElementById("safetyStatusIcon");
  const statusLabel = document.getElementById("safetyStatusLabel");
  const topicMeta = document.getElementById("safetyTopicMeta");
  const statusBadge = document.getElementById("safetyStatusBadge");

  const isSafe = r.is_safe !== false && r.status !== "REJECTED";
  const isCaution = r.status === "APPROVED_WITH_CAUTION";

  if (statusCard) {
    if (r.status === "REJECTED") {
      statusCard.className = "p-5 rounded-2xl flex flex-wrap items-center justify-between gap-4 border transition-all bg-rose-50/90 border-rose-200 shadow-sm";
    } else if (isCaution) {
      statusCard.className = "p-5 rounded-2xl flex flex-wrap items-center justify-between gap-4 border transition-all bg-amber-50/90 border-amber-200 shadow-sm";
    } else {
      statusCard.className = "p-5 rounded-2xl flex flex-wrap items-center justify-between gap-4 border transition-all bg-emerald-50/90 border-emerald-200 shadow-sm";
    }
  }

  if (statusIcon) {
    if (r.status === "REJECTED") {
      statusIcon.className = "w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shadow-sm bg-rose-500 text-white";
      statusIcon.innerText = "🚫";
    } else if (isCaution) {
      statusIcon.className = "w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shadow-sm bg-amber-500 text-white";
      statusIcon.innerText = "⚠️";
    } else {
      statusIcon.className = "w-12 h-12 rounded-2xl flex items-center justify-center text-2xl shadow-sm bg-emerald-500 text-white";
      statusIcon.innerText = "🛡️";
    }
  }

  if (statusLabel) {
    statusLabel.innerText = r.status_label || (isSafe ? "Tasdiqlandi — To'liq Pedagogik Xavfsiz" : "Rad etildi");
    if (r.status === "REJECTED") statusLabel.className = "font-fredoka font-bold text-lg text-rose-900";
    else if (isCaution) statusLabel.className = "font-fredoka font-bold text-lg text-amber-900";
    else statusLabel.className = "font-fredoka font-bold text-lg text-emerald-900";
  }

  if (topicMeta) {
    const wordCount = r.word_count || (state.topic ? state.topic.split(/\s+/).filter(Boolean).length : 0);
    const ageCategory = r.age_category || "Pedagogik";
    topicMeta.innerText = `Mavzu: "${r.topic_analyzed || state.topic}" • ${wordCount} so'z • Yosh toifasi: ${r.age_group || state.selectedAge} yosh (${ageCategory})`;
  }

  if (statusBadge) {
    if (r.status === "REJECTED") {
      statusBadge.innerHTML = `<span class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-rose-600 text-white shadow-xs">Rad etildi ✖</span>`;
    } else if (isCaution) {
      statusBadge.innerHTML = `<span class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-amber-600 text-white shadow-xs">Moslashtirish bilan ✓</span>`;
    } else {
      statusBadge.innerHTML = `<span class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-emerald-600 text-white shadow-xs">Qabul qilindi ✓</span>`;
    }
  }

  // Aniqlangan ta'limiy yo'nalishlar
  const themesContainer = document.getElementById("safetyThemesContainer");
  if (themesContainer) {
    const themes = (r.detected_themes && r.detected_themes.length > 0) ? r.detected_themes : ["Umumiy bolalar ta'limi"];
    themesContainer.innerHTML = themes.map(t => `
      <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-bold bg-indigo-50 text-indigo-700 border border-indigo-100 shadow-2xs">
        <span>✨</span> <span>${t}</span>
      </span>
    `).join("");
  }

  // Tekshirilgan xavfsizlik mezonlari (Haqiqiy audit)
  const checksGrid = document.getElementById("safetyChecksGrid");
  if (checksGrid && r.category_results) {
    checksGrid.innerHTML = r.category_results.map(c => {
      const ok = c.is_safe !== false;
      return `
        <div class="flex items-start justify-between p-3 rounded-2xl border transition-all ${ok ? 'bg-white/80 border-slate-200 shadow-2xs' : 'bg-rose-50/80 border-rose-200 shadow-xs'}">
          <div class="space-y-0.5 pr-2">
            <div class="text-xs font-bold flex items-center gap-1.5 ${ok ? 'text-slate-800' : 'text-rose-900'}">
              <span class="${ok ? 'text-emerald-500' : 'text-rose-500'} font-black">${ok ? '✓' : '✖'}</span>
              <span>${c.title}</span>
            </div>
            <div class="text-[11px] ${ok ? 'text-slate-500' : 'text-rose-600'} leading-snug">${c.details}</div>
          </div>
          <span class="shrink-0 text-[10px] font-bold px-2 py-0.5 rounded-lg ${ok ? 'text-emerald-700 bg-emerald-100/80' : 'text-rose-700 bg-rose-200/80'}">
            ${c.status_text}
          </span>
        </div>
      `;
    }).join("");
  }

  // Pedagogik maslahat
  const adviceEl = document.getElementById("safetyPedagogicalAdvice");
  if (adviceEl) {
    adviceEl.innerText = r.pedagogical_advice || "Mavzu ta'limiy mezonlarga muvofiq.";
  }

  // Qoidabuzarliklar va ogohlantirishlar
  const violationsEl = document.getElementById("safetyViolationsContainer");
  if (violationsEl) {
    if (r.violations && r.violations.length > 0) {
      violationsEl.classList.remove("hidden");
      violationsEl.innerHTML = `
        <div class="font-bold flex items-center gap-1.5 mb-1 text-rose-700">
          <span>⚠️</span> <span>Qoidabuzarliklar va cheklovlar:</span>
        </div>
        ${r.violations.map(v => `<div>• ${v}</div>`).join("")}
      `;
    } else {
      violationsEl.classList.add("hidden");
    }
  }

  const warningsEl = document.getElementById("safetyWarningsContainer");
  if (warningsEl) {
    if (r.warnings && r.warnings.length > 0) {
      warningsEl.classList.remove("hidden");
      warningsEl.innerHTML = `
        <div class="font-bold flex items-center gap-1.5 mb-1 text-amber-700">
          <span>💡</span> <span>Pedagogik tavsiyalar:</span>
        </div>
        ${r.warnings.map(w => `<div>• ${w}</div>`).join("")}
      `;
    } else {
      warningsEl.classList.add("hidden");
    }
  }
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
          🎙️ Sahnada aytiladigan gaplar (O'zbekcha matn):
        </label>
        <textarea class="w-full text-sm p-3 rounded-2xl border border-slate-200 bg-slate-50 focus:bg-white focus:border-indigo-500 outline-none transition-all font-medium text-slate-700" 
                  rows="2" onchange="updateSceneNarration(${idx}, this.value)">${scene.narration}</textarea>
      </div>

      ${scene.visual_beats && scene.visual_beats.length > 0 ? `
        <div class="mb-3 pt-3 border-t border-slate-100">
          <label class="block text-xs font-bold text-indigo-600 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <span>📊</span> Ekranda ko'rinadigan belgilar va tushunchalar:
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

window.openFlashcardsPrintView = function(customScenes = null, customTitle = null, customMoral = null) {
  const scenes = customScenes || ((state.preparedScenes && state.preparedScenes.length > 0) 
    ? state.preparedScenes 
    : ((state.screenplay && state.screenplay.scenes) ? state.screenplay.scenes : []));
    
  if (scenes.length === 0) {
    showToast("Tarqatma varaq chiqarish uchun avval video ssenariysini tayyorlang.", "info", "Eslatma 📄");
    return;
  }
  const title = cleanTitleWithoutNumbers(customTitle || (state.screenplay && state.screenplay.title) || state.topic);
  const moral = customMoral || (state.screenplay && state.screenplay.moral_summary) || "Bilim — eng katta boylikdir!";
  
  const printWin = window.open("", "_blank");
  if (!printWin) {
    showToast("Iltimos, brauzeringizda yangi oynalarga ruxsat bering!", "warning", "Brauzer eslatmasi 🖨️");
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
  <title>${title} — Dars uchun tarqatma varaq</title>
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
    <span style="font-size: 13px; color: #64748b;">TasvirLab o'qituvchilar va ota-onalar uchun dars varaqasi</span>
    <button onclick="window.print()" style="padding: 10px 22px; background: #4f46e5; color: white; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 4px 6px rgba(79, 70, 229, 0.2);">
      🖨️ Chop etish / Saqlash
    </button>
  </div>
  <div class="header">
    <h1>🎓 ${title}</h1>
    <p>Yosh guruhi: ${state.selectedAge} yosh | TasvirLab bolalar video darslari</p>
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
  statusSub.innerText = "O'zbekcha nutq yozilmoqda va kadrlar chizilmoqda. Iltimos, kuting!";
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
    if (textEl) textEl.innerHTML = `<span class="animate-pulse text-indigo-600 font-bold">🎙️ Ovoz yozilmoqda...</span>`;

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
        if (textEl) textEl.innerHTML = `<span class="text-emerald-600 font-bold">✅ Tayyor! (Vaqti: ${prep.duration}s)</span>`;
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
  statusSub.innerText = `Jami ${state.preparedScenes.length} ta sahna va ovozlar tayyorlandi (Umumiy vaqt: ${Math.round(state.totalDuration)} soniya).`;

  btnPremyere.disabled = false;
  btnPremyere.className = "px-6 py-3 rounded-2xl bg-gradient-to-r from-indigo-600 to-pink-600 text-white font-fredoka font-bold text-sm shadow-xl hover:shadow-indigo-500/25 cursor-pointer flex items-center gap-2";
  btnPremyere.innerHTML = `<span>🎬 Videoni Tomosha Qilish</span><span>→</span>`;

  // Videoni ma'lumotlar bazasiga avtomatik saqlaymiz
  try {
    await saveCompletedVideoToDatabase();
  } catch (errSave) {
    console.warn("Videoni bazaga saqlashda xatolik:", errSave);
  }
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
      duckingText.innerText = "Nutq vaqtida musiqa pasaydi";
      duckingBadge.className = "w-48 shrink-0 inline-flex items-center justify-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-medium bg-amber-950/80 text-amber-300 border border-amber-800/60 shadow-sm transition-colors";
    } else {
      duckingText.innerText = "Musiqa me'yorda";
      duckingBadge.className = "w-48 shrink-0 inline-flex items-center justify-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-medium bg-emerald-950/80 text-emerald-300 border border-emerald-800/60 shadow-sm transition-colors";
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
  showLoading("Namunaviy sahna va ovozlar yuklanmoqda...");
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
    const idleOverlay = document.getElementById("cinemaIdleOverlay");
    if (idleOverlay) idleOverlay.classList.add("hidden");

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
  c.fillText(cleanTitleWithoutNumbers(scene.title || "TasvirLab Virtual Darsi"), width / 2, stageCardY + 160);

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
          const zoom = 1.0 + (progress * 0.02);
          const panX = Math.sin(progress * Math.PI) * 8;
          ctx.translate(width / 2, height / 2);
          ctx.scale(zoom, zoom);
          ctx.drawImage(cachedImg, -width / 2 + panX, -height / 2, width, height);
          ctx.restore();
        } catch (imgErr) {
          console.warn("Rasm chizishda xatolik:", imgErr);
        }
      }
    }

    // 3. PASTKI YUMSHOQ KINEMATIK SOYA (Doska foniga mayin ulanishi uchun)
    const botVignette = ctx.createLinearGradient(0, 540, 0, height);
    botVignette.addColorStop(0, "rgba(8, 12, 22, 0)");
    botVignette.addColorStop(0.5, "rgba(8, 12, 22, 0.4)");
    botVignette.addColorStop(1, "rgba(8, 12, 22, 0.8)");
    ctx.fillStyle = botVignette;
    ctx.fillRect(0, 540, width, height - 540);

    // 4. PASTKI TA'LIMIY DOSKA VA SUBTITR PANELI (IXCHAM, KENG VA PASTROQ)
    const cardX = 28;
    const cardY = 586;
    const cardW = 1224;
    const cardH = 114;
    const cardR = 20;

    ctx.save();
    clearTextShadows(ctx);

    // Doska fon qatlami
    const cardGrad = ctx.createLinearGradient(cardX, cardY, cardX + cardW, cardY + cardH);
    if (activeBeat.highlight) {
      cardGrad.addColorStop(0, "rgba(22, 24, 40, 0.94)");
      cardGrad.addColorStop(1, "rgba(42, 26, 60, 0.94)");
    } else {
      cardGrad.addColorStop(0, "rgba(11, 16, 30, 0.92)");
      cardGrad.addColorStop(1, "rgba(18, 25, 48, 0.92)");
    }
    ctx.fillStyle = cardGrad;
    drawRoundedRect(ctx, cardX, cardY, cardW, cardH, cardR);
    ctx.fill();

    // Doska hoshiyasi
    ctx.lineWidth = activeBeat.highlight ? 2.2 : 1.4;
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

    // 4A. 1-BO'LIM: ASOSIY MAVZU / SABOQ TUSHUNCHASI (Chap tomon - ixcham va chiroyli)
    ctx.save();
    ctx.beginPath();
    ctx.rect(cardX, cardY, 290, cardH);
    ctx.clip();
    clearTextShadows(ctx);

    // Kichik nishon / chip
    ctx.font = "bold 11px 'Fredoka'";
    ctx.fillStyle = activeBeat.highlight ? "#FDE047" : "#A5B4FC";
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    ctx.fillText("✨ DARS SABOG'I", cardX + 24, cardY + 22);

    // Asosiy tushuncha / Sarlavha
    const rawMain = activeBeat.main_text || (scene && scene.title) || state.topic || "Dars Tushunchasi";
    const mainText = cleanTitleWithoutNumbers(rawMain);
    let fontSize = 24;
    ctx.font = `bold ${fontSize}px 'Fredoka'`;
    while (fontSize > 16 && ctx.measureText(mainText).width > 250) {
      fontSize -= 2;
      ctx.font = `bold ${fontSize}px 'Fredoka'`;
    }
    let displayMainText = mainText;
    if (ctx.measureText(displayMainText).width > 250) {
      while (ctx.measureText(displayMainText + "...").width > 250 && displayMainText.length > 0) {
        displayMainText = displayMainText.slice(0, -1);
      }
      displayMainText = displayMainText.trim() + "...";
    }
    ctx.fillStyle = activeBeat.highlight ? "#FDE047" : "#FFFFFF";
    ctx.fillText(displayMainText, cardX + 24, cardY + 44);

    ctx.restore();

    // Ajratuvchi vertikal chiziq
    ctx.strokeStyle = "rgba(255, 255, 255, 0.1)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cardX + 295, cardY + 16);
    ctx.lineTo(cardX + 295, cardY + cardH - 16);
    ctx.stroke();

    // 4B. 2-BO'LIM: KENG KARAOKE SUBTITR VA XULOSA (O'ng tomon - piktogrammalarsiz, keng va erkin)
    ctx.save();
    clearTextShadows(ctx);

    const subX = cardX + 315;
    const subW = cardW - 335; // ~889px keng maydon!
    const activeChunk = getActiveNarrationChunk(scene && scene.narration, progress);

    // Dinamik Karaoke Subtitr
    drawKaraokeSubtitle(ctx, activeChunk, subX, cardY + 14, subW - 10, 58, activeBeat.highlight);

    // Asosiy saboq / Xulosa qatori
    clearTextShadows(ctx);
    ctx.font = "bold 12px 'Fredoka'";
    ctx.fillStyle = "#C084FC";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText("💡 XULOSA:", subX, cardY + 90);

    const isMathTopic = (state.topic && (state.topic.toLowerCase().includes("qo'shish") || state.topic.toLowerCase().includes("matematik") || state.topic.toLowerCase().includes("hisob")));
    const ruleText = (activeBeat.highlight && isMathTopic)
      ? "Qo'shish — miqdorlarni birga jamlash va aniq hisoblash demakdir!" 
      : ((state.screenplay && state.screenplay.moral_summary) || "Bilim — eng katta boylik va kuchdir!");
    ctx.font = "500 12.5px 'Plus Jakarta Sans'";
    ctx.fillStyle = "#CBD5E1";
    let displayRule = ruleText;
    const maxRuleWidth = subW - 85;
    if (ctx.measureText(displayRule).width > maxRuleWidth) {
      while (ctx.measureText(displayRule + "...").width > maxRuleWidth && displayRule.length > 0) {
        displayRule = displayRule.slice(0, -1);
      }
      displayRule = displayRule.trim() + "...";
    }
    ctx.fillText(displayRule, subX + 75, cardY + 90);

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
  ctx.fillText("TasvirLab Video Studiyasi", width / 2, height / 2 - 25);
  
  ctx.font = "bold 16px 'Plus Jakarta Sans'";
  ctx.fillStyle = "#FDE047";
  ctx.fillText("🎬 Darsni boshlash uchun «Ko'rish» tugmasini bosing", width / 2, height / 2 + 30);
  ctx.restore();
}

// Download Manifest or Export Real Video
function downloadVideoPackage() {
  if (!state.preparedScenes || state.preparedScenes.length === 0) {
    showToast("Yuklab olishdan avval videoni to'liq tayyorlang!", "info", "Eslatma 🎬");
    return;
  }
  exportRealVideo();
}

async function exportRealVideo() {
  if (!state.preparedScenes || state.preparedScenes.length === 0) {
    showToast("Yuklab olishdan avval videoni to'liq tayyorlang!", "info", "Eslatma 🎬");
    return;
  }

  // Agar allaqachon render qilingan video mavjud bo'lsa, to'g'ridan-to'g'ri yuklab olamiz
  if (state.renderedVideoUrl) {
    const a = document.createElement("a");
    a.href = state.renderedVideoUrl;
    a.download = state.renderedVideoFilename || `TasvirLab_${state.topic.replace(/\s+/g, "_")}.mp4`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast("1080p Full HD MP4 video yuklab olinmoqda...", "success", "Yuklanmoqda 📥");
    return;
  }

  showLoading("🎬 Serverda 1080p Full HD MP4 video render qilinmoqda (FFmpeg)...\nIltimos, kuting — kadrlar va ovozlar yuqori sifatda birlashtirilmoqda!");

  const btnDl = document.getElementById("btnDownload");
  const origBtnHtml = btnDl ? btnDl.innerHTML : "";
  if (btnDl) {
    btnDl.disabled = true;
    btnDl.innerHTML = `<span>⏳</span> Render qilinmoqda...`;
  }

  try {
    const payload = {
      topic: state.topic || "Ta'limiy Video",
      age_group: state.selectedAge || "5-7",
      voice_id: state.selectedVoice || "lola",
      visual_style_id: state.visualStyle || "pixar_3d",
      bgm_track: state.selectedBgm || "bgm_cheerful.mp3",
      moral_summary: (state.screenplay && state.screenplay.moral_summary) || "Bilim — eng katta boylik va kuchdir!",
      prepared_scenes: state.preparedScenes,
      quiz_data: state.quiz || null,
      save_to_db: true
    };

    const res = await fetch(`${API_URL}/api/user/videos/render-mp4`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || "Serverda render qilishda xatolik yuz berdi.");
    }

    const data = await res.json();
    state.renderedVideoUrl = data.download_url || data.video_url;
    state.renderedVideoFilename = data.filename;

    // Faylni avtomatik kompyuterga yuklab olish
    const a = document.createElement("a");
    a.href = data.download_url || data.video_url;
    a.download = data.filename || `TasvirLab_${state.topic.replace(/\s+/g, "_")}.mp4`;
    document.body.appendChild(a);
    a.click();
    a.remove();

    hideLoading();
    showToast(`1080p Full HD MP4 video yuklab olindi! (Hajmi: ${data.size_mb} MB, 30 FPS)`, "success", "Tayyor! 🎉");
    updateMyVideosBadge();
  } catch (err) {
    hideLoading();
    console.error("FFmpeg render error:", err);
    showToast("Video eksport qilishda xatolik yuz berdi: " + (err.message || err), "error", "Xatolik ⚠️");
  } finally {
    if (btnDl) {
      btnDl.disabled = false;
      btnDl.innerHTML = origBtnHtml || `<span>📥</span> Videoni Yuklab Olish`;
    }
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

// ==================== TO'LOVLAR VA BALANS (PAYME, CLICK, UZUM) ====================
window.cachedPricingPackages = null;
window.selectedPricingPackage = null;
window.selectedPaymentProvider = "payme";
window.currentCheckoutOrder = null;
window.orderPollingInterval = null;

window.openPricingModal = async function() {
  const modal = document.getElementById("pricingModal");
  if (!modal) return;
  modal.classList.remove("hidden");

  // Har safar ochilganda paketlar ko'rinishiga qaytamiz
  backToPricingPackages();

  // Foydalanuvchi joriy balansini ko'rsatish
  const crCount = document.getElementById("modalCreditCount");
  if (crCount) {
    const u = (window.currentUser && window.currentUser.user) ? window.currentUser.user : window.currentUser;
    const bal = (u && typeof u.credits_balance === "number") ? u.credits_balance : (Number(u && u.credits_balance) || 0);
    crCount.innerText = `${bal} ta video`;
  }

  const container = document.getElementById("pricingCardsList");
  if (!container) return;

  try {
    const res = await fetch(`${API_URL}/api/billing/packages`);
    if (res.ok) {
      const data = await res.json();
      window.cachedPricingPackages = data.packages || [];
    }
  } catch (err) {
    console.warn("Paketlar yuklanmadi, zaxira ro'yxat ishlatiladi:", err);
  }

  const packages = window.cachedPricingPackages || [
    {
      id: "pack_starter",
      name: "Boshlang'ich To'plam",
      credits: 5,
      price_uzs: 15000,
      price_per_video_uzs: 3000,
      discount_percent: 0,
      popular: false,
      icon: "🌱",
      description: "Kichik oilalar va dastlabki video darslar uchun qulay to'plam."
    },
    {
      id: "pack_popular",
      name: "Oila To'plami (Ommabop)",
      credits: 20,
      price_uzs: 45000,
      price_per_video_uzs: 2250,
      discount_percent: 25,
      popular: true,
      icon: "⭐",
      description: "Eng ko'p tanlanadigan xalqchil to'plam! 20 ta video dars — bor-yo'g'i 45 000 so'm."
    },
    {
      id: "pack_pro",
      name: "O'qituvchilar & Bog'cha",
      credits: 50,
      price_uzs: 89000,
      price_per_video_uzs: 1780,
      discount_percent: 40,
      popular: false,
      icon: "🚀",
      description: "Bog'cha tarbiyachilari, repetitorlar va faol ota-onalar uchun eng tejamkor paket."
    },
    {
      id: "pack_vip",
      name: "Maktab & VIP Ta'lim",
      credits: 150,
      price_uzs: 199000,
      price_per_video_uzs: 1320,
      discount_percent: 55,
      popular: false,
      icon: "👑",
      description: "O'quv markazlari va katta ta'limiy loyihalar uchun maksimal ulgurji chegirma."
    }
  ];

  container.innerHTML = packages.map(p => `
    <div class="relative p-5 rounded-3xl border-2 ${p.popular ? 'border-indigo-600 bg-indigo-50/40 ring-4 ring-indigo-100' : 'border-slate-200 bg-white'} shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
      ${p.popular ? '<span class="absolute -top-3 right-6 bg-gradient-to-r from-indigo-600 to-pink-600 text-white text-[11px] font-fredoka font-bold px-3 py-1 rounded-full shadow-md uppercase tracking-wider">Eng Ommabop ⭐</span>' : ''}
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="text-3xl">${p.icon}</span>
          ${p.discount_percent > 0 ? `<span class="bg-emerald-100 text-emerald-700 text-xs font-bold px-2.5 py-0.5 rounded-full">-${p.discount_percent}% Chegirma</span>` : ''}
        </div>
        <h4 class="font-fredoka font-bold text-lg text-slate-800">${escapeHtml(p.name)}</h4>
        <p class="text-xs text-slate-500 mt-1 mb-4 leading-relaxed">${escapeHtml(p.description)}</p>
        <div class="mb-4">
          <div class="text-2xl font-fredoka font-extrabold text-slate-900">${p.price_uzs.toLocaleString()} <span class="text-xs font-semibold text-slate-500">so'm</span></div>
          <div class="text-[11px] text-indigo-600 font-semibold">${p.credits} ta to'liq video (${p.price_per_video_uzs.toLocaleString()} so'm / video)</div>
        </div>
      </div>
      <button onclick="startCheckoutForPackage('${p.id}')" class="w-full py-3 rounded-2xl ${p.popular ? 'bg-indigo-600 text-white hover:bg-indigo-700' : 'bg-slate-900 text-white hover:bg-slate-800'} font-fredoka font-bold text-xs shadow-sm hover:scale-[1.01] transition-all flex items-center justify-center gap-2 cursor-pointer">
        <span>💳 To'lov qilish (${p.price_uzs.toLocaleString()} so'm)</span>
        <span>→</span>
      </button>
    </div>
  `).join("");
};

window.closePricingModal = function() {
  const modal = document.getElementById("pricingModal");
  if (modal) modal.classList.add("hidden");
  if (window.orderPollingInterval) {
    clearInterval(window.orderPollingInterval);
    window.orderPollingInterval = null;
  }
};

window.startCheckoutForPackage = function(pkgId) {
  if (!window.currentUser) {
    openAuthModal();
    showToast("To'lov qilish uchun avval hisobingizga kiring.", "warning");
    return;
  }

  const pkg = (window.cachedPricingPackages || []).find(p => p.id === pkgId) || {
    id: pkgId,
    name: "Oila To'plami (Ommabop)",
    credits: 20,
    price_uzs: 45000,
    icon: "⭐"
  };

  window.selectedPricingPackage = pkg;
  window.currentCheckoutOrder = null;

  // View larni almashtirish
  const pkgView = document.getElementById("pricingPackagesView");
  const chkView = document.getElementById("pricingCheckoutView");
  if (pkgView) pkgView.classList.add("hidden");
  if (chkView) chkView.classList.remove("hidden");

  // Kartani to'ldirish
  const iconEl = document.getElementById("checkoutPkgIcon");
  if (iconEl) iconEl.innerText = pkg.icon || "🪙";
  const nameEl = document.getElementById("checkoutPkgName");
  if (nameEl) nameEl.innerText = pkg.name;
  const credEl = document.getElementById("checkoutPkgCredits");
  if (credEl) credEl.innerText = `+${pkg.credits} ta video dars`;
  const priceEl = document.getElementById("checkoutPkgPrice");
  if (priceEl) priceEl.innerText = `${pkg.price_uzs.toLocaleString()} so'm`;

  const waitBox = document.getElementById("checkoutWaitingBox");
  if (waitBox) waitBox.classList.add("hidden");

  selectPaymentProvider("payme");
};

window.backToPricingPackages = function() {
  const pkgView = document.getElementById("pricingPackagesView");
  const chkView = document.getElementById("pricingCheckoutView");
  if (pkgView) pkgView.classList.remove("hidden");
  if (chkView) chkView.classList.add("hidden");
  if (window.orderPollingInterval) {
    clearInterval(window.orderPollingInterval);
    window.orderPollingInterval = null;
  }
};

window.selectPaymentProvider = function(prov) {
  window.selectedPaymentProvider = prov;
  const paymeBtn = document.getElementById("payProviderPaymeBtn");
  const clickBtn = document.getElementById("payProviderClickBtn");
  const uzumBtn = document.getElementById("payProviderUzumBtn");
  const paynetBtn = document.getElementById("payProviderPaynetBtn");

  const unselectedClass = "p-3.5 rounded-2xl border-2 border-slate-200 bg-white hover:bg-slate-50 flex flex-col items-center justify-center gap-2 transition-all cursor-pointer hover:scale-[1.02]";

  if (paymeBtn) {
    paymeBtn.className = prov === "payme"
      ? "p-3.5 rounded-2xl border-2 border-teal-500 bg-teal-50/70 shadow-sm flex flex-col items-center justify-center gap-2 transition-all cursor-pointer ring-2 ring-teal-200 hover:scale-[1.02]"
      : unselectedClass;
  }

  if (clickBtn) {
    clickBtn.className = prov === "click"
      ? "p-3.5 rounded-2xl border-2 border-blue-500 bg-blue-50/70 shadow-sm flex flex-col items-center justify-center gap-2 transition-all cursor-pointer ring-2 ring-blue-200 hover:scale-[1.02]"
      : unselectedClass;
  }

  if (uzumBtn) {
    uzumBtn.className = prov === "uzum"
      ? "p-3.5 rounded-2xl border-2 border-purple-500 bg-purple-50/70 shadow-sm flex flex-col items-center justify-center gap-2 transition-all cursor-pointer ring-2 ring-purple-200 hover:scale-[1.02]"
      : unselectedClass;
  }

  if (paynetBtn) {
    paynetBtn.className = prov === "paynet"
      ? "p-3.5 rounded-2xl border-2 border-emerald-500 bg-emerald-50/70 shadow-sm flex flex-col items-center justify-center gap-2 transition-all cursor-pointer ring-2 ring-emerald-200 hover:scale-[1.02]"
      : unselectedClass;
  }

  const pkg = window.selectedPricingPackage;
  const priceStr = pkg ? `${pkg.price_uzs.toLocaleString()} so'm` : "";
  const providerNames = { payme: "Payme", click: "Click", uzum: "Uzum Pay", paynet: "Paynet" };
  const textEl = document.getElementById("btnProceedPaymentText");
  if (textEl) {
    textEl.innerText = `${providerNames[prov] || "To'lov"} orqali ${priceStr} to'lash`;
  }
};

window.proceedToPaymentGateway = async function() {
  const pkg = window.selectedPricingPackage;
  if (!pkg) {
    showToast("To'lov to'plami tanlanmagan.", "warning");
    return;
  }
  if (!window.currentUser) {
    openAuthModal();
    showToast("To'lov qilish uchun avval hisobingizga kiring.", "warning");
    return;
  }

  const btn = document.getElementById("btnProceedPayment");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch(`${API_URL}/api/billing/create-checkout`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        package_id: pkg.id,
        payment_provider: window.selectedPaymentProvider
      })
    });
    const data = await res.json();
    if (!res.ok) {
      showToast(data.detail || "To'lov havolasini yaratishda xatolik.", "error");
      if (btn) btn.disabled = false;
      return;
    }

    window.currentCheckoutOrder = data;

    // To'lov sahifasini yangi oynada ochamiz
    if (data.checkout_url) {
      window.open(data.checkout_url, "_blank");
    }

    // Kutish holatini ko'rsatish
    const waitBox = document.getElementById("checkoutWaitingBox");
    if (waitBox) waitBox.classList.remove("hidden");
    showToast(`${window.selectedPaymentProvider.toUpperCase()} to'lov oynasi ochildi. To'lovni tasdiqlang!`, "info");

    // To'lov holatini tekshirishni (polling) boshlaymiz
    startOrderPolling(data.order_id, pkg.credits);
  } catch (err) {
    console.error("To'lov yaratishda xatolik:", err);
    showToast("Server bilan bog'lanishda xatolik.", "error");
  } finally {
    if (btn) btn.disabled = false;
  }
};

function startOrderPolling(orderId, expectedCredits) {
  if (window.orderPollingInterval) clearInterval(window.orderPollingInterval);

  window.orderPollingInterval = setInterval(async () => {
    try {
      const res = await fetch(`${API_URL}/api/billing/orders/${orderId}`);
      if (res.ok) {
        const orderData = await res.json();
        if (orderData.is_paid) {
          clearInterval(window.orderPollingInterval);
          window.orderPollingInterval = null;

          // Foydalanuvchi ma'lumotlarini yangilash
          const creditsCount = orderData.credits_amount || expectedCredits || 20;
          await refreshCurrentUserAfterPayment(creditsCount);
        }
      }
    } catch (e) {
      // Tarmoq xatolarini e'tiborsiz qoldiramiz
    }
  }, 2500);
}


async function refreshCurrentUserAfterPayment(addedCredits) {
  try {
    const meRes = await fetch(`${API_URL}/api/auth/me`, { headers: getAuthHeaders() });
    if (meRes.ok) {
      const meData = await meRes.json();
      const userObj = meData.user || meData;
      window.currentUser = userObj;
      updateUserHeaderUI(userObj);
    }
  } catch(e) {
    console.error("Foydalanuvchi ma'lumotlarini yangilashda xatolik:", e);
  }

  // Modaldagi balansni ham darhol yangilaymiz
  const crCount = document.getElementById("modalCreditCount");
  if (crCount && window.currentUser) {
    const bal = (typeof window.currentUser.credits_balance === "number") ? window.currentUser.credits_balance : (Number(window.currentUser.credits_balance) || 0);
    crCount.innerText = `${bal} ta video`;
  }

  closePricingModal();

  const creditsCount = (typeof addedCredits === "number" && !isNaN(addedCredits))
    ? addedCredits
    : (parseInt(addedCredits) || 20);

  showNoticeModal(
    "To'lov Muvaffaqiyatli Qabul Qilindi! 🎉",
    `Hisobingizga +${creditsCount} ta yangi video yaratish imkoniyati qo'shildi!\nEndi bemalol istagan mavzuda qiziqarli bolalar darslarini yaratishingiz mumkin.`,
    "🪙"
  );
  showToast(`Hisobingiz to'ldirildi: +${creditsCount} ta video! 🚀`, "success");
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatRelativeDate(isoStr) {
  if (!isoStr) return "";
  try {
    const d = new Date(isoStr);
    const now = new Date();
    const isToday = d.toDateString() === now.toDateString();
    const hours = String(d.getHours()).padStart(2, "0");
    const mins = String(d.getMinutes()).padStart(2, "0");
    if (isToday) {
      return `Bugun, ${hours}:${mins}`;
    }
    const yesterday = new Date(now);
    yesterday.setDate(yesterday.getDate() - 1);
    if (d.toDateString() === yesterday.toDateString()) {
      return `Kecha, ${hours}:${mins}`;
    }
    const day = String(d.getDate()).padStart(2, "0");
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const year = d.getFullYear();
    return `${day}.${month}.${year}`;
  } catch (e) {
    return "";
  }
}

// Videoni ma'lumotlar bazasiga saqlash
async function saveCompletedVideoToDatabase() {
  if (!state.preparedScenes || state.preparedScenes.length === 0) return null;

  const payload = {
    topic: state.topic || "Ta'limiy Video",
    age_group: state.selectedAge || "5-7",
    voice_id: state.selectedVoice || "lola",
    visual_style_id: state.visualStyle || "pixar_3d",
    duration: state.totalDuration || 0,
    thumbnail_url: (state.preparedScenes[0] && state.preparedScenes[0].image_url) ? state.preparedScenes[0].image_url : "/images/cinema_idle_poster.jpg",
    screenplay_data: state.screenplay || {},
    prepared_scenes: state.preparedScenes
  };

  try {
    const res = await fetch(`${API_URL}/api/user/videos/save`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (res.ok) {
      const data = await res.json();
      showToast("Video 'Mening Videolarim' kutubxonasiga saqlandi!", "success", "Saqlandi 💾");
      updateMyVideosBadge();
      return data;
    }
  } catch (err) {
    console.error("Videoni saqlashda xatolik:", err);
  }
  return null;
}

// Bosh sahifadagi "Videolarim" nishonini (badge) yangilash
window.updateMyVideosBadge = async function() {
  try {
    const res = await fetch(`${API_URL}/api/user/videos`);
    if (res.ok) {
      const data = await res.json();
      const badge = document.getElementById("myVideosBadge");
      if (badge) {
        if (data.count && data.count > 0) {
          badge.innerText = data.count;
          badge.classList.remove("hidden");
        } else {
          badge.classList.add("hidden");
        }
      }
    }
  } catch (e) {}
};

// Mening Videolarim oynasi
window.savedUserVideos = [];

window.openMyVideosModal = async function() {
  const modal = document.getElementById("myVideosModal");
  if (!modal) return;
  modal.classList.remove("hidden");
  
  const container = document.getElementById("myVideosContainer");
  if (!container) return;

  container.innerHTML = `
    <div class="py-12 flex flex-col items-center justify-center gap-3 text-slate-400">
      <div class="w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      <span class="text-xs font-bold font-fredoka">Videolaringiz yuklanmoqda...</span>
    </div>
  `;

  try {
    const res = await fetch(`${API_URL}/api/user/videos`);
    if (!res.ok) throw new Error("Videolarni yuklab bo'lmadi");
    const data = await res.json();
    const videos = data.videos || [];
    window.savedUserVideos = videos;

    const badge = document.getElementById("myVideosBadge");
    if (badge) {
      if (videos.length > 0) {
        badge.innerText = videos.length;
        badge.classList.remove("hidden");
      } else {
        badge.classList.add("hidden");
      }
    }

    if (videos.length === 0) {
      container.innerHTML = `
        <div class="text-center py-12 text-slate-400">
          <div class="text-5xl mb-3">📁</div>
          <p class="font-fredoka text-lg text-slate-700 font-bold">Hozircha saqlangan videolar yo'q</p>
          <p class="text-xs text-slate-400 mt-1 max-w-sm mx-auto">Yangi ta'limiy video yarating va u avtomatik tarzda shu yerda saqlanadi!</p>
        </div>
      `;
      return;
    }

    container.innerHTML = videos.map(v => {
      const sceneList = (v.screenplay && v.screenplay.prepared_scenes) ? v.screenplay.prepared_scenes : [];
      const sceneCount = sceneList.length;
      const durationStr = formatTime(v.duration || 0);
      const dateStr = formatRelativeDate(v.created_at);
      const thumb = v.thumbnail_url || (sceneList[0] ? sceneList[0].image_url : "/images/cinema_idle_poster.jpg");
      const cleanTitle = cleanTitleWithoutNumbers(v.topic);

      return `
        <div id="videoCard_${v.id}" class="p-4 rounded-2xl bg-white border border-slate-200 hover:border-indigo-200 hover:shadow-md transition-all flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="flex items-center gap-3.5 flex-1 min-w-0">
            <div class="relative w-20 h-14 rounded-xl overflow-hidden bg-slate-100 shrink-0 border border-slate-200 shadow-sm">
              <img src="${thumb}" class="w-full h-full object-cover" alt="Muqova" onerror="this.src='/images/cinema_idle_poster.jpg'">
              <span class="absolute bottom-1 right-1 px-1.5 py-0.5 rounded bg-black/75 text-[10px] text-white font-mono font-bold leading-tight">${durationStr}</span>
            </div>
            <div class="min-w-0 flex-1">
              <h4 class="font-fredoka font-bold text-base text-slate-800 truncate" title="${escapeHtml(cleanTitle)}">${escapeHtml(cleanTitle)}</h4>
              <div class="flex flex-wrap items-center gap-2 mt-1 text-xs text-slate-500">
                <span class="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 font-bold text-[11px]">${escapeHtml(v.age_group || '5-7')} yosh</span>
                <span>•</span>
                <span>${sceneCount} ta sahna</span>
                ${dateStr ? `<span>•</span><span class="text-slate-400">${dateStr}</span>` : ''}
              </div>
            </div>
          </div>
          <div id="videoCardActions_${v.id}" class="flex items-center gap-2 self-end sm:self-center shrink-0">
            <button onclick="loadAndPlaySavedVideo(${v.id})" class="px-3 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-fredoka font-bold text-xs flex items-center gap-1.5 shadow-sm transition-all cursor-pointer">
              <span>▶️</span> Ko'rish
            </button>
            <button onclick="downloadSavedVideoMp4(${v.id})" class="px-3 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-800 font-fredoka font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer" title="1080p Full HD MP4 video yuklab olish">
              <span>📥</span> MP4
            </button>
            <button onclick="openQuizForSavedVideo(${v.id})" class="px-3 py-2 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-800 font-fredoka font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer" title="Dars bo'yicha viktorina va test">
              <span>🧠</span> Test
            </button>
            <button onclick="printSavedVideoHandout(${v.id})" class="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-fredoka font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer" title="Dars uchun tarqatma varaq">
              <span>📄</span> Varaq
            </button>
            <button onclick="promptDeleteSavedVideo(${v.id})" class="p-2 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs transition-all cursor-pointer" title="O'chirish">
              🗑️
            </button>
          </div>
        </div>
      `;
    }).join("");

  } catch (err) {
    console.error("Videolarni yuklashda xatolik:", err);
    container.innerHTML = `
      <div class="text-center py-12 text-slate-400">
        <div class="text-4xl mb-2">⚠️</div>
        <p class="font-fredoka text-base text-rose-600 font-bold">Videolarni yuklab bo'lmadi</p>
        <button onclick="openMyVideosModal()" class="mt-3 px-4 py-2 bg-indigo-50 text-indigo-700 rounded-xl font-bold text-xs hover:bg-indigo-100">Qayta urinish</button>
      </div>
    `;
  }
};

window.closeMyVideosModal = function() {
  const modal = document.getElementById("myVideosModal");
  if (modal) modal.classList.add("hidden");
};

// Saqlangan videoni o'chirishni so'rash (sahifa ichidagi tasdiqlash)
window.promptDeleteSavedVideo = function(videoId) {
  const actionsEl = document.getElementById(`videoCardActions_${videoId}`);
  if (!actionsEl) return;
  actionsEl.innerHTML = `
    <div class="flex items-center gap-1.5 bg-rose-50 border border-rose-200 px-2.5 py-1.5 rounded-xl">
      <span class="text-xs text-rose-700 font-bold">O'chirilsinmi?</span>
      <button onclick="executeDeleteSavedVideo(${videoId})" class="px-2 py-1 bg-rose-600 text-white rounded-lg text-xs font-bold hover:bg-rose-700 cursor-pointer">Ha</button>
      <button onclick="openMyVideosModal()" class="px-2 py-1 bg-white text-slate-600 border border-slate-300 rounded-lg text-xs font-bold hover:bg-slate-50 cursor-pointer">Yo'q</button>
    </div>
  `;
};

// Videoni bazadan o'chirish
window.executeDeleteSavedVideo = async function(videoId) {
  try {
    const res = await fetch(`${API_URL}/api/user/videos/${videoId}`, {
      method: "DELETE"
    });
    if (res.ok) {
      showToast("Video muvaffaqiyatli o'chirildi.", "info", "O'chirildi 🗑️");
      await openMyVideosModal();
      updateMyVideosBadge();
    } else {
      showToast("Videoni o'chirishda xatolik yuz berdi.", "warning", "Xatolik ⚠️");
    }
  } catch (e) {
    showToast("Server bilan bog'lanishda xatolik.", "warning", "Xatolik ⚠️");
  }
};

// Saqlangan videoni pleyerga yuklash va ko'rish
window.loadAndPlaySavedVideo = function(videoId) {
  const v = (window.savedUserVideos || []).find(item => item.id === videoId);
  if (!v) {
    showToast("Video ma'lumotlari topilmadi.", "warning");
    return;
  }

  const prepScenes = (v.screenplay && v.screenplay.prepared_scenes) || [];
  if (prepScenes.length === 0) {
    showToast("Ushbu videoda tayyor sahnalar topilmadi.", "warning");
    return;
  }

  // Kadr rasmlarini brauzer xotirasiga oldindan yuklaymiz
  prepScenes.forEach(s => {
    if (s.image_url) {
      const img = new Image();
      img.src = s.image_url;
      imageCache[s.image_url] = img;
    }
  });

  state.preparedScenes = prepScenes;
  state.topic = v.topic;
  state.selectedAge = v.age_group || state.selectedAge;
  state.selectedVoice = v.voice_id || state.selectedVoice;
  state.visualStyle = v.visual_style_id || state.visualStyle;
  state.totalDuration = v.duration || prepScenes.reduce((a, s) => a + (s.duration || 5), 0);
  state.screenplay = (v.screenplay && v.screenplay.screenplay) ? v.screenplay.screenplay : {
    title: v.topic,
    moral_summary: "Bilim — eng katta boylikdir!",
    scenes: prepScenes
  };

  closeMyVideosModal();
  goToStep(5);
  setupCanvasPlayer();
  initCinemaPlayer();
  showToast("Video ochildi va tomoshaga tayyor!", "success", "Ko'rish 🎬");

  // Kichik kechikish bilan avtomatik ijroni boshlaymiz
  setTimeout(() => {
    if (!state.isPlaying) {
      togglePlayPause();
    }
  }, 150);
};

// Saqlangan video uchun tarqatma varaq chiqarish
window.printSavedVideoHandout = function(videoId) {
  const v = (window.savedUserVideos || []).find(item => item.id === videoId);
  if (!v) return;
  const scenes = (v.screenplay && v.screenplay.prepared_scenes) || [];
  const moral = (v.screenplay && v.screenplay.screenplay && v.screenplay.screenplay.moral_summary) || "Bilim — eng katta boylikdir!";
  openFlashcardsPrintView(scenes, v.topic, moral);
};

// Saqlangan videoni 1080p Full HD MP4 formatida yuklab olish
window.downloadSavedVideoMp4 = async function(videoId) {
  const v = (window.savedUserVideos || []).find(item => item.id === videoId);
  if (!v) {
    showToast("Video ma'lumotlari topilmadi.", "warning");
    return;
  }

  // Agar video_url bazada allaqachon mavjud bo'lsa
  if (v.video_url) {
    const filename = v.video_url.split("/").pop();
    const downloadUrl = `/api/user/videos/download-file/${filename}`;
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = filename || `TasvirLab_${v.topic}.mp4`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast("1080p Full HD MP4 video yuklab olinmoqda...", "success", "Yuklanmoqda 📥");
    return;
  }

  // Agar hali render qilinmagan bo'lsa, serverda render qilamiz
  const prepScenes = (v.screenplay && v.screenplay.prepared_scenes) || [];
  if (prepScenes.length === 0) {
    showToast("Ushbu videoda tayyor sahnalar topilmadi.", "warning");
    return;
  }

  showLoading("🎬 Serverda 1080p Full HD MP4 video render qilinmoqda (FFmpeg)...\nIltimos, kuting — kadrlar va ovozlar yuqori sifatda birlashtirilmoqda!");

  try {
    const payload = {
      video_id: v.id,
      topic: v.topic,
      age_group: v.age_group || "5-7",
      voice_id: v.voice_id || "lola",
      visual_style_id: v.visual_style_id || "pixar_3d",
      bgm_track: "bgm_cheerful.mp3",
      moral_summary: (v.screenplay && v.screenplay.screenplay && v.screenplay.screenplay.moral_summary) || (v.screenplay && v.screenplay.moral_summary) || "Bilim — eng katta boylik va kuchdir!",
      prepared_scenes: prepScenes,
      quiz_data: (v.screenplay && v.screenplay.quiz) || null,
      save_to_db: true
    };

    const res = await fetch(`${API_URL}/api/user/videos/render-mp4`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Serverda render qilishda xatolik yuz berdi.");
    }

    const data = await res.json();
    v.video_url = data.video_url;

    const a = document.createElement("a");
    a.href = data.download_url || data.video_url;
    a.download = data.filename;
    document.body.appendChild(a);
    a.click();
    a.remove();

    hideLoading();
    showToast(`1080p Full HD MP4 video yuklab olindi! (${data.size_mb} MB, 30 FPS)`, "success", "Tayyor! 🎉");
    openMyVideosModal();
  } catch (err) {
    hideLoading();
    console.error("Download error:", err);
    showToast("Videoni render qilishda xatolik: " + (err.message || err), "error");
  }
};

// ==========================================
// QUIZ & TEST GENERATOR (2-BOSQICH)
// ==========================================
const quizState = {
  currentQuiz: null,
  currentQuestionIndex: 0,
  score: 0,
  selectedOption: null,
  isAnswered: false
};

// Viktorina oynasini ochish
window.openQuizModal = async function(customQuizData = null, customTopic = null, customAge = null, customScreenplay = null) {
  const modal = document.getElementById("quizModal");
  if (!modal) return;
  modal.classList.remove("hidden");

  const container = document.getElementById("quizContainer");
  if (!container) return;

  // Agar tayyor viktorina ma'lumotlari uzatilgan bo'lsa
  if (customQuizData && customQuizData.questions && customQuizData.questions.length > 0) {
    quizState.currentQuiz = customQuizData;
    quizState.currentQuestionIndex = 0;
    quizState.score = 0;
    quizState.selectedOption = null;
    quizState.isAnswered = false;
    renderQuizQuestion();
    return;
  }

  const targetTopic = customTopic || state.topic || "Ta'limiy Dars";
  const targetAge = customAge || state.selectedAge || "5-7";
  let targetScreenplay = customScreenplay || state.screenplay || {};
  const currentScenes = (state.preparedScenes && state.preparedScenes.length > 0)
    ? state.preparedScenes
    : (targetScreenplay.scenes || []);

  targetScreenplay = {
    ...targetScreenplay,
    title: targetScreenplay.title || targetTopic,
    moral_summary: targetScreenplay.moral_summary || (state.screenplay && state.screenplay.moral_summary) || "Bilim — eng katta boylikdir!",
    scenes: currentScenes
  };

  container.innerHTML = `
    <div class="py-12 flex flex-col items-center justify-center gap-3 text-slate-500">
      <div class="w-10 h-10 border-3 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
      <span class="text-sm font-bold font-fredoka text-slate-800">O'qituvchi viktorinasi tuzilmoqda...</span>
      <span class="text-xs text-slate-400">Dars mazmuni bo'yicha pedagogik savollar tayyorlanmoqda</span>
    </div>
  `;

  try {
    const res = await fetch(`${API_URL}/api/generate-quiz`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: targetTopic,
        age_group: targetAge,
        screenplay: targetScreenplay,
        api_key: ""
      })
    });

    if (!res.ok) throw new Error("Viktorina yaratishda xatolik");

    const quiz = await res.json();
    quizState.currentQuiz = quiz;
    quizState.currentQuestionIndex = 0;
    quizState.score = 0;
    quizState.selectedOption = null;
    quizState.isAnswered = false;

    renderQuizQuestion();
  } catch (err) {
    console.error("Viktorina yuklashda xatolik:", err);
    container.innerHTML = `
      <div class="text-center py-8 text-slate-500">
        <div class="text-4xl mb-2">⚠️</div>
        <p class="font-fredoka text-base text-rose-600 font-bold">Savollarni yuklab bo'lmadi</p>
        <button onclick="openQuizModal()" class="mt-3 px-4 py-2 bg-amber-100 text-amber-800 rounded-xl font-bold text-xs hover:bg-amber-200 cursor-pointer">Qayta urinish</button>
      </div>
    `;
  }
};

window.closeQuizModal = function() {
  const modal = document.getElementById("quizModal");
  if (modal) modal.classList.add("hidden");
};

// Viktorinaning joriy savolini chizish
function renderQuizQuestion() {
  const container = document.getElementById("quizContainer");
  const quiz = quizState.currentQuiz;
  if (!container || !quiz || !quiz.questions) return;

  const qIndex = quizState.currentQuestionIndex;
  const total = quiz.questions.length;
  const q = quiz.questions[qIndex];

  document.getElementById("quizModalTitle").innerText = quiz.quiz_title || `Darslik Viktorinasi`;
  document.getElementById("quizModalSub").innerText = `${quiz.topic} • ${quiz.age_group} yosh`;

  const pct = Math.round(((qIndex) / total) * 100);

  container.innerHTML = `
    <!-- Yuqori holat satri -->
    <div class="flex items-center justify-between text-xs text-slate-500 pb-2">
      <span class="font-fredoka font-bold text-amber-600 bg-amber-50 px-3 py-1 rounded-full">${qIndex + 1} / ${total} - savol</span>
      <span class="font-bold text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">To'g'ri javoblar: ${quizState.score} ta</span>
    </div>

    <!-- Progress bar -->
    <div class="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden mb-4">
      <div class="bg-gradient-to-r from-amber-500 to-indigo-600 h-full transition-all duration-300" style="width: ${pct}%"></div>
    </div>

    <!-- Savol matni -->
    <div class="p-4 sm:p-5 rounded-2xl bg-slate-50 border border-slate-200 mb-4">
      <h4 class="font-fredoka text-base sm:text-lg font-bold text-slate-800 leading-snug">
        ${escapeHtml(q.question)}
      </h4>
    </div>

    <!-- Variantlar -->
    <div id="quizOptionsList" class="space-y-2.5">
      ${q.options.map((opt, idx) => `
        <button id="quizOpt_${idx}" onclick="handleQuizSelectOption(${idx})" class="w-full text-left p-3.5 rounded-2xl border border-slate-200 hover:border-amber-400 hover:bg-amber-50/40 transition-all font-medium text-sm text-slate-800 flex items-center gap-3 cursor-pointer">
          <span id="quizOptLetter_${idx}" class="w-7 h-7 rounded-xl bg-slate-100 text-slate-600 font-fredoka font-bold flex items-center justify-center text-xs shrink-0">${['A', 'B', 'C', 'D'][idx]}</span>
          <span class="flex-1">${escapeHtml(opt)}</span>
        </button>
      `).join("")}
    </div>

    <!-- Izoh qutisi -->
    <div id="quizFeedbackBox" class="hidden"></div>

    <!-- Keyingi savolga o'tish tugmasi -->
    <div id="quizNextBtnBox" class="pt-3 flex justify-end hidden">
      <button onclick="handleQuizNextQuestion()" class="px-6 py-2.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-fredoka font-bold text-sm shadow-md transition-all flex items-center gap-2 cursor-pointer">
        <span>${(qIndex + 1 === total) ? "Natijalarni ko'rish 🏆" : "Keyingi savol ➔"}</span>
      </button>
    </div>
  `;
}

// Variant tanlanganda
window.handleQuizSelectOption = function(selectedIdx) {
  if (quizState.isAnswered) return;
  quizState.isAnswered = true;
  quizState.selectedOption = selectedIdx;

  const quiz = quizState.currentQuiz;
  const q = quiz.questions[quizState.currentQuestionIndex];
  const isCorrect = (selectedIdx === q.correct_index);

  if (isCorrect) {
    quizState.score++;
  }

  // Variantlarni belgilash
  q.options.forEach((_, idx) => {
    const btn = document.getElementById(`quizOpt_${idx}`);
    const letter = document.getElementById(`quizOptLetter_${idx}`);
    if (!btn || !letter) return;
    btn.disabled = true;
    btn.classList.remove("cursor-pointer", "hover:border-amber-400", "hover:bg-amber-50/40");

    if (idx === q.correct_index) {
      btn.className = "w-full text-left p-3.5 rounded-2xl border-2 border-emerald-500 bg-emerald-50 text-emerald-950 font-bold flex items-center gap-3 shadow-sm";
      letter.className = "w-7 h-7 rounded-xl bg-emerald-500 text-white font-bold flex items-center justify-center text-xs shrink-0";
    } else if (idx === selectedIdx && !isCorrect) {
      btn.className = "w-full text-left p-3.5 rounded-2xl border-2 border-rose-400 bg-rose-50 text-rose-900 font-medium flex items-center gap-3";
      letter.className = "w-7 h-7 rounded-xl bg-rose-500 text-white font-bold flex items-center justify-center text-xs shrink-0";
    } else {
      btn.className = "w-full text-left p-3.5 rounded-2xl border border-slate-200 bg-white opacity-50 flex items-center gap-3";
    }
  });

  // Izoh qutisini ko'rsatish
  const feedbackBox = document.getElementById("quizFeedbackBox");
  if (feedbackBox) {
    feedbackBox.classList.remove("hidden");
    if (isCorrect) {
      feedbackBox.innerHTML = `
        <div class="mt-4 p-3.5 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs sm:text-sm font-medium flex items-start gap-2.5">
          <span class="text-2xl shrink-0">🎉</span>
          <div>
            <div class="font-fredoka font-bold text-emerald-700 text-sm mb-0.5">To'ppa-to'g'ri, barakalla!</div>
            <div>${escapeHtml(q.explanation)}</div>
          </div>
        </div>
      `;
    } else {
      feedbackBox.innerHTML = `
        <div class="mt-4 p-3.5 rounded-2xl bg-amber-50 border border-amber-200 text-amber-900 text-xs sm:text-sm font-medium flex items-start gap-2.5">
          <span class="text-2xl shrink-0">💡</span>
          <div>
            <div class="font-fredoka font-bold text-amber-700 text-sm mb-0.5">Yaxshi harakat! Keling, eslab qolamiz:</div>
            <div>${escapeHtml(q.explanation)}</div>
          </div>
        </div>
      `;
    }
  }

  // Keyingi tugmani ko'rsatish
  const nextBtnBox = document.getElementById("quizNextBtnBox");
  if (nextBtnBox) nextBtnBox.classList.remove("hidden");
};

// Keyingi savolga o'tish
window.handleQuizNextQuestion = function() {
  quizState.currentQuestionIndex++;
  const total = quizState.currentQuiz.questions.length;

  if (quizState.currentQuestionIndex >= total) {
    renderQuizResults();
  } else {
    quizState.isAnswered = false;
    quizState.selectedOption = null;
    renderQuizQuestion();
  }
};

// Yakuniy natijalar ekrani
function renderQuizResults() {
  const container = document.getElementById("quizContainer");
  const quiz = quizState.currentQuiz;
  if (!container || !quiz) return;

  const total = quiz.questions.length;
  const score = quizState.score;
  const pct = Math.round((score / total) * 100);

  let stars = "⭐⭐⭐";
  let greeting = "Ofarin! Siz darsni a'lo darajada o'zlashtirdingiz!";
  let badgeColor = "bg-emerald-50 text-emerald-700 border-emerald-200";

  if (pct < 50) {
    stars = "⭐";
    greeting = "Yaxshi boshlanish! Videoni yana bir bor ko'rib, bilimlarni mustahkamlash mumkin!";
    badgeColor = "bg-amber-50 text-amber-700 border-amber-200";
  } else if (pct < 100) {
    stars = "⭐⭐";
    greeting = "Juda yaxshi natija! Siz ko'p narsalarni to'g'ri topdingiz!";
    badgeColor = "bg-indigo-50 text-indigo-700 border-indigo-200";
  }

  container.innerHTML = `
    <div class="text-center py-6 space-y-4">
      <div class="text-4xl animate-bounce">${stars}</div>
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border text-sm font-fredoka font-bold ${badgeColor}">
        Natija: ${total} tadan ${score} ta to'g'ri (${pct}%)
      </div>
      <h3 class="font-fredoka text-xl sm:text-2xl font-bold text-slate-800">
        ${greeting}
      </h3>
      <div class="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-100 text-left text-xs sm:text-sm text-indigo-900 max-w-lg mx-auto leading-relaxed">
        <strong>💡 Dars Sabog'i:</strong> ${escapeHtml(quiz.moral_takeaway || "Bilim — eng katta boylikdir!")}
      </div>

      <div class="flex flex-wrap items-center justify-center gap-3 pt-4">
        <button onclick="openQuizModal(quizState.currentQuiz)" class="px-5 py-2.5 rounded-2xl bg-white border border-slate-300 text-slate-700 font-fredoka font-bold text-xs hover:bg-slate-50 transition-all flex items-center gap-1.5 cursor-pointer shadow-sm">
          <span>🔄</span> Qaytadan
        </button>
        <button onclick="openQuizPrintView(quizState.currentQuiz)" class="px-5 py-2.5 rounded-2xl bg-amber-500 hover:bg-amber-600 text-white font-fredoka font-bold text-xs shadow-md transition-all flex items-center gap-1.5 cursor-pointer">
          <span>🖨️</span> Chop etish (Test varaqasi)
        </button>
        <button onclick="closeQuizModal()" class="px-5 py-2.5 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-fredoka font-bold text-xs shadow-md transition-all flex items-center gap-1.5 cursor-pointer">
          <span>🎬</span> Videoga qaytish
        </button>
      </div>
    </div>
  `;
}

// O'qituvchi va ota-onalar uchun test varaqasini chop etish (Javoblar kaliti alohida 2-sahifada)
window.openQuizPrintView = function(quizData = null) {
  const quiz = quizData || quizState.currentQuiz;
  if (!quiz || !quiz.questions || quiz.questions.length === 0) {
    showToast("Test varaqasini chiqarish uchun avval viktorinani oching.", "warning");
    return;
  }

  const printWin = window.open("", "_blank");
  if (!printWin) {
    showToast("Iltimos, brauzeringizda yangi oynalarga ruxsat bering!", "warning");
    return;
  }

  const title = escapeHtml(quiz.quiz_title || `Darslik Testi: ${quiz.topic}`);
  const topic = escapeHtml(quiz.topic || "Ta'limiy mavzu");
  const ageGroup = escapeHtml(quiz.age_group || "Umumiy");
  const moralTakeaway = escapeHtml(quiz.moral_takeaway || "Bilim olish insonni dono va ma'rifatli qiladi.");
  const letters = ['A', 'B', 'C', 'D'];

  const questionsHtml = quiz.questions.map((q, idx) => `
    <div class="quiz-item">
      <div class="q-title">${idx + 1}. ${escapeHtml(q.question)}</div>
      <div class="q-options">
        ${q.options.map((opt, oIdx) => `
          <div class="opt-row">
            <span class="opt-circle">${letters[oIdx] || (oIdx + 1)}</span>
            <span class="opt-text">${escapeHtml(opt)}</span>
          </div>
        `).join("")}
      </div>
    </div>
  `).join("");

  const answersKeyHtml = quiz.questions.map((q, idx) => {
    const correctLetter = letters[q.correct_index] || 'A';
    const correctText = q.options && q.options[q.correct_index] ? escapeHtml(q.options[q.correct_index]) : '';
    const explanation = escapeHtml(q.explanation || "To'g'ri javob");
    return `
      <div class="answer-card">
        <div class="q-ref"><strong>${idx + 1}-savol:</strong> ${escapeHtml(q.question)}</div>
        <div style="margin: 8px 0 6px 0;">
          <span class="correct-badge">To'g'ri javob: [${correctLetter}] ${correctText}</span>
        </div>
        <div class="explanation-text">
          <strong>💡 Mantiqiy-metodik izoh:</strong> ${explanation}
        </div>
      </div>
    `;
  }).join("");

  printWin.document.write(`<!DOCTYPE html>
<html lang="uz">
<head>
  <title>${title} — O'quvchi test varaqasi</title>
  <meta charset="utf-8">
  <style>
    @page {
      size: A4 portrait;
      margin: 14mm 16mm 14mm 16mm;
    }
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #0f172a;
      line-height: 1.5;
      margin: 0;
      padding: 0;
      background: #f8fafc;
    }
    .no-print { display: block; }

    /* Ekran ko'rinishi */
    .print-bar {
      max-width: 800px;
      margin: 20px auto 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 10px;
    }
    .print-hint {
      font-size: 13px;
      color: #64748b;
      font-weight: 500;
    }
    .print-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #d97706;
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
      padding: 10px 22px;
      border-radius: 10px;
      border: none;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(217, 119, 6, 0.35);
      transition: background 0.15s ease;
    }
    .print-btn:hover {
      background: #b45309;
    }
    .page-sheet {
      background: #ffffff;
      max-width: 800px;
      margin: 18px auto 26px auto;
      padding: 34px 40px;
      border-radius: 14px;
      border: 1px solid #e2e8f0;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }
    .screen-divider {
      max-width: 800px;
      margin: 30px auto;
      text-align: center;
      border-top: 2px dashed #94a3b8;
      position: relative;
    }
    .screen-divider span {
      position: relative;
      top: -13px;
      background: #e2e8f0;
      padding: 6px 18px;
      font-size: 12px;
      font-weight: 700;
      color: #334155;
      border-radius: 20px;
    }

    /* Sarlavhalar va bloklar */
    .header {
      text-align: center;
      border-bottom: 2px solid #f59e0b;
      padding-bottom: 12px;
      margin-bottom: 18px;
    }
    .header.answer-header {
      border-bottom-color: #6366f1;
    }
    .header h1 {
      margin: 0 0 5px 0;
      color: #b45309;
      font-size: 22px;
      font-weight: 800;
    }
    .header.answer-header h1 {
      color: #4338ca;
    }
    .header p {
      margin: 0;
      font-size: 13px;
      color: #64748b;
    }
    .meta-box {
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 13px;
      font-weight: 600;
      color: #334155;
      margin-top: 14px;
      border: 1px dashed #cbd5e1;
      padding: 10px 14px;
      border-radius: 8px;
      background: #f8fafc;
    }
    .instruction-box {
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 8px;
      padding: 9px 13px;
      font-size: 12.5px;
      color: #92400e;
      margin-bottom: 18px;
      font-weight: 500;
    }

    /* Savollar */
    .quiz-item {
      margin-bottom: 18px;
      padding: 15px 18px;
      border: 1.5px solid #e2e8f0;
      border-radius: 12px;
      background: #ffffff;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    .q-title {
      font-weight: 700;
      font-size: 14.5px;
      color: #0f172a;
      margin-bottom: 11px;
    }
    .q-options {
      display: flex;
      flex-direction: column;
      gap: 9px;
    }
    .opt-row {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 13.5px;
      color: #334155;
    }
    .opt-circle {
      display: inline-flex;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border: 1.5px solid #64748b;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: bold;
      color: #475569;
      flex-shrink: 0;
    }
    .page-footer {
      text-align: center;
      font-size: 11px;
      color: #94a3b8;
      margin-top: 22px;
      border-top: 1px solid #f1f5f9;
      padding-top: 10px;
    }

    /* Javoblar kaliti sahifasi (2-sahifa) */
    .answer-card {
      margin-bottom: 15px;
      padding: 14px 17px;
      border: 1.5px solid #e0e7ff;
      border-radius: 12px;
      background: #faf5ff;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    .answer-card .q-ref {
      font-weight: 700;
      font-size: 13.5px;
      color: #1e1b4b;
      margin-bottom: 6px;
    }
    .answer-card .correct-badge {
      display: inline-block;
      background: #059669;
      color: #ffffff;
      font-weight: 700;
      font-size: 12px;
      padding: 3px 10px;
      border-radius: 6px;
    }
    .answer-card .explanation-text {
      font-size: 12.5px;
      color: #475569;
      line-height: 1.45;
      margin-top: 6px;
    }
    .moral-box {
      margin-top: 20px;
      padding: 12px 16px;
      background: #ecfdf5;
      border: 1.5px solid #a7f3d0;
      border-radius: 10px;
      font-size: 13px;
      color: #065f46;
      page-break-inside: avoid;
      break-inside: avoid;
    }
    .signature-box {
      margin-top: 24px;
      display: flex;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 12.5px;
      color: #475569;
      border-top: 1px dashed #cbd5e1;
      padding-top: 15px;
      page-break-inside: avoid;
      break-inside: avoid;
    }

    /* Chop etish (Print) qoidalari */
    @media print {
      body {
        background: #ffffff !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 12.5px !important;
      }
      .no-print {
        display: none !important;
      }
      .page-sheet {
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
      }
      .page-break {
        page-break-before: always !important;
        break-before: page !important;
        clear: both !important;
        padding-top: 8mm !important;
      }
      .quiz-item {
        border-color: #cbd5e1 !important;
        padding: 12px 14px !important;
        margin-bottom: 12px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .answer-card {
        border-color: #cbd5e1 !important;
        background: #f8fafc !important;
        padding: 12px 14px !important;
        margin-bottom: 12px !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
    }
  </style>
</head>
<body>
  <!-- Yuqori boshqaruv paneli (Faqat ekranda ko'rinadi) -->
  <div class="print-bar no-print">
    <div class="print-hint">
      📄 1-sahifa: O'quvchi test varaqasi | 2-sahifa: Javoblar kaliti
    </div>
    <button class="print-btn" onclick="window.print()">
      🖨️ Chop etish (A4 / PDF)
    </button>
  </div>

  <!-- 1-SAHIFA: O'QUVCHI UCHUN TEST VARAQASI -->
  <div class="page-sheet student-page">
    <div class="header">
      <h1>${title}</h1>
      <p>Ta'limiy Video Darslik • Mavzu: <strong>${topic}</strong> (${ageGroup} yosh)</p>
      <div class="meta-box">
        <span>O'quvchi ismi: __________________________</span>
        <span>Sinf / Guruh: _________</span>
        <span>Sana: ____________</span>
        <span>Baho / Ball: _______</span>
      </div>
    </div>

    <div class="instruction-box">
      📋 <strong>Ko'rsatma:</strong> Har bir savolni diqqat bilan o'qib chiqing va to'g'ri deb bilgan javob variantini doirachasiga belgilang.
    </div>

    <div class="quiz-list">
      ${questionsHtml}
    </div>

    <div class="page-footer">
      TasvirLab Ta'lim Platformasi • O'quvchi uchun mustaqil topshiriq varaqasi (1-sahifa)
    </div>
  </div>

  <!-- Ekranda ko'rinadigan bo'luvchi chiziq (Chop etishda chiqmaydi) -->
  <div class="screen-divider no-print">
    <span>✂️ Chop etilganda yoki PDF ga saqlanganda javoblar kaliti quyidagi ALOHIDA 2-VAROQDA chiqadi</span>
  </div>

  <!-- 2-SAHIFA: O'QITUVCHI VA OTA-ONALAR UCHUN JAVOBLAR KALITI -->
  <div class="page-sheet answer-key-page page-break">
    <div class="header answer-header">
      <h1>🔑 TO'G'RI JAVOBLAR KALITI VA METODIK IZOHLAR</h1>
      <p>O'qituvchilar va ota-onalar uchun mo'ljallangan tekshiruv varaqasi (2-sahifa)</p>
      <div class="meta-box">
        <span>Mavzu: <strong>${topic}</strong></span>
        <span>Savollar soni: <strong>${quiz.questions.length} ta</strong></span>
        <span>Yosh guruhi: <strong>${ageGroup} yosh</strong></span>
      </div>
    </div>

    <div class="answers-list">
      ${answersKeyHtml}
    </div>

    <div class="moral-box">
      <strong>🌟 Darsning tarbiyaviy sabog'i:</strong> ${moralTakeaway}
    </div>

    <div class="signature-box">
      <span>Tekshirdi (Ustoz / Ota-ona): __________________________</span>
      <span>Imzo: ____________</span>
      <span>Sana: ____________</span>
    </div>

    <div class="page-footer">
      TasvirLab Ta'lim Platformasi • Pedagogik nazorat va baholash varaqasi (2-sahifa)
    </div>
  </div>
</body>
</html>`);
  printWin.document.close();
};

// Saqlangan video uchun viktorina ochish
window.openQuizForSavedVideo = function(videoId) {
  const v = (window.savedUserVideos || []).find(item => item.id === videoId);
  if (!v) return;

  const savedQuiz = v.screenplay && v.screenplay.quiz;
  const rawScreenplay = (v.screenplay && v.screenplay.screenplay) ? v.screenplay.screenplay : {};
  const scenes = (v.screenplay && v.screenplay.prepared_scenes) || (rawScreenplay.scenes || []);

  const screenplay = {
    ...rawScreenplay,
    title: v.topic,
    moral_summary: rawScreenplay.moral_summary || "Bilim — eng katta boylikdir!",
    scenes: scenes
  };

  closeMyVideosModal();
  openQuizModal(savedQuiz, v.topic, v.age_group, screenplay);
};

// ==============================================================================
// 👤 FOYDALANUVCHILAR VA ADMINISTRATOR TIZIMI (AUTH & ADMIN PANEL)
// ==============================================================================

window.currentUser = null;

// Avtorizatsiya sarlavhalari (Bearer token bilan)
window.getAuthHeaders = function() {
  const token = localStorage.getItem("tasvirlab_token");
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
};

// Dastur ishga tushganda tokenni tekshirish va profilni yuklash
window.initAuthAndUser = async function() {
  const token = localStorage.getItem("tasvirlab_token");
  if (!token) {
    updateUserHeaderUI(null);
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/auth/me`, {
      headers: getAuthHeaders()
    });
    if (res.ok) {
      const data = await res.json();
      window.currentUser = data.user;
      updateUserHeaderUI(data.user);
    } else {
      localStorage.removeItem("tasvirlab_token");
      localStorage.removeItem("tasvirlab_is_admin");
      updateUserHeaderUI(null);
    }
  } catch (err) {
    console.warn("[Auth] Profil yuklanmadi:", err);
    updateUserHeaderUI(null);
  }
};

// Yuqori header qismidagi foydalanuvchi ma'lumotlarini yangilash
window.updateUserHeaderUI = function(rawUser) {
  const userHeaderArea = document.getElementById("userHeaderArea");
  const creditDisplay = document.getElementById("headerCreditDisplay");
  const adminBtn = document.getElementById("btnAdminPanel");

  if (!userHeaderArea) return;

  const user = (rawUser && rawUser.user) ? rawUser.user : rawUser;

  if (user) {
    // Balansni aniqlash - hech qachon undefined bo'lmasligi uchun
    let balance = 0;
    if (typeof user.credits_balance === "number") {
      balance = user.credits_balance;
    } else if (user.credits_balance !== undefined && user.credits_balance !== null && !isNaN(Number(user.credits_balance))) {
      balance = Number(user.credits_balance);
    } else if (window.currentUser && typeof window.currentUser.credits_balance === "number") {
      balance = window.currentUser.credits_balance;
    }

    if (creditDisplay) {
      creditDisplay.innerText = `${balance} ta video`;
    }

    const modalCredit = document.getElementById("modalCreditCount");
    if (modalCredit) {
      modalCredit.innerText = `${balance} ta video`;
    }

    // Admin bo'lsa boshqaruv tugmasini ko'rsatish
    if (user.is_admin && adminBtn) {
      adminBtn.classList.remove("hidden");
    } else if (adminBtn) {
      adminBtn.classList.add("hidden");
    }

    // Profil chipi
    const displayName = escapeHtml(user.full_name || user.phone_number || "Foydalanuvchi");
    userHeaderArea.innerHTML = `
      <div class="flex items-center gap-2 bg-indigo-50 border border-indigo-200/80 px-3 py-1.5 rounded-2xl">
        <span class="text-base">${user.is_admin ? '👑' : '👤'}</span>
        <span class="text-xs font-bold text-indigo-950 max-w-[110px] truncate">${displayName}</span>
        <button onclick="logoutUser()" title="Chiqish" class="text-slate-400 hover:text-rose-600 font-bold text-xs ml-1 transition-colors cursor-pointer">
          ✕
        </button>
      </div>
    `;
  } else {
    if (adminBtn) adminBtn.classList.add("hidden");
    if (creditDisplay) creditDisplay.innerText = "3 ta bepul video";
    const modalCredit = document.getElementById("modalCreditCount");
    if (modalCredit) modalCredit.innerText = "3 ta video";
    userHeaderArea.innerHTML = `
      <button id="btnOpenAuth" onclick="openAuthModal()" class="px-4 py-2 rounded-2xl bg-indigo-600 hover:bg-indigo-700 text-white font-fredoka font-bold text-xs shadow-md transition-all flex items-center gap-1.5 cursor-pointer">
        <span>👤</span> <span>Kirish</span>
      </button>
    `;
  }
};

// Tizimdan chiqish
window.logoutUser = function() {
  localStorage.removeItem("tasvirlab_token");
  localStorage.removeItem("tasvirlab_is_admin");
  window.currentUser = null;
  updateUserHeaderUI(null);
  showToast("Tizimdan muvaffaqiyatli chiqdingiz.", "info");
};

// ==================== AUTH MODAL BOSHQARUVI ====================

window.openAuthModal = function() {
  const modal = document.getElementById("authModal");
  if (modal) modal.classList.remove("hidden");
  switchAuthTab('phone');
};

window.closeAuthModal = function() {
  const modal = document.getElementById("authModal");
  if (modal) modal.classList.add("hidden");
  const otpSec = document.getElementById("authOtpSection");
  if (otpSec) otpSec.classList.add("hidden");
  const phoneBtn = document.getElementById("authPhoneSubmitBtn");
  if (phoneBtn) phoneBtn.innerHTML = `<span>SMS kodni olish</span> <span>→</span>`;
  if (window.telegramPollingTimer) {
    clearInterval(window.telegramPollingTimer);
    window.telegramPollingTimer = null;
  }
};

window.switchAuthTab = function(tabName) {
  const tabs = ['phone', 'google', 'telegram', 'password'];
  tabs.forEach(t => {
    const btn = document.getElementById(`authTab${t.charAt(0).toUpperCase() + t.slice(1)}Btn`);
    const panel = document.getElementById(`authTab${t.charAt(0).toUpperCase() + t.slice(1)}`);
    if (btn && panel) {
      if (t === tabName) {
        btn.className = "flex-1 py-2 rounded-xl bg-white text-indigo-600 shadow-sm transition-all cursor-pointer font-bold flex items-center justify-center gap-1.5";
        panel.classList.remove("hidden");
      } else {
        btn.className = "flex-1 py-2 rounded-xl text-slate-600 hover:text-slate-900 transition-all cursor-pointer font-bold flex items-center justify-center gap-1.5";
        panel.classList.add("hidden");
      }
    }
  });

  if (tabName === 'google') {
    if (typeof window.setupGoogleAuthIfNeeded === 'function') {
      window.setupGoogleAuthIfNeeded();
    }
  }
};

// 1. Telefon (SMS OTP) orqali kirish
window.handlePhoneAuthStep = async function() {
  const phoneInput = document.getElementById("authPhoneInput");
  const otpInput = document.getElementById("authOtpInput");
  const otpSection = document.getElementById("authOtpSection");
  const btn = document.getElementById("authPhoneSubmitBtn");
  const hint = document.getElementById("authOtpHint");

  const phone = (phoneInput.value || "").trim();
  if (phone.length < 9) {
    showToast("Iltimos, to'liq telefon raqamingizni kiriting (+998...).", "warning");
    return;
  }

  // 1-bosqich: SMS kod yuborish
  if (otpSection.classList.contains("hidden")) {
    btn.disabled = true;
    btn.innerText = "Yuborilmoqda...";
    try {
      const res = await fetch(`${API_URL}/api/auth/send-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone_number: phone })
      });
      const data = await res.json();
      if (res.ok) {
        otpSection.classList.remove("hidden");
        btn.innerHTML = `<span>Tasdiqlash va Kirish</span> <span>🎉</span>`;
        hint.innerText = "Telefoningizga 6 xonali SMS kod yuborildi. Uni kiriting.";
        otpInput.value = "";
        showToast("SMS kod yuborildi!", "success");
      } else {
        showToast(data.detail || "SMS yuborishda xatolik yuz berdi.", "error");
      }
    } catch (e) {
      showToast("Server bilan bog'lanishda xatolik.", "error");
    } finally {
      btn.disabled = false;
    }
    return;
  }

  // 2-bosqich: SMS kodni tekshirish
  const code = (otpInput.value || "").trim();
  if (code.length < 4) {
    showToast("SMS kodni kiriting.", "warning");
    return;
  }

  btn.disabled = true;
  btn.innerText = "Tekshirilmoqda...";
  try {
    const res = await fetch(`${API_URL}/api/auth/verify-otp`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone_number: phone, code: code })
    });
    const data = await res.json();
    if (res.ok && data.access_token) {
      localStorage.setItem("tasvirlab_token", data.access_token);
      window.currentUser = data.user;
      updateUserHeaderUI(data.user);
      closeAuthModal();
      showToast(data.message || "Xush kelibsiz! 3 ta bepul video hisobingizga qo'shildi 🎉", "success");
    } else {
      showToast(data.detail || "Tasdiqlash kodi noto'g'ri.", "error");
    }
  } catch (e) {
    showToast("Server bilan bog'lanishda xatolik.", "error");
  } finally {
    btn.disabled = false;
  }
};

// 2. Google orqali kirish (Google Identity Services & OAuth 2.0)
window.cachedPublicAuthConfig = null;

async function fetchPublicAuthConfig() {
  if (window.cachedPublicAuthConfig) return window.cachedPublicAuthConfig;
  try {
    const res = await fetch(`${API_URL}/api/auth/config`);
    if (res.ok) {
      window.cachedPublicAuthConfig = await res.json();
      return window.cachedPublicAuthConfig;
    }
  } catch (e) {
    console.error("Auth config yuklashda xatolik:", e);
  }
  return { google_client_id: "", telegram_bot_username: "" };
}

window.setupGoogleAuthIfNeeded = async function() {
  const cfg = await fetchPublicAuthConfig();
  const clientId = cfg.google_client_id;
  const statusBox = document.getElementById("googleStatusNoteBox");
  const troubleshootBox = document.getElementById("googleTroubleshootBox");
  
  if (!clientId) {
    if (statusBox) {
      statusBox.innerHTML = `⚠️ <strong>Google Client ID ulanmagan:</strong> Admin panelida Google Client ID ni kiriting.`;
      statusBox.className = "p-3 bg-amber-50 border border-amber-200 rounded-2xl text-[11px] text-amber-900 text-center leading-relaxed";
    }
    return;
  }

  // Google SDK yuklanganligini tekshirish
  let attempts = 0;
  const checkGoogleLoaded = () => {
    if (window.google && window.google.accounts && window.google.accounts.id) {
      try {
        window.google.accounts.id.initialize({
          client_id: clientId,
          callback: window.handleGoogleCredentialResponse,
          auto_select: false,
          cancel_on_tap_outside: true
        });

        const container = document.getElementById("googleOfficialBtnContainer");
        const customBtn = document.getElementById("googleCustomBtn");
        if (container) {
          container.innerHTML = "";
          window.google.accounts.id.renderButton(container, {
            type: "standard",
            theme: "outline",
            size: "large",
            text: "signin_with",
            shape: "pill",
            logo_alignment: "left",
            width: 300
          });
          // Rasmiy tugma muvaffaqiyatli chiqqanda dublikat zaxira tugmani yashiramiz
          if (customBtn) customBtn.classList.add("hidden");
        }
      } catch (err) {
        console.error("Google Auth render xatolik:", err);
        const customBtn = document.getElementById("googleCustomBtn");
        if (customBtn) customBtn.classList.remove("hidden");
        if (troubleshootBox) troubleshootBox.classList.remove("hidden");
      }
    } else {
      attempts++;
      if (attempts < 15) {
        setTimeout(checkGoogleLoaded, 200);
      } else {
        const customBtn = document.getElementById("googleCustomBtn");
        if (customBtn) customBtn.classList.remove("hidden");
        if (troubleshootBox) troubleshootBox.classList.remove("hidden");
      }
    }
  };
  checkGoogleLoaded();
};

window.handleGoogleCredentialResponse = async function(response) {
  if (!response || !response.credential) {
    showToast("Google orqali autentifikatsiya ma'lumotlari olinmadi.", "error");
    return;
  }
  showToast("Google hisobingiz tekshirilmoqda...", "info");

  let email = null;
  let fullName = null;
  let picture = null;
  try {
    const payloadBase64 = response.credential.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    const payloadJson = decodeURIComponent(escape(atob(payloadBase64)));
    const parsed = JSON.parse(payloadJson);
    email = parsed.email;
    fullName = parsed.name;
    picture = parsed.picture;
  } catch (e) {
    console.warn("JWT dekodlash xatosi:", e);
  }

  try {
    const res = await fetch(`${API_URL}/api/auth/social-login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        provider: "google",
        id_token: response.credential,
        email: email,
        full_name: fullName,
        avatar_url: picture
      })
    });
    const data = await res.json();
    if (res.ok && data.access_token) {
      localStorage.setItem("tasvirlab_token", data.access_token);
      window.currentUser = data.user;
      updateUserHeaderUI(data.user);
      closeAuthModal();
      showToast(data.message || `Xush kelibsiz, ${data.user.full_name}! 🎉`, "success");
    } else {
      showToast(data.detail || "Google orqali kirishda xatolik yuz berdi.", "error");
    }
  } catch (err) {
    console.error("Google auth request error:", err);
    showToast("Server bilan bog'lanishda xatolik.", "error");
  }
};

window.handleGoogleSignIn = async function() {
  const cfg = await fetchPublicAuthConfig();
  const clientId = cfg.google_client_id;
  const troubleshootBox = document.getElementById("googleTroubleshootBox");

  if (!clientId) {
    showToast("Google Client ID kiritilmagan. Admin panelida saqlang.", "warning");
    return;
  }

  // 1. Agar google.accounts.oauth2 mavjud bo'lsa, to'g'ridan-to'g'ri Google popup oynasini ochish
  if (window.google && window.google.accounts && window.google.accounts.oauth2) {
    try {
      const tokenClient = window.google.accounts.oauth2.initTokenClient({
        client_id: clientId,
        scope: "email profile openid",
        callback: async (tokenRes) => {
          if (tokenRes && tokenRes.access_token) {
            showToast("Google hisobi tasdiqlandi, kirilmoqda...", "info");
            let userEmail = null;
            let userName = null;
            let userPic = null;
            try {
              const uRes = await fetch("https://www.googleapis.com/oauth2/v3/userinfo", {
                headers: { Authorization: `Bearer ${tokenRes.access_token}` }
              });
              if (uRes.ok) {
                const uData = await uRes.json();
                userEmail = uData.email;
                userName = uData.name;
                userPic = uData.picture;
              }
            } catch(e) {}

            const res = await fetch(`${API_URL}/api/auth/social-login`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                provider: "google",
                id_token: tokenRes.access_token,
                email: userEmail,
                full_name: userName,
                avatar_url: userPic
              })
            });
            const data = await res.json();
            if (res.ok && data.access_token) {
              localStorage.setItem("tasvirlab_token", data.access_token);
              window.currentUser = data.user;
              updateUserHeaderUI(data.user);
              closeAuthModal();
              showToast(`Google orqali xush kelibsiz, ${data.user.full_name}! 🎉`, "success");
            } else {
              showToast(data.detail || "Google kirishda xatolik.", "error");
            }
          }
        },
        error_callback: (err) => {
          console.error("Google token client error:", err);
          if (troubleshootBox) troubleshootBox.classList.remove("hidden");
          showToast("Google oynasi ochilmadi. Konsoldagi Authorized Origins ni tekshiring.", "warning");
        }
      });
      tokenClient.requestAccessToken();
      return;
    } catch (err) {
      console.warn("initTokenClient fallback:", err);
    }
  }

  // 2. Prompt (OneTap) orqali urinish
  if (window.google && window.google.accounts && window.google.accounts.id) {
    window.google.accounts.id.prompt((notification) => {
      if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
        if (troubleshootBox) troubleshootBox.classList.remove("hidden");
      }
    });
    return;
  }

  if (troubleshootBox) troubleshootBox.classList.remove("hidden");
  showToast("Google Identity xizmati yuklanmadi. Sahifani qayta yuklang.", "warning");
};

// 3. Telegram orqali kirish (Bot orqali 1-bosishda tasdiqlash)
window.telegramPollingTimer = null;
window.currentTelegramAuthToken = null;

window.handleTelegramSignIn = async function() {
  const btn = document.getElementById("btnStartTelegramAuth");
  const waitingBox = document.getElementById("telegramWaitingBox");
  const tgBtnLabel = document.getElementById("tgBtnLabel");

  if (btn) btn.disabled = true;
  if (tgBtnLabel) tgBtnLabel.innerText = "Telegram botga ulanmoqda...";

  try {
    const res = await fetch(`${API_URL}/api/auth/telegram/request-session`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({})
    });
    const data = await res.json();
    if (res.ok && data.auth_token) {
      window.currentTelegramAuthToken = data.auth_token;
      
      const botUser = data.bot_username || "TasvirLabbot";
      const deepLink = data.deep_link || `https://t.me/${botUser}?start=${data.auth_token}`;
      
      // Yangi oynada botni ochamiz
      window.open(deepLink, "_blank");

      // UI holatini yangilash
      if (waitingBox) waitingBox.classList.remove("hidden");
      if (tgBtnLabel) tgBtnLabel.innerText = `Qaytadan ochish (@${botUser})`;

      showToast(`Telegram bot ochildi! "Start" tugmasini bosing.`, "info");

      // Jonli tekshiruv (polling) ni boshlaymiz
      startTelegramPolling(data.auth_token);
    } else {
      showToast(data.detail || "Telegram sessiyasini yaratishda xatolik.", "error");
    }
  } catch (e) {
    showToast("Telegram tizimi bilan bog'lanishda xatolik.", "error");
  } finally {
    if (btn) btn.disabled = false;
  }
};

window.startTelegramPolling = function(authToken) {
  if (window.telegramPollingTimer) clearInterval(window.telegramPollingTimer);

  let attempts = 0;
  window.telegramPollingTimer = setInterval(async () => {
    attempts++;
    if (attempts > 120) { // 3 daqiqa kutish
      clearInterval(window.telegramPollingTimer);
      window.telegramPollingTimer = null;
      return;
    }

    try {
      const res = await fetch(`${API_URL}/api/auth/telegram/check-session/${authToken}`);
      if (res.ok) {
        const data = await res.json();
        if (data.status === "confirmed" && data.access_token) {
          clearInterval(window.telegramPollingTimer);
          window.telegramPollingTimer = null;

          localStorage.setItem("tasvirlab_token", data.access_token);
          window.currentUser = data.user;
          updateUserHeaderUI(data.user);
          closeAuthModal();
          showToast(data.message || "Telegram orqali muvaffaqiyatli kirdingiz! 🎉", "success");
        }
      }
    } catch (e) {
      // Background check error ignored
    }
  }, 1500);
};


// 4. Parol va Admin yagona kirish
window.handlePasswordAuth = async function() {
  const loginInput = document.getElementById("authLoginInput");
  const passwordInput = document.getElementById("authPasswordInput");

  const loginVal = (loginInput.value || "").trim();
  const passwordVal = (passwordInput.value || "").trim();

  if (!loginVal || !passwordVal) {
    showToast("Iltimos, login va parolingizni kiriting.", "warning");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        phone_number: loginVal,
        password: passwordVal
      })
    });
    const data = await res.json();
    if (res.ok && data.access_token) {
      localStorage.setItem("tasvirlab_token", data.access_token);
      window.currentUser = data.user;

      if (data.is_admin) {
        localStorage.setItem("tasvirlab_is_admin", "true");
        updateUserHeaderUI(data.user);
        closeAuthModal();
        openAdminModal();
        showToast("Administrator sifatida muvaffaqiyatli kirdingiz! 🛡️", "success");
      } else {
        updateUserHeaderUI(data.user);
        closeAuthModal();
        showToast(data.message || "Xush kelibsiz!", "success");
      }
    } else {
      showToast(data.detail || "Login yoki parol noto'g'ri.", "error");
    }
  } catch (e) {
    showToast("Server bilan bog'lanishda xatolik.", "error");
  }
};

// Footer dagi Boshqaruv (Admin) tugmasi bosilganda
window.handleFooterAdminClick = function() {
  if (window.currentUser && window.currentUser.is_admin) {
    openAdminModal();
  } else {
    openAuthModal();
    switchAuthTab('password');
    const loginInput = document.getElementById("authLoginInput");
    if (loginInput) {
      loginInput.value = "admin";
      loginInput.focus();
    }
  }
};

// ==============================================================================
// 🛡️ ADMINISTRATOR BOSHQARUV MARKAZI (ADMIN DASHBOARD)
// ==============================================================================

window.openAdminModal = function() {
  const modal = document.getElementById("adminModal");
  if (modal) modal.classList.remove("hidden");
  switchAdminTab('overview');
};

window.closeAdminModal = function() {
  const modal = document.getElementById("adminModal");
  if (modal) modal.classList.add("hidden");
};

window.adminLogout = function() {
  logoutUser();
  closeAdminModal();
};

window.switchAdminTab = function(tabName) {
  const tabs = ['overview', 'users', 'topics', 'integrations'];
  tabs.forEach(t => {
    const btn = document.getElementById(`adminTabBtn${t.charAt(0).toUpperCase() + t.slice(1)}`);
    const panel = document.getElementById(`adminTab${t.charAt(0).toUpperCase() + t.slice(1)}`);
    if (btn && panel) {
      if (t === tabName) {
        btn.className = "px-4 py-2 rounded-2xl font-fredoka font-bold text-xs bg-indigo-600 text-white shadow-sm transition-all cursor-pointer flex items-center gap-1.5";
        panel.classList.remove("hidden");
      } else {
        btn.className = "px-4 py-2 rounded-2xl font-fredoka font-bold text-xs bg-slate-100 text-slate-600 hover:bg-slate-200 transition-all cursor-pointer flex items-center gap-1.5";
        panel.classList.add("hidden");
      }
    }
  });

  if (tabName === 'overview') loadAdminOverview();
  else if (tabName === 'users') loadAdminUsers();
  else if (tabName === 'topics') loadAdminTopics();
  else if (tabName === 'integrations') loadAdminIntegrations();
};

// 1. Umumiy va Iqtisodiy Statistika yuklash
window.loadAdminOverview = async function() {
  try {
    const res = await fetch(`${API_URL}/api/admin/overview`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Statistikani yuklab bo'lmadi");
    const data = await res.json();

    document.getElementById("adminStatUsers").innerText = data.users.total;
    document.getElementById("adminStatUsersToday").innerText = `Bugun: ${data.users.new_today} ta yangi`;
    
    document.getElementById("adminStatRevenue").innerText = `${(data.economics.total_revenue_uzs || 0).toLocaleString()} so'm`;
    document.getElementById("adminStatCreditsSpent").innerText = `${data.economics.total_credits_spent || 0} ta video`;
    document.getElementById("adminStatCreditsBalance").innerText = `Qoldiq balans: ${data.economics.total_active_balance || 0}`;

    document.getElementById("adminStatVideos").innerText = `${data.videos.total} ta`;
    document.getElementById("adminStatVideosToday").innerText = `Bugun: ${data.videos.today} ta dars`;

    const providersArea = document.getElementById("adminProvidersBreakdown");
    const provs = data.users.by_provider || {};
    const provLabels = {
      phone: "📱 Telefon (SMS OTP)",
      google: `<span class="inline-flex items-center gap-1.5"><svg class="w-3.5 h-3.5 inline shrink-0" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg> Google Hisobi</span>`,
      telegram: `<span class="inline-flex items-center gap-1.5"><svg class="w-3.5 h-3.5 fill-[#229ED9] inline shrink-0" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.75-.56 2.94-1.28 4.9-2.12 5.88-2.54 2.8-1.2 3.38-1.41 3.76-1.42.08 0 .28.02.4.12.1.08.13.2.14.28-.01.07-.01.21-.03.37z"/></svg> Telegram</span>`,
      admin: "👑 Administrator",
      guest: "👤 Mehmon"
    };
    providersArea.innerHTML = Object.keys(provs).map(k => `
      <div class="flex items-center justify-between p-2 rounded-xl bg-white border border-slate-200">
        <span class="font-medium text-slate-700">${provLabels[k] || k}</span>
        <span class="font-bold text-indigo-600 bg-indigo-50 px-2.5 py-0.5 rounded-full">${provs[k]} ta</span>
      </div>
    `).join("");

    const healthArea = document.getElementById("adminSystemHealthArea");
    const sh = data.system_health || {};
    healthArea.innerHTML = `
      <div class="flex items-center justify-between p-2 rounded-xl bg-white border border-slate-200">
        <span class="font-medium text-slate-700">🧠 Gemini Sun'iy Intellekt:</span>
        <span class="font-bold ${sh.gemini_api_configured ? 'text-emerald-600 bg-emerald-50' : 'text-amber-600 bg-amber-50'} px-2 py-0.5 rounded-full">
          ${sh.gemini_api_configured ? '✓ Faol va tayyor' : '⚠️ Kalit kiritilmagan'}
        </span>
      </div>
      <div class="flex items-center justify-between p-2 rounded-xl bg-white border border-slate-200">
        <span class="font-medium text-slate-700">🎙️ Mohir AI O'zbekcha Ovoz:</span>
        <span class="font-bold ${sh.mohirai_tts_configured ? 'text-emerald-600 bg-emerald-50' : 'text-amber-600 bg-amber-50'} px-2 py-0.5 rounded-full">
          ${sh.mohirai_tts_configured ? '✓ Ulangan' : '⚠️ Kalit kiritilmagan'}
        </span>
      </div>
      <div class="flex items-center justify-between p-2 rounded-xl bg-white border border-slate-200">
        <span class="font-medium text-slate-700">💾 Ma'lumotlar bazasi:</span>
        <span class="font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">${sh.database_status}</span>
      </div>
    `;
  } catch (err) {
    console.error("Overview xatosi:", err);
  }
};

// 2. Foydalanuvchilar ro'yxati
window.loadAdminUsers = async function() {
  const search = (document.getElementById("adminUsersSearchInput").value || "").trim();
  const tbody = document.getElementById("adminUsersTableBody");
  tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-slate-400">Yuklanmoqda...</td></tr>`;

  try {
    const url = `${API_URL}/api/admin/users?search=${encodeURIComponent(search)}`;
    const res = await fetch(url, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error("Foydalanuvchilarni yuklab bo'lmadi");
    const data = await res.json();
    const users = data.users || [];

    if (users.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-slate-400">Foydalanuvchilar topilmadi.</td></tr>`;
      return;
    }

    tbody.innerHTML = users.map(u => `
      <tr class="hover:bg-slate-50 transition-colors">
        <td class="p-3 font-mono font-bold text-slate-400">#${u.id}</td>
        <td class="p-3">
          <div class="font-bold text-slate-800">${escapeHtml(u.full_name || 'Noma\'lum')}</div>
          <div class="text-[11px] text-slate-400 font-mono">${escapeHtml(u.phone_number || u.email || '')}</div>
        </td>
        <td class="p-3">
          <span class="px-2 py-0.5 rounded-lg text-[10px] font-bold bg-slate-100 text-slate-700 uppercase">${u.auth_provider}</span>
        </td>
        <td class="p-3">
          <span class="font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-md font-mono">${u.credits_balance} video</span>
        </td>
        <td class="p-3 font-semibold text-slate-700">${u.videos_count || 0} ta</td>
        <td class="p-3">
          <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${u.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}">
            ${u.is_active ? 'Faol' : 'Bloklangan'}
          </span>
        </td>
        <td class="p-3 text-right space-x-1">
          <button onclick="adminPromptAdjustCredits(${u.id}, ${u.credits_balance})" class="px-2.5 py-1 rounded-lg bg-indigo-50 hover:bg-indigo-100 text-indigo-700 font-bold text-[11px] transition-all cursor-pointer">
            + Bonus
          </button>
          <button onclick="adminToggleUserStatus(${u.id})" class="px-2.5 py-1 rounded-lg ${u.is_active ? 'bg-rose-50 hover:bg-rose-100 text-rose-600' : 'bg-emerald-50 hover:bg-emerald-100 text-emerald-700'} font-bold text-[11px] transition-all cursor-pointer">
            ${u.is_active ? 'Bloklash' : 'Ochish'}
          </button>
        </td>
      </tr>
    `).join("");
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-rose-500">Xatolik yuz berdi.</td></tr>`;
  }
};

window.handleAdminUsersSearch = function(event) {
  if (event.key === 'Enter') {
    loadAdminUsers();
  }
};

window.adminPromptAdjustCredits = async function(userId, currentBalance) {
  const amountStr = prompt(`Foydalanuvchi hisobiga nechta video bonusi qo'shmoqchisiz? (Masalan: 5 yoki 10):`, "5");
  if (!amountStr) return;
  const amount = parseInt(amountStr);
  if (isNaN(amount) || amount === 0) {
    showToast("Noto'g'ri son kiritildi.", "warning");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/admin/users/${userId}/adjust-credits`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        amount: amount,
        reason: "Administrator tomonidan bonus ajratildi"
      })
    });
    const data = await res.json();
    if (res.ok) {
      showToast(data.message || "Balans muvaffaqiyatli yangilandi!", "success");
      loadAdminUsers();
      loadAdminOverview();
    } else {
      showToast(data.detail || "Xatolik yuz berdi.", "error");
    }
  } catch (e) {
    showToast("Server xatosi.", "error");
  }
};

window.adminToggleUserStatus = async function(userId) {
  try {
    const res = await fetch(`${API_URL}/api/admin/users/${userId}/toggle-status`, {
      method: "POST",
      headers: getAuthHeaders()
    });
    const data = await res.json();
    if (res.ok) {
      showToast(data.message || "Foydalanuvchi holati yangilandi.", "success");
      loadAdminUsers();
      loadAdminOverview();
    } else {
      showToast(data.detail || "Xatolik yuz berdi.", "error");
    }
  } catch (e) {
    showToast("Server xatosi.", "error");
  }
};

// 3. Tavsiyaviy Mavzular boshqaruvi
window.loadAdminTopics = async function() {
  const container = document.getElementById("adminTopicsListContainer");
  const badge = document.getElementById("adminTopicsCountBadge");
  container.innerHTML = `<div class="p-4 text-center text-slate-400 text-xs">Mavzular yuklanmoqda...</div>`;

  try {
    const res = await fetch(`${API_URL}/api/admin/topics`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error("Yuklab bo'lmadi");
    const data = await res.json();
    const topics = data.topics || [];

    if (badge) badge.innerText = `${topics.length} ta`;

    if (topics.length === 0) {
      container.innerHTML = `<div class="p-4 text-center text-slate-400 text-xs">Hozircha tavsiyaviy mavzular yo'q.</div>`;
      return;
    }

    container.innerHTML = topics.map(t => `
      <div class="flex items-center justify-between p-3 rounded-2xl bg-white border border-slate-200 hover:border-indigo-200 transition-all text-xs">
        <div class="space-y-0.5 flex-1 pr-3">
          <div class="flex items-center gap-2">
            <span class="font-bold text-slate-800">${escapeHtml(t.title)}</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-50 text-indigo-700">${t.age_group || t.age || 'Umumiy'} yosh</span>
          </div>
          <p class="text-slate-500 text-[11px] line-clamp-1">${escapeHtml(t.prompt || '')}</p>
        </div>
        <button onclick="handleAdminDeleteTopic('${encodeURIComponent(t.id || t.title)}')" class="px-3 py-1.5 rounded-xl border border-rose-200 text-rose-600 hover:bg-rose-50 text-xs font-bold transition-all cursor-pointer shrink-0">
          🗑️ O'chirish
        </button>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<div class="p-4 text-center text-rose-500 text-xs">Mavzularni yuklashda xatolik.</div>`;
  }
};

window.handleAdminAddTopic = async function() {
  const age = document.getElementById("adminNewTopicAge").value;
  const title = (document.getElementById("adminNewTopicTitle").value || "").trim();
  const promptVal = (document.getElementById("adminNewTopicPrompt").value || "").trim();

  if (!title) {
    showToast("Iltimos, mavzu nomini kiriting.", "warning");
    return;
  }

  try {
    const res = await fetch(`${API_URL}/api/admin/topics`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({
        title: title,
        age_group: age,
        prompt: promptVal
      })
    });
    const data = await res.json();
    if (res.ok) {
      showToast("Yangi tavsiyaviy mavzu muvaffaqiyatli qo'shildi! ✨", "success");
      document.getElementById("adminNewTopicTitle").value = "";
      document.getElementById("adminNewTopicPrompt").value = "";
      loadAdminTopics();
      await loadPresets();
    } else {
      showToast(data.detail || "Xatolik yuz berdi.", "error");
    }
  } catch (e) {
    showToast("Server xatosi.", "error");
  }
};

window.handleAdminDeleteTopic = async function(topicIdOrTitle) {
  if (!confirm("Haqiqatan ham ushbu tavsiyaviy mavzuni o'chirmoqchimisiz?")) return;

  try {
    const res = await fetch(`${API_URL}/api/admin/topics/${topicIdOrTitle}`, {
      method: "DELETE",
      headers: getAuthHeaders()
    });
    const data = await res.json();
    if (res.ok) {
      showToast("Mavzu o'chirildi.", "info");
      loadAdminTopics();
      await loadPresets();
    } else {
      showToast(data.detail || "O'chirishda xatolik.", "error");
    }
  } catch (e) {
    showToast("Server xatosi.", "error");
  }
};

// 4. Integratsiyalar va API sozlamalari
window.loadAdminIntegrations = async function() {
  try {
    const res = await fetch(`${API_URL}/api/admin/integrations`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Integratsiyalarni yuklab bo'lmadi");
    const data = await res.json();

    const gInput = document.getElementById("adminGoogleClientId");
    if (gInput) gInput.value = data.google_client_id || "";

    const tTokenInput = document.getElementById("adminTgBotToken");
    if (tTokenInput) tTokenInput.value = data.telegram_bot_token || "";

    const tUserInput = document.getElementById("adminTgBotUsername");
    if (tUserInput) tUserInput.value = data.telegram_bot_username || "";

    // AI Kalitlari
    const geminiInput = document.getElementById("adminGeminiApiKey");
    if (geminiInput) geminiInput.value = data.gemini_api_key || "";

    const mohiraiInput = document.getElementById("adminMohiraiApiKey");
    if (mohiraiInput) mohiraiInput.value = data.mohirai_api_key || "";

    // To'lov kalitlari
    const pMerc = document.getElementById("adminPaymeMerchantId");
    if (pMerc) pMerc.value = data.payme_merchant_id || "";
    const pSec = document.getElementById("adminPaymeSecretKey");
    if (pSec) pSec.value = data.payme_secret_key || "";

    const cSrv = document.getElementById("adminClickServiceId");
    if (cSrv) cSrv.value = data.click_service_id || "";
    const cMerc = document.getElementById("adminClickMerchantId");
    if (cMerc) cMerc.value = data.click_merchant_id || "";
    const cSec = document.getElementById("adminClickSecretKey");
    if (cSec) cSec.value = data.click_secret_key || "";

    const uMerc = document.getElementById("adminUzumMerchantId");
    if (uMerc) uMerc.value = data.uzum_merchant_id || "";
    const uSec = document.getElementById("adminUzumSecretKey");
    if (uSec) uSec.value = data.uzum_secret_key || "";

    const pnetSrv = document.getElementById("adminPaynetServiceId");
    if (pnetSrv) pnetSrv.value = data.paynet_service_id || "";
    const pnetSec = document.getElementById("adminPaynetSecretKey");
    if (pnetSec) pnetSec.value = data.paynet_secret_key || "";
  } catch (err) {
    console.warn("[Admin] Integratsiyalar yuklanmadi:", err);
  }
};

window.handleAdminSaveIntegrations = async function() {
  const geminiApiKey = (document.getElementById("adminGeminiApiKey")?.value || "").trim();
  const mohiraiApiKey = (document.getElementById("adminMohiraiApiKey")?.value || "").trim();
  const googleClientId = (document.getElementById("adminGoogleClientId")?.value || "").trim();
  const tgToken = (document.getElementById("adminTgBotToken")?.value || "").trim();
  const tgUsername = (document.getElementById("adminTgBotUsername")?.value || "").trim();
  const newPass = (document.getElementById("adminNewPasswordInput")?.value || "").trim();

  const paymeMerc = (document.getElementById("adminPaymeMerchantId")?.value || "").trim();
  const paymeSec = (document.getElementById("adminPaymeSecretKey")?.value || "").trim();
  const clickSrv = (document.getElementById("adminClickServiceId")?.value || "").trim();
  const clickMerc = (document.getElementById("adminClickMerchantId")?.value || "").trim();
  const clickSec = (document.getElementById("adminClickSecretKey")?.value || "").trim();
  const uzumMerc = (document.getElementById("adminUzumMerchantId")?.value || "").trim();
  const uzumSec = (document.getElementById("adminUzumSecretKey")?.value || "").trim();
  const paynetSrv = (document.getElementById("adminPaynetServiceId")?.value || "").trim();
  const paynetSec = (document.getElementById("adminPaynetSecretKey")?.value || "").trim();

  const payload = {
    gemini_api_key: geminiApiKey,
    mohirai_api_key: mohiraiApiKey,
    google_client_id: googleClientId,
    telegram_bot_token: tgToken,
    telegram_bot_username: tgUsername,
    payme_merchant_id: paymeMerc,
    payme_secret_key: paymeSec,
    click_service_id: clickSrv,
    click_merchant_id: clickMerc,
    click_secret_key: clickSec,
    uzum_merchant_id: uzumMerc,
    uzum_secret_key: uzumSec,
    paynet_service_id: paynetSrv,
    paynet_secret_key: paynetSec
  };

  if (newPass) {
    if (newPass.length < 6) {
      showToast("Yangi parol kamida 6 ta belgidan iborat bo'lishi kerak.", "warning");
      return;
    }
    payload.admin_password = newPass;
  }

  try {
    const res = await fetch(`${API_URL}/api/admin/integrations`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (res.ok) {
      showToast("Integratsiya va to'lov sozlamalari muvaffaqiyatli saqlandi! 💾", "success");
      const passInp = document.getElementById("adminNewPasswordInput");
      if (passInp) passInp.value = "";
    } else {
      showToast(data.detail || "Saqlashda xatolik yuz berdi.", "error");
    }
  } catch (e) {
    showToast("Server bilan bog'lanishda xatolik.", "error");
  }
};


