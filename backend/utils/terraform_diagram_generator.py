# -*- coding: utf-8 -*-
import json

def generate_terraform_diagram(languages, services, project_name="Project"):
    """Generate Terraform configuration and AWS architecture diagram based on uploaded project."""
    
    # Analyze project to determine AWS services
    detected_services = _analyze_project_services(languages, services)
    
    # Create tech architecture diagram
    diagram = _create_tech_architecture_diagram(detected_services, project_name)
    
    # Generate Terraform configuration based on detected services
    terraform_config = _generate_terraform_config(diagram['services'], project_name)
    
    return {
        "terraform_config": terraform_config,
        "diagram": diagram
    }

def _create_tech_architecture_diagram(detected_services, project_name):
    """Create tech architecture diagram based on actual project analysis."""
    
    # AWS service mapping based on detected patterns
    service_mapping = {
        'auth': {'id': 'auth', 'name': 'Authentication', 'icon': '🔐', 'color': '#FF6B6B'},
        'api': {'id': 'api', 'name': 'API Server', 'icon': '🔄', 'color': '#FF6B9D'},
        'serverless': {'id': 'serverless', 'name': 'Serverless Functions', 'icon': '🔶', 'color': '#FF9500'},
        'nosql_database': {'id': 'nosql_db', 'name': 'NoSQL Database', 'icon': '⚡', 'color': '#4ECDC4'},
        'sql_database': {'id': 'sql_db', 'name': 'SQL Database', 'icon': '🗄️', 'color': '#4ECDC4'},
        'storage': {'id': 'storage', 'name': 'File Storage', 'icon': '🪣', 'color': '#52C41A'},
        'cdn': {'id': 'cdn', 'name': 'Content Delivery', 'icon': '🌐', 'color': '#722ED1'},
        'container': {'id': 'container', 'name': 'Container Service', 'icon': '📦', 'color': '#FF7A45'},
        'compute': {'id': 'compute', 'name': 'Compute Service', 'icon': '💻', 'color': '#FF9500'}
    }
    
    # Build services based on what was actually detected
    services = []
    step_counter = 1
    workflow_steps = []
    
    for service_type, is_detected in detected_services.items():
        if is_detected and service_type in service_mapping:
            service_config = service_mapping[service_type]
            services.append({
                'id': service_config['id'],
                'name': service_config['name'],
                'icon': service_config['icon'],
                'color': service_config['color'],
                'category': service_type,
                'inputs': [{'id': f"{service_config['id']}_input", 'label': 'Input'}],
                'outputs': [{'id': f"{service_config['id']}_output", 'label': 'Output'}]
            })
            
            # Add workflow step
            workflow_steps.append({
                'step': step_counter,
                'service': service_config['id'],
                'description': f'{service_config["name"]} processing'
            })
            step_counter += 1
    
    # Only add CloudFormation if other AWS services are detected
    if services:
        services.append({
            'id': 'cloudformation',
            'name': 'Infrastructure',
            'icon': '📋',
            'color': '#FF6B9D',
            'category': 'management',
            'inputs': [{'id': 'cloudformation_input', 'label': 'Input'}],
            'outputs': [{'id': 'cloudformation_output', 'label': 'Output'}]
        })
    
    return {
        'title': f'{project_name} Architecture',
        'style': 'tech_diagram',
        'project_name': project_name,
        'services': services,
        'workflow_steps': workflow_steps
    }



def _analyze_project_services(languages, services):
    """Analyze project to determine which AWS services to include."""
    detected = {
        'compute': False,
        'storage': False,
        'nosql_database': False,
        'sql_database': False,
        'database': False,
        'cdn': False,
        'serverless': False,
        'dns': False,
        'auth': False,
        'api': False,
        'container': False
    }
    
    # Combine all text for analysis
    all_text = ' '.join([str(k).lower() + ' ' + str(v) for k, v in {**languages, **services}.items()])
    
    # Enhanced detection patterns
    patterns = {
        'auth': ['auth', 'cognito', 'oauth', 'jwt', 'login', 'user', 'session'],
        'api': ['api', 'graphql', 'rest', 'endpoint', 'appsync', 'gateway'],
        'serverless': ['lambda', 'serverless', 'function', 'event', 'trigger'],
        'container': ['docker', 'container', 'fargate', 'ecs', 'kubernetes', 'k8s'],
        'storage': ['s3', 'storage', 'bucket', 'file', 'upload', 'blob'],
        'database': ['database', 'db', 'data', 'store'],
        'nosql_database': ['dynamo', 'mongodb', 'nosql', 'document', 'dynamodb'],
        'sql_database': ['postgres', 'mysql', 'rds', 'sql', 'relational'],
        'cdn': ['cdn', 'cloudfront', 'web', 'static', 'content'],
        'dns': ['route', 'dns', 'domain', 'routing', 'route53']
    }
    
    # Check for patterns in the combined text
    for category, keywords in patterns.items():
        if any(keyword in all_text for keyword in keywords):
            detected[category] = True
    
    # Only detect AWS services if explicitly mentioned - no language-based assumptions
    
    # Only show services if actually detected - no defaults
    # Remove this fallback to avoid showing AWS services for non-AWS projects
    
    return detected

