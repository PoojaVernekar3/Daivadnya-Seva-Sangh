/**
 * Main Application Logic
 * Daivadnya Ganesh Utsav Mandal, Belgaum
 * Digital Hawal Book Platform
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize Flipbook Engine
  const flipbook = new HawalFlipbook('flipbookContainer', BOOK_PAGES);

  // Expose flipbook globally for ad cards & toolbar
  window.appFlipbook = flipbook;

  // 2. Simulate & Dismiss Loading Screen
  initLoadingScreen();

  // 3. Setup Devotional Ambient Audio Generator
  initAmbientAudio();

  // 4. Setup Toolbar Actions
  initToolbarControls(flipbook);

  // 5. Setup Mobile Navigation Drawer & Hamburger Menu
  initMobileNavigation(flipbook);

  // 6. Setup Multi-Language Switcher (Marathi, English, Kannada)
  initLanguageSwitcher();

  // 7. Setup Share Modal & Native Share
  initShareFunctionality();

  // 8. Setup PDF Download / Print
  initDownloadActions();
});

/* ==========================================================================
   LOADING SCREEN CONTROLLER
   ========================================================================== */
function initLoadingScreen() {
  const loadingScreen = document.getElementById('loadingScreen');
  const progressBar = document.getElementById('loaderProgressBar');
  const statusText = document.getElementById('loaderStatus');

  if (!loadingScreen) return;

  const steps = [
    { progress: 25, text: 'श्री गणपती बाप्पाच्या आशीर्वादाने...' },
    { progress: 60, text: 'अहवाल स्मरणिका (१९६ पाने) लोड होत आहेत...' },
    { progress: 85, text: 'जाहिरातदार सूची व सुवर्ण डिझाइन्स तयार होत आहेत...' },
    { progress: 100, text: 'स्वागतम! दैवज्ञ सेवा संघ, श्री गणेश उत्सव मंडळ, शहापूर-बेळगांव' }
  ];

  let currentStep = 0;

  const interval = setInterval(() => {
    if (currentStep < steps.length) {
      const step = steps[currentStep];
      if (progressBar) progressBar.style.width = `${step.progress}%`;
      if (statusText) statusText.textContent = step.text;
      currentStep++;
    } else {
      clearInterval(interval);
      setTimeout(() => {
        loadingScreen.classList.add('hidden');
      }, 400);
    }
  }, 240);
}

/* ==========================================================================
   DEVOTIONAL AMBIENT SYNTHESIZER (WEB AUDIO API)
   ========================================================================== */
function initAmbientAudio() {
  const audioBtn = document.getElementById('audioToggleBtn');
  let audioCtx = null;
  let isPlaying = false;
  let intervalId = null;

  function createTempleBell(freq, time) {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, time);

    gain.gain.setValueAtTime(0.08, time);
    gain.gain.exponentialRampToValueAtTime(0.0001, time + 2.4);

    osc.connect(gain);
    gain.connect(audioCtx.destination);

    osc.start(time);
    osc.stop(time + 2.5);
  }

  function startAmbience() {
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) return;
    if (!audioCtx) audioCtx = new AudioContext();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    isPlaying = true;
    window.isAmbientAudioPlaying = true;
    audioBtn?.classList.add('playing');
    audioBtn.setAttribute('title', 'Mute Devotional Chimes');
    showToast('🔔 Devotional Ambient Chimes Playing');

    // Play initial bell
    const now = audioCtx.currentTime;
    createTempleBell(528, now); // 528Hz Solfeggio / meditative tone
    createTempleBell(792, now + 0.1);

    // Play periodic soothing bell harmonics
    intervalId = setInterval(() => {
      if (!isPlaying || !audioCtx) return;
      const t = audioCtx.currentTime;
      const notes = [440, 528, 660, 792, 880];
      const note = notes[Math.floor(Math.random() * notes.length)];
      createTempleBell(note, t);
    }, 3800);
  }

  function stopAmbience() {
    isPlaying = false;
    window.isAmbientAudioPlaying = false;
    audioBtn?.classList.remove('playing');
    audioBtn.setAttribute('title', 'Play Devotional Chimes');
    if (intervalId) clearInterval(intervalId);
    showToast('Devotional Chimes Muted');
  }

  audioBtn?.addEventListener('click', () => {
    if (isPlaying) {
      stopAmbience();
    } else {
      startAmbience();
    }
  });
}

/* ==========================================================================
   TOOLBAR CONTROLS
   ========================================================================== */
