// Dashboard JavaScript
let trendsChart, distributionChart, comparisonChart;
let playersData = [];
let currentSection = 'dashboard';

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

async function initializeDashboard() {
    showLoading(true);
    try {
        await loadPlayersData();
        await updateDashboardMetrics();
        await updateAnalytics();
        initializeCharts();
        showSection('dashboard');
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        showError('Failed to initialize dashboard');
    } finally {
        showLoading(false);
    }
}

// Section Management
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => section.style.display = 'none');
    
    // Show selected section
    document.getElementById(sectionName + '-section').style.display = 'block';
    
    // Update navigation
    updateNavigation(sectionName);
    currentSection = sectionName;
    
    // Load section-specific data
    switch(sectionName) {
        case 'players':
            loadPlayersTable();
            break;
        case 'analytics':
            updateAnalytics();
            break;
        case 'leaderboard':
            updateLeaderboard();
            break;
    }
}

function updateNavigation(activeSection) {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => link.classList.remove('active'));
    
    // Find and activate the current section link
    navLinks.forEach(link => {
        if (link.getAttribute('href') === '#' + activeSection) {
            link.classList.add('active');
        }
    });
}

// Data Loading Functions
async function loadPlayersData() {
    try {
        const response = await fetch('/api/players');
        if (!response.ok) throw new Error('Failed to load players');
        playersData = await response.json();
        return playersData;
    } catch (error) {
        console.error('Error loading players:', error);
        return [];
    }
}

async function updateDashboardMetrics() {
    try {
        const analytics = await fetchAnalytics('week');
        
        // Update KPI cards
        document.getElementById('total-players').textContent = playersData.length;
        document.getElementById('total-games').textContent = analytics.total_games || 0;
        document.getElementById('avg-score').textContent = analytics.average_score || '0.0';
        document.getElementById('avg-efficiency').textContent = analytics.average_efficiency || '0.0';
        
        // Update top performers
        updateTopPerformers(analytics.top_performers || []);
        
        // Add animation effect
        const kpiCards = document.querySelectorAll('.card h3');
        kpiCards.forEach(card => {
            card.classList.add('data-update');
            setTimeout(() => card.classList.remove('data-update'), 500);
        });
        
    } catch (error) {
        console.error('Error updating dashboard metrics:', error);
    }
}

async function fetchAnalytics(period = 'week') {
    try {
        const response = await fetch(`/api/analytics/performance?period=${period}`);
        if (!response.ok) throw new Error('Failed to fetch analytics');
        return await response.json();
    } catch (error) {
        console.error('Error fetching analytics:', error);
        return {};
    }
}

function updateTopPerformers(performers) {
    const container = document.getElementById('top-performers-list');
    if (!performers || performers.length === 0) {
        container.innerHTML = '<p class="text-muted">No performance data available</p>';
        return;
    }
    
    container.innerHTML = performers.slice(0, 5).map((performer, index) => `
        <div class="top-performer-item">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <div class="top-performer-name">${performer.player_name}</div>
                    <div class="top-performer-stats">
                        Score: ${performer.average_score} | 
                        Efficiency: ${performer.average_efficiency}
                    </div>
                </div>
                <div class="leaderboard-rank rank-${index + 1}">#${index + 1}</div>
            </div>
        </div>
    `).join('');
}

// Players Management
function loadPlayersTable() {
    const tbody = document.getElementById('players-tbody');
    if (playersData.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No players found</td></tr>';
        return;
    }
    
    tbody.innerHTML = playersData.map(player => `
        <tr>
            <td>
                <strong>${player.name}</strong>
                <span class="status-indicator status-active"></span>
            </td>
            <td><span class="badge bg-secondary">${player.position}</span></td>
            <td>${player.team}</td>
            <td>${player.age || 'N/A'}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary" onclick="viewPlayerDetails('${player.id}')">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-outline-success" onclick="addPlayerStats('${player.id}')">
                    <i class="fas fa-plus"></i> Stats
                </button>
            </td>
        </tr>
    `).join('');
}

async function addPlayer() {
    const playerData = {
        name: document.getElementById('playerName').value,
        position: document.getElementById('playerPosition').value,
        team: document.getElementById('playerTeam').value,
        age: parseInt(document.getElementById('playerAge').value) || null
    };
    
    if (!playerData.name || !playerData.position || !playerData.team) {
        showError('Please fill in all required fields');
        return;
    }
    
    try {
        showLoading(true);
        const response = await fetch('/api/players', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(playerData)
        });
        
        if (!response.ok) throw new Error('Failed to add player');
        
        // Close modal and refresh data
        const modal = bootstrap.Modal.getInstance(document.getElementById('addPlayerModal'));
        modal.hide();
        document.getElementById('addPlayerForm').reset();
        
        await loadPlayersData();
        loadPlayersTable();
        await updateDashboardMetrics();
        
        showSuccess('Player added successfully!');
        
    } catch (error) {
        console.error('Error adding player:', error);
        showError('Failed to add player');
    } finally {
        showLoading(false);
    }
}