def _generate_terraform_config(services, project_name):
    """Generate Terraform configuration based on diagram components."""
    terraform_config = {
        "terraform": {
            "required_providers": {
                "aws": {
                    "source": "hashicorp/aws",
                    "version": "~> 5.0"
                }
            }
        },
        "provider": {
            "aws": {
                "region": "us-east-1"
            }
        },
        "resource": {}
    }
    
    # Add resources based on detected services
    for service in services:
        service_id = service["id"]
        
        if service_id == "ec2":
            terraform_config["resource"]["aws_instance"] = {
                "main": {
                    "ami": "ami-0c02fb55956c7d316",
                    "instance_type": "t3.micro",
                    "tags": {
                        "Name": f"{project_name}-ec2",
                        "Environment": "development"
                    }
                }
            }
        elif service_id == "s3":
            bucket_name = f"{project_name.lower().replace('_', '-')}-{hash(project_name) % 10000}"
            terraform_config["resource"]["aws_s3_bucket"] = {
                "main": {
                    "bucket": bucket_name,
                    "tags": {
                        "Name": f"{project_name}-storage",
                        "Environment": "development"
                    }
                }
            }
        elif service_id == "dynamodb":
            terraform_config["resource"]["aws_dynamodb_table"] = {
                "main": {
                    "name": f"{project_name}-table",
                    "billing_mode": "PAY_PER_REQUEST",
                    "hash_key": "id",
                    "attribute": [
                        {
                            "name": "id",
                            "type": "S"
                        }
                    ],
                    "tags": {
                        "Name": f"{project_name}-dynamodb",
                        "Environment": "development"
                    }
                }
            }
        elif service_id == "lambda":
            terraform_config["resource"]["aws_lambda_function"] = {
                "main": {
                    "filename": "lambda_function.zip",
                    "function_name": f"{project_name}-lambda",
                    "role": "${aws_iam_role.lambda_role.arn}",
                    "handler": "index.handler",
                    "runtime": "python3.9",
                    "tags": {
                        "Name": f"{project_name}-lambda",
                        "Environment": "development"
                    }
                }
            }
            terraform_config["resource"]["aws_iam_role"] = {
                "lambda_role": {
                    "name": f"{project_name}-lambda-role",
                    "assume_role_policy": json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": "sts:AssumeRole",
                                "Effect": "Allow",
                                "Principal": {
                                    "Service": "lambda.amazonaws.com"
                                }
                            }
                        ]
                    })
                }
            }
    
    return terraform_config

def generate_terraform_hcl(terraform_config):
    """Convert Terraform config to HCL format with proper formatting."""
    
    def format_value(value, indent=0):
        spaces = "  " * indent
        
        if isinstance(value, dict):
            lines = ["{"]
            for k, v in value.items():
                if isinstance(v, dict):
                    lines.append(f"{spaces}  {k} = {{")
                    lines.extend([f"{spaces}    {line}" for line in format_value(v, 0)])
                    lines.append(f"{spaces}  }}")
                elif isinstance(v, list):
                    lines.append(f"{spaces}  {k} = [")
                    for item in v:
                        if isinstance(item, dict):
                            lines.append(f"{spaces}    {{")
                            lines.extend([f"{spaces}      {line}" for line in format_value(item, 0)])
                            lines.append(f"{spaces}    }},")
                        else:
                            lines.append(f"{spaces}    \"{item}\",")
                    lines.append(f"{spaces}  ]")
                else:
                    formatted_val = format_value(v)
                    lines.append(f"{spaces}  {k} = {formatted_val}")
            lines.append("}")
            return lines
        elif isinstance(value, str):
            if value.startswith("${") and value.endswith("}"):
                return value
            return f'"{value}"'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return f'"{value}"'
    
    hcl_lines = []
    
    # Process top-level blocks
    for block_type, block_content in terraform_config.items():
        if block_type in ["terraform", "provider"]:
            hcl_lines.append(f"{block_type} {{")
            if isinstance(block_content, dict):
                for key, value in block_content.items():
                    if isinstance(value, dict):
                        hcl_lines.append(f"  {key} = {{")
                        for k, v in value.items():
                            formatted_val = format_value(v)
                            if isinstance(formatted_val, list):
                                hcl_lines.extend([f"    {line}" for line in formatted_val])
                            else:
                                hcl_lines.append(f"    {k} = {formatted_val}")
                        hcl_lines.append("  }")
                    else:
                        formatted_val = format_value(value)
                        hcl_lines.append(f"  {key} = {formatted_val}")
            hcl_lines.append("}")
            hcl_lines.append("")
        elif block_type == "resource":
            for resource_type, resources in block_content.items():
                for resource_name, resource_config in resources.items():
                    hcl_lines.append(f'resource "{resource_type}" "{resource_name}" {{')
                    for key, value in resource_config.items():
                        formatted_val = format_value(value)
                        if isinstance(formatted_val, list):
                            hcl_lines.extend([f"  {line}" for line in formatted_val])
                        else:
                            hcl_lines.append(f"  {key} = {formatted_val}")
                    hcl_lines.append("}")
                    hcl_lines.append("")
    
    return "\n".join(hcl_lines).strip()