// ============= NAVBAR RESPONSIVE MANAGEMENT =============

class NavbarManager {
    constructor() {
        this.navToggle = document.getElementById('mobile-nav-toggle');
        this.sidebar = document.getElementById('pro-sidebar');
        this.overlay = document.getElementById('sidebar-overlay');
        this.navLinks = document.querySelectorAll('.nav-item');
        this.navbar = document.getElementById('navbar'); // For landing page
        this.breakpoint = 1024;
        this.isMenuOpen = false;

        this.init();
    }

    init() {
        if (this.navToggle) {
            this.navToggle.addEventListener('click', () => this.toggleMobileMenu());
        }

        if (this.overlay) {
            this.overlay.addEventListener('click', () => this.closeMobileMenu());
        }

        this.navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= this.breakpoint) {
                    this.closeMobileMenu();
                }
            });
        });

        window.addEventListener('resize', () => {
            if (window.innerWidth > this.breakpoint && this.isMenuOpen) {
                this.closeMobileMenu();
            }
        });

        // Landing page scroll effect
        window.addEventListener('scroll', () => {
            if (this.navbar) {
                if (window.scrollY > 50) {
                    this.navbar.classList.add('scrolled');
                } else {
                    this.navbar.classList.remove('scrolled');
                }
            }
        });
    }

    toggleMobileMenu() {
        this.isMenuOpen = !this.isMenuOpen;
        if (this.isMenuOpen) {
            this.openMobileMenu();
        } else {
            this.closeMobileMenu();
        }
    }

    openMobileMenu() {
        if (this.sidebar) this.sidebar.classList.add('active');
        if (this.overlay) this.overlay.classList.add('active');
        if (this.navToggle) this.navToggle.classList.add('active');
        document.body.style.overflow = 'hidden';
        this.isMenuOpen = true;
    }

    closeMobileMenu() {
        if (this.sidebar) this.sidebar.classList.remove('active');
        if (this.overlay) this.overlay.classList.remove('active');
        if (this.navToggle) this.navToggle.classList.remove('active');
        document.body.style.overflow = '';
        this.isMenuOpen = false;
    }

    updateActiveLink() {
        let current = '';
        const sections = document.querySelectorAll('section[id]');

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            if (window.scrollY >= sectionTop - 150) {
                current = section.getAttribute('id');
            }
        });

        this.navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');

            if (href && href.substring(1) === current) {
                link.classList.add('active');
            }
        });
    }

    // Public method pour scroll
    scrollToSection(sectionId) {
        this.closeMobileMenu();
        setTimeout(() => {
            const section = document.getElementById(sectionId);
            if (section) {
                const offset = 80;
                const elementPosition = section.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - offset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        }, 100);
    }
}

// Initialize navbar manager
let navbarManager;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        navbarManager = new NavbarManager();
    });
} else {
    navbarManager = new NavbarManager();
}

// Global functions
function scrollToSection(e, sectionId) {
    if (e) e.preventDefault();
    if (navbarManager) {
        navbarManager.scrollToSection(sectionId);
    } else {
        const section = document.getElementById(sectionId);
        if (section) {
            const offset = 80;
            const elementPosition = section.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - offset;
            window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
        }
    }
}

function closeMobileMenu() {
    if (navbarManager) {
        navbarManager.closeMobileMenu();
    }
}

// ============= MODE SOMBRE =============
const themeToggle = document.getElementById('theme-toggle');

if (themeToggle) {
    themeToggle.addEventListener('click', function () {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        updateThemeIcon();
    });
}

function updateThemeIcon() {
    if (themeToggle) {
        if (document.body.classList.contains('dark-mode')) {
            themeToggle.textContent = '☀️';
        } else {
            themeToggle.textContent = '🌙';
        }
    }
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
    updateThemeIcon();
}

// ============= HISTORIQUE ============= 
const historyToggle = document.getElementById('history-toggle');

function toggleHistory() {
    const sidebar = document.getElementById('history-sidebar');
    if (sidebar) {
        sidebar.classList.toggle('active');
        loadHistory();
    }
}

if (historyToggle) {
    historyToggle.addEventListener('click', toggleHistory);
}

function saveAnalysis(data) {
    let history = JSON.parse(localStorage.getItem('jobmatchHistory') || '[]');
    const analysis = {
        id: Date.now(),
        date: new Date().toLocaleString('fr-FR'),
        score: data.scores.final,
        recommendation: data.recommendation.substring(0, 50) + '...',
        data: data
    };
    history.unshift(analysis);
    if (history.length > 20) history.pop();
    localStorage.setItem('jobmatchHistory', JSON.stringify(history));
}

function loadHistory() {
    const history = JSON.parse(localStorage.getItem('jobmatchHistory') || '[]');
    const historyList = document.getElementById('history-list');

    if (history.length === 0) {
        historyList.innerHTML = '<p class="empty-message">Aucune analyse pour le moment</p>';
        return;
    }

    historyList.innerHTML = history.map(item => `
        <div class="history-item" onclick="restoreAnalysis(${item.id})">
            <div class="history-item-title">Score: <strong>${item.score}%</strong></div>
            <div class="history-item-score">${item.date}</div>
        </div>
    `).join('');
}

function restoreAnalysis(id) {
    const history = JSON.parse(localStorage.getItem('jobmatchHistory') || '[]');
    const analysis = history.find(item => item.id === id);
    if (analysis) {
        displayResults(analysis.data);
        toggleHistory();
        showToast('Analyse restaurée');
    }
}

// ============= FAQ ============= 
function toggleFAQ(element) {
    const faqItem = element.closest('.faq-item-premium');
    if (!faqItem) return;

    const isActive = faqItem.classList.contains('active');

    // Fermer tous les autres
    document.querySelectorAll('.faq-item-premium.active').forEach(item => {
        if (item !== faqItem) {
            item.classList.remove('active');
        }
    });

    faqItem.classList.toggle('active');
}

// Add event listeners for new FAQ
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.faq-question-premium').forEach(q => {
        q.addEventListener('click', () => toggleFAQ(q));
    });
});

// ============= NOTIFICATIONS ============= 
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ============= NAVBAR MOBILE ============= 
// Géré par NavbarManager ci-dessus

// Update active nav link on scroll
window.addEventListener('scroll', function () {
    let current = '';
    const sections = document.querySelectorAll('section[id]');

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// ============= DOM ELEMENTS =============
const pdfFileInput = document.getElementById('pdf_file');
const jobOfferTextarea = document.getElementById('job_offer');
const analyzeBtn = document.getElementById('analyze-btn');
const thresholdSlider = document.getElementById('threshold');
const thresholdValue = document.getElementById('threshold-value');
const showDetailsCheckbox = document.getElementById('show_details');
const resultsSection = document.getElementById('results-section');
const fileNameDisplay = document.getElementById('file-name');

// Wait for DOM to be ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPage);
} else {
    initPage();
}

function initPage() {
    // Initialize file input if exists
    if (pdfFileInput) {
        pdfFileInput.addEventListener('change', function (e) {
            if (this.files.length > 0 && fileNameDisplay) {
                fileNameDisplay.textContent = this.files[0].name;
                fileNameDisplay.style.fontWeight = '600';
                fileNameDisplay.style.color = '#2ECC71';
            }
        });
    }

    // Initialize threshold slider if exists
    if (thresholdSlider && thresholdValue) {
        thresholdSlider.addEventListener('input', function () {
            thresholdValue.textContent = this.value;
        });
    }

    // Initialize analyze button if exists
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', analyzeCV);
    }

    // Initialize AI generator button
    const btnGenerateAI = document.getElementById('btn-generate-ai');
    if (btnGenerateAI) {
        btnGenerateAI.addEventListener('click', generateAIOffer);
    }
}

// File upload, threshold slider, and analyze button handlers are now in initPage()

