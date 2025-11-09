def generate_layered_architecture_diagram(languages, services, project_name="Project", file_details=None):
    """Generate layered architecture diagram with actual file names."""
    
    # Categorize actual files into layers
    layers = categorize_actual_files_into_layers(file_details or [])
    
    # Generate ASCII diagram
    ascii_diagram = create_ascii_layered_diagram(layers)
    
    return {
        "style": "layered_architecture",
        "title": f"{project_name} - Layered Architecture",
        "ascii_diagram": ascii_diagram,
        "layers": layers,
        "layer_summary": generate_layer_summary(layers)
    }

def categorize_actual_files_into_layers(file_details):
    """Categorize actual files into architectural layers based on file paths and content."""
    
    layers = {
        "frontend": {
            "name": "🌐 Frontend Layer",
            "icon": "🌐",
            "files": [],
            "description": "User interface and client-side logic"
        },
        "backend": {
            "name": "🔧 Backend Layer", 
            "icon": "🔧",
            "files": [],
            "description": "Server-side logic and APIs"
        },
        "data": {
            "name": "💾 Data Layer",
            "icon": "💾", 
            "files": [],
            "description": "Data storage and management"
        },
        "config": {
            "name": "⚙️ Configuration Layer",
            "icon": "⚙️",
            "files": [],
            "description": "Configuration and deployment files"
        }
    }
    
    # Frontend indicators
    frontend_paths = ['frontend', 'client', 'ui', 'web', 'public', 'static', 'assets', 'components', 'pages', 'src/components', 'src/pages']
    frontend_extensions = ['.html', '.css', '.scss', '.sass', '.less', '.jsx', '.tsx', '.vue', '.svelte']
    frontend_files = ['index.html', 'app.js', 'main.js', 'bundle.js', 'style.css', 'styles.css']
    frontend_services = ['react', 'vue', 'angular', 'next.js', 'svelte', 'frontend', 'jquery', 'bootstrap']
    
    # Backend indicators  
    backend_paths = ['backend', 'server', 'api', 'src/server', 'src/api', 'controllers', 'routes', 'middleware', 'models', 'services']
    backend_extensions = ['.py', '.java', '.cs', '.go', '.rb', '.php', '.rs', '.kt', '.scala']
    backend_files = ['server.js', 'app.py', 'main.py', 'index.js', 'server.py', 'api.py']
    backend_services = ['node.js', 'express', 'django', 'flask', 'spring', 'api', 'server', 'fastapi']
    
    # Data indicators
    data_paths = ['database', 'db', 'data', 'migrations', 'schemas', 'models/db']
    data_extensions = ['.sql', '.db', '.sqlite', '.mdb']
    data_files = ['schema.sql', 'migrations.sql', 'database.py', 'models.py']
    data_services = ['mongodb', 'postgresql', 'mysql', 'redis', 'database', 'sql', 'nosql', 'sqlite']
    
    # Config indicators
    config_paths = ['config', 'configs', 'deployment', 'infrastructure', 'terraform', '.github', 'docker']
    config_extensions = ['.json', '.yaml', '.yml', '.toml', '.ini', '.env', '.tf', '.dockerfile']
    config_files = ['package.json', 'requirements.txt', 'Dockerfile', 'docker-compose.yml', 'terraform.tf', '.env', 'config.json']
    
    def categorize_file(file_info):
        """Determine which layer a file belongs to."""
        file_path = file_info['file'].lower()
        file_name = file_path.split('/')[-1]
        file_ext = '.' + file_name.split('.')[-1] if '.' in file_name else ''
        
        # Check services first (most reliable)
        services = [s.lower() for s in file_info.get('services', [])]
        
        if any(service in frontend_services for service in services):
            return 'frontend'
        elif any(service in backend_services for service in services):
            return 'backend'
        elif any(service in data_services for service in services):
            return 'data'
        
        # Check file path
        if any(path in file_path for path in frontend_paths):
            return 'frontend'
        elif any(path in file_path for path in backend_paths):
            return 'backend'
        elif any(path in file_path for path in data_paths):
            return 'data'
        elif any(path in file_path for path in config_paths):
            return 'config'
        
        # Check file extension
        if file_ext in frontend_extensions:
            return 'frontend'
        elif file_ext in backend_extensions:
            return 'backend'
        elif file_ext in data_extensions:
            return 'data'
        elif file_ext in config_extensions:
            return 'config'
        
        # Check specific file names
        if file_name in frontend_files:
            return 'frontend'
        elif file_name in backend_files:
            return 'backend'
        elif file_name in data_files:
            return 'data'
        elif file_name in config_files:
            return 'config'
        
        # Default to backend for code files, config for others
        if file_ext in ['.js', '.ts', '.py', '.java', '.cs', '.go', '.rb', '.php']:
            return 'backend'
        else:
            return 'config'
    
    # Categorize each file
    for file_info in file_details:
        layer = categorize_file(file_info)
        
        # Create file entry with languages and services
        file_entry = {
            'name': file_info['file'],
            'languages': file_info.get('languages', []),
            'services': file_info.get('services', [])
        }
        
        layers[layer]['files'].append(file_entry)
    
    return layers

