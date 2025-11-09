def generate_project_overview(languages, services, file_details, project_name="Project"):
    """Generate a comprehensive project overview based on analysis."""
    
    # Analyze project type and architecture
    project_type = determine_project_type(languages, services, file_details)
    tech_stack = identify_tech_stack(languages, services)
    architecture_pattern = detect_architecture_pattern(file_details, services)
    complexity_assessment = assess_project_complexity(languages, services, file_details)
    
    # Generate overview text
    overview_text = create_overview_description(
        project_name, project_type, tech_stack, 
        architecture_pattern, complexity_assessment, file_details
    )
    
    return {
        "overview_text": overview_text,
        "project_type": project_type,
        "tech_stack": tech_stack,
        "architecture_pattern": architecture_pattern,
        "complexity": complexity_assessment,
        "key_metrics": {
            "total_files": len(file_details),
            "languages_count": len(languages),
            "services_count": len(services),
            "estimated_size": categorize_project_size(len(file_details))
        }
    }

def determine_project_type(languages, services, file_details):
    """Determine the type of project based on technologies used."""
    
    # Check for web frameworks
    web_frameworks = ['react', 'vue', 'angular', 'next.js', 'svelte', 'express', 'django', 'flask']
    if any(fw.lower() in str(services).lower() for fw in web_frameworks):
        if any(lang in ['JavaScript', 'TypeScript', 'HTML', 'CSS'] for lang in languages):
            return "Full-Stack Web Application"
        else:
            return "Web API/Backend Service"
    
    # Check for mobile
    mobile_indicators = ['react native', 'flutter', 'ionic', 'xamarin']
    if any(mobile.lower() in str(services).lower() for mobile in mobile_indicators):
        return "Mobile Application"
    
    # Check for infrastructure
    infra_indicators = ['terraform', 'docker', 'kubernetes', 'aws', 'azure', 'gcp']
    if any(infra.lower() in str(services).lower() for infra in infra_indicators):
        return "Infrastructure as Code Project"
    
    # Check for data/ML
    data_indicators = ['pandas', 'numpy', 'tensorflow', 'pytorch', 'jupyter']
    if any(data.lower() in str(services).lower() for data in data_indicators):
        return "Data Science/ML Project"
    
    # Check for CLI tools
    if 'Python' in languages and len([f for f in file_details if 'main.py' in f.get('file', '')]) > 0:
        return "Command Line Tool"
    
    # Default based on primary language
    if 'JavaScript' in languages or 'TypeScript' in languages:
        return "JavaScript Application"
    elif 'Python' in languages:
        return "Python Application"
    elif 'Java' in languages:
        return "Java Application"
    else:
        return "Software Project"

def identify_tech_stack(languages, services):
    """Identify the main technology stack."""
    
    stack = {
        "frontend": [],
        "backend": [],
        "database": [],
        "infrastructure": []
    }
    
    # Frontend technologies
    frontend_techs = ['react', 'vue', 'angular', 'next.js', 'svelte', 'html', 'css', 'javascript', 'typescript']
    for tech in frontend_techs:
        if tech.lower() in str(services).lower() or tech.title() in languages:
            stack["frontend"].append(tech.title())
    
    # Backend technologies
    backend_techs = ['node.js', 'express', 'django', 'flask', 'spring', 'fastapi', 'python', 'java', 'go']
    for tech in backend_techs:
        if tech.lower() in str(services).lower() or tech.title() in languages:
            stack["backend"].append(tech.title())
    
    # Database technologies
    db_techs = ['mongodb', 'postgresql', 'mysql', 'redis', 'sqlite', 'dynamodb']
    for tech in db_techs:
        if tech.lower() in str(services).lower():
            stack["database"].append(tech.title())
    
    # Infrastructure technologies
    infra_techs = ['docker', 'kubernetes', 'terraform', 'aws', 'azure', 'gcp', 'nginx']
    for tech in infra_techs:
        if tech.lower() in str(services).lower():
            stack["infrastructure"].append(tech.title())
    
    return stack