async function analyzeCV(e) {
    if (e) e.preventDefault();
    
    // Validation
    if (!pdfFileInput || !pdfFileInput.files.length) {
        showError('Veuillez télécharger un CV en PDF');
        return;
    }

    if (!jobOfferTextarea || !jobOfferTextarea.value.trim() || jobOfferTextarea.value.trim().length < 20) {
        showError('Veuillez coller une offre d\'emploi valide (au minimum 20 caractères)');
        return;
    }

    // Prepare form data
    const formData = new FormData();
    formData.append('pdf_file', pdfFileInput.files[0]);
    formData.append('job_offer', jobOfferTextarea.value);
    formData.append('threshold', thresholdSlider ? thresholdSlider.value : 3);

    // Show loading state
    if (analyzeBtn) {
        analyzeBtn.disabled = true;
        const btnText = analyzeBtn.querySelector('.btn-text');
        const btnLoading = analyzeBtn.querySelector('.btn-loading');
        if (btnText) btnText.style.display = 'none';
        if (btnLoading) btnLoading.style.display = 'inline';
    }

    try {
        // Send request
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erreur lors de l\'analyse');
        }

        // Display results
        displayResults(data);
        saveAnalysis(data); // Sauvegarder dans l'historique local
        
        let msg = 'Analyse terminée avec succès';
        if (data.candidacy_id) {
            msg += ' et ajoutée à vos candidatures !';
        }
        showToast(msg);

    } catch (error) {
        showError(error.message);
    } finally {
        // Reset button state
        if (analyzeBtn) {
            analyzeBtn.disabled = false;
            const btnText = analyzeBtn.querySelector('.btn-text');
            const btnLoading = analyzeBtn.querySelector('.btn-loading');
            if (btnText) btnText.style.display = 'inline';
            if (btnLoading) btnLoading.style.display = 'none';
        }
    }
}

// ============= DISPLAY RESULTS =============
function displayResults(data) {
    if (!resultsSection) return;

    // Show results section
    resultsSection.style.display = 'block';

    // Smooth scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);

    // Status message
    displayStatusMessage(data);

    // Scores
    const mainScore = document.getElementById('main-score');
    const similarityScore = document.getElementById('similarity-score');
    const coverageScore = document.getElementById('coverage-score');

    mainScore.textContent = data.scores.final;
    mainScore.className = 'score-value ' + data.score_color;
    similarityScore.textContent = data.scores.similarity;
    coverageScore.textContent = data.scores.coverage;

    // Recommendation
    const recommendationBox = document.getElementById('recommendation-box');
    recommendationBox.innerHTML = parseMarkdown(data.recommendation);

    // Set recommendation class
    if (data.scores.final >= 70) {
        recommendationBox.className = 'recommendation-box recommendation-success';
    } else if (data.scores.final >= 50) {
        recommendationBox.className = 'recommendation-box recommendation-warning';
    } else {
        recommendationBox.className = 'recommendation-box recommendation-info';
    }

    // Missing keywords
    const missingKeywordsContainer = document.getElementById('missing-keywords');
    if (data.missing_keywords.length > 0) {
        missingKeywordsContainer.innerHTML = data.missing_keywords
            .map(kw => `<div class="keyword-box">📍 <strong>${kw.keyword}</strong></div>`)
            .join('');
    } else {
        missingKeywordsContainer.innerHTML = '<p style="color: #2ECC71; font-weight: 600; text-align: center; width: 100%;">✅ Votre CV contient déjà les mots-clés principaux!</p>';
    }

    // Detailed analysis
    if (showDetailsCheckbox && showDetailsCheckbox.checked) {
        displayDetailedAnalysis(data);
    } else {
        const detailedSection = document.getElementById('detailed-section');
        if (detailedSection) detailedSection.style.display = 'none';
    }

    // Save to history
    saveAnalysis(data);
}

// ============= DISPLAY STATUS MESSAGE =============
function displayStatusMessage(data) {
    const statusBox = document.getElementById('status-message');

    if (data.scores.final >= 70) {
        statusBox.className = 'status-message status-success';
        statusBox.innerHTML = '✅ Analyse complétée!';
    } else if (data.scores.final >= 50) {
        statusBox.className = 'status-message status-warning';
        statusBox.innerHTML = '✅ Analyse complétée!';
    } else {
        statusBox.className = 'status-message status-info';
        statusBox.innerHTML = '✅ Analyse complétée!';
    }
}

// ============= DISPLAY DETAILED ANALYSIS =============
function displayDetailedAnalysis(data) {
    const detailedSection = document.getElementById('detailed-section');
    const cvKeywordsList = document.getElementById('cv-keywords');
    const jobKeywordsList = document.getElementById('job-keywords');

    // CV keywords
    cvKeywordsList.innerHTML = data.cv_keywords
        .map(kw => `<li><strong>${kw.keyword}</strong> (${kw.count})</li>`)
        .join('');

    // Job keywords
    jobKeywordsList.innerHTML = data.job_keywords
        .map(kw => `<li><strong>${kw.keyword}</strong> (${kw.count})</li>`)
        .join('');

    detailedSection.style.display = 'block';
}

// ============= ERROR HANDLING =============
function showError(message) {
    // Create error container if not exists
    let errorContainer = document.getElementById('error-message');
    if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.id = 'error-message';
        errorContainer.className = 'status-message';
        document.querySelector('.input-section').parentElement.insertBefore(
            errorContainer,
            document.querySelector('.input-section')
        );
    }

    errorContainer.className = 'status-message';
    errorContainer.style.background = '#f8d7da';
    errorContainer.style.borderColor = '#f5c6cb';
    errorContainer.style.color = '#721c24';
    errorContainer.innerHTML = `❌ ${message}`;
    errorContainer.style.display = 'block';

    // Scroll to error
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Auto-hide after 5 seconds
    setTimeout(() => {
        errorContainer.style.display = 'none';
    }, 5000);
}

// ============= MARKDOWN PARSER =============
function parseMarkdown(text) {
    // Bold
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
    // Return parsed text
    return text;
}

// ============= KEYBOARD SHORTCUT =============
document.addEventListener('keydown', function (e) {
    // Ctrl/Cmd + Enter to analyze
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        if (jobOfferTextarea === document.activeElement) {
            analyzeCV();
        }
    }
});

// ============= RESULTS ACTIONS =============
function copyResults() {
    const resultsText = generateResultsText();
    navigator.clipboard.writeText(resultsText).then(() => {
        showToast('Résultats copiés dans le presse-papier!', 'success');
    }).catch(() => {
        showToast('Erreur lors de la copie', 'error');
    });
}

function shareViaEmail() {
    const resultsText = generateResultsText();
    const subject = encodeURIComponent('Résultats d\'analyse JobMatch');
    const body = encodeURIComponent(resultsText);
    window.location.href = `mailto:?subject=${subject}&body=${body}`;
}

function exportPDF() {
    // Alias vers la fonction réelle
    exportPDFReal();
}

function newAnalysis() {
    // Reset form
    if (pdfFileInput) pdfFileInput.value = '';
    if (jobOfferTextarea) jobOfferTextarea.value = '';
    if (fileNameDisplay) {
        fileNameDisplay.textContent = 'Sélectionnez un fichier PDF';
        fileNameDisplay.style.fontWeight = 'normal';
        fileNameDisplay.style.color = '';
    }

    // Hide results
    if (resultsSection) resultsSection.style.display = 'none';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    showToast('Nouvelle analyse prête', 'success');
}

function generateResultsText() {
    const mainScore = document.getElementById('main-score')?.textContent || '--';
    const similarityScore = document.getElementById('similarity-score')?.textContent || '--';
    const coverageScore = document.getElementById('coverage-score')?.textContent || '--';
    const recommendation = document.getElementById('recommendation-box')?.textContent || '';
    const missingKeywords = Array.from(document.querySelectorAll('#missing-keywords .keyword-box'))
        .map(el => el.textContent.trim())
        .join(', ');

    return `Résultats d'analyse JobMatch
========================

Score Global: ${mainScore}%
Similarité Textuelle: ${similarityScore}%
Couverture Mots-clés: ${coverageScore}%

Recommandation:
${recommendation}

Mots-clés à ajouter:
${missingKeywords || 'Aucun'}

Généré le ${new Date().toLocaleString('fr-FR')}`;
}

// Carousel functions removed

// ============= TABS MANAGEMENT =============
function showTab(tabId) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
        tab.style.display = 'none';
    });

    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab content
    const activeTab = document.getElementById(tabId);
    if (activeTab) {
        activeTab.classList.add('active');
        activeTab.style.display = 'block';
    }

    // Add active class to the clicked button
    if (event && event.target) {
        event.target.classList.add('active');
    }
}

