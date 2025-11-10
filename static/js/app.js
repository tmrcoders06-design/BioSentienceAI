// BioSentience Frontend Application

let currentData = null;
let currentResults = null;
let simulationChart = null;

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const useSampleBtn = document.getElementById('useSampleBtn');
const previewSection = document.getElementById('previewSection');
const dataPreview = document.getElementById('dataPreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const resultsSection = document.getElementById('resultsSection');
const simulationSection = document.getElementById('simulationSection');
const varyFeature = document.getElementById('varyFeature');
const variationRange = document.getElementById('variationRange');
const rangeDisplay = document.getElementById('rangeDisplay');
const runSimBtn = document.getElementById('runSimBtn');
const simulationResults = document.getElementById('simulationResults');
const downloadBtn = document.getElementById('downloadBtn');

// Upload area click handler
uploadArea.addEventListener('click', () => fileInput.click());

// File upload handler
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        showLoading('Uploading and validating data...');
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        displayPreview(data);
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Upload Error: ' + error.message);
    }
});

// Use sample data
useSampleBtn.addEventListener('click', async () => {
    try {
        showLoading('Loading sample data...');
        const response = await fetch('/api/sample-data');
        const result = await response.json();
        
        currentData = result.data;
        displaySamplePreview(result);
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Error loading sample data: ' + error.message);
    }
});

// Analyze button
analyzeBtn.addEventListener('click', async () => {
    try {
        showLoading('Analyzing biological data...');
        
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: currentData })
        });
        
        const results = await response.json();
        
        if (!response.ok) {
            throw new Error(results.error || 'Analysis failed');
        }
        
        currentResults = results;
        displayResults(results);
        setupSimulation(results);
        hideLoading();
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        hideLoading();
        showError('Analysis Error: ' + error.message);
    }
});

// Variation range slider
variationRange.addEventListener('input', (e) => {
    rangeDisplay.textContent = e.target.value;
});

// Run simulation
runSimBtn.addEventListener('click', async () => {
    const feature = varyFeature.value;
    if (!feature) {
        showError('Please select a feature to vary');
        return;
    }
    
    try {
        showLoading('Running simulation...');
        
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                base_features: currentData,
                vary_feature: feature,
                steps: 15,
                variation_range: parseFloat(variationRange.value) / 100
            })
        });
        
        const simData = await response.json();
        
        if (!response.ok) {
            throw new Error(simData.error || 'Simulation failed');
        }
        
        displaySimulation(simData);
        hideLoading();
    } catch (error) {
        hideLoading();
        showError('Simulation Error: ' + error.message);
    }
});