function initToolbarControls(flipbook) {
  // Fullscreen
  document.getElementById('fullscreenBtn')?.addEventListener('click', () => {
    flipbook.toggleFullscreen();
  });

  // Zoom In / Out / Reset
  document.getElementById('zoomInBtn')?.addEventListener('click', () => {
    flipbook.setZoom(0.15);
  });

  document.getElementById('zoomOutBtn')?.addEventListener('click', () => {
    flipbook.setZoom(-0.15);
  });

  document.getElementById('zoomResetBtn')?.addEventListener('click', () => {
    flipbook.resetZoom();
  });

  // Thumbnail Drawer Toggle
  document.getElementById('toggleThumbnailsBtn')?.addEventListener('click', () => {
    flipbook.toggleThumbnailDrawer();
  });

  document.getElementById('closeThumbnailsBtn')?.addEventListener('click', () => {
    flipbook.toggleThumbnailDrawer(false);
  });

  // Bookmark Page
  document.getElementById('bookmarkBtn')?.addEventListener('click', () => {
    const page = flipbook.currentPage;
    localStorage.setItem('daivadnya_book_bookmark', page);
    showToast(`🔖 Page ${page} bookmarked for your next visit!`);
  });

  // Check saved bookmark on initial visit
  const savedBookmark = localStorage.getItem('daivadnya_book_bookmark');
  if (savedBookmark && parseInt(savedBookmark, 10) > 1) {
    const bmNum = parseInt(savedBookmark, 10);
    const resumePrompt = document.getElementById('resumeBookmarkBanner');
    if (resumePrompt) {
      resumePrompt.style.display = 'flex';
      document.getElementById('resumeBookmarkBtn')?.addEventListener('click', () => {
        flipbook.goToPage(bmNum);
        resumePrompt.style.display = 'none';
      });
      document.getElementById('dismissBookmarkBtn')?.addEventListener('click', () => {
        resumePrompt.style.display = 'none';
      });
    }
  }
}

/* ==========================================================================
   MOBILE NAVIGATION DRAWER & HAMBURGER CONTROLLER
   Smooth off-canvas side sheet navigation for smartphones and tablets
   ========================================================================== */
function initMobileNavigation(flipbook) {
  const hamburgerBtn = document.getElementById('hamburgerBtn');
  const drawer = document.getElementById('mobileNavDrawer');
  const backdrop = document.getElementById('mobileNavBackdrop');
  const closeBtn = document.getElementById('closeMobileNavBtn');
  const closeLinks = document.querySelectorAll('.mobile-link-close');
  const thumbnailsTrigger = document.getElementById('mobileThumbnailsTrigger');
  const mobileAudioBtn = document.getElementById('mobileAudioToggleBtn');
  const mobileAudioBadge = document.getElementById('mobileAudioBadge');
  const mobileAudioStatus = document.getElementById('mobileAudioStatusText');

  function openDrawer() {
    drawer?.classList.add('open');
    backdrop?.classList.add('active');
    hamburgerBtn?.classList.add('active');
    hamburgerBtn?.setAttribute('aria-expanded', 'true');
    drawer?.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    updateMobileAudioState();
  }

  function closeDrawer() {
    drawer?.classList.remove('open');
    backdrop?.classList.remove('active');
    hamburgerBtn?.classList.remove('active');
    hamburgerBtn?.setAttribute('aria-expanded', 'false');
    drawer?.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  hamburgerBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    if (drawer?.classList.contains('open')) {
      closeDrawer();
    } else {
      openDrawer();
    }
  });

  closeBtn?.addEventListener('click', closeDrawer);
  backdrop?.addEventListener('click', closeDrawer);

  // Close on Escape key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (drawer?.classList.contains('open')) closeDrawer();
      if (flipbook?.thumbnailDrawer?.classList.contains('open')) flipbook.toggleThumbnailDrawer(false);
    }
  });

  // Close when tapping navigation links
  closeLinks.forEach(link => {
    link.addEventListener('click', () => {
      closeDrawer();
    });
  });

  // Thumbnails button inside mobile drawer
  thumbnailsTrigger?.addEventListener('click', () => {
    closeDrawer();
    setTimeout(() => {
      flipbook.toggleThumbnailDrawer(true);
    }, 280);
  });

  // Mobile Audio Toggle & Sync
  mobileAudioBtn?.addEventListener('click', () => {
    document.getElementById('audioToggleBtn')?.click();
    updateMobileAudioState();
  });

  function updateMobileAudioState() {
    const isPlaying = !!window.isAmbientAudioPlaying;
    if (mobileAudioBadge) {
      mobileAudioBadge.textContent = isPlaying ? 'ON' : 'OFF';
      mobileAudioBadge.classList.toggle('active', isPlaying);
    }
    if (mobileAudioStatus) {
      mobileAudioStatus.textContent = isPlaying ? 'संगीत सुरू आहे (टॅप करा बंद करण्यासाठी)' : 'भक्तीमय संगीत सुरू करा';
    }
  }

  // Sync state if audio toggled from header
  document.getElementById('audioToggleBtn')?.addEventListener('click', () => {
    setTimeout(updateMobileAudioState, 50);
  });

  // Thumbnail Backdrop click to close drawer
  const thumbBackdrop = document.getElementById('thumbnailBackdrop');
  thumbBackdrop?.addEventListener('click', () => {
    flipbook.toggleThumbnailDrawer(false);
  });

  // Touch swipe-to-close on drawer (swipe right towards screen edge)
  let touchStartX = 0;
  drawer?.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });

  drawer?.addEventListener('touchend', (e) => {
    const touchEndX = e.changedTouches[0].clientX;
    if (touchEndX - touchStartX > 50) {
      closeDrawer();
    }
  }, { passive: true });
}