// ============= DASHBOARD V3 LOGIC =============

async function initDashboardV3() {
    console.log('Initializing Dashboard V3 console...');
    try {
        const response = await fetch('/api/dashboard-stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;

            // Update Metric Cards
            updateV3Metric('v3-total-analyses', stats.total_analyses);
            updateV3Metric('v3-avg-score', stats.avg_score, '%');
            updateV3Metric('v3-best-score', stats.best_score, '%');
            updateV3Metric('v3-improvement', stats.improvement_rate, '%');

            // Update Activity Feed with real notifications
            updateActivityFeed(stats.notifications || []);

            // Update Job Alerts with real saved offers
            updateJobAlerts(stats.saved_offers || []);

            // Update Recent Analyses Table
            updateAnalysesTable(stats.recent_analyses || []);

            // Initialize Pro Chart
            initV3Chart(stats);
        }
    } catch (error) {
        console.error('V3 Dashboard Load Error:', error);
        showToast('Échec de la console V3', 'error');
    }
}

function updateActivityFeed(notifications) {
    const feedContainer = document.querySelector('.pro-feed');
    if (!feedContainer) return;

    if (notifications.length === 0) {
        feedContainer.innerHTML = '<p style="color: var(--text-muted); padding: 16px; text-align: center;">Aucune activité récente</p>';
        return;
    }

    const iconColors = ['blue', 'purple', 'orange'];
    feedContainer.innerHTML = notifications.map((notif, idx) => `
        <div class="feed-entry">
            <div class="feed-icon ${iconColors[idx % 3]}"></div>
            <div class="feed-info">
                <p>${notif.title}</p>
                <span>${new Date(notif.date).toLocaleString('fr-FR')}</span>
            </div>
        </div>
    `).join('');
}

function updateJobAlerts(savedOffers) {
    const jobAlertsContainer = document.querySelector('.job-alerts');
    if (!jobAlertsContainer) return;

    if (savedOffers.length === 0) {
        jobAlertsContainer.innerHTML = '<p style="color: var(--text-muted); padding: 16px; text-align: center;">Aucune offre sauvegardée</p>';
        return;
    }

    const statusMap = {
        'saved': { label: 'Sauvegardée', class: 'high' },
        'applied': { label: 'Appliquée', class: 'medium' },
        'rejected': { label: 'Rejetée', class: 'low' }
    };

    jobAlertsContainer.innerHTML = savedOffers.map(offer => {
        const statusInfo = statusMap[offer.status] || { label: 'Inconnue', class: 'medium' };
        return `
            <div class="job-alert-item">
                <div class="job-alert-header">
                    <span class="job-title">${offer.title}</span>
                    <span class="match-badge ${statusInfo.class}">${statusInfo.label}</span>
                </div>
                <div class="job-alert-meta">
                    <span>${offer.company}</span>
                    <span class="salary">${offer.date}</span>
                </div>
            </div>
        `;
    }).join('');
}

function updateAnalysesTable(analyses) {
    const tbody = document.querySelector('.pro-table tbody');
    if (!tbody) return;

    if (analyses.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px; color: var(--text-muted);">Aucune analyse réalisée</td></tr>';
        return;
    }

    tbody.innerHTML = analyses.map(analysis => {
        const scoreClass = analysis.score >= 70 ? 'pos' : (analysis.score >= 50 ? 'mid' : 'neg');
        const statusClass = analysis.score >= 70 ? 'pos' : (analysis.score >= 50 ? 'mid' : 'neg');
        const statusText = analysis.score >= 70 ? 'Optimal' : (analysis.score >= 50 ? 'À Améliorer' : 'Faible Match');
        return `
            <tr>
                <td>
                    <div class="td-main">${analysis.title}</div>
                    <div class="td-sub">${analysis.similarity_score}% similarité</div>
                </td>
                <td>${analysis.date}</td>
                <td><span class="score-pill ${scoreClass}">${analysis.score}%</span></td>
                <td><span class="status-pill ${statusClass}">${statusText}</span></td>
                <td><button class="tbl-action">Voir</button></td>
            </tr>
        `;
    }).join('');
}

function updateV3Metric(id, value, suffix = '') {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = (typeof value === 'number' ? Math.round(value) : value) + suffix;
    }
}

function initV3Chart(stats) {
    const ctx = document.getElementById('v3-main-chart');
    if (!ctx) return;

    if (window.v3Chart) window.v3Chart.destroy();

    window.v3Chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
            datasets: [{
                label: 'Volume Analyses',
                data: [4, 8, 5, 12, 9, 15, stats.total_analyses],
                backgroundColor: '#6366f1',
                borderRadius: 4
            }, {
                label: 'Score Médian',
                data: [60, 65, 70, 68, 82, 75, stats.avg_score],
                type: 'line',
                borderColor: '#10b981',
                borderWidth: 3,
                tension: 0.4,
                pointRadius: 0,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top', align: 'end', labels: { boxWidth: 12, usePointStyle: true } }
            },
            scales: {
                y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { font: { size: 10 } } },
                x: { grid: { display: false }, ticks: { font: { size: 10 } } }
            }
        }
    });
}

async function startV3Analysis() {
    const jobText = document.getElementById('v3-job-text').value;
    const pdfFile = document.getElementById('v3-pdf-file').files[0];
    const btn = document.querySelector('.so-cta');

    if (!jobText || !pdfFile) {
        showToast("Données incomplètes pour l'analyse", "warning");
        return;
    }

    btn.disabled = true;
    btn.textContent = "Analyse Cognitive...";

    const formData = new FormData();
    formData.append('job_offer', jobText);
    formData.append('pdf_file', pdfFile);
    formData.append('threshold', 50);

    try {
        const resp = await fetch('/api/improve-cv', { method: 'POST', body: formData });
        const data = await resp.json();

        if (data.success) {
            document.getElementById('v3-panel-results').style.display = 'block';

            // Score final
            let score = 0;
            if (data.score_optimisation) {
                score = data.score_optimisation;
            } else if (data.data && data.data.score_optimisation) {
                score = data.data.score_optimisation;
            } else if (data.score_matching) {
                score = data.score_matching;
            } else if (data.scores && data.scores.final) {
                score = data.scores.final;
            }
            document.getElementById('v3-final-score').textContent = score + "%";

            // Recommandations
            const recText = data.improvements.join('\n');
            document.getElementById('v3-rec-text').innerHTML = data.improvements.map(i => `• ${i}`).join('<br>');

            // Afficher le bouton de téléchargement si on a des données structurées
            if (data.data) {
                window.lastImprovedCVData = data.data;
                document.getElementById('v3-download-section').style.display = 'block';
            }

            showToast("Optimisation terminée avec succès");
        } else {
            showToast(data.error || "Erreur analyse", "error");
        }
    } catch (e) {
        showToast("Erreur de communication API", "error");
        console.error(e);
    } finally {
        btn.disabled = false;
        btn.textContent = "Lancer l'Optimisation Cognitive";
    }
}

async function downloadImprovedCVPDF() {
    if (!window.lastImprovedCVData) {
        showToast("Aucune donnée disponible pour le téléchargement", "warning");
        return;
    }

    try {
        const response = await fetch('/api/download-cv-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                cv_data: window.lastImprovedCVData,
                nom: window.lastImprovedCVData.nom || 'Mon_CV_Optimise'
            })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${window.lastImprovedCVData.nom || 'Mon_CV'}_Optimise.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            showToast("Erreur lors de la génération du PDF", "error");
        }
    } catch (e) {
        showToast("Erreur de téléchargement", "error");
        console.error(e);
    }
}

// Dropzone logic V3
document.addEventListener('DOMContentLoaded', () => {
    const dz = document.getElementById('v3-drop-zone');
    const inp = document.getElementById('v3-pdf-file');
    if (dz && inp) {
        dz.onclick = () => inp.click();
        inp.onchange = () => {
            if (inp.files[0]) document.getElementById('v3-file-text').textContent = inp.files[0].name;
        };
    }
});

