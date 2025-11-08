# intellens

A project analysis tool that generates interactive architecture workflow diagrams from uploaded code projects.

## Features

- **Workflow Diagrams**: Generates step-by-step architecture workflows similar to AWS diagrams
- **Multi-language Support**: Analyzes Python, JavaScript, Terraform, and more
- **Service Detection**: Identifies cloud services, databases, and technologies
- **Interactive Visualization**: Web-based interface with workflow steps and components
- **Mermaid Export**: Generates Mermaid diagram syntax for documentation
- **AI-Powered Analysis**: Uses Claude AI for intelligent project descriptions and file summaries

## Setup

1. **Environment Setup**: Copy `.env.example` to `.env` and add your Claude API key:
   ```
   CLAUDE_API_KEY=your_claude_api_key_here
   ```

2. **Install Dependencies**: 
   ```bash
   cd backend && pip install -r requirements.txt
   ```

3. **Start Backend**: 
   ```bash
   python3 -m uvicorn main:app --reload
   ```

4. **Open Frontend**: Open `frontend/index.html` in your browser

5. **Upload Project**: Upload a ZIP file containing your project and view the generated workflow diagram

## API Endpoints

- `POST /upload`: Upload project ZIP file and get analysis results including workflow diagram

## Workflow Diagram Output

The tool generates workflow diagrams with:
- Numbered steps showing the analysis process
- Technology components (languages, services)
- Project complexity assessment
- Mermaid diagram syntax for documentation