/* ==========================================================================
   LANGUAGE SWITCHER (MARATHI, ENGLISH, KANNADA)
   ========================================================================== */
function initLanguageSwitcher() {
  const langButtons = document.querySelectorAll('.lang-btn, .drawer-lang-btn');
  const storedLang = localStorage.getItem('daivadnya_lang');
  
  // Default language is Marathi ('mr')
  let currentLang = (storedLang && typeof TRANSLATIONS !== 'undefined' && TRANSLATIONS[storedLang]) ? storedLang : 'mr';

  function applyLanguage(lang, userTriggered = false) {
    if (typeof TRANSLATIONS === 'undefined' || !TRANSLATIONS[lang]) return;
    currentLang = lang;
    window.currentAppLang = lang;
    localStorage.setItem('daivadnya_lang', lang);

    // Update document lang attribute
    document.documentElement.lang = lang;

    // Apply translations to all data-i18n elements
    const translatableElements = document.querySelectorAll('[data-i18n]');
    translatableElements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (TRANSLATIONS[lang][key] !== undefined) {
        el.innerHTML = TRANSLATIONS[lang][key];
      }
    });

    // Update all button active states in both header and drawer
    langButtons.forEach(btn => {
      const btnLang = btn.getAttribute('data-lang');
      if (btnLang === lang) {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });

    // Update share metadata
    if (typeof updateShareMetadata === 'function') {
      updateShareMetadata();
    }

    // Optional user feedback on click
    if (userTriggered) {
      const toasts = {
        mr: '🌐 भाषा: मराठी निवडली आहे',
        en: '🌐 Language switched to English (Official Translation)',
        kn: '🌐 ಭಾಷೆ: ಕನ್ನಡ ಆಯ್ಕೆ ಮಾಡಲಾಗಿದೆ'
      };
      if (typeof showToast === 'function') {
        showToast(toasts[lang] || 'Language updated');
      }
    }
  }

  // Attach click listeners to all language selector buttons
  langButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const selectedLang = btn.getAttribute('data-lang');
      if (selectedLang && selectedLang !== currentLang) {
        applyLanguage(selectedLang, true);
      }
    });
  });

  // Apply initial language
  applyLanguage(currentLang, false);
}

/* ==========================================================================
   SHARE MODAL & NATIVE SHARING CONTROLLER
   ========================================================================== */
let updateShareMetadata = null;

