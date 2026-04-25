function showApplicationDetails(app) {
    document.getElementById('modal-title').textContent = app.title || app.poste;
    document.getElementById('modal-company').textContent = app.company || app.entreprise;
    document.getElementById('modal-date').textContent = app.date;
    document.getElementById('modal-statut').innerHTML = `<span class="status-pill pos">${app.status || app.statut}</span>`;

    // Safety check for score
    if (app.score) {
        document.getElementById('modal-score').innerHTML = `<span class="score-pill pos">${app.score}</span>`;
    } else {
        document.getElementById('modal-score').innerHTML = `<span style="color:var(--text-muted)">N/A</span>`;
    }

    document.getElementById('modal-description').textContent = app.description || "Aucune description fournie.";
    document.getElementById('modal-contact').textContent = app.contact || "Non renseigné";

    // Competences
    const compDiv = document.getElementById('modal-competences');
    compDiv.innerHTML = '';
    const competences = app.competences || [];
    if (competences.length > 0) {
        competences.forEach(comp => {
            const tag = document.createElement('span');
            tag.style.cssText = 'background: var(--bg-tertiary); padding: 6px 12px; border-radius: 6px; font-size: 12px; color: var(--text-primary); border: 1px solid var(--border);';
            tag.textContent = comp;
            compDiv.appendChild(tag);
        });
    } else {
        compDiv.innerHTML = '<span style="color:var(--text-muted)">Aucune compétence spécifiée.</span>';
    }

    document.getElementById('applicationDetailsModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeDetailsModal() {
    document.getElementById('applicationDetailsModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function copyContact() {
    const contact = document.getElementById('modal-contact').textContent;
    if (contact && contact !== "Non renseigné") {
        navigator.clipboard.writeText(contact).then(() => {
            const btn = event.target;
            const originalText = btn.innerHTML;
            btn.innerHTML = '✓ Copié !';
            setTimeout(() => {
                btn.innerHTML = originalText;
            }, 2000);
        });
    }
}
