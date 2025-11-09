from dotenv import load_dotenv
import os
import boto3
import json
from .cost_estimator import estimate_costs_for_services

# Load .env variables
load_dotenv()

def generate_readme(languages, services, file_details, project_name):
    """Generate comprehensive README using AWS Bedrock Claude 3.5."""
    
    # Generate AI-powered content
    description, file_explanations, architecture_overview, setup_instructions = generate_bedrock_readme_content(
        languages, services, file_details, project_name
    )
    
    # Generate cost estimates
    cost_estimates = estimate_costs_for_services(services)

    # Build comprehensive README
    readme = f"# {project_name}\n\n"
    readme += f"{description}\n\n"
    
    # Table of Contents
    readme += "## Table of Contents\n\n"
    readme += "- [Overview](#overview)\n"
    readme += "- [Architecture](#architecture)\n"
    readme += "- [Features](#features)\n"
    readme += "- [Tech Stack](#tech-stack)\n"
    readme += "- [File Structure](#file-structure)\n"
    readme += "- [Setup & Installation](#setup--installation)\n"
    readme += "- [Usage](#usage)\n"
    readme += "- [Cost Estimation](#cost-estimation)\n"
    readme += "- [API Documentation](#api-documentation)\n"
    readme += "- [Contributing](#contributing)\n\n"
    
    # Overview
    readme += "## Overview\n\n"
    readme += f"{architecture_overview}\n\n"
    
    # Architecture
    readme += "## Architecture\n\n"
    readme += generate_architecture_section(languages, services) + "\n\n"
    
    # Features
    features = generate_enhanced_features_section(languages, services, file_details)
    readme += f"## Features\n\n{features}\n\n"
    
    # Tech Stack
    readme += generate_tech_stack_section(languages, services)
    
    # File Structure
    readme += "## File Structure\n\n"
    readme += generate_file_structure_section(file_details, file_explanations)
    
    # Setup & Installation
    readme += f"## Setup & Installation\n\n{setup_instructions}\n\n"
    
    # Usage
    readme += generate_usage_section(languages, services)
    
    # Cost Estimation
    readme += generate_cost_estimation_section(cost_estimates)
    
    # API Documentation
    readme += generate_api_documentation(services)
    
    # Contributing
    readme += generate_contributing_section()
    
    return readme

def generate_bedrock_readme_content(languages, services, file_details, project_name):
    """Use AWS Bedrock Claude 3.5 to generate comprehensive README content."""
    
    # Force Bedrock usage only
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

    try:
        # Prepare context
        context = prepare_project_context(languages, services, file_details, project_name)
        
        # Generate comprehensive README content
        prompt = f"""
You are a senior technical writer creating a comprehensive README for a software project. 

Project Analysis:
{context}

Generate a professional README with these sections:
1. Project description (2-3 sentences explaining what it does)
2. Architecture overview (how components interact)
3. Detailed setup instructions
4. File explanations for each major file

Write in professional GitHub README style with clear, concise explanations.
Return as JSON with keys: description, architecture_overview, setup_instructions, file_explanations
"""
        
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        
        result = json.loads(response['body'].read())
        response_text = result['content'][0]['text']
        
        # Try to extract JSON from response text
        try:
            # Look for JSON block in response
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            if json_match:
                content = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
        except:
            # Fallback to simple parsing
            content = {
                'description': response_text[:200] + '...',
                'architecture_overview': 'Multi-tier architecture with clear separation of concerns.',
                'setup_instructions': generate_quick_start(languages, services),
                'file_explanations': {}
            }
        
        return (
            content.get('description', ''),
            content.get('file_explanations', {}),
            content.get('architecture_overview', ''),
            content.get('setup_instructions', '')
        )
        
    except Exception as e:
        print(f"Bedrock error: {e}")
        raise Exception(f"Bedrock required but failed: {e}")

def prepare_project_context(languages, services, file_details, project_name):
    """Prepare structured context for Bedrock."""
    context = f"Project: {project_name}\n"
    context += f"Languages: {', '.join(languages.keys())}\n"
    context += f"Services: {', '.join(list(services.keys())[:10])}\n\n"
    
    context += "Key Files:\n"
    for f in file_details[:15]:
        context += f"- {f['file']}: {', '.join(f.get('languages', []))} {', '.join(f.get('services', []))}\n"
    
    return context

