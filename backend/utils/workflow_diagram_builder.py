import json

def get_language_logo(lang):
    """Get logo URL for programming language."""
    logos = {
        "python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        "javascript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
        "typescript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
        "java": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
        "go": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/go/go-original.svg",
        "terraform": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/terraform/terraform-original.svg",
        "html": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
        "css": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg"
    }
    return logos.get(lang.lower(), "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/devicon/devicon-original.svg")

def get_service_logo(service):
    """Get specific logo URL for each service/technology."""
    service_lower = service.lower()
    
    # AWS Services with working logos
    aws_service_icons = {
        'lambda': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/awslambda.svg',
        's3': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazons3.svg',
        'ec2': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonec2.svg',
        'rds': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonrds.svg',
        'dynamodb': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazondynamodb.svg',
        'iot': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'kinesis': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'sqs': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'sns': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'cloudformation': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'cloudwatch': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'apigateway': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'ecs': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg',
        'eks': 'https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg'
    }
    
    # Check for specific AWS services first
    for aws_service, icon_url in aws_service_icons.items():
        if aws_service in service_lower:
            return icon_url
    
    # Generic AWS services
    if "aws" in service_lower:
        return "https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/amazonwebservices.svg"
    
    # Microsoft Azure
    elif "azure" in service_lower or "microsoft azure" in service_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/f/fa/Microsoft_Azure.svg"
    
    # Google Cloud Platform
    elif "google cloud" in service_lower or "gcp" in service_lower:
        return "https://upload.wikimedia.org/wikipedia/commons/5/51/Google_Cloud_logo.svg"
    
    # Other cloud services
    elif "docker" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg"
    elif "kubernetes" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kubernetes/kubernetes-plain.svg"
    elif "terraform" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/terraform/terraform-original.svg"
    
    # Databases
    elif "postgres" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg"
    elif "mysql" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg"
    elif "mongodb" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg"
    elif "redis" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg"
    
    # Web servers
    elif "nginx" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nginx/nginx-original.svg"
    elif "apache" in service_lower:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apache/apache-original.svg"
    
    else:
        return "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/devicon/devicon-original.svg"

def generate_flow_explanations(languages, services):
    """Generate detailed explanations for component interactions."""
    explanations = []
    
    # User to application interactions
    if languages:
        app_list = ", ".join(list(languages.keys())[:3])
        explanations.append(f"User sends HTTP requests to applications built with {app_list}")
    
    # Application to service interactions
    if services:
        for service in list(services.keys())[:3]:
            if "aws" in service.lower():
                explanations.append(f"Applications authenticate and make API calls to {service}")
            elif "database" in service.lower() or "postgres" in service.lower() or "mysql" in service.lower():
                explanations.append(f"Applications execute SQL queries and store/retrieve data from {service}")
            elif "docker" in service.lower():
                explanations.append(f"Applications are containerized and deployed using {service}")
            else:
                explanations.append(f"Applications integrate with and consume services from {service}")
    
    return explanations

def build_workflow_diagram(languages, services, project_name="Project"):
    """Build a system architecture diagram with detailed flow explanations."""
    
    components = []
    connections = []
    
    # User component
    components.append({
        "id": "user",
        "title": "User/Client",
        "description": "End user or client application",
        "type": "user",
        "logo": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23333' d='M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 7V9C15 10.1 14.1 11 13 11V16L15 18V22H13V19L11 17V22H9V18L11 16V11C9.9 11 9 10.1 9 9V7H3V9H5V16C5 17.1 5.9 18 7 18H9V20H11V18H13C14.1 18 15 17.1 15 16V9H21Z'/%3E%3C/svg%3E",
        "inputs": [],
        "outputs": [{"id": "user_output", "label": "Output"}]
    })
    
    # All languages as application components
    for lang, count in languages.items():
        components.append({
            "id": f"lang_{lang}",
            "title": f"{lang} Application",
            "description": f"Built with {count} {lang} files",
            "type": "application",
            "logo": get_language_logo(lang),
            "inputs": [{"id": f"lang_{lang}_input", "label": "Input"}],
            "outputs": [{"id": f"lang_{lang}_output", "label": "Output"}]
        })
    
    # All services as service components
    for service, count in services.items():
        # Truncate extremely long service names
        display_title = service if len(service) <= 25 else service[:22] + "..."
        service_type = "database" if any(x in service.lower() for x in ["postgres", "mysql", "mongodb", "redis"]) else "cloud" if "aws" in service.lower() else "service"
        service_id = f"service_{service.replace(' ', '_').replace('.', '_')[:20]}"
        components.append({
            "id": service_id,
            "title": display_title,
            "description": f"Referenced {count} times in code",
            "type": service_type,
            "logo": get_service_logo(service),
            "inputs": [{"id": f"{service_id}_input", "label": "Input"}],
            "outputs": [{"id": f"{service_id}_output", "label": "Output"}]
        })
    
    # Generate detailed flow explanations
    flow_explanations = generate_flow_explanations(languages, services)
    
    return {
        "architecture": {
            "title": f"{project_name} System Architecture & Data Flow",
            "components": components,
            "connections": connections,
            "flow_explanations": flow_explanations,
            "diagram_type": "System Architecture / Data Flow Diagram",
            "purpose": f"Explains how {len(languages)} programming languages interact with {len(services)} services to handle data processing and system operations"
        },
        "metadata": {
            "total_components": len(components),
            "languages_detected": len(languages),
            "services_detected": len(services),
            "project_complexity": "High" if len(services) > 5 else "Medium" if len(services) > 2 else "Low"
        }
    }

def generate_mermaid_workflow(languages, services, project_name="Project"):
    """Generate Mermaid diagram for system architecture."""
    mermaid = ["graph TD"]
    mermaid.append("    User[User] --> App[Application]")
    mermaid.append("    App --> DB[Database]")
    if services:
        mermaid.append("    App --> EXT[External Services]")
    return "\n".join(mermaid)