// Analytics Functions
async function updateAnalytics() {
    const period = document.getElementById('time-period-select')?.value || 'week';
    
    try {
        showLoading(true);
        const analytics = await fetchAnalytics(period);
        
        // Update trends chart
        if (trendsChart) {
            await updateTrendsChart();
        }
        
        // Update distribution chart
        if (distributionChart) {
            updateDistributionChart(analytics);
        }
        
        // Update comparison chart
        if (comparisonChart) {
            updateComparisonChart();
        }
        
    } catch (error) {
        console.error('Error updating analytics:', error);
        showError('Failed to update analytics');
    } finally {
        showLoading(false);
    }
}

// Leaderboard Functions
async function updateLeaderboard() {
    const metric = document.getElementById('leaderboard-metric')?.value || 'score';
    
    try {
        showLoading(true);
        const response = await fetch(`/api/analytics/leaderboard?metric=${metric}&limit=10`);
        if (!response.ok) throw new Error('Failed to fetch leaderboard');
        
        const leaderboard = await response.json();
        displayLeaderboard(leaderboard);
        
    } catch (error) {
        console.error('Error updating leaderboard:', error);
        showError('Failed to update leaderboard');
    } finally {
        showLoading(false);
    }
}

function displayLeaderboard(leaderboard) {
    const container = document.getElementById('leaderboard-content');
    
    if (!leaderboard || leaderboard.length === 0) {
        container.innerHTML = '<p class="text-center text-muted">No leaderboard data available</p>';
        return;
    }
    
    container.innerHTML = leaderboard.map(player => `
        <div class="leaderboard-item d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
                <div class="leaderboard-rank rank-${player.rank} me-3">#${player.rank}</div>
                <div>
                    <h6 class="mb-1">${player.player_name}</h6>
                    <small class="text-muted">${player.team} • ${player.position}</small>
                </div>
            </div>
            <div class="text-end">
                <div class="h5 mb-0">${player.value}</div>
                <small class="text-muted">${player.games_played} games</small>
            </div>
        </div>
    `).join('');
}

// Chart Functions
function initializeCharts() {
    initializeTrendsChart();
    initializeDistributionChart();
    initializeComparisonChart();
}

function initializeTrendsChart() {
    const ctx = document.getElementById('trendsChart');
    if (!ctx) return;
    
    trendsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Average Score',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }, {
                label: 'Efficiency Rating',
                data: [],
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
}

function initializeDistributionChart() {
    const ctx = document.getElementById('distributionChart');
    if (!ctx) return;
    
    distributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Excellent', 'Good', 'Average', 'Below Average'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',
                    'rgba(23, 162, 184, 0.8)',
                    'rgba(255, 193, 7, 0.8)',
                    'rgba(220, 53, 69, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function initializeComparisonChart() {
    const ctx = document.getElementById('comparisonChart');
    if (!ctx) return;
    
    comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Score',
                data: [],
                backgroundColor: 'rgba(102, 126, 234, 0.8)'
            }, {
                label: 'Assists',
                data: [],
                backgroundColor: 'rgba(86, 171, 47, 0.8)'
            }, {
                label: 'Rebounds',
                data: [],
                backgroundColor: 'rgba(240, 147, 251, 0.8)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function updateTrendsChart() {
    try {
        const response = await fetch('/api/analytics/trends');
        if (!response.ok) return;
        
        const data = await response.json();
        const trends = data.trends || [];
        
        if (trends.length === 0) return;
        
        trendsChart.data.labels = trends.map(t => t.week);
        trendsChart.data.datasets[0].data = trends.map(t => t.average_score);
        trendsChart.data.datasets[1].data = trends.map(t => t.average_efficiency);
        trendsChart.update();
        
    } catch (error) {
        console.error('Error updating trends chart:', error);
    }
}

function updateDistributionChart(analytics) {
    // Mock data for distribution - in real app, this would come from analytics
    const mockDistribution = [25, 35, 30, 10];
    distributionChart.data.datasets[0].data = mockDistribution;
    distributionChart.update();
}

function updateComparisonChart() {
    // Mock data for comparison - in real app, this would show top players comparison
    const topPlayers = playersData.slice(0, 5);
    comparisonChart.data.labels = topPlayers.map(p => p.name);
    comparisonChart.data.datasets[0].data = topPlayers.map(() => Math.floor(Math.random() * 30) + 10);
    comparisonChart.data.datasets[1].data = topPlayers.map(() => Math.floor(Math.random() * 15) + 5);
    comparisonChart.data.datasets[2].data = topPlayers.map(() => Math.floor(Math.random() * 20) + 5);
    comparisonChart.update();
}

// Utility Functions
function showLoading(show) {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = show ? 'flex' : 'none';
    }
}

function showSuccess(message) {
    // Create toast notification
    const toast = createToast(message, 'success');
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function showError(message) {
    // Create toast notification
    const toast = createToast(message, 'error');
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function createToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 10000; min-width: 300px;';
    toast.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <span>${message}</span>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    return toast;
}

// Placeholder functions for future implementation
function viewPlayerDetails(playerId) {
    showSuccess(`Viewing details for player ${playerId} - Feature coming soon!`);
}

function addPlayerStats(playerId) {
    showSuccess(`Adding stats for player ${playerId} - Feature coming soon!`);
}