def generate_fallback_content(languages, services, file_details, project_name):
    """Enhanced fallback content when AI is unavailable."""
    description = f"**{project_name}** is a {', '.join(languages.keys())} application that integrates with {len(services)} services including {', '.join(list(services.keys())[:3])}."
    
    file_explanations = {}
    for f in file_details[:15]:
        name = f['file']
        if name.endswith('.py'):
            file_explanations[name] = "Python module with application logic and API endpoints"
        elif name.endswith('.js'):
            file_explanations[name] = "JavaScript file handling frontend interactions and UI"
        elif name.endswith('.html'):
            file_explanations[name] = "HTML template defining the web interface structure"
        elif name.endswith('.json'):
            file_explanations[name] = "JSON configuration file with project settings"
        elif name.endswith('.tf'):
            file_explanations[name] = "Terraform infrastructure configuration"
        else:
            file_explanations[name] = f"Project file containing {name.split('.')[-1]} code"
    
    architecture = f"This project implements a **multi-tier architecture** with {len(languages)} programming languages and {len(services)} integrated services."
    setup = generate_quick_start(languages, services)
    
    return description, file_explanations, architecture, setup

def generate_architecture_section(languages, services):
    """Generate architecture overview section."""
    arch = "This project implements a "
    
    if 'Terraform' in languages:
        arch += "**Infrastructure as Code** architecture using Terraform for cloud resource management.\n\n"
    elif len(languages) > 2:
        arch += "**multi-tier architecture** with the following layers:\n\n"
        if 'JavaScript' in languages or 'HTML' in languages:
            arch += "- **Frontend Layer**: User interface and client-side logic\n"
        if 'Python' in languages or 'Java' in languages:
            arch += "- **Backend Layer**: Business logic and API endpoints\n"
        if any('database' in s.lower() for s in services):
            arch += "- **Data Layer**: Database and storage management\n"
    else:
        arch += "**modular architecture** with clear separation of concerns.\n\n"
    
    return arch

def generate_enhanced_features_section(languages, services, file_details):
    """Generate comprehensive features list."""
    features = []
    
    # Core functionality features
    if 'FastAPI' in services or 'Flask' in services:
        features.append("✨ **REST API**: RESTful endpoints for data access and manipulation")
    if 'React' in services or 'Vue' in services:
        features.append("📱 **Interactive UI**: Modern responsive web interface")
    if 'Docker' in services:
        features.append("📦 **Containerization**: Docker support for easy deployment")
    if any('database' in s.lower() or 'sql' in s.lower() for s in services):
        features.append("💾 **Data Persistence**: Database integration and management")
    if 'Terraform' in languages:
        features.append("☁️ **Infrastructure as Code**: Automated cloud resource provisioning")
    if any('aws' in s.lower() for s in services):
        features.append("🌐 **Cloud Integration**: AWS services integration")
    if any('test' in f['file'].lower() for f in file_details) if file_details else False:
        features.append("✅ **Testing Suite**: Comprehensive automated testing")
    if 'Redis' in services:
        features.append("⚡ **Caching**: Redis-based performance optimization")
    if any('auth' in s.lower() for s in services):
        features.append("🔒 **Authentication**: Secure user authentication system")
    
    return "\n".join(features) if features else "- Core application functionality"

def generate_tech_stack_section(languages, services):
    """Generate detailed tech stack section."""
    section = "## Tech Stack\n\n"
    
    if languages:
        section += "### Languages\n"
        for lang, count in languages.items():
            section += f"- **{lang}** ({count} files)\n"
        section += "\n"
    
    if services:
        section += "### Technologies & Services\n"
        for service, count in list(services.items())[:10]:
            section += f"- **{service}** ({count} references)\n"
        section += "\n"
    
    return section

