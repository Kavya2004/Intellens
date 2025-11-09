/**
 * Cost Estimator Visualization Component
 * Displays projected monthly and yearly costs for detected services
 */

class CostEstimatorRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.costData = null;
    }

    render(costEstimates) {
        if (!costEstimates || !costEstimates.service_estimates) {
            this.container.innerHTML = '<p>No cost data available</p>';
            return;
        }

        this.costData = costEstimates;
        this.container.innerHTML = this.generateHTML();
        this.addInteractivity();
    }

    generateHTML() {
        const { service_estimates, total_costs, cost_breakdown, recommendations } = this.costData;

        return `
            <div class="cost-estimator-container">
                <div class="cost-header">
                    <h2>💰 Project Cost Estimation</h2>
                    <div class="cost-summary">
                        <div class="cost-card total-cost">
                            <h3>Total Estimated Costs</h3>
                            <div class="cost-range">
                                <div class="monthly">
                                    <span class="label">Monthly:</span>
                                    <span class="amount">${total_costs.monthly_range}</span>
                                </div>
                                <div class="yearly">
                                    <span class="label">Yearly:</span>
                                    <span class="amount">${total_costs.yearly_range}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="cost-breakdown-section">
                    <h3>📊 Cost Breakdown by Category</h3>
                    <div class="breakdown-cards">
                        <div class="breakdown-card">
                            <div class="category-icon">☁️</div>
                            <div class="category-info">
                                <h4>Infrastructure</h4>
                                <span class="category-cost">$${cost_breakdown.infrastructure.toFixed(0)}/month</span>
                            </div>
                        </div>
                        <div class="breakdown-card">
                            <div class="category-icon">🗄️</div>
                            <div class="category-info">
                                <h4>Databases</h4>
                                <span class="category-cost">$${cost_breakdown.databases.toFixed(0)}/month</span>
                            </div>
                        </div>
                        <div class="breakdown-card">
                            <div class="category-icon">⚡</div>
                            <div class="category-info">
                                <h4>Frameworks</h4>
                                <span class="category-cost">$${cost_breakdown.frameworks.toFixed(0)}/month</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="services-cost-section">
                    <h3>🔧 Service-by-Service Costs</h3>
                    <div class="services-grid">
                        ${service_estimates.map(service => this.generateServiceCard(service)).join('')}
                    </div>
                </div>

                <div class="recommendations-section">
                    <h3>💡 Cost Optimization Recommendations</h3>
                    <div class="recommendations-list">
                        ${recommendations.map(rec => `
                            <div class="recommendation-item">
                                <span class="rec-icon">💡</span>
                                <span class="rec-text">${rec}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <div class="cost-disclaimer">
                    <p><strong>Disclaimer:</strong> These are estimated costs based on typical usage patterns. 
                    Actual costs may vary significantly based on your specific usage, region, and pricing changes. 
                    Always refer to the official pricing calculators for accurate estimates.</p>
                </div>
            </div>

            <style>
                .cost-estimator-container {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    color: white;
                }

                .cost-header h2 {
                    text-align: center;
                    margin-bottom: 20px;
                    font-size: 2.2em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }

                .cost-summary {
                    display: flex;
                    justify-content: center;
                    margin-bottom: 30px;
                }

                .cost-card {
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    padding: 25px;
                    text-align: center;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }

                .total-cost h3 {
                    margin-bottom: 15px;
                    font-size: 1.3em;
                }

                .cost-range {
                    display: flex;
                    gap: 30px;
                    justify-content: center;
                }

                .monthly, .yearly {
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                }

                .label {
                    font-size: 0.9em;
                    opacity: 0.8;
                }

                .amount {
                    font-size: 1.4em;
                    font-weight: bold;
                    color: #FFD700;
                }

                .cost-breakdown-section, .services-cost-section, .recommendations-section {
                    margin: 30px 0;
                }

                .cost-breakdown-section h3, .services-cost-section h3, .recommendations-section h3 {
                    margin-bottom: 20px;
                    font-size: 1.4em;
                }

                .breakdown-cards {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin-bottom: 20px;
                }

                .breakdown-card {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 20px;
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }

                .category-icon {
                    font-size: 2em;
                }

                .category-info h4 {
                    margin: 0 0 5px 0;
                    font-size: 1.1em;
                }

                .category-cost {
                    color: #FFD700;
                    font-weight: bold;
                }

                .services-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 15px;
                }

                .service-card {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    padding: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    transition: transform 0.2s, box-shadow 0.2s;
                }

                .service-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
                }

                .service-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 10px;
                }

                .service-name {
                    font-weight: bold;
                    font-size: 1.1em;
                }

                .usage-badge {
                    background: rgba(255, 215, 0, 0.2);
                    color: #FFD700;
                    padding: 2px 8px;
                    border-radius: 12px;
                    font-size: 0.8em;
                }

                .service-costs {
                    display: flex;
                    justify-content: space-between;
                    margin: 10px 0;
                }

                .cost-item {
                    text-align: center;
                }

                .cost-label {
                    font-size: 0.8em;
                    opacity: 0.8;
                    display: block;
                }

                .cost-value {
                    font-weight: bold;
                    color: #FFD700;
                }

                .service-assumptions {
                    font-size: 0.8em;
                    opacity: 0.7;
                    margin-top: 10px;
                    font-style: italic;
                }

                .recommendations-list {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }

                .recommendation-item {
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    padding: 15px;
                    display: flex;
                    align-items: flex-start;
                    gap: 10px;
                    border-left: 3px solid #FFD700;
                }

                .rec-icon {
                    font-size: 1.2em;
                    margin-top: 2px;
                }

                .rec-text {
                    flex: 1;
                    line-height: 1.4;
                }

                .cost-disclaimer {
                    margin-top: 30px;
                    padding: 20px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    border-left: 4px solid #FFD700;
                }

                .cost-disclaimer p {
                    margin: 0;
                    font-size: 0.9em;
                    line-height: 1.5;
                }

                @media (max-width: 768px) {
                    .cost-range {
                        flex-direction: column;
                        gap: 15px;
                    }
                    
                    .breakdown-cards {
                        grid-template-columns: 1fr;
                    }
                    
                    .services-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        `;
    }

    generateServiceCard(service) {
        return `
            <div class="service-card" data-service="${service.service}">
                <div class="service-header">
                    <span class="service-name">${service.service}</span>
                    <span class="usage-badge">${service.usage_detected}x detected</span>
                </div>
                <div class="service-costs">
                    <div class="cost-item">
                        <span class="cost-label">Monthly</span>
                        <span class="cost-value">${service.monthly_cost_range}</span>
                    </div>
                    <div class="cost-item">
                        <span class="cost-label">Yearly</span>
                        <span class="cost-value">${service.yearly_cost_range}</span>
                    </div>
                </div>
                <div class="service-assumptions">
                    <strong>Assumptions:</strong> ${service.assumptions}
                </div>
            </div>
        `;
    }

    addInteractivity() {
        // Add click handlers for service cards
        const serviceCards = this.container.querySelectorAll('.service-card');
        serviceCards.forEach(card => {
            card.addEventListener('click', () => {
                const serviceName = card.dataset.service;
                this.showServiceDetails(serviceName);
            });
        });
    }

    showServiceDetails(serviceName) {
        const service = this.costData.service_estimates.find(s => s.service === serviceName);
        if (!service) return;

        alert(`${serviceName} Details:
        
Monthly Cost: ${service.monthly_cost_range}
Yearly Cost: ${service.yearly_cost_range}
Usage Detected: ${service.usage_detected} times
Assumptions: ${service.assumptions}

Note: These are estimates based on typical usage patterns. Actual costs may vary.`);
    }
}

// Export for use in other modules
window.CostEstimatorRenderer = CostEstimatorRenderer;