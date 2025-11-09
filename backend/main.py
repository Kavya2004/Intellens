from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import os, zipfile, shutil, tempfile
from utils.parser import parse_terraform_files
from utils.diagram_builder import build_graph_json
from utils.multi_parser import detect_language_and_services, detect_language_and_services_with_references
from utils.enhanced_diagram_builder import build_comprehensive_diagram
from utils.workflow_diagram_builder import build_workflow_diagram, generate_mermaid_workflow
from utils.terraform_diagram_generator import generate_terraform_diagram, generate_terraform_hcl
from utils.aws_diagram_generator import AWSInfrastructureDiagramGenerator
from utils.readme_generator import generate_readme
from utils.frontend_preview_generator import generate_frontend_preview
from utils.layered_diagram_generator import generate_layered_architecture_diagram
from utils.project_overview_generator import generate_project_overview

app = FastAPI(title="Intellens")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_project(file: UploadFile = File(...)):
    """Upload a zip file containing project files."""
    # Save uploaded file
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Extract the zip
    extract_dir = tempfile.mkdtemp()
    with zipfile.ZipFile(temp_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    # Parse all files for languages and services with references
    languages, services_with_refs, all_connections, file_details = detect_language_and_services_with_references(extract_dir)
    
    # Convert to legacy format for backward compatibility
    services = {name: data['count'] for name, data in services_with_refs.items()}
    
    # Also parse Terraform specifically for backward compatibility
    tf_services, tf_connections = parse_terraform_files(extract_dir)
    
    # Build comprehensive diagram
    diagram_data = build_comprehensive_diagram(languages, services, all_connections)
    
    # Build workflow diagram
    workflow_data = build_workflow_diagram(languages, services, file.filename.split('.')[0], file_details)
    
    # Generate Mermaid syntax
    mermaid_syntax = generate_mermaid_workflow(languages, services, file.filename.split('.')[0])
    
    # Generate Terraform diagram
    terraform_data = generate_terraform_diagram(languages, services, file.filename.split('.')[0])
    terraform_hcl = generate_terraform_hcl(terraform_data['terraform_config'])
    
    # Generate AWS Infrastructure diagram from actual Terraform files or project analysis
    aws_generator = AWSInfrastructureDiagramGenerator()
    aws_infrastructure_data = aws_generator.generate_infrastructure_diagram(
        extract_dir, 
        file.filename.split('.')[0],
        languages,
        services
    )
    
    # Generate README
    readme_content = generate_readme(languages, services, file_details, file.filename.split('.')[0])
    
    # Generate frontend preview
    frontend_preview = generate_frontend_preview(languages, services, file_details)
    
    # Generate layered architecture diagram
    layered_diagram = generate_layered_architecture_diagram(languages, services, file.filename.split('.')[0], file_details)
    
    # Generate project overview
    project_overview = generate_project_overview(languages, services, file_details, file.filename.split('.')[0])
    
    # Save README to project (create a downloadable version)
    readme_filename = f"{file.filename.split('.')[0]}_README.md"
    readme_path = os.path.join(UPLOAD_DIR, readme_filename)
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Legacy diagram for TF only
    tf_diagram_data = build_graph_json(tf_services, tf_connections)

    # Cleanup
    os.remove(temp_path)
    shutil.rmtree(extract_dir)

    response_data = {
        "comprehensive_diagram": diagram_data,
        "workflow_diagram": workflow_data,
        "mermaid_syntax": mermaid_syntax,
        "terraform_diagram": tf_diagram_data,
        "terraform_infrastructure": terraform_data,
        "terraform_hcl": terraform_hcl,
        "aws_infrastructure_diagram": aws_infrastructure_data,
        "languages": languages,
        "services": services,
        "services_with_references": services_with_refs,
        "terraform_services": tf_services,
        "file_details": file_details,
        "readme_content": readme_content,
        "readme_filename": readme_filename,
        "frontend_preview": frontend_preview,
        "layered_diagram": layered_diagram,
        "project_overview": project_overview
    }
    
    return JSONResponse(content=response_data, media_type="application/json; charset=utf-8")

@app.get("/download-readme/{filename}")
async def download_readme(filename: str):
    """Download generated README file."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='text/markdown'
        )
    return JSONResponse({"error": "File not found"}, status_code=404)