def generate_file_structure_section(file_details, file_explanations):
    """Generate file structure with explanations."""
    section = "```\n"
    
    # Group files by directory
    dirs = {}
    for f in file_details[:20]:
        path_parts = f['file'].split('/')
        if len(path_parts) > 1:
            dir_name = path_parts[0]
            if dir_name not in dirs:
                dirs[dir_name] = []
            dirs[dir_name].append(f['file'])
        else:
            if 'root' not in dirs:
                dirs['root'] = []
            dirs['root'].append(f['file'])
    
    for dir_name, files in dirs.items():
        if dir_name != 'root':
            section += f"{dir_name}/\n"
        for file in files[:5]:
            indent = "│   " if dir_name != 'root' else ""
            section += f"{indent}├── {file.split('/')[-1]}\n"
        if len(files) > 5:
            indent = "│   " if dir_name != 'root' else ""
            section += f"{indent}└── ... and {len(files) - 5} more files\n"
    
    section += "```\n\n"
    
    # Add file explanations
    if file_explanations:
        section += "### Key Files\n\n"
        for file, explanation in list(file_explanations.items())[:10]:
            section += f"- **`{file}`**: {explanation}\n"
        section += "\n"
    
    return section

def generate_usage_section(languages, services):
    """Generate usage examples section."""
    section = "## Usage\n\n"
    
    if 'FastAPI' in services:
        section += "### API Endpoints\n\n"
        section += "The API server provides the following endpoints:\n\n"
        section += "- `GET /` - Health check\n"
        section += "- `POST /upload` - Upload and analyze project files\n"
        section += "- `GET /docs` - Interactive API documentation\n\n"
    
    if 'JavaScript' in languages:
        section += "### Frontend Usage\n\n"
        section += "1. Open your browser to `http://localhost:3000`\n"
        section += "2. Upload a ZIP file containing your project\n"
        section += "3. View the generated architecture diagrams\n\n"
    
    if 'Terraform' in languages:
        section += "### Infrastructure Deployment\n\n"
        section += "```bash\n"
        section += "# Initialize Terraform\n"
        section += "terraform init\n\n"
        section += "# Review planned changes\n"
        section += "terraform plan\n\n"
        section += "# Apply infrastructure\n"
        section += "terraform apply\n"
        section += "```\n\n"
    
    return section

def generate_api_documentation(services):
    """Generate API documentation section."""
    if 'FastAPI' in services or 'Flask' in services:
        return """## API Documentation

### Endpoints

#### POST /upload
Upload and analyze a project ZIP file.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: ZIP file containing project files

**Response:**
```json
{
  "languages": {"Python": 5, "JavaScript": 3},
  "services": {"FastAPI": 2, "AWS S3": 1},
  "architecture_diagram": {...},
  "workflow_diagram": {...}
}
```

#### GET /docs
Interactive API documentation (Swagger UI)

"""
    return ""

def generate_contributing_section():
    """Generate contributing guidelines."""
    return """## Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/project-name.git
cd project-name

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest

# Start development server
python run.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Check the documentation
- Review existing issues for solutions

---

**Made with ❤️ by the development team**
"""

def generate_quick_start(languages, services):
    """Generate quick start instructions."""
    steps = []
    
    # Prerequisites
    steps.append("### Prerequisites\n")
    if 'Python' in languages:
        steps.append("- Python 3.8+")
    if 'JavaScript' in languages:
        steps.append("- Node.js 16+")
    if 'Terraform' in languages:
        steps.append("- Terraform 1.0+")
    if any('aws' in s.lower() for s in services):
        steps.append("- AWS CLI configured")
    steps.append("\n")
    
    # Installation steps
    steps.append("### Installation\n")
    
    if 'Python' in languages:
        steps.append("1. **Clone the repository:**\n   ```bash\n   git clone <repository-url>\n   cd project-directory\n   ```\n")
        steps.append("2. **Install Python dependencies:**\n   ```bash\n   pip install -r requirements.txt\n   ```\n")
        
        if 'FastAPI' in services:
            steps.append("3. **Start the backend server:**\n   ```bash\n   cd backend\n   uvicorn main:app --reload --port 8000\n   ```\n")
        else:
            steps.append("3. **Run the application:**\n   ```bash\n   python main.py\n   ```\n")
    
    if 'JavaScript' in languages:
        steps.append("4. **Start the frontend (in a new terminal):**\n   ```bash\n   cd frontend\n   python -m http.server 3000\n   ```\n")
        steps.append("5. **Open your browser:**\n   Navigate to `http://localhost:3000`\n\n")
    
    if 'Docker' in services:
        steps.append("### Docker Alternative\n\n")
        steps.append("```bash\n# Build and run with Docker\ndocker build -t app .\ndocker run -p 8000:8000 -p 3000:3000 app\n```\n\n")
    
    return "".join(steps) if steps else "No specific setup instructions available."

