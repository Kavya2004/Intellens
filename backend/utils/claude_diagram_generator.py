import anthropic
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Claude API
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

def generate_architecture_diagram(languages, services, connections, file_structure):
    """Generate professional architecture diagram using Claude AI."""
    
    # Create context for Claude
    context = f"""
    Analyze this project and create a detailed architecture flow diagram:
    
    Languages: {languages}
    Services: {services}
    Connections: {connections[:10]}  # Limit for context
    
    Generate a JSON response with this structure:
    {{
        "title": "Project Architecture",
        "components": [
            {{
                "id": "comp1",
                "name": "Component Name",
                "type": "service|database|api|frontend|backend",
                "description": "Brief description",
                "position": {{"x": 100, "y": 100}},
                "icon": "service-icon-name"
            }}
        ],
        "flows": [
            {{
                "from": "comp1",
                "to": "comp2",
                "label": "Data flow description",
                "step": 1
            }}
        ],
        "description": "Overall architecture description"
    }}
    
    Create a professional flow showing:
    1. User interactions
    2. Data flow between components
    3. Service integrations
    4. Processing steps
    5. Output generation
    
    Make it similar to AWS architecture diagrams with numbered steps and clear flow.
    """
    
    try:
        if not CLAUDE_API_KEY:
            return create_fallback_diagram(languages, services)
            
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": context}
            ]
        )
        
        # Parse JSON response
        diagram_data = json.loads(response.content[0].text)
        return diagram_data
        
    except Exception as e:
        # Fallback diagram if API fails
        return create_fallback_diagram(languages, services)

def create_fallback_diagram(languages, services):
    """Create comprehensive workflow with every component numbered."""
    components = []
    flows = []
    all_components = []
    
    # User entry point
    components.append({
        "id": "user",
        "name": "User",
        "type": "user",
        "description": "Initiates application",
        "position": {"x": 50, "y": 200}
    })
    
    # Better grid positioning
    cols = 4
    x_start = 200
    y_start = 80
    x_spacing = 180
    y_spacing = 120
    component_index = 0
    
    # Add each language as separate component
    for lang_name, file_count in languages.items():
        row = component_index // cols
        col = component_index % cols
        x_pos = x_start + (col * x_spacing)
        y_pos = y_start + (row * y_spacing)
        
        lang_id = f"lang_{component_index + 1}"
        components.append({
            "id": lang_id,
            "name": lang_name,
            "type": "code",
            "description": f"Processes {file_count} {lang_name} files",
            "position": {"x": x_pos, "y": y_pos}
        })
        all_components.append(lang_id)
        component_index += 1
    
    # Add each service as separate component
    for service_name, ref_count in services.items():
        row = component_index // cols
        col = component_index % cols
        x_pos = x_start + (col * x_spacing)
        y_pos = y_start + (row * y_spacing)
        
        service_id = f"svc_{component_index + 1}"
        
        # Determine type and action
        if any(k in service_name.lower() for k in ['aws', 'cloud', 'azure']):
            svc_type, action = 'cloud', 'manages cloud resources'
        elif any(k in service_name.lower() for k in ['sql', 'mongo', 'redis', 'db']):
            svc_type, action = 'database', 'stores and queries data'
        elif any(k in service_name.lower() for k in ['api', 'rest']):
            svc_type, action = 'api', 'handles API requests'
        elif any(k in service_name.lower() for k in ['docker', 'container']):
            svc_type, action = 'backend', 'containerizes applications'
        else:
            svc_type, action = 'service', 'processes requests'
        
        components.append({
            "id": service_id,
            "name": service_name,
            "type": svc_type,
            "description": f"{action} with {ref_count} references",
            "position": {"x": x_pos, "y": y_pos}
        })
        all_components.append(service_id)
        component_index += 1
    
    # Create numbered flows connecting everything
    flow_step = 1
    
    # User connects to first component
    if all_components:
        flows.append({
            "from": "user",
            "to": all_components[0],
            "label": "Starts application",
            "step": flow_step
        })
        flow_step += 1
    
    # Chain all components together
    for i in range(len(all_components) - 1):
        current = all_components[i]
        next_comp = all_components[i + 1]
        
        # Get component names for dynamic labels
        current_comp = next(c for c in components if c['id'] == current)
        next_comp_obj = next(c for c in components if c['id'] == next_comp)
        
        # Dynamic flow labels
        if current_comp['type'] == 'code' and next_comp_obj['type'] == 'database':
            label = f"Sends data to {next_comp_obj['name']}"
        elif current_comp['type'] == 'database' and next_comp_obj['type'] == 'cloud':
            label = f"Backs up to {next_comp_obj['name']}"
        elif current_comp['type'] == 'code' and next_comp_obj['type'] == 'api':
            label = f"Makes calls to {next_comp_obj['name']}"
        else:
            label = f"Connects to {next_comp_obj['name']}"
        
        flows.append({
            "from": current,
            "to": next_comp,
            "label": label,
            "step": flow_step
        })
        flow_step += 1
    
    # Add final output if we have components
    if all_components:
        components.append({
            "id": "output",
            "name": "Application Output",
            "type": "frontend",
            "description": "Final result delivered to user",
            "position": {"x": 450, "y": 500}
        })
        
        flows.append({
            "from": all_components[-1],
            "to": "output",
            "label": "Delivers final output",
            "step": flow_step
        })
    
    total_components = len(languages) + len(services)
    return {
        "title": "Complete Project Architecture",
        "components": components,
        "flows": flows,
        "description": f"Workflow showing {total_components} components with numbered steps"
    }