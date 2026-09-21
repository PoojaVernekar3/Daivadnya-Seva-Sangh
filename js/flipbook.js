/**
 * Interactive 3D Flipbook Engine
 * Daivadnya Seva Sangh, Shree Ganesh Utsav Mandal, Shahapur - Belgaum
 * 47th Ahawal 2026-27 (४७ वा अहवाल २०२६-२७)
 */

class HawalFlipbook {
  constructor(containerId, pagesData) {
    this.container = document.getElementById(containerId);
    this.pages = pagesData;
    this.currentPage = 1; // 1-indexed
    this.totalPages = pagesData.length;
    this.isAnimating = false;
    this.isSinglePageMode = window.innerWidth <= 820;
    this.zoomLevel = 1;

    // DOM Elements
    this.bookStage = document.getElementById('bookStage');
    this.leftSlot = document.getElementById('leftPageSlot');
    this.rightSlot = document.getElementById('rightPageSlot');
    this.prevBtn = document.getElementById('prevPageBtn');
    this.nextBtn = document.getElementById('nextPageBtn');
    this.indicator = document.getElementById('pageIndicator');
    this.jumpSelect = document.getElementById('pageJumpSelect');
    this.thumbnailDrawer = document.getElementById('thumbnailDrawer');
    this.thumbnailsTrack = document.getElementById('thumbnailsTrack');

    this.audioCtx = null;
    this.preloadedImages = new Set();

    this.init();
  }

  init() {
    this.populateJumpSelect();
    this.renderThumbnails();
    this.renderCurrentSpread();
    this.bindEvents();
    this.updateControls();
    this.preloadAdjacentPages(this.currentPage);
  }

  // Preload images for smooth flipping
  preloadAdjacentPages(centerPage) {
    const pagesToPreload = [
      centerPage - 2,
      centerPage - 1,
      centerPage,
      centerPage + 1,
      centerPage + 2,
      centerPage + 3
    ];

    pagesToPreload.forEach(pNum => {
      if (pNum >= 1 && pNum <= this.totalPages && !this.preloadedImages.has(pNum)) {
        const page = this.pages[pNum - 1];
        if (page && page.image) {
          const img = new Image();
          img.src = page.image;
          this.preloadedImages.add(pNum);
        }
      }
    });
  }

