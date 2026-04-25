/**
 * Gestion des Candidatures - JobMatch
 * Ce script gère l'enregistrement, la consultation et la mise à jour des candidatures
 */

// ============= SAUVEGARDER UNE OFFRE =============
async function saveJob(jobData) {
    /**
     * Sauvegarde une offre d'emploi
     * jobData = {
     *   title: "Senior Developer",
     *   company: "Google",
     *   location: "Mountain View",
     *   salary: "$150K-$200K",
     *   description: "...",
     *   contract_type: "CDI"
     * }
     */
    try {
        const response = await fetch('/api/save-offer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(jobData)
        });

        const result = await response.json();
        if (response.ok) {
            showToast('Offre sauvegardée ! 💾', 'success');
            return result.offer_id;
        } else {
            showToast(result.error || 'Erreur lors de la sauvegarde', 'error');
        }
    } catch (err) {
        console.error('Erreur:', err);
        showToast('Erreur de communication', 'error');
    }
}

// ============= RÉCUPÉRER LES CANDIDATURES =============
async function loadApplications() {
    /**
     * Charge toutes les candidatures de l'utilisateur
     */
    try {
        const response = await fetch('/api/get-applications');
        const data = await response.json();

        if (data.success) {
            displayApplications(data.applications);
            return data.applications;
        }
    } catch (err) {
        console.error('Erreur chargement candidatures:', err);
        showToast('Erreur de chargement', 'error');
    }
}

function displayApplications(applications) {
    /**
     * Affiche les candidatures dans un tableau
     */
    const container = document.querySelector('.applications-list') || 
                     document.querySelector('.pro-table tbody');
    
    if (!container) return;

    if (applications.length === 0) {
        container.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px; color: var(--text-muted);">Aucune candidature sauvegardée</td></tr>';
        return;
    }

    const rows = applications.map(app => `
        <tr data-app-id="${app.id}">
            <td>
                <div class="td-main">${app.title}</div>
                <div class="td-sub">${app.company} • ${app.location || 'Remote'}</div>
            </td>
            <td>${app.date}</td>
            <td>${app.salary || 'Non spécifié'}</td>
            <td>
                <select class="status-select" data-app-id="${app.id}" onchange="updateApplicationStatus(${app.id}, this.value)">
                    <option value="saved" ${app.status === 'saved' ? 'selected' : ''}>📌 Sauvegardée</option>
                    <option value="applied" ${app.status === 'applied' ? 'selected' : ''}>✅ Appliquée</option>
                    <option value="rejected" ${app.status === 'rejected' ? 'selected' : ''}>❌ Rejetée</option>
                </select>
            </td>
            <td>
                <button class="tbl-action" onclick="viewApplication(${app.id})">👁️ Voir</button>
                <button class="tbl-action delete" onclick="deleteApplication(${app.id})">🗑️</button>
            </td>
        </tr>
    `).join('');

    container.innerHTML = rows;
}

// ============= METTRE À JOUR LE STATUT =============
async function updateApplicationStatus(applicationId, newStatus) {
    /**
     * Met à jour le statut d'une candidature
     * statut: 'saved' | 'applied' | 'rejected'
     */
    try {
        const response = await fetch('/api/update-application-status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id: applicationId,
                status: newStatus
            })
        });

        const result = await response.json();
        if (response.ok) {
            showToast(`Statut mis à jour en "${newStatus}" ✅`, 'success');
            
            // Recharger le tableau
            loadApplications();
        } else {
            showToast(result.error || 'Erreur', 'error');
        }
    } catch (err) {
        console.error('Erreur:', err);
        showToast('Erreur de communication', 'error');
    }
}

// ============= SUPPRIMER UNE CANDIDATURE =============
async function deleteApplication(applicationId) {
    /**
     * Supprime une candidature
     */
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette candidature ?')) {
        return;
    }

    try {
        const response = await fetch('/api/delete-application', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: applicationId })
        });

        const result = await response.json();
        if (response.ok) {
            showToast('Candidature supprimée 🗑️', 'success');
            loadApplications();
        } else {
            showToast(result.error || 'Erreur', 'error');
        }
    } catch (err) {
        console.error('Erreur:', err);
        showToast('Erreur de communication', 'error');
    }
}

// ============= VOIR LES DÉTAILS =============
function viewApplication(applicationId) {
    /**
     * Affiche les détails d'une candidature
     */
    // À implémenter selon votre modal/template préféré
    console.log('Voir candidature:', applicationId);
    showToast('Ouverture des détails...', 'info');
}

// ============= HELPER: SAUVEGARDER DEPUIS L'ANALYSEUR =============
function saveAnalyzedJobOffer(jobTitle, companyName) {
    /**
     * Sauvegarde l'offre analysée directement
     * Appel depuis job_generator_v3.html
     */
    return saveJob({
        title: jobTitle || document.getElementById('analyzed-job-title')?.value || 'Offre analysée',
        company: companyName || 'Non spécifié',
        description: document.getElementById('jobOfferText')?.value || '',
        contract_type: 'CDI'
    });
}

// Charger les candidatures au chargement de la page "Mes Offres"
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/my-offers' || document.getElementById('applications-page')) {
        loadApplications();
    }
});
