// AWS Infrastructure Designer - Interactive diagram renderer
class AWSInfrastructureDesigner {
    constructor(container, diagramData) {
        this.container = container;
        this.data = diagramData;
        this.selectedService = null;
        this.init();
    }

    init() {
        this.container.innerHTML = '';
        this.container.className = 'aws-infrastructure-designer';
        
        console.log('AWS Designer Init - Data:', this.data);
        console.log('Canvas Services:', this.data.canvas?.services?.length || 0);
        
        if (!this.data.canvas || !this.data.canvas.services || this.data.canvas.services.length === 0) {
            console.log('Rendering empty state - no services found');
            this.renderEmptyState();
            return;
        }
        
        console.log('Rendering full diagram');
        this.render();
    }

    renderEmptyState() {
        // If we have summary data, show it instead of empty state
        if (this.data.summary && this.data.summary.total_services > 0) {
            this.container.innerHTML = `
                <div style="padding: 20px; text-align: center;">
                    <h3>Infrastructure Analysis Complete</h3>
                    <p>Generated ${this.data.summary.total_services} AWS services for your project:</p>
                    <div style="margin: 20px 0; display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
                        ${this.data.summary.service_types.map(service => 
                            `<span style="background: #e3f2fd; color: #1976d2; padding: 5px 10px; border-radius: 15px; font-size: 12px;">${service}</span>`
                        ).join('')}
                    </div>
                    <p style="color: #666; font-size: 14px;">Click on services above to view Terraform configuration.</p>
                </div>
            `;
        } else {
            this.container.innerHTML = `
                <div style="
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    height: 400px;
                    background: #f8f9fa;
                    border: 2px dashed #dee2e6;
                    border-radius: 8px;
                    flex-direction: column;
                    color: #6c757d;
                ">
                    <div style="font-size: 48px; margin-bottom: 20px;">🔧</div>
                    <h3 style="margin: 0 0 10px 0;">Generating Infrastructure</h3>
                    <p style="margin: 0; text-align: center; max-width: 400px;">
                        ${this.data.canvas?.message || 'Analyzing your project to recommend appropriate AWS infrastructure based on detected languages and services.'}
                    </p>
                </div>
            `;
        }
    }

    render() {
        const designerHTML = `
            <div class="aws-designer">
                ${this.renderSidebar()}
                ${this.renderCanvas()}
                ${this.renderPanel()}
            </div>
        `;
        
        this.container.innerHTML = designerHTML;
        this.attachEventListeners();
        
        // Select first service by default
        if (this.data.canvas.services.length > 0) {
            this.selectService(this.data.canvas.services[0]);
        }
    }

