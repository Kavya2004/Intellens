import os
import re
import ast
import json
from collections import defaultdict

# Language detection by file extension
LANGUAGE_MAP = {
    '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript', '.java': 'Java',
    '.c': 'C', '.cpp': 'C++', '.cc': 'C++', '.cxx': 'C++', '.h': 'C/C++',
    '.cs': 'C#', '.go': 'Go', '.rs': 'Rust', '.rb': 'Ruby', '.php': 'PHP',
    '.tf': 'Terraform', '.yml': 'YAML', '.yaml': 'YAML', '.json': 'JSON',
    '.sh': 'Shell', '.bash': 'Bash', '.dockerfile': 'Docker', '.sql': 'SQL'
}

from .auto_service_detector import detect_all_services, detect_all_services_with_references
from .auto_language_detector import auto_detect_languages

def detect_language_and_services(folder_path):
    """Parse all files and detect languages and services automatically."""
    connections = []
    file_details = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            ext = os.path.splitext(file)[1].lower()
            
            # Skip binary/large files
            if ext in ['.exe', '.bin', '.so', '.dll', '.zip', '.tar', '.gz']:
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Detect languages for this file
                from .auto_language_detector import detect_language_from_content, detect_language_from_shebang
                file_languages = []
                
                # Check shebang first
                shebang_lang = detect_language_from_shebang(content)
                if shebang_lang:
                    file_languages.append(shebang_lang)
                else:
                    # Detect from content patterns
                    detected_langs = detect_language_from_content(content, file)
                    file_languages.extend(detected_langs)
                    
                    # Fallback: extension mapping
                    if not detected_langs and ext in LANGUAGE_MAP:
                        file_languages.append(LANGUAGE_MAP[ext])
                
                # Detect services for this file
                from .auto_service_detector import auto_detect_services
                file_services = auto_detect_services(content)
                
                # Store file details
                if file_languages or file_services:
                    file_details.append({
                        'file': relative_path,
                        'languages': file_languages,
                        'services': list(file_services.keys())
                    })
                
                # Parse specific file types for connections
                if ext == '.py':
                    connections.extend(parse_python_imports(content, file))
                elif ext == '.tf':
                    connections.extend(parse_terraform_deps(content, file))
                    
            except Exception:
                continue
    
    # Auto-detect languages and services (overall counts)
    languages = auto_detect_languages(folder_path)
    services = detect_all_services(folder_path)
    
    return languages, services, connections, file_details

def detect_language_and_services_with_references(folder_path):
    """Enhanced version that includes service code references."""
    connections = []
    file_details = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            ext = os.path.splitext(file)[1].lower()
            
            if ext in ['.exe', '.bin', '.so', '.dll', '.zip', '.tar', '.gz']:
                continue
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                from .auto_language_detector import detect_language_from_content, detect_language_from_shebang
                file_languages = []
                
                shebang_lang = detect_language_from_shebang(content)
                if shebang_lang:
                    file_languages.append(shebang_lang)
                else:
                    detected_langs = detect_language_from_content(content, file)
                    file_languages.extend(detected_langs)
                    
                    if not detected_langs and ext in LANGUAGE_MAP:
                        file_languages.append(LANGUAGE_MAP[ext])
                
                from .auto_service_detector import auto_detect_services
                file_services = auto_detect_services(content)
                
                if file_languages or file_services:
                    file_details.append({
                        'file': relative_path,
                        'languages': file_languages,
                        'services': list(file_services.keys())
                    })
                
                if ext == '.py':
                    connections.extend(parse_python_imports(content, file))
                elif ext == '.tf':
                    connections.extend(parse_terraform_deps(content, file))
                    
            except Exception:
                continue
    
    languages = auto_detect_languages(folder_path)
    services_with_refs = detect_all_services_with_references(folder_path)
    
    return languages, services_with_refs, connections, file_details

def parse_python_imports(content, filename):
    """Extract Python import relationships."""
    connections = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    connections.append((filename, alias.name))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    connections.append((filename, node.module))
    except:
        pass
    return connections

def parse_terraform_deps(content, filename):
    """Extract Terraform dependencies."""
    connections = []
    depends_pattern = r'depends_on\s*=\s*\[(.*?)\]'
    matches = re.findall(depends_pattern, content, re.DOTALL)
    for match in matches:
        deps = re.findall(r'[\w.]+', match)
        for dep in deps:
            connections.append((dep, filename))
    return connections