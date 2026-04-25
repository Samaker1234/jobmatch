$dashboardContent = @'
{% extends "base_v3.html" %}

{% block title %}JobMatch - Dashboard Console{% endblock %}
{% block page_title %}Dashboard{% endblock %}

{% block content %}
<!-- 1. Performance Overview (High Density Stats) -->
<div class="pro-metric-grid">
    <div class="metric-card-pro highlight">
        <div class="metric-header">
            <span class="metric-title">Score Moyen Global</span>
            <span class="trend-pro {% if improvement >= 0 %}pos{% else %}neg{% endif %}">{{ improvement }}%</span>
        </div>
        <div class="metric-value" id="v3-avg-score">{{ avg_score }}%</div>
        <div class="metric-footer">Performance moyenne des CV</div>
    </div>

    <div class="metric-card-pro">
        <div class="metric-header">
            <span class="metric-title">Index de Progression</span>
            <span class="trend-pro pos">+24%</span>
        </div>
        <div class="metric-value" id="v3-improvement">{{ improvement }}%</div>
        <div class="metric-footer">Évolution de la qualité CV</div>
    </div>

    <div class="metric-card-pro">
        <div class="metric-header">
            <span class="metric-title">Taux de Match Maximal</span>
            <span class="trend-pro neutral">Stable</span>
        </div>
        <div class="metric-value" id="v3-best-score">{{ best_score }}%</div>
        <div class="metric-footer">Meilleure adéquation détectée</div>
    </div>

    <div class="metric-card-pro">
        <div class="metric-header">
            <span class="metric-title">Analyses Réalisées</span>
            <span class="trend-pro pos">+{{ total_analyses }}</span>
        </div>
        <div class="metric-value" id="v3-total-analyses">{{ total_analyses }}</div>
        <div class="metric-footer">Volumes sur les 30 derniers jours</div>
    </div>
</div>

<!-- 2. Main Analytics & Activity Grid -->
<div class="pro-grid-main">
    <!-- Engagement Chart -->
    <div class="pro-card pro-chart-area">
        <div class="card-head">
            <h3>Activité & Performance Temporelle</h3>
            <div class="card-controls">
                <button class="filter-btn active">Semaine</button>
            </div>
        </div>
        <div class="chart-canvas-wrapper" style="height: 300px;">
            <div id="v3-main-chart-apex"></div>
        </div>
    </div>

    <!-- Right Sidebar Widgets -->
    <div class="pro-side-widgets">
        <!-- Quick Profile Card -->
        <div class="pro-card user-quick-card">
            <div class="qr-header">
                <div class="qr-avatar">{{ user.firstname[0] }}</div>
                <h3>{{ user.firstname }}</h3>
            </div>
            <div class="qr-stats">
                <div class="qr-stat">
                    <span class="val">84%</span>
                    <span class="lab">Complétion Profil</span>
                </div>
                <div class="qr-stat">
                    <span class="val">32</span>
                    <span class="lab">Offres Vues</span>
                </div>
            </div>
            <button class="pro-btn-outline full">Gérer le Profil</button>
        </div>

        <!-- Match Distribution Chart -->
        <div class="pro-card dist-card">
            <div class="card-head">
                <h3>Distribution des Matchs</h3>
            </div>
            <div id="v3-dist-chart-apex" style="min-height: 250px;"></div>
        </div>

        <!-- Activity Feed -->
        <div class="pro-card feed-card">
            <div class="card-head">
                <h3>Flux d'Activité</h3>
            </div>
            <div class="pro-feed">
                <!-- Rempli dynamiquement par JavaScript -->
            </div>
        </div>
    </div>
</div>

<!-- 3. Application Registry (Real Table) -->
<div class="pro-card table-section">
    <div class="card-head">
        <h3>Registre des Candidatures</h3>
        <div class="search-table-wrapper">
            <input type="text" placeholder="Filtrer les résultats...">
        </div>
    </div>
    <div class="pro-table-wrapper">
        <table class="pro-table">
            <thead>
                <tr>
                    <th>Poste / Entreprise</th>
                    <th>Date d'Analyse</th>
                    <th>Score Match</th>
                    <th>Statut IA</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for analysis in latest_analyses %}
                <tr class="pro-fade-in">
                    <td>
                        <div class="job-info">
                            <span class="job-title">{{ analysis.job_title[:30] }}...</span>
                            <span class="company-name">{{ analysis.filename }}</span>
                        </div>
                    </td>
                    <td>{{ analysis.created_at.strftime('%d/%m/%Y') }}</td>
                    <td>
                        <div
                            class="score-pill {% if analysis.final_score >= 70 %}high{% elif analysis.final_score >= 50 %}med{% else %}low{% endif %}">
                            {{ analysis.final_score|round|int }}%
                        </div>
                    </td>
                    <td><span class="status-ai">Généré par Gemini</span></td>
                    <td>
                        <button class="btn-view" onclick="viewDetailedAnalysis({{ analysis.id }})">Voir</button>
                    </td>
                </tr>
                {% endfor %}
                {% if not latest_analyses %}
                <tr>
                    <td colspan="5" style="text-align: center; padding: 40px; color: var(--text-muted);">
                        Aucune analyse trouvée. Commencez par uploader un CV.
                    </td>
                </tr>
                {% endif %}
            </tbody>
        </table>
    </div>
</div>