def generate_cost_estimation_section(cost_estimates):
    """Generate cost estimation section for README."""
    if not cost_estimates or not cost_estimates.get('service_estimates'):
        return "## Cost Estimation\n\nNo cost data available for this project.\n\n"
    
    section = "## Cost Estimation\n\n"
    section += "💰 **Projected Monthly Costs**: " + cost_estimates['total_costs']['monthly_range'] + "\n"
    section += "📅 **Projected Yearly Costs**: " + cost_estimates['total_costs']['yearly_range'] + "\n\n"
    
    section += "### Service Breakdown\n\n"
    section += "\n| Service | Monthly Cost | Yearly Cost | Usage Detected |\n"
    section += "| :------: |:------------:| :-----------:| :--------------:|\n"
    
    for service in cost_estimates['service_estimates'][:10]:
        section += f"| {service['service']} | {service['monthly_cost_range']} | {service['yearly_cost_range']} | {service['usage_detected']}x |\n"
    
    section += "\n### Cost Optimization Tips\n\n"
    for i, rec in enumerate(cost_estimates.get('recommendations', [])[:5], 1):
        section += f"{i}. {rec}\n"
    
    section += "\n**Note**: These are estimated costs based on typical usage patterns. Actual costs may vary significantly based on your specific usage, region, and pricing changes. Always refer to official pricing calculators for accurate estimates.\n\n"
    
    return section

def generate_smart_fallback_description(languages, services, file_details, project_name):
    """Fallback description if Bedrock is unavailable."""
    
    has_web = 'JavaScript' in languages or 'HTML' in languages or 'CSS' in languages
    has_backend = 'Python' in languages or 'Java' in languages or 'Go' in languages
    has_infra = 'Terraform' in languages or 'YAML' in languages
    has_data = any('sql' in s.lower() or 'database' in s.lower() for s in services.keys())
    has_api = any('api' in s.lower() or 'rest' in s.lower() or 'fastapi' in s.lower() for s in services.keys())

    if has_infra:
        return "Infrastructure automation and cloud resource management using Terraform or YAML configurations."
    elif has_web and has_backend and has_api:
        return f"Full-stack web application with {', '.join(languages.keys())}. Handles frontend, backend, and API interactions."
    elif has_backend and has_api:
        return f"Backend API service built with {max(languages.items(), key=lambda x: x[1])[0]}. Provides REST endpoints and business logic."
    elif has_web:
        return f"Frontend web application using {', '.join(languages.keys())}. Provides client-side interface and interactions."
    elif has_data and has_backend:
        return f"Data processing application with backend services and database integrations."
    else:
        primary_lang = max(languages.items(), key=lambda x: x[1])[0] if languages else 'Multi-language'
        return f"{primary_lang} application implementing core functionality with modular architecture."

def generate_features_section(languages, services, file_details):
    features = []
    if 'FastAPI' in services or 'Flask' in services:
        features.append("- REST API: HTTP endpoints for data access and manipulation")
    if 'Docker' in services:
        features.append("- Containerization: Docker support for deployment")
    if any('database' in s.lower() for s in services.keys()):
        features.append("- Data Storage: Database integration")
    if 'JavaScript' in languages:
        features.append("- Interactive UI: Dynamic frontend")
    if 'Terraform' in languages:
        features.append("- Infrastructure as Code: Automated provisioning")
    if any('test' in f['file'].lower() for f in file_details) if file_details else False:
        features.append("- Testing: Automated test suite")
    return "\n".join(features) if features else None