function initShareFunctionality() {
  const shareModal = document.getElementById('shareModal');
  const openShareBtns = document.querySelectorAll('.trigger-share-modal');
  const closeModalBtn = document.getElementById('closeShareModalBtn');
  const copyLinkBtn = document.getElementById('copyShareLinkBtn');
  const shareLinkInput = document.getElementById('shareLinkInput');

  function getShareData() {
    const lang = window.currentAppLang || 'mr';
    const t = (typeof TRANSLATIONS !== 'undefined' && TRANSLATIONS[lang]) ? TRANSLATIONS[lang] : {};
    return {
      title: t.share_official_title || (typeof MANDAL_CONFIG !== 'undefined' ? MANDAL_CONFIG.shareTitle : 'दैवज्ञ सेवा संघ, श्री गणेश उत्सव मंडळ, शहापूर-बेळगांव'),
      text: t.share_official_desc || (typeof MANDAL_CONFIG !== 'undefined' ? MANDAL_CONFIG.shareDescription : 'Explore 47th Ahawal Book'),
      url: window.location.href
    };
  }

  // Function to refresh social URLs whenever opened or language changed
  updateShareMetadata = function() {
    const currentData = getShareData();
    if (shareLinkInput) {
      shareLinkInput.value = currentData.url;
    }

    const encodedText = encodeURIComponent(`${currentData.title}\n\n${currentData.text}\n\n${currentData.url}`);
    const encodedUrl = encodeURIComponent(currentData.url);

    const whatsappBtn = document.getElementById('shareWhatsAppBtn');
    if (whatsappBtn) {
      whatsappBtn.href = `https://api.whatsapp.com/send?text=${encodedText}`;
    }

    const facebookBtn = document.getElementById('shareFacebookBtn');
    if (facebookBtn) {
      facebookBtn.href = `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`;
    }

    const twitterBtn = document.getElementById('shareTwitterBtn');
    if (twitterBtn) {
      twitterBtn.href = `https://twitter.com/intent/tweet?text=${encodedText}`;
    }

    const telegramBtn = document.getElementById('shareTelegramBtn');
    if (telegramBtn) {
      telegramBtn.href = `https://t.me/share/url?url=${encodedUrl}&text=${encodeURIComponent(currentData.title)}`;
    }
  };

  updateShareMetadata();

  function openModal() {
    updateShareMetadata();
    shareModal?.classList.add('open');
  }

  function closeModal() {
    shareModal?.classList.remove('open');
  }

  // Bind Open Buttons
  openShareBtns.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const currentData = getShareData();
      // Check if user is on mobile with native Web Share API
      if (navigator.share && window.innerWidth <= 768) {
        try {
          await navigator.share(currentData);
          showToast('🙏 Thank you for sharing the Hawal Book!');
          return;
        } catch (err) {
          // Fallback to modal if cancelled or unsupported
        }
      }
      openModal();
    });
  });

  closeModalBtn?.addEventListener('click', closeModal);

  // Close on outside click
  shareModal?.addEventListener('click', (e) => {
    if (e.target === shareModal) closeModal();
  });

  // Close on Escape key
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && shareModal?.classList.contains('open')) {
      closeModal();
    }
  });

  // Copy Link Button
  copyLinkBtn?.addEventListener('click', () => {
    const currentData = getShareData();
    const textToCopy = `${currentData.title}\n${currentData.text}\n${currentData.url}`;
    navigator.clipboard.writeText(textToCopy).then(() => {
      showToast('✓ Share link & message copied to clipboard!');
      copyLinkBtn.textContent = 'Copied!';
      setTimeout(() => {
        copyLinkBtn.textContent = (typeof TRANSLATIONS !== 'undefined' && TRANSLATIONS[window.currentAppLang || 'mr']) 
          ? TRANSLATIONS[window.currentAppLang || 'mr'].share_copy_btn 
          : 'Copy Link';
      }, 2000);
    }).catch(() => {
      // Fallback
      if (shareLinkInput) {
        shareLinkInput.select();
        document.execCommand('copy');
        showToast('✓ Link copied!');
      }
    });
  });
}

/* ==========================================================================
   DOWNLOAD & PRINT CONTROLLER
   ========================================================================== */
function initDownloadActions() {
  const downloadPdfBtns = document.querySelectorAll('.trigger-download-pdf');
  const printBookBtns = document.querySelectorAll('.trigger-print-book');

  function triggerPrint() {
    showToast('🖨️ Preparing high-resolution PDF print preview...');
    setTimeout(() => {
      window.print();
    }, 300);
  }

  downloadPdfBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // Show auspicious download notification
      showToast('📥 अधिकृत ४७ वा अहवाल (98 MB PDF) डाउनलोड होत आहे...');
      // Allow browser natural download via href and download attribute
    });
  });

  printBookBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      triggerPrint();
    });
  });
}

/* ==========================================================================
   TOAST NOTIFICATION UTILITY
   ========================================================================== */
function showToast(message) {
  let toast = document.getElementById('appToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'appToast';
    toast.className = 'toast-notice';
    document.body.appendChild(toast);
  }

  toast.innerHTML = message;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3200);
}