<!-- 4. Bottom Section: Skills & Insights Grid -->
<div class="pro-bottom-grid">
    <!-- Top Skills Card -->
    <div class="pro-card insights-card">
        <div class="card-head">
            <h3>🎯 Compétences Clés</h3>
        </div>
        <div class="skills-list">
            <div class="skill-item">
                <span class="skill-name">Machine Learning</span>
                <span class="skill-bar">
                    <span class="skill-fill" style="width: 92%"></span>
                </span>
                <span class="skill-pct">92%</span>
            </div>
            <div class="skill-item">
                <span class="skill-name">Python</span>
                <span class="skill-bar">
                    <span class="skill-fill" style="width: 88%"></span>
                </span>
                <span class="skill-pct">88%</span>
            </div>
            <div class="skill-item">
                <span class="skill-name">Data Analysis</span>
                <span class="skill-bar">
                    <span class="skill-fill" style="width: 85%"></span>
                </span>
                <span class="skill-pct">85%</span>
            </div>
            <div class="skill-item">
                <span class="skill-name">Cloud Computing</span>
                <span class="skill-bar">
                    <span class="skill-fill" style="width: 78%"></span>
                </span>
                <span class="skill-pct">78%</span>
            </div>
        </div>
    </div>

    <!-- Recommendations Card -->
    <div class="pro-card insights-card">
        <div class="card-head">
            <h3>💡 Recommandations IA</h3>
        </div>
        <div class="recommendations-list">
            <div class="rec-item">
                <span class="rec-icon">📝</span>
                <div class="rec-content">
                    <p class="rec-title">Mettre à jour les points forts</p>
                    <span class="rec-desc">Ajoutez 3-5 projets récents</span>
                </div>
                <span class="rec-arrow">→</span>
            </div>
            <div class="rec-item">
                <span class="rec-icon">🎓</span>
                <div class="rec-content">
                    <p class="rec-title">Certifications recommandées</p>
                    <span class="rec-desc">AWS Architect, GCP Professional</span>
                </div>
                <span class="rec-arrow">→</span>
            </div>
            <div class="rec-item">
                <span class="rec-icon">🌐</span>
                <div class="rec-content">
                    <p class="rec-title">Améliorer la visibilité Online</p>
                    <span class="rec-desc">Créer un portfolio professionnel</span>
                </div>
                <span class="rec-arrow">→</span>
            </div>
        </div>
    </div>

    <!-- Job Alerts Card -->
    <div class="pro-card insights-card">
        <div class="card-head">
            <h3>🔔 Offres Correspondantes</h3>
        </div>
        <div class="job-alerts">
            <!-- Rempli dynamiquement par JavaScript -->
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    document.addEventListener('DOMContentLoaded', () => {
        // Linear Performance Chart
        const lineOptions = {
            series: [{
                name: 'Score de Performance',
                data: {{ weekly_values | tojson }}
            }],
            chart: {
                type: 'area',
                height: 300,
                toolbar: { show: false },
                animations: {
                    enabled: true,
                    easing: 'easeinout',
                    speed: 800,
                },
                background: 'transparent',
                foreColor: '#94a3b8'
            },
            dataLabels: { enabled: false },
            stroke: {
                curve: 'smooth',
                width: 3,
                colors: ['#6366f1']
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    opacityFrom: 0.45,
                    opacityTo: 0.05,
                    stops: [20, 100],
                    colorStops: [
                        { offset: 0, color: "#6366f1", opacity: 0.4 },
                        { offset: 100, color: "#6366f1", opacity: 0.01 }
                    ]
                }
            },
            grid: {
                borderColor: 'rgba(255, 255, 255, 0.05)',
                strokeDashArray: 4,
            },
            xaxis: {
                categories: {{ weekly_labels | tojson }},
                axisBorder: { show: false },
                axisTicks: { show: false }
            },
            yaxis: {
                min: 0,
                max: 100,
                tickAmount: 5
            },
            theme: { mode: 'dark' },
            tooltip: {
                theme: 'dark',
                x: { show: true },
                marker: { show: true }
            }
        };

        const mainChart = new ApexCharts(document.querySelector("#v3-main-chart-apex"), lineOptions);
        mainChart.render();

        // Distribution Donut Chart
        const donutOptions = {
            series: [{{ dist.high }}, {{ dist.medium }}, {{ dist.low }}],
            chart: {
                type: 'donut',
                height: 250,
                animations: { enabled: true }
            },
            labels: ['Match Élevé (>=70%)', 'Match Moyen (50-69%)', 'Match Faible (<50%)'],
            colors: ['#10b981', '#f59e0b', '#ef4444'],
            plotOptions: {
                pie: {
                    donut: {
                        size: '70%',
                        labels: {
                            show: true,
                            total: {
                                show: true,
                                label: 'Total',
                                color: '#94a3b8',
                                formatter: function (w) {
                                    return w.globals.seriesTotals.reduce((a, b) => a + b, 0)
                                }
                            }
                        }
                    }
                }
            },
            dataLabels: { enabled: false },
            legend: {
                position: 'bottom',
                offsetY: 0,
                labels: { colors: '#94a3b8' }
            },
            stroke: { show: false },
            theme: { mode: 'dark' }
        };

        const distChart = new ApexCharts(document.querySelector("#v3-dist-chart-apex"), donutOptions);
        distChart.render();
    });
</script>
{% endblock %}
'@

$dashboardContent | Out-File -FilePath "c:\Users\DataVista\Desktop\jobmaths\flask_app\templates\dashboard.html" -Encoding utf8 -Force