  // Populate Jump Select with Optgroups
  populateJumpSelect() {
    if (!this.jumpSelect) return;
    this.jumpSelect.innerHTML = '';

    // Landmark Jump Links
    const landmarkGroup = document.createElement('optgroup');
    landmarkGroup.label = '✦ Key Sections & Landmarks';

    const landmarks = [
      { page: 1, title: 'Page 1 - मुखपृष्ठ / Cover Page' },
      { page: 2, title: 'Page 2 - Mysore Jewellery House & SV Farms' },
      { page: 3, title: 'Page 3 - Anvekar Gold Loan' },
      { page: 4, title: 'Page 4 - Paramapujya Swamiji Blessings' },
      { page: 5, title: 'Page 5 - Vinayak H. Kudtarkar Gold Wholesalers' },
      { page: 7, title: 'Page 7 - RK & RK Anavekar Jewellers' },
      { page: 8, title: 'Page 8 - Laxmi Gold Ornaments' },
      { page: 11, title: 'Page 11 - President Address (Manoj Kolvekar)' },
      { page: 12, title: 'Page 12 - Secretary Address (Sudhir Vernekar)' },
      { page: 13, title: 'Page 13 - Utsav Schedule (English)' },
      { page: 15, title: 'Page 15 - उत्सव कार्यक्रम (मराठी वेळापत्रक)' },
      { page: 17, title: 'Page 17 - ಉತ್ಸವ ಕಾರ್ಯಕ್ರಮ (ಕನ್ನಡ ವೇಳಾಪಟ್ಟಿ)' },
      { page: 19, title: 'Page 19 - Prize Distribution Programme' },
      { page: 22, title: 'Page 22 - Motichand Jewels Wholesalers' },
      { page: 25, title: 'Page 25 - Managing Committee 2026-2028' },
      { page: 26, title: 'Page 26 - Utsav 2025 Photos: Murthi Agaman' },
      { page: 27, title: 'Page 27 - Utsav 2025 Photos: Mahapooja' },
      { page: 28, title: 'Page 28 - Utsav 2025 Photos: Dhol Group & Pooja' },
      { page: 32, title: 'Page 32 - Utsav 2025 Photos: Medical Camp' },
      { page: 33, title: 'Page 33 - Utsav 2025 Photos: Lilav Auction' },
      { page: 34, title: 'Page 34 - Utsav 2025 Photos: Visarjan Procession' },
      { page: 35, title: 'Page 35 - Daivadnya Brahman Mangal Karyalaya' },
      { page: 36, title: 'Page 36 - Daivadnya Mahila Mandal, Belagavi' },
      { page: 193, title: 'Page 193 - Omkrown PharmaChem Pvt Ltd' },
      { page: 194, title: 'Page 194 - Shri Ganesh Gold Chains' },
      { page: 195, title: 'Page 195 - Shri Munishwar Motors (Royal Enfield)' },
      { page: 196, title: 'Page 196 - Back Cover: भगवान गणेश माहिती' }
    ];

    landmarks.forEach(lm => {
      const opt = document.createElement('option');
      opt.value = lm.page;
      opt.textContent = lm.title;
      landmarkGroup.appendChild(opt);
    });
    this.jumpSelect.appendChild(landmarkGroup);

    // All 196 Pages Optgroup
    const allGroup = document.createElement('optgroup');
    allGroup.label = '📖 All Pages (1 - 196)';

    this.pages.forEach(page => {
      const opt = document.createElement('option');
      opt.value = page.pageNumber;
      opt.textContent = `Page ${page.pageNumber}: ${page.title}`;
      allGroup.appendChild(opt);
    });
    this.jumpSelect.appendChild(allGroup);

    this.jumpSelect.addEventListener('change', (e) => {
      this.goToPage(parseInt(e.target.value, 10));
    });
  }

  // Render Thumbnails in Drawer
  renderThumbnails() {
    if (!this.thumbnailsTrack) return;
    this.thumbnailsTrack.innerHTML = '';

    this.pages.forEach(page => {
      const thumb = document.createElement('div');
      thumb.className = `thumb-card ${page.pageNumber === this.currentPage ? 'active' : ''}`;
      thumb.dataset.page = page.pageNumber;
      thumb.innerHTML = `
        <div class="thumb-img-wrap">
          <img src="${page.thumbnail}" alt="${page.title}" loading="lazy" class="thumb-img" />
        </div>
        <span class="thumb-number">P. ${page.pageNumber}</span>
        <span class="thumb-title" title="${page.title}">${page.title}</span>
      `;
      thumb.addEventListener('click', () => {
        this.goToPage(page.pageNumber);
        this.toggleThumbnailDrawer(false);
      });
      this.thumbnailsTrack.appendChild(thumb);
    });
  }

  // Realistic paper-turn sound using Web Audio API
  playPageTurnSound() {
    try {
      if (!this.audioCtx) {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (AudioContext) this.audioCtx = new AudioContext();
      }
      if (!this.audioCtx || this.audioCtx.state === 'suspended') {
        this.audioCtx?.resume();
      }
      if (!this.audioCtx) return;

      const bufferSize = this.audioCtx.sampleRate * 0.14; // 140ms
      const buffer = this.audioCtx.createBuffer(1, bufferSize, this.audioCtx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }

      const noise = this.audioCtx.createBufferSource();
      noise.buffer = buffer;

      const filter = this.audioCtx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(900, this.audioCtx.currentTime);
      filter.frequency.exponentialRampToValueAtTime(100, this.audioCtx.currentTime + 0.14);

      const gain = this.audioCtx.createGain();
      gain.gain.setValueAtTime(0.09, this.audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + 0.14);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(this.audioCtx.destination);

      noise.start();
    } catch (e) {
      // Ignore if audio permissions not granted
    }
  }