// Download report
downloadBtn.addEventListener('click', () => {
    if (!currentResults) return;
    
    const report = {
        timestamp: new Date().toISOString(),
        analysis: currentResults,
        input_data: currentData
    };
    
    const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `biosentience_report_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
});

// Display functions
function displayPreview(data) {
    const table = `
        <table>
            <thead>
                <tr>
                    ${data.columns.map(col => `<th>${col}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
                ${data.preview_data.slice(0, 5).map(row => `
                    <tr>
                        ${data.columns.map(col => `<td>${row[col]}</td>`).join('')}
                    </tr>
                `).join('')}
            </tbody>
        </table>
        <p style="margin-top: 1rem; color: var(--text-secondary);">
            Showing 5 of ${data.rows} rows | ${data.columns.length} columns
        </p>
    `;
    
    dataPreview.innerHTML = table;
    previewSection.classList.remove('hidden');
    
    // Store first row as current data
    currentData = data.preview_data[0];
}

function displaySamplePreview(result) {
    const data = result.data;
    const table = `
        <div style="background: rgba(0, 245, 255, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            📋 ${result.note}
        </div>
        <table>
            <thead>
                <tr>
                    <th>Feature</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                ${Object.entries(data).map(([key, value]) => `
                    <tr>
                        <td>${key.replace(/_/g, ' ').toUpperCase()}</td>
                        <td>${typeof value === 'number' ? value.toFixed(2) : value}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    
    dataPreview.innerHTML = table;
    previewSection.classList.remove('hidden');
}

function displayResults(results) {
    // Update metric values
    document.getElementById('healthValue').textContent = results.predictions.health_index.toFixed(2);
    document.getElementById('riskValue').textContent = results.predictions.mutation_risk.toFixed(2);
    document.getElementById('adaptationValue').textContent = results.predictions.adaptation_score.toFixed(2);
    
    // Update confidence
    document.getElementById('healthConfidence').textContent = (results.confidence.health_index * 100).toFixed(1) + '%';
    document.getElementById('riskConfidence').textContent = (results.confidence.mutation_risk * 100).toFixed(1) + '%';
    document.getElementById('adaptationConfidence').textContent = (results.confidence.adaptation_score * 100).toFixed(1) + '%';
    
    // Update progress bars
    document.getElementById('healthBar').style.width = (results.predictions.health_index * 100) + '%';
    document.getElementById('riskBar').style.width = (results.predictions.mutation_risk * 100) + '%';
    document.getElementById('adaptationBar').style.width = (results.predictions.adaptation_score * 100) + '%';
    
    // Update explanation
    document.getElementById('explanationSummary').textContent = results.explanation.summary;
    
    // Display feature importance
    const featureList = document.getElementById('featureList');
    featureList.innerHTML = '';
    
    results.explanation.health_index.forEach(feat => {
        const item = document.createElement('div');
        item.className = 'feature-item';
        item.innerHTML = `
            <span class="feature-name">${feat.feature}</span>
            <span class="feature-badge ${feat.impact}">${feat.impact.toUpperCase()}</span>
        `;
        featureList.appendChild(item);
    });
    
    // Show results section
    resultsSection.classList.remove('hidden');
}

function setupSimulation(results) {
    // Populate feature dropdown
    varyFeature.innerHTML = '<option value="">Select a feature...</option>';
    
    Object.keys(results.input_features).forEach(feature => {
        const option = document.createElement('option');
        option.value = feature;
        option.textContent = feature.replace(/_/g, ' ').toUpperCase();
        varyFeature.appendChild(option);
    });
    
    simulationSection.classList.remove('hidden');
}

function displaySimulation(simData) {
    simulationResults.classList.remove('hidden');
    
    // Prepare chart data
    const labels = simData.trajectory.map(t => t[simData.varied_feature].toFixed(2));
    const healthData = simData.trajectory.map(t => t.health_index);
    const riskData = simData.trajectory.map(t => t.mutation_risk);
    const adaptationData = simData.trajectory.map(t => t.adaptation_score);
    
    // Destroy existing chart
    if (simulationChart) {
        simulationChart.destroy();
    }
    
    // Create new chart
    const ctx = document.getElementById('simulationChart').getContext('2d');
    simulationChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Health Index',
                    data: healthData,
                    borderColor: 'rgb(6, 255, 165)',
                    backgroundColor: 'rgba(6, 255, 165, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Mutation Risk',
                    data: riskData,
                    borderColor: 'rgb(255, 0, 110)',
                    backgroundColor: 'rgba(255, 0, 110, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Adaptation Score',
                    data: adaptationData,
                    borderColor: 'rgb(131, 56, 236)',
                    backgroundColor: 'rgba(131, 56, 236, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#ffffff' }
                },
                title: {
                    display: true,
                    text: `Impact of ${simData.varied_feature.replace(/_/g, ' ').toUpperCase()} Variation`,
                    color: '#00f5ff',
                    font: { size: 16 }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: simData.varied_feature.replace(/_/g, ' ').toUpperCase(),
                        color: '#a0a0b0'
                    },
                    ticks: { color: '#a0a0b0' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Prediction Value',
                        color: '#a0a0b0'
                    },
                    ticks: { color: '#a0a0b0' },
                    grid: { color: 'rgba(255, 255, 255, 0.1)' },
                    min: 0,
                    max: 1
                }
            }
        }
    });
    
    // Set canvas height
    document.getElementById('simulationChart').style.height = '400px';
}

// Utility functions
function showLoading(message) {
    // Simple loading indicator
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        color: white;
        font-size: 1.5rem;
    `;
    overlay.innerHTML = `<div style="text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚗️</div>
        <div>${message}</div>
    </div>`;
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.remove();
}

function showError(message) {
    alert('❌ ' + message);
}
