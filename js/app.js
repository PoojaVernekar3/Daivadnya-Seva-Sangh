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


  // 6. Setup Share Modal & Native Share
  initShareFunctionality();

  // 7. Setup PDF Download / Print
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
   SHARE MODAL & NATIVE SHARING CONTROLLER
   Official Share Title: Daivadnya Ganesh Utsav Mandal, Belgaum – Digital Hawal Book
   Official Description: Explore the digital Hawal/advertisement book of Daivadnya Ganesh Utsav Mandal, Belgaum.
   ========================================================================== */
function initShareFunctionality() {
  const shareModal = document.getElementById('shareModal');
  const openShareBtns = document.querySelectorAll('.trigger-share-modal');
  const closeModalBtn = document.getElementById('closeShareModalBtn');
  const copyLinkBtn = document.getElementById('copyShareLinkBtn');
  const shareLinkInput = document.getElementById('shareLinkInput');

  const shareData = {
    title: MANDAL_CONFIG.shareTitle,
    text: MANDAL_CONFIG.shareDescription,
    url: window.location.href
  };

  // Set input value
  if (shareLinkInput) {
    shareLinkInput.value = window.location.href;
  }

  function openModal() {
    shareModal?.classList.add('open');
  }

  function closeModal() {
    shareModal?.classList.remove('open');
  }

  // Bind Open Buttons
  openShareBtns.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      // Check if user is on mobile with native Web Share API
      if (navigator.share && window.innerWidth <= 768) {
        try {
          await navigator.share(shareData);
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
    const textToCopy = `${shareData.title}\n${shareData.text}\n${shareData.url}`;
    navigator.clipboard.writeText(textToCopy).then(() => {
      showToast('✓ Share link & message copied to clipboard!');
      copyLinkBtn.textContent = 'Copied!';
      setTimeout(() => {
        copyLinkBtn.textContent = 'Copy';
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

  // Setup social channel buttons
  const encodedText = encodeURIComponent(`${shareData.title}\n\n${shareData.text}\n\n${shareData.url}`);
  const encodedUrl = encodeURIComponent(shareData.url);

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
    telegramBtn.href = `https://t.me/share/url?url=${encodedUrl}&text=${encodeURIComponent(shareData.title)}`;
  }
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