// ============= END OF SCRIPT =============
async function loadDashboard() {
    try {
        const response = await fetch('/api/dashboard-stats');
        const data = await response.json();

        if (data.success) {
            const stats = data.stats;

            // Update new large IDs
            if (document.getElementById('total-analyses-large')) document.getElementById('total-analyses-large').textContent = stats.total_analyses;
            if (document.getElementById('avg-score-large')) document.getElementById('avg-score-large').textContent = stats.avg_score.toFixed(1) + '%';
            if (document.getElementById('best-score-large')) document.getElementById('best-score-large').textContent = stats.best_score.toFixed(1) + '%';
            if (document.getElementById('improvement-large')) document.getElementById('improvement-large').textContent = '+' + stats.improvement_rate.toFixed(1) + '%';

            // Initialize Charts if elements exist
            initDashboardCharts(stats);
        }
    } catch (error) {
        console.error('Dashboard load error:', error);
    }
}

function initDashboardCharts(stats) {
    const ctx = document.getElementById('scores-evolution-chart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Anal. 1', 'Anal. 2', 'Anal. 3', 'Anal. 4', 'Anal. 5'],
                datasets: [{
                    label: 'Score Match',
                    data: [stats.avg_score - 10, stats.avg_score - 5, stats.avg_score, stats.avg_score + 2, stats.best_score],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { color: 'rgba(0,0,0,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }
}

// ============= TRENDS =============
async function loadTrends() {
    try {
        const response = await fetch('/api/trends');
        const data = await response.json();

        if (data.success) {
            const trends = data.trends;

            // Display keywords
            const keywordsContainer = document.getElementById('trends-keywords');
            if (keywordsContainer) {
                keywordsContainer.innerHTML = trends.top_keywords.map(kw => `
                    <div class="trend-item">
                        <span class="trend-keyword">${kw.keyword}</span>
                        <span class="trend-frequency">${kw.frequency}%</span>
                        <span class="trend-arrow ${kw.trend}">${kw.trend === 'up' ? '📈' : kw.trend === 'down' ? '📉' : '➡️'}</span>
                    </div>
                `).join('');
            }

            // Display sectors
            const sectorsContainer = document.getElementById('trends-sectors');
            if (sectorsContainer) {
                sectorsContainer.innerHTML = trends.sectors.map(sec => `
                    <div class="trend-item">
                        <span class="trend-keyword">${sec.sector}</span>
                        <span class="trend-frequency">${sec.demand}%</span>
                        <span class="trend-arrow up">🔥</span>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        showToast('Erreur lors du chargement des tendances', 'error');
    }
}

// ============= AI GENERATOR =============
async function generateAIOffer() {
    const btn = document.getElementById('btn-generate-ai');
    const textarea = document.getElementById('job_offer');

    if (!btn || !textarea) return;

    // Show loading state
    btn.classList.add('loading');
    btn.disabled = true;
    const originalContent = btn.innerHTML;
    btn.innerHTML = '<span class="btn-icon">⏳</span> <span class="btn-text">Génération...</span>';

    try {
        const response = await fetch('/api/generate-job-offer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ role_type: null })
        });

        const data = await response.json();

        if (data.success && data.offer) {
            textarea.value = data.offer.description;

            // Met à jour manuellement le compteur de caractères
            const charCount = document.getElementById('charCount');
            if (charCount) {
                charCount.textContent = textarea.value.length;
            }

            // Met à jour l'aperçu si nécessaire (si script existant le gère)
            textarea.dispatchEvent(new Event('input'));

            showToast('Offre générée avec succès !', 'success');

            // Animation flash sur le textarea
            textarea.style.transition = 'background 0.3s';
            textarea.style.background = 'rgba(46, 204, 113, 0.1)';
            setTimeout(() => {
                textarea.style.background = '';
            }, 1000);

        } else {
            throw new Error(data.error || 'Erreur lors de la génération');
        }
    } catch (error) {
        showToast('Erreur: ' + error.message, 'error');
    } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
        btn.innerHTML = originalContent;
    }
}

// ============= COMPARE CVs =============
document.addEventListener('DOMContentLoaded', function () {
    const compareFiles = document.getElementById('compare_files');
    const compareBtn = document.getElementById('compare-btn');
    const compareResults = document.getElementById('compare-results');

    if (compareFiles) {
        compareFiles.addEventListener('change', function () {
            const files = Array.from(this.files);
            const names = files.map(f => f.name).join(', ');
            document.getElementById('compare-files-names').textContent =
                files.length > 0 ? `${files.length} fichier(s) sélectionné(s)` : 'Sélectionnez 2 CV ou plus (PDF)';
        });
    }

    if (compareBtn) {
        compareBtn.addEventListener('click', async function () {
            const files = document.getElementById('compare_files').files;
            const jobOffer = document.getElementById('job_offer').value;

            if (files.length < 2) {
                showError('Veuillez sélectionner au moins 2 CV');
                return;
            }

            if (!jobOffer || jobOffer.length < 50) {
                showError('Veuillez coller une offre d\'emploi valide');
                return;
            }

            const formData = new FormData();
            for (let file of files) {
                formData.append('pdf_files', file);
            }
            formData.append('job_offer', jobOffer);

            compareBtn.disabled = true;
            const btnText = compareBtn.querySelector('.btn-text');
            const btnLoading = compareBtn.querySelector('.btn-loading');
            if (btnText) btnText.style.display = 'none';
            if (btnLoading) btnLoading.style.display = 'inline';

            try {
                const response = await fetch('/api/compare-cvs', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || 'Erreur lors de la comparaison');
                }

                // Display results
                compareResults.style.display = 'block';
                compareResults.innerHTML = `
                    <h3>📊 Résultats de la Comparaison</h3>
                    ${data.comparison.map((cv, idx) => `
                        <div class="compare-item ${idx === 0 ? 'best' : ''}">
                            <div class="compare-header">
                                <span class="compare-filename">${cv.filename}</span>
                                ${idx === 0 ? '<span class="compare-badge">🏆 Meilleur Match</span>' : ''}
                            </div>
                            <div class="compare-scores">
                                <div class="compare-score-item">
                                    <div class="compare-score-label">Score Global</div>
                                    <div class="compare-score-value ${cv.score_color}">${cv.scores.final}%</div>
                                </div>
                                <div class="compare-score-item">
                                    <div class="compare-score-label">Similarité</div>
                                    <div class="compare-score-value">${cv.scores.similarity}%</div>
                                </div>
                                <div class="compare-score-item">
                                    <div class="compare-score-label">Couverture</div>
                                    <div class="compare-score-value">${cv.scores.coverage}%</div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                `;

                showToast('Comparaison terminée!', 'success');
            } catch (error) {
                showError(error.message);
            } finally {
                compareBtn.disabled = false;
                if (btnText) btnText.style.display = 'inline';
                if (btnLoading) btnLoading.style.display = 'none';
            }
        });
    }
});

// ============= SUGGESTIONS =============
document.addEventListener('DOMContentLoaded', function () {
    const suggestionsBtn = document.getElementById('suggestions-btn');
    const suggestionsResults = document.getElementById('suggestions-results');

    if (suggestionsBtn) {
        suggestionsBtn.addEventListener('click', async function () {
            const pdfFile = document.getElementById('pdf_file').files[0];
            const jobOffer = document.getElementById('job_offer').value;

            if (!pdfFile) {
                showError('Veuillez sélectionner un CV');
                return;
            }

            if (!jobOffer || jobOffer.length < 50) {
                showError('Veuillez coller une offre d\'emploi valide');
                return;
            }

            // Extract text from PDF (simplified - in production, use the backend)
            const formData = new FormData();
            formData.append('pdf_file', pdfFile);
            formData.append('job_offer', jobOffer);

            suggestionsBtn.disabled = true;
            const btnText = suggestionsBtn.querySelector('.btn-text');
            const btnLoading = suggestionsBtn.querySelector('.btn-loading');
            if (btnText) btnText.style.display = 'none';
            if (btnLoading) btnLoading.style.display = 'inline';

            try {
                // First analyze to get CV text
                const analyzeResponse = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });

                const analyzeData = await analyzeResponse.json();

                if (!analyzeResponse.ok) {
                    throw new Error(analyzeData.error || 'Erreur lors de l\'analyse');
                }

                // Get suggestions
                const suggestResponse = await fetch('/api/suggest-rephrasing', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        cv_text: analyzeData.cv_keywords.map(k => k.keyword).join(' '), // Use extracted keywords as a proxy for text
                        job_offer: jobOffer
                    })
                });

                const suggestData = await suggestResponse.json();

                if (!suggestResponse.ok) {
                    throw new Error(suggestData.error || 'Erreur lors de la génération des suggestions');
                }

                // Display suggestions
                suggestionsResults.style.display = 'block';
                suggestionsResults.innerHTML = `
                    <h3>💡 Suggestions de Reformulation</h3>
                    ${suggestData.suggestions.map(sug => `
                        <div class="suggestion-item ${sug.priority}">
                            <div class="suggestion-header">
                                <span class="suggestion-keyword">${sug.keyword}</span>
                                <span class="suggestion-priority ${sug.priority}">${sug.priority === 'high' ? 'Priorité Haute' : 'Priorité Moyenne'}</span>
                            </div>
                            <div class="suggestion-text">${sug.suggestion}</div>
                        </div>
                    `).join('')}
                `;

                showToast('Suggestions générées!', 'success');
            } catch (error) {
                showError(error.message);
            } finally {
                suggestionsBtn.disabled = false;
                if (btnText) btnText.style.display = 'inline';
                if (btnLoading) btnLoading.style.display = 'none';
            }
        });
    }
});