    renderSidebar() {
        // Get services from canvas.services directly
        const allServices = this.data.canvas?.services || [];
        
        // Group by category
        const servicesByCategory = {};
        allServices.forEach(service => {
            const category = service.category || 'Other';
            if (!servicesByCategory[category]) {
                servicesByCategory[category] = [];
            }
            servicesByCategory[category].push(service);
        });
        
        if (Object.keys(servicesByCategory).length === 0) {
            return `
                <div class="designer-sidebar">
                    <div class="category-header">No Services</div>
                    <p style="padding: 20px; color: #666; font-size: 12px;">No services detected in this project.</p>
                </div>
            `;
        }
        
        return `
            <div class="designer-sidebar">
                <div class="sidebar-toggle" onclick="this.parentElement.classList.toggle('collapsed')">
                    <span class="toggle-icon">◀</span>
                </div>
                <div class="sidebar-content">
                    <input type="text" class="search-input" placeholder="Search services..." />
                    
                    <div class="category-header">Project Services</div>
                    
                    ${Object.entries(servicesByCategory).map(([categoryName, services]) => `
                        <div class="service-category">
                            <div class="category-item category-title" data-category="${categoryName}">
                                <span class="category-icon">📁</span>
                                ${categoryName} (${services.length})
                                <span class="expand-icon">▼</span>
                            </div>
                            <div class="category-services" data-category="${categoryName}" style="display: block;">
                                ${services.map(service => `
                                    <div class="category-service" data-service="${service.name}" data-service-id="${service.id}">
                                        <span class="service-icon">${service.icon}</span>
                                        <span class="service-name">${service.name}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }
    
    getCategoryForService(serviceName) {
        const categoryMap = {
            'EC2': 'Compute',
            'Lambda': 'Compute',
            'ECS': 'Compute',
            'EKS': 'Compute',
            'S3': 'Storage',
            'EBS': 'Storage',
            'EFS': 'Storage',
            'DynamoDB': 'Database',
            'RDS': 'Database',
            'ElastiCache': 'Database',
            'VPC': 'Networking',
            'CloudFront': 'Networking',
            'Security Group': 'Security'
        };
        return categoryMap[serviceName] || 'Application';
    }

    renderCanvas() {
        return `
            <div class="designer-canvas">
                <div class="canvas-header">
                    <h3>${this.data.project_name} Infrastructure</h3>
                    <div class="canvas-stats">
                        ${this.data.summary.total_services} services • ${Object.keys(this.data.summary.groups).length} groups
                    </div>
                </div>
                
                <div class="canvas-content-flex">
                    ${this.renderGroupsFlex()}
                </div>
            </div>
        `;
    }

    renderGroups() {
        // Calculate better positions to avoid overlapping
        const groupsWithPositions = this.calculateGroupPositions(this.data.canvas.groups);
        
        return groupsWithPositions.map(group => `
            <div class="service-group" data-group="${group.id}" style="
                position: absolute;
                left: ${group.position.x}px;
                top: ${group.position.y}px;
                min-width: ${group.width}px;
            ">
                <div class="group-title">${group.title}</div>
                <div class="group-border">
                    ${group.services.map(service => this.renderService(service)).join('')}
                </div>
            </div>
        `).join('');
    }

    renderGroupsFlex() {
        const groups = this.data.canvas.groups;
        
        return groups.map(group => `
            <div class="service-group-flex">
                <div class="group-title">${group.title}</div>
                <div class="group-border">
                    ${group.services.map(service => this.renderService(service)).join('')}
                </div>
            </div>
        `).join('');
    }

    renderService(service) {
        const inputs = service.inputs || [];
        const outputs = service.outputs || [];
        
        return `
            <div class="aws-service" data-service-id="${service.id}" data-service-type="${service.name}">
                <div class="service-inputs">
                    ${inputs.map(input => `<div class="input-node" data-input-id="${input.id}">●</div>`).join('')}
                </div>
                <div class="service-content">
                    <div class="service-icon">${service.icon}</div>
                    <div class="service-details">
                        <div class="service-name">${service.name}</div>
                        <div class="service-resource">${service.resource_name}</div>
                    </div>
                </div>
                <div class="service-outputs">
                    ${outputs.map(output => `<div class="output-node" data-output-id="${output.id}">●</div>`).join('')}
                </div>
            </div>
        `;
    }

    renderConnections() {
        return this.data.canvas.connections.map(connection => `
            <div class="service-connection" data-from="${connection.from}" data-to="${connection.to}">
                <div class="connection-line"></div>
                <div class="connection-label">${connection.label}</div>
            </div>
        `).join('');
    }

    renderPanel() {
        const panel = this.data.panel;
        
        return `
            <div class="designer-panel">
                <div class="panel-header">
                    <div class="panel-title">${panel.title}</div>
                    <div class="panel-subtitle">Generated</div>
                </div>
                
                <div class="panel-content">
                    ${this.selectedService ? this.renderServiceDetails(this.selectedService) : this.renderDefaultPanel()}
                </div>
            </div>
        `;
    }

    renderServiceDetails(service) {
        const config = {
            'Resource Name': service.resource_name || 'N/A',
            'Service Type': service.name
        };
        
        // Add service-specific config
        if (service.config) {
            Object.entries(service.config).forEach(([key, value]) => {
                config[key.charAt(0).toUpperCase() + key.slice(1)] = value;
            });
        }
        
        const useCases = service.use_cases || ['General use cases'];
        
        return `
            <div class="service-description">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <span style="font-size: 24px;">${service.icon}</span>
                    <div>
                        <div style="font-weight: bold;">${service.name}</div>
                        <div style="font-size: 12px; color: #666;">${service.resource_name || service.name}</div>
                    </div>
                </div>
                
                <p>${service.description}</p>
            </div>

            <div class="service-configuration">
                <h4>Configuration</h4>
                ${Object.entries(config).map(([key, value]) => `
                    <div class="config-item">
                        <div class="config-label">${key}</div>
                        <div class="config-value">${this.formatConfigValue(value)}</div>
                    </div>
                `).join('')}
            </div>

            <div class="service-features">
                <h4>Common Use Cases</h4>
                <ul>
                    ${useCases.map(use => `<li>${use}</li>`).join('')}
                </ul>
            </div>

            <div class="terraform-preview">
                <h4>Terraform Configuration</h4>
                <pre><code>${service.terraform_config || '# No configuration available'}</code></pre>
            </div>
        `;
    }

    renderDefaultPanel() {
        return `
            <div class="service-description">
                <h4>Infrastructure Overview</h4>
                <p>This diagram shows your AWS infrastructure based on Terraform configuration files.</p>
                
                <div style="margin: 20px 0;">
                    <strong>Services Detected:</strong>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        ${this.data.summary.service_types.map(type => `<li>${type}</li>`).join('')}
                    </ul>
                </div>
                
                <p>Click on any service in the diagram to view detailed configuration and Terraform code.</p>
            </div>
        `;
    }



    formatConfigValue(value) {
        if (typeof value === 'object' && value !== null) {
            return JSON.stringify(value, null, 2);
        }
        return String(value);
    }

    attachEventListeners() {
        // Service selection and drag from canvas
        this.container.querySelectorAll('.aws-service').forEach(serviceEl => {
            let isDragging = false;
            let dragLine = null;
            let startService = null;
            const canvas = this.container.querySelector('.canvas-content-flex');
            
            serviceEl.addEventListener('mousedown', (e) => {
                e.preventDefault();
                isDragging = true;
                startService = serviceEl;
                serviceEl.style.borderColor = '#ffc107';
                
                const canvasRect = canvas.getBoundingClientRect();
                const serviceRect = serviceEl.getBoundingClientRect();
                const startX = serviceRect.left - canvasRect.left + canvas.scrollLeft + serviceRect.width / 2;
                const startY = serviceRect.top - canvasRect.top + canvas.scrollTop + serviceRect.height / 2;
                
                dragLine = document.createElement('div');
                dragLine.style.cssText = `position: absolute; left: ${startX}px; top: ${startY}px; width: 0px; height: 2px; background: #ffc107; transform-origin: left center; pointer-events: none; z-index: 1000;`;
                canvas.appendChild(dragLine);
                
                canvas.addEventListener('mousemove', handleMouseMove);
            });
            
            const handleMouseMove = (e) => {
                if (!isDragging || !dragLine) return;
                
                const canvasRect = canvas.getBoundingClientRect();
                const serviceRect = startService.getBoundingClientRect();
                const startX = serviceRect.left - canvasRect.left + canvas.scrollLeft + serviceRect.width / 2;
                const startY = serviceRect.top - canvasRect.top + canvas.scrollTop + serviceRect.height / 2;
                const endX = e.clientX - canvasRect.left + canvas.scrollLeft;
                const endY = e.clientY - canvasRect.top + canvas.scrollTop;
                
                const length = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
                const angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;
                
                dragLine.style.width = `${length}px`;
                dragLine.style.transform = `rotate(${angle}deg)`;
            };
            
            canvas.addEventListener('mousemove', handleMouseMove);
            
            const handleMouseUp = (e) => {
                if (isDragging) {
                    const targetService = document.elementFromPoint(e.clientX, e.clientY)?.closest('.aws-service');
                    if (targetService && targetService !== startService) {
                        this.createServiceConnection(startService, targetService);
                    }
                    
                    startService.style.borderColor = '#ccc';
                    if (dragLine) dragLine.remove();
                    canvas.removeEventListener('mousemove', handleMouseMove);
                    canvas.removeEventListener('mouseup', handleMouseUp);
                    isDragging = false;
                    dragLine = null;
                    startService = null;
                }
            };
            
            serviceEl.addEventListener('mouseup', (e) => {
                if (!isDragging) {
                    const serviceId = e.currentTarget.dataset.serviceId;
                    const service = this.data.canvas.services.find(s => s.id === serviceId);
                    if (service) {
                        this.selectService(service);
                    }
                }
            });
            
            canvas.addEventListener('mouseup', handleMouseUp);
        });
        
        // Service selection from sidebar
        this.container.querySelectorAll('.category-service').forEach(serviceEl => {
            serviceEl.addEventListener('click', (e) => {
                const serviceId = e.currentTarget.dataset.serviceId;
                if (serviceId) {
                    const service = this.data.canvas.services.find(s => s.id === serviceId);
                    if (service) {
                        this.selectService(service);
                    }
                }
            });
        });

        // Category expansion
        this.container.querySelectorAll('.category-title').forEach(categoryEl => {
            categoryEl.addEventListener('click', (e) => {
                const category = e.currentTarget.dataset.category;
                const servicesEl = this.container.querySelector(`.category-services[data-category="${category}"]`);
                const expandIcon = e.currentTarget.querySelector('.expand-icon');
                
                if (servicesEl.style.display === 'none') {
                    servicesEl.style.display = 'block';
                    expandIcon.textContent = '▼';
                } else {
                    servicesEl.style.display = 'none';
                    expandIcon.textContent = '▶';
                }
            });
        });

        // Search functionality
        const searchInput = this.container.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.filterServices(e.target.value);
            });
        }

        this.attachScrollListener();
    }

    selectService(service) {
        this.selectedService = service;
        
        // Update panel with service details
        const panelContent = this.container.querySelector('.panel-content');
        if (panelContent) {
            panelContent.innerHTML = this.renderServiceDetails(service);
        }
        
        // Update panel header
        const panelTitle = this.container.querySelector('.panel-title');
        if (panelTitle) {
            panelTitle.textContent = `${service.name} Configuration`;
        }
        
        // Highlight selected service
        this.container.querySelectorAll('.aws-service').forEach(el => {
            el.classList.remove('selected');
        });
        
        const selectedEl = this.container.querySelector(`[data-service-id="${service.id}"]`);
        if (selectedEl) {
            selectedEl.classList.add('selected');
        }
    }

    filterServices(searchTerm) {
        const term = searchTerm.toLowerCase();
        
        this.container.querySelectorAll('.category-service').forEach(serviceEl => {
            const serviceName = serviceEl.querySelector('.service-name').textContent.toLowerCase();
            if (serviceName.includes(term)) {
                serviceEl.style.display = 'flex';
            } else {
                serviceEl.style.display = 'none';
            }
        });
    }

    createServiceConnection(fromService, toService) {
        const canvas = this.container.querySelector('.canvas-content-flex');
        const canvasRect = canvas.getBoundingClientRect();
        
        const fromRect = fromService.getBoundingClientRect();
        const toRect = toService.getBoundingClientRect();
        
        const startX = fromRect.left - canvasRect.left + canvas.scrollLeft + fromRect.width / 2;
        const startY = fromRect.top - canvasRect.top + canvas.scrollTop + fromRect.height / 2;
        const endX = toRect.left - canvasRect.left + canvas.scrollLeft + toRect.width / 2;
        const endY = toRect.top - canvasRect.top + canvas.scrollTop + toRect.height / 2;
        
        const connection = document.createElement('div');
        const length = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
        const angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;
        
        connection.fromNode = fromService;
        connection.toNode = toService;
        
        connection.style.cssText = `position: absolute; left: ${startX}px; top: ${startY}px; width: ${length}px; height: 2px; background: #007bff; transform-origin: left center; transform: rotate(${angle}deg); pointer-events: auto; z-index: 5; cursor: pointer;`;
        
        connection.addEventListener('click', () => connection.remove());
        
        const arrow = document.createElement('div');
        arrow.style.cssText = `position: absolute; left: 100%; top: 50%; transform: translateY(-50%); width: 0; height: 0; border-left: 6px solid #007bff; border-top: 3px solid transparent; border-bottom: 3px solid transparent;`;
        
        connection.appendChild(arrow);
        canvas.appendChild(connection);
    }

    attachScrollListener() {
        const container = this.container.querySelector('.canvas-content-flex');
        
        const updateConnections = () => {
            // Find all connection elements created by createConnectionFromMouse
            const connections = container.querySelectorAll('div[style*="position: absolute"][style*="background: #007bff"]');
            
            connections.forEach(connection => {
                // Skip if this connection has stored node references
                if (!connection.fromNode || !connection.toNode) return;
                
                const containerRect = container.getBoundingClientRect();
                const fromRect = connection.fromNode.getBoundingClientRect();
                const toRect = connection.toNode.getBoundingClientRect();
                
                const startX = fromRect.left - containerRect.left + container.scrollLeft + fromRect.width / 2;
                const startY = fromRect.top - containerRect.top + container.scrollTop + fromRect.height / 2;
                const endX = toRect.left - containerRect.left + container.scrollLeft + toRect.width / 2;
                const endY = toRect.top - containerRect.top + container.scrollTop + toRect.height / 2;
                
                const length = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
                const angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;
                
                connection.style.left = `${startX}px`;
                connection.style.top = `${startY}px`;
                connection.style.width = `${length}px`;
                connection.style.transform = `rotate(${angle}deg)`;
            });
        };
        
        container.addEventListener('scroll', updateConnections);
        window.addEventListener('resize', updateConnections);
    }

    attachDragDropListeners() {
        let isDragging = false;
        let dragLine = null;
        let startService = null;
        const canvas = this.container.querySelector('.canvas-content-flex');
        
        // Mouse down on service block - start drag
        this.container.querySelectorAll('.aws-service').forEach(service => {
            service.addEventListener('mousedown', (e) => {
                // Don't interfere with service selection clicks
                if (e.target.closest('.service-content')) return;
                
                e.preventDefault();
                e.stopPropagation();
                
                isDragging = true;
                startService = service;
                service.style.borderColor = '#ffc107';
                service.style.borderWidth = '2px';
                
                const canvasRect = canvas.getBoundingClientRect();
                const serviceRect = service.getBoundingClientRect();
                
                const startX = serviceRect.right - canvasRect.left + canvas.scrollLeft;
                const startY = serviceRect.top - canvasRect.top + canvas.scrollTop + serviceRect.height / 2;
                
                // Create temporary drag line
                dragLine = document.createElement('div');
                dragLine.style.cssText = `
                    position: absolute;
                    left: ${startX}px;
                    top: ${startY}px;
                    width: 0px;
                    height: 2px;
                    background: #ffc107;
                    transform-origin: left center;
                    pointer-events: none;
                    z-index: 1000;
                `;
                canvas.appendChild(dragLine);
            });
        });
        
        // Mouse move - update drag line
        document.addEventListener('mousemove', (e) => {
            if (!isDragging || !dragLine || !startService) return;
            
            const canvasRect = canvas.getBoundingClientRect();
            const serviceRect = startService.getBoundingClientRect();
            
            const startX = serviceRect.right - canvasRect.left + canvas.scrollLeft;
            const startY = serviceRect.top - canvasRect.top + canvas.scrollTop + serviceRect.height / 2;
            const endX = e.clientX - canvasRect.left + canvas.scrollLeft;
            const endY = e.clientY - canvasRect.top + canvas.scrollTop;
            
            const length = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
            const angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;
            
            dragLine.style.width = `${length}px`;
            dragLine.style.transform = `rotate(${angle}deg)`;
        });
        
        // Mouse up on service block - create connection
        this.container.querySelectorAll('.aws-service').forEach(service => {
            service.addEventListener('mouseup', (e) => {
                if (!isDragging || !startService || service === startService) return;
                
                e.preventDefault();
                e.stopPropagation();
                
                // Create permanent connection
                this.createServiceConnection(startService, service);
                this.endDrag();
            });
        });
        
        // Mouse up anywhere else - cancel drag
        document.addEventListener('mouseup', (e) => {
            if (isDragging) {
                this.endDrag();
            }
        });
        
        // Helper function to end drag
        this.endDrag = () => {
            if (startService) {
                startService.style.borderColor = '#ccc';
                startService.style.borderWidth = '1px';
            }
            if (dragLine) {
                dragLine.remove();
            }
            isDragging = false;
            dragLine = null;
            startService = null;
        };
    }
    
    createServiceConnection(fromService, toService) {
        const canvas = this.container.querySelector('.canvas-content-flex');
        const canvasRect = canvas.getBoundingClientRect();
        
        const fromRect = fromService.getBoundingClientRect();
        const toRect = toService.getBoundingClientRect();
        
        const startX = fromRect.right - canvasRect.left + canvas.scrollLeft;
        const startY = fromRect.top - canvasRect.top + canvas.scrollTop + fromRect.height / 2;
        const endX = toRect.left - canvasRect.left + canvas.scrollLeft;
        const endY = toRect.top - canvasRect.top + canvas.scrollTop + toRect.height / 2;
        
        const connection = document.createElement('div');
        const length = Math.sqrt((endX - startX) ** 2 + (endY - startY) ** 2);
        const angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;
        
        // Store service references for scroll updates
        connection.fromNode = fromService;
        connection.toNode = toService;
        
        connection.style.cssText = `
            position: absolute;
            left: ${startX}px;
            top: ${startY}px;
            width: ${length}px;
            height: 2px;
            background: #007bff;
            transform-origin: left center;
            transform: rotate(${angle}deg);
            pointer-events: auto;
            z-index: 5;
            cursor: pointer;
        `;
        
        // Click to remove connection
        connection.addEventListener('click', () => {
            connection.remove();
        });
        
        // Add arrow at the end
        const arrow = document.createElement('div');
        arrow.style.cssText = `
            position: absolute;
            left: 100%;
            top: 50%;
            transform: translateY(-50%);
            width: 0;
            height: 0;
            border-left: 6px solid #007bff;
            border-top: 3px solid transparent;
            border-bottom: 3px solid transparent;
        `;
        
        connection.appendChild(arrow);
        canvas.appendChild(connection);
    }
}