def create_ascii_layered_diagram(layers):
    """Create ASCII-style layered architecture diagram with actual file names."""
    
    diagram_lines = []
    box_width = 55  # Fixed box width
    content_width = box_width - 4  # Account for "│ " and " │"
    
    # Process layers in order: frontend -> backend -> data -> config
    layer_order = ["frontend", "backend", "data", "config"]
    
    for i, layer_key in enumerate(layer_order):
        layer = layers[layer_key]
        
        # Skip empty layers
        if not layer["files"]:
            continue
            
        # Layer header
        diagram_lines.append(f"{layer['name']}")
        diagram_lines.append("┌" + "─" * (box_width - 2) + "┐")
        
        # Add actual files (limit to first 6 files to avoid too long diagrams)
        files_to_show = layer["files"][:6]
        
        for file_entry in files_to_show:
            file_name = file_entry['name']
            
            # Add language/service info if available
            tech_info = []
            if file_entry['languages']:
                tech_info.extend(file_entry['languages'][:1])  # Only first language
            if file_entry['services']:
                tech_info.extend(file_entry['services'][:1])   # Only first service
            
            if tech_info:
                tech_str = f" ({tech_info[0]})"
            else:
                tech_str = ""
            
            # Create display string and truncate if needed
            file_display = file_name + tech_str
            
            if len(file_display) > content_width:
                # Truncate file name to fit
                available_for_name = content_width - len(tech_str) - 3  # 3 for "..."
                if available_for_name > 10:  # Minimum readable length
                    truncated_name = file_name[:available_for_name] + "..."
                    file_display = truncated_name + tech_str
                else:
                    # If tech info is too long, just show truncated file name
                    file_display = file_name[:content_width-3] + "..."
            
            # Pad to exact width
            padded_display = file_display.ljust(content_width)
            diagram_lines.append(f"│ {padded_display} │")
        
        # Show count if there are more files
        if len(layer["files"]) > 6:
            remaining = len(layer["files"]) - 6
            more_text = f"... and {remaining} more files"
            padded_more = more_text.ljust(content_width)
            diagram_lines.append(f"│ {padded_more} │")
        
        # Layer footer
        diagram_lines.append("└" + "─" * (box_width - 2) + "┘")
        
        # Add connection arrow (except for last layer)
        if i < len(layer_order) - 1:
            # Check if next layer has content
            next_layers = layer_order[i+1:]
            has_next_content = any(layers[next_key]["files"] for next_key in next_layers)
            
            if has_next_content:
                arrow_padding = " " * ((box_width - 11) // 2)  # Center the arrow
                diagram_lines.append(f"{arrow_padding}↕ Data Flow")
        
        diagram_lines.append("")  # Empty line between layers
    
    return "\n".join(diagram_lines)

def generate_layer_summary(layers):
    """Generate a summary of each layer with actual file counts."""
    
    summary = {}
    
    for layer_key, layer_data in layers.items():
        file_count = len(layer_data["files"])
        
        if file_count > 0:
            # Count unique languages and services
            all_languages = set()
            all_services = set()
            
            for file_entry in layer_data["files"]:
                all_languages.update(file_entry.get('languages', []))
                all_services.update(file_entry.get('services', []))
            
            summary[layer_key] = {
                "name": layer_data["name"],
                "description": layer_data["description"],
                "file_count": file_count,
                "languages": list(all_languages),
                "services": list(all_services),
                "complexity": "High" if file_count > 10 else 
                            "Medium" if file_count > 3 else "Low"
            }
    
    return summary