// ============= EXPORT PDF REAL =============
async function exportPDFReal() {
    try {
        // Get current results data
        const resultsData = {
            scores: {
                final: document.getElementById('main-score')?.textContent || '0',
                similarity: document.getElementById('similarity-score')?.textContent || '0',
                coverage: document.getElementById('coverage-score')?.textContent || '0'
            },
            recommendation: document.getElementById('recommendation-box')?.textContent || '',
            missing_keywords: Array.from(document.querySelectorAll('#missing-keywords .keyword-box'))
                .map(el => ({ keyword: el.textContent.trim().replace('📍', '').trim() }))
        };

        const response = await fetch('/api/export-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(resultsData)
        });

        if (!response.ok) {
            throw new Error('Erreur lors de l\'export');
        }

        // Download the PDF
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `JobMatch_Analyse_${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        showToast('PDF exporté avec succès!', 'success');
    } catch (error) {
        showToast('Erreur lors de l\'export PDF', 'error');
    }
}

// Load trends on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadTrends);
} else {
    loadTrends();
}

// Carousel removed

// ============= UPLOAD FILE HANDLER - PREMIUM DESIGN =============

document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('pdf_file');
    const filePreview = document.getElementById('filePreview');
    const uploadContent = document.querySelector('.upload-content');
    const jobOfferTextarea = document.getElementById('job_offer');
    const charCountElement = document.getElementById('charCount');

    // Drag and Drop Events
    if (dropZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('dragover');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('dragover');
            });
        });

        dropZone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            handleFileSelect(files);
        });

        // Click to select
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (e) => {
            handleFileSelect(e.target.files);
        });
    }

    function handleFileSelect(files) {
        if (files.length > 0) {
            const file = files[0];

            // Check if PDF
            if (file.type !== 'application/pdf') {
                alert('⚠️ Veuillez sélectionner un fichier PDF');
                return;
            }

            // Check file size (max 10MB)
            const maxSize = 10 * 1024 * 1024;
            if (file.size > maxSize) {
                alert('⚠️ Le fichier ne doit pas dépasser 10 MB');
                return;
            }

            // Show preview
            // Show preview in drop text
            const fileName = file.name;
            const fileSize = (file.size / (1024 * 1024)).toFixed(2) + ' MB';

            if (fileNameDisplay) {
                fileNameDisplay.textContent = `${fileName} (${fileSize})`;
                fileNameDisplay.style.color = 'var(--primary)';
            }
        }
    }
});

function clearFile() {
    const fileInput = document.getElementById('pdf_file');
    const filePreview = document.getElementById('filePreview');
    const uploadContent = document.querySelector('.upload-content');

    fileInput.value = '';
    filePreview.style.display = 'none';
    uploadContent.style.display = 'flex';
}

// ============= GLOBAL ANALYZER CONTROLS =============
function openAnalyzerV3() {
    const overlay = document.getElementById('v3-analyzer-overlay');
    if (overlay) overlay.classList.add('active');
}

function closeAnalyzerV3() {
    const overlay = document.getElementById('v3-analyzer-overlay');
    if (overlay) overlay.classList.remove('active');
}

// Remove separate threshold handler - unified in main logic

// ============= OPTIMIZE CV FOR JOB OFFER =============
async function optimizeCVForJobOffer(cvText, jobOfferText) {
    try {
        const response = await fetch('/api/optimize-cv-for-offer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                cv_text: cvText,
                job_offer_text: jobOfferText
            })
        });

        if (!response.ok) {
            const error = await response.json();
            return { error: error.error || 'Erreur lors de l\'optimisation' };
        }

        const data = await response.json();
        return data.optimization;
    } catch (error) {
        console.error('Erreur optimisation CV:', error);
        return { error: error.message };
    }
}

// ============= PREMIUM CV GENERATION =============
async function generatePremiumCV() {
    const fileInput = document.getElementById('pdf_file');
    if (!fileInput || !fileInput.files[0]) {
        alert("⚠️ Veuillez d'abord téléverser votre CV.");
        return;
    }

    const btn = document.querySelector('.btn-premium-trigger');
    const originalText = btn.innerHTML;
    btn.innerHTML = "⏳ Génération...";
    btn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('pdf_file', fileInput.files[0]);

        const response = await fetch('/api/generate-premium-cv', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const html = await response.text();
            const win = window.open('', '_blank');
            win.document.write(html);
            win.document.close();
        } else {
            const error = await response.json();
            const msg = error.details ? `❌ ${error.error} : ${error.details}` : `❌ Erreur: ${error.error}`;
            alert(msg);
        }
    } catch (e) {
        console.error(e);
        alert("❌ Une erreur est survenue lors de la génération.");
    } finally {
        if (btn) {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }
}
// ============= NOTIFICATION SYSTEM =============
async function fetchNotifications() {
    try {
        const response = await fetch('/api/notifications');
        const data = await response.json();

        if (data.success) {
            updateNotificationUI(data.notifications);
        }
    } catch (err) {
        console.error("Failed to fetch notifications:", err);
    }
}

function updateNotificationUI(notifications) {
    const list = document.getElementById('notif-list');
    const badge = document.getElementById('notif-count');
    if (!list) return;

    const unreadCount = notifications.filter(n => !n.is_read).length;

    // Update Badge
    if (badge) {
        if (unreadCount > 0) {
            badge.textContent = unreadCount > 9 ? '9+' : unreadCount;
            badge.style.display = 'flex';
        } else {
            badge.style.display = 'none';
        }
    }

    // Update List
    if (notifications.length === 0) {
        list.innerHTML = `<div class="notif-empty-pro">Aucune notification</div>`;
        return;
    }

    list.innerHTML = notifications.map(n => `
        <div class="notif-item-pro ${n.is_read ? '' : 'unread'}" onclick="markAsRead(${n.id}, this)">
            <div class="notif-item-title">${n.title}</div>
            <div class="notif-item-msg">${n.message}</div>
            <div class="notif-item-time">${formatNotifDate(n.created_at)}</div>
        </div>
    `).join('');
}

async function clearAllNotifs() {
    try {
        const response = await fetch('/api/notifications/read-all', { method: 'POST' });
        if (response.ok) {
            fetchNotifications(); // Refresh list and badge
        }
    } catch (err) {
        console.error("Error clearing notifications:", err);
    }
}

async function markAsRead(id, element) {
    try {
        const response = await fetch(`/api/notifications/read/${id}`, { method: 'POST' });
        if (response.ok) {
            element.classList.remove('unread');
            // Refresh badge count
            const badge = document.getElementById('notif-count');
            if (badge) {
                let count = parseInt(badge.textContent) || 0;
                if (count > 0) {
                    count--;
                    if (count === 0) badge.style.display = 'none';
                    else badge.textContent = count;
                }
            }
        }
    } catch (err) {
        console.error("Error marking notification as read:", err);
    }
}

function formatNotifDate(dateStr) {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = (now - date) / 1000; // seconds

    if (diff < 60) return "À l'instant";
    if (diff < 3600) return `Il y a ${Math.floor(diff / 60)} min`;
    if (diff < 86400) return `Il y a ${Math.floor(diff / 3600)} h`;
    return date.toLocaleDateString('fr-FR');
}

function initNotificationPanel() {
    const bell = document.getElementById('notification-bell');
    const panel = document.getElementById('notif-panel');

    if (!bell || !panel) return;

    bell.addEventListener('click', (e) => {
        e.stopPropagation();
        panel.classList.toggle('active');
        if (panel.classList.contains('active')) {
            fetchNotifications();
        }
    });

    document.addEventListener('click', (e) => {
        if (!panel.contains(e.target) && !bell.contains(e.target)) {
            panel.classList.remove('active');
        }
    });

    // Initial fetch
    fetchNotifications();
    // Poll for new notifications every 60s
    setInterval(fetchNotifications, 60000);
}

// ============= DASHBOARD V3 ANALYSIS =============
function initDashboardV3() {
    console.log("Initializing Dashboard V3 Console...");
    const dropZone = document.getElementById('v3-drop-zone');
    const fileInput = document.getElementById('v3-pdf-file');
    const fileText = document.getElementById('v3-file-text');

    if (dropZone && fileInput) {
        dropZone.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                fileText.textContent = e.target.files[0].name;
                dropZone.classList.add('has-file');
            }
        });

        // Drag & Drop
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('drag-over');
        });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('drag-over');
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                fileText.textContent = e.dataTransfer.files[0].name;
            }
        });
    }
}

async function startV3Analysis() {
    const jobText = document.getElementById('v3-job-text').value.trim();
    const fileInput = document.getElementById('v3-pdf-file');
    const btn = document.querySelector('.so-cta');
    const resultsPanel = document.getElementById('v3-panel-results');
    const formPanel = document.querySelector('.so-form');

    if (!jobText || !fileInput.files[0]) {
        alert("⚠️ Veuillez fournir l'offre ET votre CV.");
        return;
    }

    btn.disabled = true;
    btn.textContent = "⏳ Analyse en cours...";

    const formData = new FormData();
    formData.append('pdf_file', fileInput.files[0]);
    formData.append('job_offer', jobText);

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        if (data.success) {
            // Update UI
            document.getElementById('v3-final-score').textContent = data.final_score + '%';
            document.getElementById('v3-rec-text').textContent = data.recommendation;

            formPanel.style.display = 'none';
            resultsPanel.style.display = 'block';

            // Pulse the notification bell if score is high
            if (data.final_score > 80) {
                const bell = document.getElementById('notification-bell');
                if (bell) bell.classList.add('pulse-notif');
            }
        } else {
            const msg = data.details ? `❌ ${data.error} : ${data.details}` : `❌ Erreur: ${data.error}`;
            alert(msg);
        }
    } catch (err) {
        console.error(err);
        alert("❌ Une erreur est survenue lors de l'analyse.");
    } finally {
        btn.disabled = false;
        btn.textContent = "Lancer l'Analyse Cognitive";
    }
}

// Global initialization
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (typeof initChatbotPro === 'function') initChatbotPro();
        initNotificationPanel();
        if (typeof initDashboardV3 === 'function') initDashboardV3();
    });
} else {
    if (typeof initChatbotPro === 'function') initChatbotPro();
    initNotificationPanel();
    if (typeof initDashboardV3 === 'function') initDashboardV3();
}

// Generate test job offer for V3 dashboard slide-over
async function generateTestJobOfferV3() {
    const jobTextArea = document.getElementById('v3-job-text');
    const btn = event.target;
    const originalText = btn.innerHTML;

    btn.disabled = true;
    btn.innerHTML = "⏳";

    try {
        const response = await fetch('/api/generate-test-job-offer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        const data = await response.json();

        if (data.success) {
            jobTextArea.value = data.job_offer;
            jobTextArea.style.transition = 'all 0.3s ease';
            jobTextArea.style.background = 'rgba(52, 152, 219, 0.1)';
            setTimeout(() => {
                jobTextArea.style.background = '';
            }, 1000);
        } else {
            alert(`❌ Erreur: ${data.error}`);
        }
    } catch (err) {
        console.error(err);
        alert("❌ Erreur lors de la génération.");
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

// ============= SEARCH & NAVIGATION FUNCTIONS =============

/**
 * Filter users table in superadmin page
 */
function filterUsers() {
    const searchInput = document.getElementById('userSearch');
    if (!searchInput) return;

    const filter = searchInput.value.toLowerCase();
    const table = document.querySelector('.users-table');
    if (!table) return;

    const rows = table.querySelectorAll('tbody tr');
    let visibleCount = 0;

    rows.forEach(row => {
        const userName = row.querySelector('.user-name')?.textContent.toLowerCase() || '';
        const userEmail = row.querySelector('.email-cell')?.textContent.toLowerCase() || '';
        const userId = row.querySelector('.user-id')?.textContent.toLowerCase() || '';

        if (userName.includes(filter) || userEmail.includes(filter) || userId.includes(filter)) {
            row.style.display = '';
            visibleCount++;
        } else {
            row.style.display = 'none';
        }
    });

    // Show message if no results
    const tableBody = table.querySelector('tbody');
    let noResultsRow = table.querySelector('.no-results-row');

    if (visibleCount === 0) {
        if (!noResultsRow) {
            noResultsRow = document.createElement('tr');
            noResultsRow.className = 'no-results-row';
            noResultsRow.innerHTML = '<td colspan="4" style="text-align: center; padding: 40px; color: var(--text-muted);">Aucun utilisateur trouvé</td>';
            tableBody.appendChild(noResultsRow);
        }
    } else {
        if (noResultsRow) {
            noResultsRow.remove();
        }
    }
}

/**
 * Navigate to CV Analyzer page
 */
function openAnalyzerV3() {
    window.location.href = '/cv-improver';
}

/**
 * Header search functionality
 */
function initHeaderSearch() {
    const searchInput = document.querySelector('.search-pro input');
    if (!searchInput) return;

    searchInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            const query = this.value.trim();
            if (query) {
                performGlobalSearch(query);
            }
        }
    });

    // Add search icon click handler
    const searchIcon = document.querySelector('.search-ico');
    if (searchIcon) {
        searchIcon.style.cursor = 'pointer';
        searchIcon.addEventListener('click', function () {
            const query = searchInput.value.trim();
            if (query) {
                performGlobalSearch(query);
            }
        });
    }
}

/**
 * Perform global platform search
 */
function performGlobalSearch(query) {
    // Check current page and perform contextual search
    const currentPath = window.location.pathname;

    if (currentPath.includes('superadmin')) {
        // Search in user table
        const userSearch = document.getElementById('userSearch');
        if (userSearch) {
            userSearch.value = query;
            filterUsers();
        }
    } else if (currentPath.includes('my-offers')) {
        // Search in job offers
        searchJobOffers(query);
    } else if (currentPath.includes('dashboard')) {
        // Search in dashboard
        searchDashboard(query);
    } else {
        // Default: show search results or redirect to search page
        showToast(`Recherche: "${query}"`, 'info');
        // Could implement a dedicated search results page here
    }
}

/**
 * Search job offers (placeholder for my-offers page)
 */
function searchJobOffers(query) {
    const offers = document.querySelectorAll('.offer-card, .job-card');
    let visibleCount = 0;

    offers.forEach(offer => {
        const text = offer.textContent.toLowerCase();
        if (text.includes(query.toLowerCase())) {
            offer.style.display = '';
            visibleCount++;
        } else {
            offer.style.display = 'none';
        }
    });

    if (visibleCount === 0) {
        showToast('Aucune offre trouvée', 'warning');
    } else {
        showToast(`${visibleCount} offre(s) trouvée(s)`, 'success');
    }
}

/**
 * Search dashboard (placeholder for dashboard page)
 */
function searchDashboard(query) {
    showToast(`Recherche dans le dashboard: "${query}"`, 'info');
    // Implement dashboard-specific search logic here
}

/**
 * Initialize search functionality on page load
 */
document.addEventListener('DOMContentLoaded', function () {
    initHeaderSearch();
});

// ============= UTILITY FUNCTIONS =============

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    // Check if toast container exists, create if not
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 10000;';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-left: 4px solid ${type === 'success' ? 'var(--success)' : type === 'warning' ? 'var(--warning)' : type === 'error' ? 'var(--danger)' : 'var(--info)'};
        padding: 12px 20px;
        margin-bottom: 10px;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        min-width: 250px;
        animation: slideInRight 0.3s ease;
        color: var(--text-primary);
    `;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Add CSS animations for toast
if (!document.getElementById('toast-animations')) {
    const style = document.createElement('style');
    style.id = 'toast-animations';
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// ============= USER MANAGEMENT FUNCTIONS (SUPERADMIN) =============

/**
 * Edit user - Opens modal with user data
 */
function editUser(userId) {
    // Find user data from the table
    const userRow = document.querySelector(`tr[data-user-id="${userId}"]`);
    if (!userRow) {
        console.error('User row not found for ID:', userId);
        showToast('Utilisateur introuvable', 'error');
        return;
    }

    // Extract user data from the row
    const userName = userRow.querySelector('.user-name')?.textContent.trim() || '';
    const userEmail = userRow.querySelector('.email-cell')?.textContent.trim() || '';
    const isAdmin = userRow.querySelector('.badge-pro.admin') !== null;

    // Create edit modal
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content pro-card" style="max-width: 500px; animation: slideInUp 0.3s ease;">
            <div class="modal-header">
                <h3>✏️ Modifier l'utilisateur</h3>
                <button class="close-btn" onclick="closeModal(this)">&times;</button>
            </div>
            <div class="modal-body">
                <div class="form-group">
                    <label>Nom complet</label>
                    <input type="text" id="edit-user-name" value="${userName}" class="form-input" readonly style="background: var(--bg-tertiary); cursor: not-allowed;">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="edit-user-email" value="${userEmail}" class="form-input" readonly style="background: var(--bg-tertiary); cursor: not-allowed;">
                </div>
                <div class="form-group">
                    <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                        <input type="checkbox" id="edit-user-admin" ${isAdmin ? 'checked' : ''} style="width: 20px; height: 20px;">
                        <span>Administrateur</span>
                    </label>
                </div>
            </div>
            <div class="modal-footer" style="display: flex; gap: 10px; justify-content: flex-end;">
                <button class="btn-secondary" onclick="closeModal(this)">Annuler</button>
                <button class="btn-primary" onclick="saveUserChanges(${userId})">Enregistrer</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Add click outside to close
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal(modal.querySelector('.close-btn'));
        }
    });
}

