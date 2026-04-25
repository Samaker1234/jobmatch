$superadminContent = Get-Content -Path "c:\Users\DataVista\Desktop\jobmaths\flask_app\templates\superadmin.html" -Raw
$target = "// --- Init Advanced Charts ---"

# This is a bit complex for a single PowerShell command, but since I have the restored block content, 
# I will just write a specific replacement script for the mangled section.

$mangledToCorrect = @'
    // --- Init Advanced Charts ---
    try {
        let adminMainChart, roleDistChart;
        const chartData = {
            weekly: {
                labels: {{ weekly_labels | tojson }},
                users: {{ weekly_users | tojson }},
                analyses: {{ weekly_analyses | tojson }}
            },
            monthly: {
                labels: {{ monthly_labels | tojson }},
                users: {{ monthly_users | tojson }},
                analyses: {{ monthly_analyses | tojson }}
            }
        };

        function initAdminCharts() {
            // 1. Multi-series Area Chart (Growth)
            const lineOptions = {
                series: [
                    { name: 'Nouveaux Utilisateurs', data: chartData.weekly.users },
                    { name: 'Analyses CV', data: chartData.weekly.analyses }
                ],
                chart: {
                    type: 'area',
                    height: 300,
                    toolbar: { show: false },
                    animations: { enabled: true, easing: 'easeinout', speed: 800 },
                    background: 'transparent',
                    foreColor: '#94a3b8'
                },
                colors: ['#00d2ff', '#9d50bb'],
                dataLabels: { enabled: false },
                stroke: { curve: 'smooth', width: 3 },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shadeIntensity: 1,
                        opacityFrom: 0.4,
                        opacityTo: 0.1,
                        stops: [0, 90, 100]
                    }
                },
                grid: { borderColor: 'rgba(255, 255, 255, 0.05)', strokeDashArray: 4 },
                xaxis: {
                    categories: chartData.weekly.labels,
                    axisBorder: { show: false },
                    axisTicks: { show: false }
                },
                yaxis: { tickAmount: 5 },
                theme: { mode: 'dark' },
                tooltip: { theme: 'dark' }
            };

            adminMainChart = new ApexCharts(document.querySelector("#v3-admin-main-chart"), lineOptions);
            adminMainChart.render();

            // 2. Role Distribution Donut Chart
            const donutOptions = {
                series: [{{ user_distribution.admins }}, {{ user_distribution.users }}],
                chart: {
                    type: 'donut',
                    height: 300,
                    animations: { enabled: true }
                },
                labels: ['Administrateurs', 'Utilisateurs Standards'],
                colors: ['#00d2ff', '#6366f1'],
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
                legend: { position: 'bottom', labels: { colors: '#94a3b8' } },
                stroke: { show: false },
                theme: { mode: 'dark' }
            };

            roleDistChart = new ApexCharts(document.querySelector("#v3-role-dist-chart"), donutOptions);
            roleDistChart.render();
        }

        function toggleChart(type) {
            const btnWeekly = document.getElementById('btnWeekly');
            const btnMonthly = document.getElementById('btnMonthly');
            if (!btnWeekly || !btnMonthly || !adminMainChart) return;

            if (type === 'weekly') {
                btnWeekly.classList.add('active');
                btnMonthly.classList.remove('active');
                adminMainChart.updateSeries([
                    { name: 'Nouveaux Utilisateurs', data: chartData.weekly.users },
                    { name: 'Analyses CV', data: chartData.weekly.analyses }
                ]);
                adminMainChart.updateOptions({ xaxis: { categories: chartData.weekly.labels } });
            } else {
                btnMonthly.classList.add('active');
                btnWeekly.classList.remove('active');
                adminMainChart.updateSeries([
                    { name: 'Nouveaux Utilisateurs', data: chartData.monthly.users },
                    { name: 'Analyses CV', data: chartData.monthly.analyses }
                ]);
                adminMainChart.updateOptions({ xaxis: { categories: chartData.monthly.labels } });
            }
        }
        window.toggleChart = toggleChart;
        window.initCharts = initAdminCharts;
    } catch (err) {
        console.error("Critical Error initializing SuperAdmin JS:", err);
    }
'@

# This is risky without knowing the exact current state of the file, 
# so I will just overwrite the entire superadmin.html by reading it and replacing the section.
# But superadmin.html is too large to handle easily in a script variable.

# I will try replace_file_content once more now that the lock is gone.