def detect_architecture_pattern(file_details, services):
    """Detect the architectural pattern used."""
    
    # Check for common patterns based on file structure
    file_paths = [f.get('file', '') for f in file_details]
    
    # Microservices pattern
    if any('service' in path.lower() for path in file_paths) or 'docker' in str(services).lower():
        return "Microservices Architecture"
    
    # MVC pattern
    if any(pattern in str(file_paths).lower() for pattern in ['controller', 'model', 'view']):
        return "Model-View-Controller (MVC)"
    
    # Component-based (React/Vue)
    if any(fw in str(services).lower() for fw in ['react', 'vue', 'angular']):
        return "Component-Based Architecture"
    
    # Layered architecture
    if any(layer in str(file_paths).lower() for layer in ['api', 'service', 'repository', 'dao']):
        return "Layered Architecture"
    
    # Serverless
    if 'lambda' in str(services).lower() or 'serverless' in str(services).lower():
        return "Serverless Architecture"
    
    return "Modular Architecture"

def assess_project_complexity(languages, services, file_details):
    """Assess overall project complexity."""
    
    complexity_score = 0
    
    # File count factor
    file_count = len(file_details)
    if file_count > 50:
        complexity_score += 3
    elif file_count > 20:
        complexity_score += 2
    elif file_count > 5:
        complexity_score += 1
    
    # Language diversity factor
    lang_count = len(languages)
    if lang_count > 4:
        complexity_score += 2
    elif lang_count > 2:
        complexity_score += 1
    
    # Service/technology factor
    service_count = len(services)
    if service_count > 10:
        complexity_score += 2
    elif service_count > 5:
        complexity_score += 1
    
    # Determine complexity level
    if complexity_score >= 6:
        return "High"
    elif complexity_score >= 3:
        return "Medium"
    else:
        return "Low"

def categorize_project_size(file_count):
    """Categorize project size based on file count."""
    if file_count > 100:
        return "Large"
    elif file_count > 30:
        return "Medium"
    elif file_count > 10:
        return "Small"
    else:
        return "Micro"

def create_overview_description(project_name, project_type, tech_stack, 
                              architecture_pattern, complexity, file_details):
    """Create a human-readable project overview description."""
    
    # Build technology summary
    tech_summary = []
    if tech_stack["frontend"]:
        tech_summary.append(f"frontend built with {', '.join(tech_stack['frontend'][:2])}")
    if tech_stack["backend"]:
        tech_summary.append(f"backend using {', '.join(tech_stack['backend'][:2])}")
    if tech_stack["database"]:
        tech_summary.append(f"data storage with {', '.join(tech_stack['database'][:2])}")
    
    tech_description = " and ".join(tech_summary) if tech_summary else "modern technology stack"
    
    # Count unique languages safely
    unique_langs = set()
    for f in file_details:
        if f.get('languages'):
            unique_langs.update(f['languages'])
    lang_count = len(unique_langs)
    
    # Build overview text
    overview = f"""
**{project_name}** is a {project_type.lower()} with {tech_description}. 

The project follows a {architecture_pattern.lower()} pattern and has {complexity.lower()} complexity with {len(file_details)} files across {lang_count} programming languages.

**Key Characteristics:**
• Architecture: {architecture_pattern}
• Complexity Level: {complexity}
• File Count: {len(file_details)} files
• Technology Stack: {len(tech_stack['frontend']) + len(tech_stack['backend'])} main technologies

This appears to be a {"production-ready" if complexity == "High" else "development-stage" if complexity == "Medium" else "prototype or learning"} project suitable for {"enterprise deployment" if complexity == "High" else "small to medium-scale deployment" if complexity == "Medium" else "personal or educational use"}.
    """.strip()
    
    return overview