/**
 * Save user changes
 */
async function saveUserChanges(userId) {
    const isAdmin = document.getElementById('edit-user-admin').checked;

    try {
        const response = await fetch(`/api/users/${userId}/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                is_admin: isAdmin
            })
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showToast('Utilisateur mis à jour avec succès', 'success');

            // Update the UI
            const userRow = document.querySelector(`tr[data-user-id="${userId}"]`);
            if (userRow) {
                const badge = userRow.querySelector('.badge-pro');
                if (badge) {
                    badge.className = `badge-pro ${isAdmin ? 'admin' : 'member'}`;
                    badge.textContent = isAdmin ? 'Administrateur' : 'Membre';
                }
            }

            // Close modal
            const modal = document.querySelector('.modal-overlay');
            if (modal) modal.remove();
        } else {
            showToast(data.error || 'Erreur lors de la mise à jour', 'error');
        }
    } catch (error) {
        console.error('Error updating user:', error);
        showToast('Erreur de connexion au serveur', 'error');
    }
}

/**
 * Delete user - Shows confirmation dialog
 */
function deleteUser(userId) {
    const userRow = document.querySelector(`tr[data-user-id="${userId}"]`);
    if (!userRow) {
        showToast('Utilisateur introuvable', 'error');
        return;
    }

    const userName = userRow.querySelector('.user-name')?.textContent.trim() || 'cet utilisateur';

    // Create confirmation modal
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-content pro-card" style="max-width: 450px; animation: slideInUp 0.3s ease;">
            <div class="modal-header">
                <h3>🗑️ Supprimer l'utilisateur</h3>
                <button class="close-btn" onclick="closeModal(this)">&times;</button>
            </div>
            <div class="modal-body">
                <p style="color: var(--text-secondary); margin-bottom: 20px;">
                    Êtes-vous sûr de vouloir supprimer <strong>${userName}</strong> ?
                </p>
                <div style="background: rgba(239, 68, 68, 0.1); border-left: 4px solid var(--danger); padding: 12px; border-radius: 8px;">
                    <p style="color: var(--danger); margin: 0; font-size: 0.9rem;">
                        ⚠️ Cette action est irréversible. Toutes les données de l'utilisateur seront supprimées.
                    </p>
                </div>
            </div>
            <div class="modal-footer" style="display: flex; gap: 10px; justify-content: flex-end;">
                <button class="btn-secondary" onclick="closeModal(this)">Annuler</button>
                <button class="btn-danger" onclick="confirmDeleteUser(${userId})" style="background: var(--danger);">Supprimer</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Add click outside to close
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            closeModal(modal.querySelector('.close-btn'));
        }
    });
}

/**
 * Confirm and execute user deletion
 */
async function confirmDeleteUser(userId) {
    try {
        const response = await fetch(`/api/users/${userId}/delete`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();

        if (response.ok && data.success) {
            showToast('Utilisateur supprimé avec succès', 'success');

            // Remove the row from table with animation
            const userRow = document.querySelector(`tr[data-user-id="${userId}"]`);
            if (userRow) {
                userRow.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => userRow.remove(), 300);
            }

            // Close modal
            const modal = document.querySelector('.modal-overlay');
            if (modal) modal.remove();
        } else {
            showToast(data.error || 'Erreur lors de la suppression', 'error');
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        showToast('Erreur de connexion au serveur', 'error');
    }
}

/**
 * Close modal helper
 */
function closeModal(button) {
    const modal = button.closest('.modal-overlay');
    if (modal) {
        modal.style.animation = 'fadeOut 0.2s ease';
        setTimeout(() => modal.remove(), 200);
    }
}

// Add modal styles if not already present
if (!document.getElementById('modal-styles')) {
    const style = document.createElement('style');
    style.id = 'modal-styles';
    style.textContent = `
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.2s ease;
        }

        .modal-content {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 16px;
            max-width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: var(--shadow-xl);
        }

        .modal-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-header h3 {
            margin: 0;
            color: var(--text-primary);
        }

        .close-btn {
            background: none;
            border: none;
            font-size: 28px;
            color: var(--text-muted);
            cursor: pointer;
            padding: 0;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            transition: all 0.2s;
        }

        .close-btn:hover {
            background: var(--bg-hover);
            color: var(--text-primary);
        }

        .modal-body {
            padding: 20px;
        }

        .modal-footer {
            padding: 20px;
            border-top: 1px solid var(--border);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            color: var(--text-secondary);
            font-weight: 500;
        }

        .form-input {
            width: 100%;
            padding: 12px;
            background: var(--bg-primary);
            border: 1px solid var(--border);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 14px;
            transition: all 0.2s;
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }

        .btn-primary, .btn-secondary, .btn-danger {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background: var(--primary-dark);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }

        .btn-secondary:hover {
            background: var(--bg-hover);
        }

        .btn-danger {
            background: var(--danger);
            color: white;
        }

        .btn-danger:hover {
            background: #dc2626;
            transform: translateY(-1px);
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }

        @keyframes slideInUp {
            from {
                transform: translateY(20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
}

// ============= CHATBOT FUNCTIONALITY =============

/**
 * Initialize chatbot interactions
 */
function initChatbotPro() {
    const chatbotFab = document.getElementById('chatbot-fab');
    const chatWindow = document.getElementById('chat-window');
    const closeChat = document.getElementById('close-chat');
    const sendChat = document.getElementById('send-chat');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');

    if (!chatbotFab || !chatWindow) {
        console.log('Chatbot elements not found');
        return;
    }

    // Open chat window
    chatbotFab.addEventListener('click', function () {
        chatWindow.classList.add('active');
        chatbotFab.style.display = 'none';

        // Focus input
        setTimeout(() => {
            if (chatInput) chatInput.focus();
        }, 100);

        // Load chat history
        loadChatHistory();
    });

    // Close chat window
    if (closeChat) {
        closeChat.addEventListener('click', function () {
            chatWindow.classList.remove('active');
            chatbotFab.style.display = 'flex';
        });
    }

    // Send message on button click
    if (sendChat && chatInput && chatMessages) {
        sendChat.addEventListener('click', sendChatMessage);

        // Send message on Enter key
        chatInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendChatMessage();
            }
        });
    }

    /**
 * Load chat history from server
 */
    function loadChatHistory() {
        const chatMessages = document.getElementById('chat-messages');
        if (!chatMessages) return;

        fetch('/api/chatbot/history')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.history.length > 0) {
                    // Clear existing messages (except if empty)
                    chatMessages.innerHTML = '';

                    // Add welcome message if history is short or just as header
                    const welcomeDiv = document.createElement('div');
                    welcomeDiv.className = 'chat-welcome';
                    welcomeDiv.innerHTML = `
                    <div class="welcome-icon">👋</div>
                    <h3>Bonjour!</h3>
                    <p>Je suis l'assistant JobMatch. Comment puis-je vous aider aujourd'hui ?</p>
                `;
                    chatMessages.appendChild(welcomeDiv);

                    // Add history messages
                    data.history.forEach(msg => {
                        const msgDiv = document.createElement('div');
                        msgDiv.className = `message ${msg.role === 'user' ? 'user-message' : 'bot-message'}`;
                        msgDiv.textContent = msg.message;
                        chatMessages.appendChild(msgDiv);
                    });

                    // Add quick replies at the end
                    const quickReplies = document.createElement('div');
                    quickReplies.className = 'quick-replies';
                    quickReplies.innerHTML = `
                    <button class="quick-reply-btn" onclick="botHelp('analyzer')">📊 Analyser mon CV</button>
                    <button class="quick-reply-btn" onclick="botHelp('trends')">📈 Tendances</button>
                    <button class="quick-reply-btn" onclick="botHelp('profile')">👤 Mon profil</button>
                    <button class="quick-reply-btn" onclick="botHelp('tips')">💡 Conseils</button>
                `;
                    chatMessages.appendChild(quickReplies);

                    // Scroll to bottom
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            })
            .catch(error => console.error('Error loading history:', error));
    }

    // Emoji picker functionality
    const emojiBtn = document.getElementById('emoji-btn');
    if (emojiBtn && chatInput) {
        const emojis = ['😊', '😂', '❤️', '👍', '🎉', '🔥', '💡', '✨', '🚀', '💪', '👏', '🙏', '😍', '🤔', '😎', '🎯', '📊', '💼', '📝', '✅'];

        emojiBtn.addEventListener('click', function (e) {
            e.preventDefault();

            // Check if emoji popup already exists
            let emojiPopup = document.getElementById('emoji-popup');

            if (emojiPopup) {
                // Toggle visibility
                emojiPopup.style.display = emojiPopup.style.display === 'none' ? 'grid' : 'none';
            } else {
                // Create emoji popup
                emojiPopup = document.createElement('div');
                emojiPopup.id = 'emoji-popup';
                emojiPopup.className = 'emoji-popup';
                emojiPopup.style.cssText = `
                    position: absolute;
                    bottom: 70px;
                    left: 20px;
                    background: white;
                    border: 1px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 12px;
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                    gap: 8px;
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
                    z-index: 1000;
                `;

                emojis.forEach(emoji => {
                    const emojiSpan = document.createElement('span');
                    emojiSpan.textContent = emoji;
                    emojiSpan.style.cssText = `
                        font-size: 24px;
                        cursor: pointer;
                        padding: 8px;
                        border-radius: 8px;
                        transition: all 0.2s;
                        text-align: center;
                    `;
                    emojiSpan.addEventListener('mouseenter', function () {
                        this.style.background = '#f1f5f9';
                        this.style.transform = 'scale(1.2)';
                    });
                    emojiSpan.addEventListener('mouseleave', function () {
                        this.style.background = 'transparent';
                        this.style.transform = 'scale(1)';
                    });
                    emojiSpan.addEventListener('click', function () {
                        chatInput.value += emoji;
                        chatInput.focus();
                        emojiPopup.style.display = 'none';
                    });
                    emojiPopup.appendChild(emojiSpan);
                });

                chatWindow.appendChild(emojiPopup);
            }
        });

        // Close emoji popup when clicking outside
        document.addEventListener('click', function (e) {
            const emojiPopup = document.getElementById('emoji-popup');
            if (emojiPopup && !emojiBtn.contains(e.target) && !emojiPopup.contains(e.target)) {
                emojiPopup.style.display = 'none';
            }
        });
    }

    function sendChatMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Add user message to chat
        const userMessageDiv = document.createElement('div');
        userMessageDiv.className = 'message user-message';
        userMessageDiv.textContent = message;
        chatMessages.appendChild(userMessageDiv);

        // Clear input
        chatInput.value = '';

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Call Gemini API
        fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                typingDiv.remove();

                // Add bot response
                const botMessageDiv = document.createElement('div');
                botMessageDiv.className = 'message bot-message';

                if (data.success && data.response) {
                    botMessageDiv.textContent = data.response;
                } else {
                    botMessageDiv.textContent = data.response || "Désolé, je n'ai pas pu traiter votre demande.";
                }

                chatMessages.appendChild(botMessageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            })
            .catch(error => {
                console.error('Erreur chatbot:', error);

                // Remove typing indicator
                typingDiv.remove();

                // Show error message
                const botMessageDiv = document.createElement('div');
                botMessageDiv.className = 'message bot-message';
                botMessageDiv.textContent = "Désolé, une erreur s'est produite. Veuillez réessayer.";
                chatMessages.appendChild(botMessageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            });
    }

    function getBotResponse(userMessage) {
        const msg = userMessage.toLowerCase();

        if (msg.includes('cv') || msg.includes('curriculum')) {
            return "Pour optimiser votre CV, utilisez notre outil d'analyse CV. Il vous aidera à identifier les mots-clés importants et à améliorer votre compatibilité avec les offres d'emploi.";
        } else if (msg.includes('offre') || msg.includes('emploi')) {
            return "Vous pouvez analyser des offres d'emploi avec notre analyseur intelligent. Il compare votre profil avec les exigences de l'offre.";
        } else if (msg.includes('aide') || msg.includes('help')) {
            return "Je peux vous aider avec : l'analyse de CV, la recherche d'emploi, l'optimisation de profil, et les tendances du marché. Que souhaitez-vous savoir ?";
        } else {
            return "Merci pour votre message ! Pour une assistance personnalisée, n'hésitez pas à explorer nos outils d'analyse CV et de matching d'offres.";
        }
    }
}

/**
 * Handle quick help buttons
 */
function botHelp(topic) {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;

    let questionMap = {
        'analyzer': "Comment utiliser l'analyseur de CV ?",
        'trends': "Quelles sont les tendances du marché de l'emploi ?",
        'profile': "Comment mettre à jour mon profil ?",
        'tips': "Quels conseils pour améliorer mon CV ?"
    };

    const question = questionMap[topic] || "Comment puis-je vous aider ?";

    // Add user question to chat
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user-message';
    userMessageDiv.textContent = question;
    chatMessages.appendChild(userMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.innerHTML = '<span></span><span></span><span></span>';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Call API
    fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: question })
    })
        .then(response => response.json())
        .then(data => {
            typingDiv.remove();

            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'message bot-message';
            botMessageDiv.textContent = data.response || "Comment puis-je vous aider ?";
            chatMessages.appendChild(botMessageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        })
        .catch(error => {
            console.error('Erreur botHelp:', error);
            typingDiv.remove();

            const botMessageDiv = document.createElement('div');
            botMessageDiv.className = 'message bot-message';
            botMessageDiv.textContent = "Une erreur s'est produite. Veuillez réessayer.";
            chatMessages.appendChild(botMessageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
}