  // Generate Page Element with High-Resolution Image
  generatePageHTML(page) {
    if (!page) {
      return '<div class="book-page-image-container empty-page"></div>';
    }

    return `
      <div class="book-page-image-container" data-page="${page.pageNumber}">
        <img 
          src="${page.image}" 
          alt="${page.title}" 
          class="book-page-img" 
          loading="eager"
          decoding="async"
        />
        <div class="page-overlay-gloss"></div>
        <div class="page-number-footer-tag">${page.pageNumber}</div>
      </div>
    `;
  }

  // Render current spread based on viewport mode
  renderCurrentSpread() {
    this.isSinglePageMode = window.innerWidth <= 820;

    if (this.isSinglePageMode) {
      // Mobile Single Page View
      this.bookStage.classList.add('single-cover-mode');
      const page = this.pages[this.currentPage - 1];
      this.leftSlot.style.display = 'none';
      this.rightSlot.style.display = 'block';
      this.rightSlot.innerHTML = this.generatePageHTML(page);
      this.indicator.textContent = `Page ${this.currentPage} of ${this.totalPages}`;
    } else {
      // Desktop Two-Page Spread View
      if (this.currentPage === 1) {
        // Front Cover alone centered
        this.bookStage.classList.add('single-cover-mode');
        this.leftSlot.innerHTML = '';
        this.leftSlot.style.display = 'none';
        this.rightSlot.style.display = 'block';
        this.rightSlot.innerHTML = this.generatePageHTML(this.pages[0]);
        this.indicator.textContent = `Cover (Page 1 of ${this.totalPages})`;
      } else if (this.currentPage === this.totalPages) {
        // Back Cover alone centered
        this.bookStage.classList.add('single-cover-mode');
        this.leftSlot.innerHTML = '';
        this.leftSlot.style.display = 'none';
        this.rightSlot.style.display = 'block';
        this.rightSlot.innerHTML = this.generatePageHTML(this.pages[this.totalPages - 1]);
        this.indicator.textContent = `Back Cover (Page ${this.totalPages} of ${this.totalPages})`;
      } else {
        // Two-page spread
        this.bookStage.classList.remove('single-cover-mode');
        this.leftSlot.style.display = 'block';
        this.rightSlot.style.display = 'block';

        // Even page on left, odd page on right
        let leftPageNum = this.currentPage % 2 === 0 ? this.currentPage : this.currentPage - 1;
        let rightPageNum = leftPageNum + 1;

        if (rightPageNum > this.totalPages) {
          rightPageNum = this.totalPages;
        }

        const leftPage = this.pages[leftPageNum - 1];
        const rightPage = this.pages[rightPageNum - 1];

        this.leftSlot.innerHTML = this.generatePageHTML(leftPage);
        this.rightSlot.innerHTML = this.generatePageHTML(rightPage);

        this.indicator.textContent = `Pages ${leftPageNum} - ${rightPageNum} of ${this.totalPages}`;
      }
    }

    if (this.jumpSelect) {
      this.jumpSelect.value = this.currentPage;
    }

    // Highlight active thumbnail and auto-scroll thumbnail track
    document.querySelectorAll('.thumb-card').forEach(card => {
      const pageNum = parseInt(card.dataset.page, 10);
      const isActive = pageNum === this.currentPage || (!this.isSinglePageMode && pageNum === this.currentPage + 1);
      card.classList.toggle('active', isActive);
      if (pageNum === this.currentPage && this.thumbnailDrawer?.classList.contains('open')) {
        card.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });

    this.updateControls();
    this.preloadAdjacentPages(this.currentPage);
  }

  // Update next / prev button states
  updateControls() {
    if (this.prevBtn) {
      this.prevBtn.disabled = this.currentPage <= 1;
    }
    if (this.nextBtn) {
      this.nextBtn.disabled = this.currentPage >= this.totalPages;
    }
  }

  // Advance forward
  nextPage() {
    if (this.isAnimating || this.currentPage >= this.totalPages) return;
    this.playPageTurnSound();

    let step = 1;
    if (!this.isSinglePageMode) {
      if (this.currentPage === 1) {
        step = 1; // From cover (1) to spread 2-3
      } else if (this.currentPage >= this.totalPages - 2) {
        step = this.totalPages - this.currentPage; // To back cover
      } else {
        step = 2; // Flip 2 pages
      }
    }

    this.currentPage = Math.min(this.totalPages, this.currentPage + step);
    this.renderCurrentSpread();
  }

  // Go backward
  prevPage() {
    if (this.isAnimating || this.currentPage <= 1) return;
    this.playPageTurnSound();

    let step = 1;
    if (!this.isSinglePageMode) {
      if (this.currentPage === this.totalPages) {
        // From back cover (196) back to 194-195
        this.currentPage = this.totalPages - 2;
        this.renderCurrentSpread();
        return;
      } else if (this.currentPage <= 3) {
        this.currentPage = 1;
        this.renderCurrentSpread();
        return;
      } else {
        step = 2;
      }
    }

    this.currentPage = Math.max(1, this.currentPage - step);
    this.renderCurrentSpread();
  }

  // Direct page navigation
  goToPage(pageNum) {
    const target = Math.max(1, Math.min(this.totalPages, pageNum));
    if (target === this.currentPage && this.rightSlot.hasChildNodes()) return;

    this.playPageTurnSound();
    this.currentPage = target;
    this.renderCurrentSpread();

    // Scroll smoothly to the flipbook
    this.container.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // Toggle Thumbnail Drawer
  toggleThumbnailDrawer(open) {
    if (!this.thumbnailDrawer) return;
    const shouldOpen = open !== undefined ? open : !this.thumbnailDrawer.classList.contains('open');
    this.thumbnailDrawer.classList.toggle('open', shouldOpen);
    const backdrop = document.getElementById('thumbnailBackdrop');
    if (backdrop) {
      backdrop.classList.toggle('active', shouldOpen);
    }
    if (shouldOpen) {
      const activeCard = this.thumbnailsTrack.querySelector(`.thumb-card[data-page="${this.currentPage}"]`);
      if (activeCard) {
        setTimeout(() => activeCard.scrollIntoView({ behavior: 'smooth', inline: 'center' }), 100);
      }
    }
  }

  // Zoom Controls
  setZoom(delta) {
    this.zoomLevel = Math.max(0.8, Math.min(2.0, this.zoomLevel + delta));
    this.bookStage.style.transform = `scale(${this.zoomLevel})`;
    this.bookStage.style.cursor = this.zoomLevel > 1 ? 'grab' : 'default';
  }

  resetZoom() {
    this.zoomLevel = 1;
    this.bookStage.style.transform = 'scale(1)';
    this.bookStage.style.cursor = 'default';
  }

  // Toggle Fullscreen
  toggleFullscreen() {
    if (!document.fullscreenElement) {
      this.container.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  }

  // Bind Events
  bindEvents() {
    this.prevBtn?.addEventListener('click', () => this.prevPage());
    this.nextBtn?.addEventListener('click', () => this.nextPage());

    // Click on book sides to flip
    this.leftSlot?.addEventListener('click', (e) => {
      if (this.zoomLevel === 1) this.prevPage();
    });
    this.rightSlot?.addEventListener('click', (e) => {
      if (this.zoomLevel === 1) this.nextPage();
    });

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        this.nextPage();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        this.prevPage();
      } else if (e.key === 'Home') {
        this.goToPage(1);
      } else if (e.key === 'End') {
        this.goToPage(this.totalPages);
      }
    });

    // Touch Swipe Navigation for Mobile
    let touchStartX = 0;
    let touchEndX = 0;

    this.container.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    this.container.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      const swipeDistance = touchEndX - touchStartX;
      if (Math.abs(swipeDistance) > 45) {
        if (swipeDistance < 0) {
          this.nextPage(); // Swiped left
        } else {
          this.prevPage(); // Swiped right
        }
      }
    }, { passive: true });

    // Window resize
    window.addEventListener('resize', () => {
      const wasSingle = this.isSinglePageMode;
      this.isSinglePageMode = window.innerWidth <= 820;
      if (wasSingle !== this.isSinglePageMode) {
        this.renderCurrentSpread();
      }
    });
  }
}
