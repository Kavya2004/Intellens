// AWS Tech Architecture Diagram Renderer
function renderAwsTechDiagram(diagramData) {
    const container = document.createElement('div');
    container.className = 'aws-tech-diagram';
    container.style.cssText = `
        width: 100%;
        height: 600px;
        background: #f8f9fa;
        border: 2px solid #232f3e;
        border-radius: 8px;
        position: relative;
        overflow: hidden;
    `;

    // AWS Cloud header
    const header = document.createElement('div');
    header.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 50px;
        background: #232f3e;
        color: white;
        display: flex;
        align-items: center;
        padding: 0 20px;
        font-weight: bold;
    `;
    header.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #ff9900; color: #232f3e; padding: 4px 8px; border-radius: 4px; font-size: 12px;">aws</div>
            <span>Technology Stack</span>
        </div>
    `;

    // Customer account section
    const customerAccount = document.createElement('div');
    customerAccount.style.cssText = `
        position: absolute;
        top: 80px;
        left: 30px;
        right: 30px;
        bottom: 30px;
        border: 2px dashed #666;
        border-radius: 8px;
        background: white;
        padding: 20px;
    `;

    const accountHeader = document.createElement('div');
    accountHeader.style.cssText = `
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
        font-weight: bold;
        color: #232f3e;
    `;
    accountHeader.innerHTML = `
        <div style="width: 30px; height: 30px; background: #666; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: white;">☁️</div>
        <span>Application Architecture</span>
    `;

    // Render services in a grid layout
    const servicesGrid = document.createElement('div');
    servicesGrid.style.cssText = `
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 20px;
    `;

    // Add user icon
    const userIcon = document.createElement('div');
    userIcon.style.cssText = `
        position: absolute;
        left: -50px;
        top: 50%;
        transform: translateY(-50%);
        width: 60px;
        height: 60px;
        background: white;
        border: 2px solid #232f3e;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        z-index: 10;
    `;
    userIcon.innerHTML = '<div style="font-size: 20px; font-weight: bold; color: #232f3e;">👤</div>';

    const userLabel = document.createElement('div');
    userLabel.style.cssText = `
        position: absolute;
        left: -50px;
        top: calc(50% + 40px);
        transform: translateX(-50%);
        font-size: 12px;
        font-weight: bold;
        color: #232f3e;
        text-align: center;
        width: 60px;
    `;
    userLabel.textContent = 'User';

    // Render each service
    diagramData.services.forEach((service, index) => {
        const serviceElement = createServiceElement(service, index + 1);
        servicesGrid.appendChild(serviceElement);
    });

    customerAccount.appendChild(accountHeader);
    customerAccount.appendChild(servicesGrid);
    customerAccount.appendChild(userIcon);
    customerAccount.appendChild(userLabel);

    container.appendChild(header);
    container.appendChild(customerAccount);

    return container;
}

function createServiceElement(service, stepNumber) {
    const element = document.createElement('div');
    element.style.cssText = `
        background: white;
        border: 2px solid ${service.color || '#ccc'};
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        position: relative;
        min-height: 120px;
        display: flex;
        cursor: pointer;
        transition: transform 0.2s ease;
    `;
    element.setAttribute('data-service-id', service.id);

    element.addEventListener('mouseenter', () => {
        element.style.transform = 'scale(1.05)';
    });

    element.addEventListener('mouseleave', () => {
        element.style.transform = 'scale(1)';
    });

    // Input nodes
    const inputs = service.inputs || [];
    const inputsContainer = document.createElement('div');
    inputsContainer.style.cssText = `
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 4px;
        align-items: center;
        justify-content: center;
    `;
    inputs.forEach(input => {
        const inputNode = document.createElement('div');
        inputNode.style.cssText = `
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #28a745;
            border: 2px solid #1e7e34;
            cursor: pointer;
        `;
        inputNode.setAttribute('data-input-id', input.id);
        inputsContainer.appendChild(inputNode);
    });

    // Service content
    const serviceContent = document.createElement('div');
    serviceContent.style.cssText = `
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 0 10px;
    `;

    // Step number
    const stepBadge = document.createElement('div');
    stepBadge.style.cssText = `
        position: absolute;
        top: -10px;
        left: -10px;
        width: 25px;
        height: 25px;
        background: #232f3e;
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
    `;
    stepBadge.textContent = stepNumber;

    // Service icon
    const icon = document.createElement('div');
    icon.style.cssText = `
        font-size: 32px;
        margin-bottom: 10px;
    `;
    icon.textContent = service.icon;

    // Service name
    const name = document.createElement('div');
    name.style.cssText = `
        font-weight: bold;
        font-size: 14px;
        color: #232f3e;
        margin-bottom: 5px;
        line-height: 1.2;
    `;
    name.textContent = service.name;

    // Service category
    const category = document.createElement('div');
    category.style.cssText = `
        font-size: 11px;
        color: #666;
        text-transform: capitalize;
    `;
    category.textContent = service.category.replace('_', ' ');

    serviceContent.appendChild(stepBadge);
    serviceContent.appendChild(icon);
    serviceContent.appendChild(name);
    serviceContent.appendChild(category);

    // Output nodes
    const outputs = service.outputs || [];
    const outputsContainer = document.createElement('div');
    outputsContainer.style.cssText = `
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 4px;
        align-items: center;
        justify-content: center;
    `;
    outputs.forEach(output => {
        const outputNode = document.createElement('div');
        outputNode.style.cssText = `
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #dc3545;
            border: 2px solid #c82333;
            cursor: pointer;
        `;
        outputNode.setAttribute('data-output-id', output.id);
        outputsContainer.appendChild(outputNode);
    });

    element.appendChild(inputsContainer);
    element.appendChild(serviceContent);
    element.appendChild(outputsContainer);

    return element;
}