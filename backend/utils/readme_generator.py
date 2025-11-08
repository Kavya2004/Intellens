from dotenv import load_dotenv
import os
from openai import OpenAI
import zipfile

# Load .env variables
load_dotenv()

def generate_readme(languages, services, file_details, project_name):
    """Generate README content with project-level summary and file explanations."""
    
    description, file_explanations = generate_ai_project_and_file_summary(
        languages, services, file_details, project_name
    )

    readme = f"# {project_name}\n\n{description}\n\n"

    # File Overview
    if file_explanations:
        readme += "## File Overview\n\n"
        for f, summary in file_explanations.items():
            readme += f"- `{f}`: {summary}\n"
        readme += "\n"

    # Features section
    features = generate_features_section(languages, services, file_details)
    if features:
        readme += f"## Features\n\n{features}\n\n"
    
    # Tech Stack
    if languages:
        readme += "## Tech Stack\n\n"
        for lang in languages.keys():
            readme += f"- **{lang}**\n"
        readme += "\n"

    # Quick Start
    quick_start = generate_quick_start(languages, services)
    if quick_start:
        readme += f"## Quick Start\n\n{quick_start}\n\n"

    # Project structure snippet
    if file_details and len(file_details) > 3:
        readme += "## Project Structure\n\n```\n"
        for file in file_details[:8]:
            readme += f"{file['file']}\n"
        if len(file_details) > 8:
            readme += f"... and {len(file_details) - 8} more files\n"
        readme += "```\n\n"

    return readme


def generate_ai_project_and_file_summary(languages, services, file_details, project_name):
    """Use OpenRouter AI to generate project description and per-file explanations."""
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("⚠️ OPENROUTER_API_KEY not found, using fallback description")
        return (
            generate_smart_fallback_description(languages, services, file_details, project_name),
            {}
        )

    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        # Summarize file snippets for AI context
        summarized_files = []
        for f in file_details[:10]:  # limit to first 10 files
            name = f["file"]
            snippet = f.get("snippet") or f.get("content", "")[:400]
            summarized_files.append(f"File: {name}\nSnippet:\n{snippet}\n")
        context = "\n".join(summarized_files)

        # Step 1: Project overview
        project_prompt = f"""
You are analyzing a software project.
Project name: {project_name}
Languages: {', '.join(languages.keys())}
Technologies: {', '.join(list(services.keys())[:10])}

Here is a sample of project files and their content:
{context}

Explain what the entire project does in 2-3 sentences, and how the files connect
(frontend ↔ backend ↔ database ↔ configs). Write like a human GitHub README introduction.
"""
        
        response = client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct",
            messages=[{"role": "user", "content": project_prompt}],
            max_tokens=500
        )
        project_desc = response.choices[0].message.content.strip()

        # Step 2: Per-file explanations (limited to reduce API calls)
        file_summaries = {}
        for f in file_details[:5]:
            name = f["file"]
            snippet = f.get("snippet") or f.get("content", "")[:500]
            prompt = f"""
Explain briefly what this file does in 1-2 sentences:
File: {name}
{snippet}
"""
            try:
                resp = client.chat.completions.create(
                    model="meta-llama/llama-3.2-3b-instruct",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200
                )
                file_summaries[name] = resp.choices[0].message.content.strip()
            except Exception:
                file_summaries[name] = "Could not summarize this file."

        return project_desc, file_summaries

    except Exception as e:
        print(f"OpenRouter AI error: {e}")
        return (
            generate_smart_fallback_description(languages, services, file_details, project_name),
            {}
        )


def generate_smart_fallback_description(languages, services, file_details, project_name):
    """Fallback description if Gemini AI key is missing."""
    
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
        features.append("- **REST API**: HTTP endpoints for data access and manipulation")
    if 'Docker' in services:
        features.append("- **Containerization**: Docker support for deployment")
    if any('database' in s.lower() for s in services.keys()):
        features.append("- **Data Storage**: Database integration")
    if 'JavaScript' in languages:
        features.append("- **Interactive UI**: Dynamic frontend")
    if 'Terraform' in languages:
        features.append("- **Infrastructure as Code**: Automated provisioning")
    if any('test' in f['file'].lower() for f in file_details) if file_details else False:
        features.append("- **Testing**: Automated test suite")
    return "\n".join(features) if features else None


def generate_quick_start(languages, services):
    steps = []
    if 'Python' in languages:
        steps.append("1. **Install dependencies**:\n   ```bash\n   pip install -r requirements.txt\n   ```")
        if 'FastAPI' in services:
            steps.append("2. **Start server**:\n   ```bash\n   uvicorn main:app --reload\n   ```")
        else:
            steps.append("2. **Run application**:\n   ```bash\n   python main.py\n   ```")
    elif 'JavaScript' in languages:
        steps.append("1. **Install packages**:\n   ```bash\n   npm install\n   ```")
        steps.append("2. **Start development**:\n   ```bash\n   npm start\n   ```")
    elif 'Terraform' in languages:
        steps.append("1. **Initialize**:\n   ```bash\n   terraform init\n   ```")
        steps.append("2. **Plan**:\n   ```bash\n   terraform plan\n   ```")
        steps.append("3. **Apply**:\n   ```bash\n   terraform apply\n   ```")
    if 'Docker' in services:
        steps.append("\n### Docker Alternative\n")
        steps.append("```bash\ndocker build -t app .\ndocker run -p 8000:8000 app\n```")
    return "\n\n".join(steps) if steps else None