// Render function for integration
function renderAWSInfrastructureDiagram(container, diagramData) {
    // Add required CSS
    if (!document.getElementById('aws-designer-styles')) {
        const styles = document.createElement('style');
        styles.id = 'aws-designer-styles';
        styles.textContent = `
            .aws-designer {
                display: flex;
                height: 600px;
                border: 1px solid #ddd;
                border-radius: 8px;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .designer-sidebar {
                width: 250px;
                background: #f8f9fa;
                border-right: 1px solid #ddd;
                overflow-y: scroll;
                height: 600px;
                flex-shrink: 0;
                box-sizing: border-box;
                position: relative;
                transition: width 0.3s ease;
            }
            
            .designer-sidebar.collapsed {
                width: 40px;
            }
            
            .sidebar-toggle {
                position: absolute;
                top: 10px;
                right: 5px;
                width: 30px;
                height: 30px;
                background: #007bff;
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                z-index: 100;
                font-size: 12px;
            }
            
            .sidebar-content {
                padding: 15px;
                transition: opacity 0.3s ease;
            }
            
            .designer-sidebar.collapsed .sidebar-content {
                opacity: 0;
                pointer-events: none;
            }
            
            .designer-sidebar.collapsed .toggle-icon {
                transform: rotate(180deg);
            }
            
            .search-input {
                width: calc(100% - 16px);
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-bottom: 15px;
                font-size: 13px;
                box-sizing: border-box;
                max-width: 100%;
            }
            
            .category-header {
                font-weight: bold;
                margin-bottom: 10px;
                color: #495057;
            }
            
            .service-category {
                margin-bottom: 5px;
            }
            
            .category-title {
                display: flex;
                align-items: center;
                padding: 8px 4px;
                cursor: pointer;
                font-weight: 500;
                color: #495057;
                border-radius: 4px;
            }
            
            .category-title:hover {
                background: #e9ecef;
            }
            
            .category-icon {
                margin-right: 8px;
                font-size: 12px;
            }
            
            .expand-icon {
                margin-left: auto;
                font-size: 10px;
            }
            
            .category-services {
                margin-left: 20px;
                margin-top: 5px;
            }
            
            .category-service {
                display: flex;
                align-items: center;
                padding: 6px 8px;
                cursor: pointer;
                border-radius: 4px;
                margin: 2px 0;
            }
            
            .category-service:hover {
                background: #e3f2fd;
            }
            
            .category-service .service-icon {
                margin-right: 8px;
                font-size: 14px;
            }
            
            .category-service .service-name {
                font-size: 13px;
                color: #495057;
            }
            
            .designer-canvas {
                flex: 1;
                background: #fafafa;
                position: relative;
                overflow: auto;
            }
            
            .canvas-content-flex {
                position: relative;
            }
            
            .canvas-header {
                padding: 15px 20px;
                background: white;
                border-bottom: 1px solid #e9ecef;
                position: sticky;
                top: 0;
                z-index: 10;
            }
            
            .canvas-header h3 {
                margin: 0 0 5px 0;
                color: #495057;
                font-size: 16px;
            }
            
            .canvas-stats {
                font-size: 12px;
                color: #6c757d;
            }
            
            .canvas-content-flex {
                display: flex;
                flex-direction: row;
                flex-wrap: nowrap;
                gap: 20px;
                padding: 20px;
                align-items: flex-start;
                overflow-x: auto;
                position: relative;
            }
            
            .service-group-flex {
                flex: 0 0 auto;
                width: 280px;
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                padding: 15px;
                background: rgba(255, 255, 255, 0.8);
                height: fit-content;
            }
            
            .service-group {
                position: absolute;
            }
            
            .group-title {
                font-size: 12px;
                color: #666;
                margin-bottom: 10px;
                text-align: center;
                font-weight: 500;
            }
            
            .group-border {
                border: 2px dashed #dee2e6;
                border-radius: 8px;
                padding: 15px;
                background: rgba(255, 255, 255, 0.8);
                min-width: 200px;
                min-height: 120px;
            }
            
            .aws-service {
                border: 1px solid #ccc;
                border-radius: 6px;
                background: white;
                padding: 8px;
                margin: 8px 0;
                display: flex;
                align-items: center;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                position: relative;
            }
            
            .service-content {
                display: flex;
                align-items: center;
                gap: 10px;
                flex: 1;
                padding: 4px 8px;
            }
            
            .service-inputs, .service-outputs {
                display: flex;
                flex-direction: column;
                gap: 4px;
                padding: 4px;
            }
            
            .input-node, .output-node {
                width: 12px;
                height: 12px;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 8px;
            }
            
            .input-node {
                background: #28a745;
                color: white;
                border: 2px solid #1e7e34;
            }
            
            .output-node {
                background: #dc3545;
                color: white;
                border: 2px solid #c82333;
            }
            
            .input-node:hover, .output-node:hover {
                transform: scale(1.2);
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            
            .aws-service:hover {
                border-color: #007bff;
                transform: translateY(-1px);
                box-shadow: 0 2px 6px rgba(0,0,0,0.15);
            }
            
            .aws-service.selected {
                border-color: #007bff;
                border-width: 2px;
                background: #f0f8ff;
            }
            
            .aws-service .service-icon {
                font-size: 20px;
                flex-shrink: 0;
            }
            
            .service-details {
                flex: 1;
                min-width: 0;
            }
            
            .service-details .service-name {
                font-weight: 600;
                font-size: 13px;
                color: #495057;
                margin-bottom: 2px;
            }
            
            .service-details .service-resource {
                font-size: 11px;
                color: #6c757d;
                font-family: monospace;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            
            .service-status {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #28a745;
                flex-shrink: 0;
            }
            
            .designer-panel {
                width: 350px;
                background: white;
                border-left: 1px solid #ddd;
                overflow-y: auto;
            }
            
            .panel-header {
                padding: 20px;
                border-bottom: 1px solid #e9ecef;
                background: #f8f9fa;
            }
            
            .panel-title {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 4px;
            }
            
            .panel-subtitle {
                font-size: 12px;
                color: #6c757d;
            }
            
            .panel-content {
                padding: 20px;
            }
            
            .service-description {
                margin-bottom: 25px;
            }
            
            .service-description p {
                font-size: 14px;
                line-height: 1.5;
                color: #495057;
                margin: 10px 0;
            }
            
            .service-configuration h4,
            .service-features h4,
            .terraform-preview h4 {
                font-size: 14px;
                font-weight: 600;
                color: #495057;
                margin: 20px 0 10px 0;
                padding-bottom: 5px;
                border-bottom: 1px solid #e9ecef;
            }
            
            .config-item {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin: 8px 0;
                padding: 8px 0;
                border-bottom: 1px solid #f8f9fa;
            }
            
            .config-label {
                font-weight: 500;
                font-size: 13px;
                color: #495057;
                flex: 1;
            }
            
            .config-value {
                background: #f8f9fa;
                padding: 4px 8px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 12px;
                color: #495057;
                max-width: 60%;
                word-break: break-all;
            }
            
            .service-features ul {
                margin: 10px 0;
                padding-left: 20px;
            }
            
            .service-features li {
                margin: 6px 0;
                color: #495057;
                font-size: 13px;
            }
            
            .terraform-preview pre {
                background: #1e1e1e;
                color: #d4d4d4;
                padding: 15px;
                border-radius: 6px;
                font-size: 11px;
                overflow-x: auto;
                margin: 10px 0;
            }
            
            .service-connection {
                position: absolute;
                pointer-events: none;
            }
            
            .connection-line {
                border-top: 2px dashed #007bff;
                opacity: 0.6;
            }
            
            .connection-label {
                font-size: 10px;
                color: #007bff;
                background: white;
                padding: 2px 6px;
                border-radius: 3px;
                border: 1px solid #007bff;
                position: absolute;
                top: -10px;
                left: 50%;
                transform: translateX(-50%);
                white-space: nowrap;
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Create and render the designer
    new AWSInfrastructureDesigner(container, diagramData);
}