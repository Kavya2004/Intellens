# -*- coding: utf-8 -*-
from typing import Dict, List, Any
from .terraform_parser import TerraformParser
from .description_generator import DescriptionGenerator

class AWSInfrastructureDiagramGenerator:
    """Generate AWS infrastructure diagrams similar to AWS Console designer."""
    
    def __init__(self):
        self.parser = TerraformParser()
        self.desc_generator = DescriptionGenerator()
        
        # AWS service categories for sidebar
        self.service_categories = {
            'Compute': {
                'EC2': {'icon': '💻', 'description': 'Virtual servers in the cloud'},
                'Lambda': {'icon': '🔶', 'description': 'Run code without servers'},
                'ECS': {'icon': '📦', 'description': 'Container orchestration'},
                'EKS': {'icon': '📦', 'description': 'Managed Kubernetes'}
            },
            'Storage': {
                'S3': {'icon': '🪣', 'description': 'Object storage service'},
                'EBS': {'icon': '💾', 'description': 'Block storage volumes'},
                'EFS': {'icon': '📁', 'description': 'Managed file system'}
            },
            'Database': {
                'DynamoDB': {'icon': '⚡', 'description': 'NoSQL database'},
                'RDS': {'icon': '🗄️', 'description': 'Relational database'},
                'ElastiCache': {'icon': '🔄', 'description': 'In-memory cache'}
            },
            'Networking': {
                'VPC': {'icon': '🌐', 'description': 'Virtual private cloud'},
                'CloudFront': {'icon': '🌍', 'description': 'Content delivery network'},
                'Route 53': {'icon': '🔄', 'description': 'DNS service'},
                'API Gateway': {'icon': '🔄', 'description': 'API management'}
            },
            'Security': {
                'IAM': {'icon': '🔐', 'description': 'Identity and access management'},
                'Security Groups': {'icon': '🔒', 'description': 'Virtual firewall'},
                'WAF': {'icon': '🛡️', 'description': 'Web application firewall'}
            }
        }
    
    def generate_infrastructure_diagram(self, terraform_directory: str, project_name: str = "Project", languages: Dict = None, services: Dict = None) -> Dict[str, Any]:
        """Generate complete infrastructure diagram from Terraform files or project analysis."""
        
        # First try to parse existing Terraform files
        terraform_data = self.parser.parse_terraform_directory(terraform_directory)
        
        if terraform_data['resources']:
            # Use existing Terraform resources
            diagram_data = {
                'project_name': project_name,
                'sidebar': self._generate_sidebar(),
                'canvas': self._generate_canvas(terraform_data['diagram_data']),
                'panel': self._generate_service_panel(terraform_data['diagram_data']['services']),
                'terraform_config': terraform_data['resources'],
                'summary': {
                    'total_services': terraform_data['diagram_data']['total_services'],
                    'service_types': list(set([s['name'] for s in terraform_data['diagram_data']['services']])),
                    'groups': terraform_data['diagram_data']['groups']
                }
            }
        else:
            # Generate infrastructure based on project analysis
            diagram_data = self._generate_infrastructure_from_project(project_name, languages or {}, services or {})
        
        return diagram_data
    
    def _generate_infrastructure_from_project(self, project_name: str, languages: Dict, services: Dict) -> Dict[str, Any]:
        """Generate infrastructure diagram based on project languages and services."""
        
        # Analyze project to determine appropriate AWS services
        recommended_services = self._recommend_aws_services(languages, services)
        
        if not recommended_services:
            # Show simple project info instead of empty diagram
            return self._generate_simple_project_diagram(project_name, languages, services)
        
        # Create diagram data
        diagram_data = {
            'services': recommended_services,
            'groups': self._group_services(recommended_services),
            'total_services': len(recommended_services)
        }
        
        return {
            'project_name': project_name,
            'sidebar': self._generate_sidebar(),
            'canvas': self._generate_canvas(diagram_data),
            'panel': self._generate_service_panel(recommended_services),
            'terraform_config': self._generate_terraform_from_services(recommended_services, project_name),
            'summary': {
                'total_services': len(recommended_services),
                'service_types': list(set([s['name'] for s in recommended_services])),
                'groups': diagram_data['groups']
            }
        }
    
    def _generate_simple_project_diagram(self, project_name: str, languages: Dict, services: Dict) -> Dict[str, Any]:
        """Generate diagram for simple projects without AWS services."""
        return {
            'project_name': project_name,
            'sidebar': self._generate_sidebar(),
            'canvas': {
                'groups': [{
                    'id': 'app-group',
                    'title': 'Application',
                    'position': {'x': 200, 'y': 200},
                    'services': [self._create_language_component(lang, count) for lang, count in languages.items()]
                }] if languages else [],
                'services': [self._create_language_component(lang, count) for lang, count in languages.items()],
                'connections': [],
                'message': f'Local development project with {len(languages)} programming languages.' if languages else 'No services detected.'
            },
            'panel': {
                'title': 'Local Development Project',
                'description': f'This appears to be a local development project using {list(languages.keys())[0] if languages else "various technologies"}. Consider adding cloud services if you need hosting, databases, or other infrastructure.',
                'services': []
            },
            'terraform_config': {},
            'summary': {
                'total_services': 0,
                'service_types': [],
                'groups': {}
            }
        }
    
    def _generate_empty_diagram(self, project_name: str) -> Dict[str, Any]:
        """Generate empty diagram when no infrastructure can be determined."""
        return {
            'project_name': project_name,
            'sidebar': self._generate_sidebar(),
            'canvas': {
                'groups': [],
                'services': [],
                'message': 'No infrastructure services detected.'
            },
            'panel': {
                'title': 'Simple Project Detected',
                'description': 'This project may not require complex cloud infrastructure. Consider adding databases, APIs, or web hosting needs.',
                'services': []
            },
            'terraform_config': {},
            'summary': {
                'total_services': 0,
                'service_types': [],
                'groups': {}
            }
        }
    
    def _generate_sidebar(self) -> Dict[str, Any]:
        """Generate sidebar with AWS service categories."""
        return {
            'title': 'AWS Services',
            'search_placeholder': 'Search services...',
            'categories': self.service_categories
        }
    
    def _generate_canvas(self, diagram_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate canvas with positioned services."""
        canvas = {
            'groups': [],
            'services': diagram_data['services'],
            'connections': []
        }
        
        # Position services in groups
        groups = diagram_data['groups']
        
        # Application Group (left side)
        if groups.get('Application'):
            app_group = {
                'id': 'app-group',
                'title': 'Application',
                'position': {'x': 50, 'y': 150},
                'services': groups['Application']
            }
            canvas['groups'].append(app_group)
        
        # VM Group (center left)
        if groups.get('Virtual Machine (VM)'):
            vm_group = {
                'id': 'vm-group',
                'title': 'Virtual Machine (VM)',
                'position': {'x': 200, 'y': 200},
                'services': groups['Virtual Machine (VM)']
            }
            canvas['groups'].append(vm_group)
        
        # Database Group (right side)
        if groups.get('Database'):
            db_group = {
                'id': 'database-group',
                'title': 'Database',
                'position': {'x': 500, 'y': 100},
                'services': groups['Database']
            }
            canvas['groups'].append(db_group)
        
        # Service Group (center right)
        if groups.get('Service'):
            service_group = {
                'id': 'service-group',
                'title': 'Services',
                'position': {'x': 350, 'y': 300},
                'services': groups['Service']
            }
            canvas['groups'].append(service_group)
        
        # Security Group (bottom)
        if groups.get('Security'):
            security_group = {
                'id': 'security-group',
                'title': 'Security',
                'position': {'x': 300, 'y': 400},
                'services': groups['Security']
            }
            canvas['groups'].append(security_group)
        
        # Generate connections between services
        canvas['connections'] = self._generate_connections(diagram_data['services'])
        
        return canvas
    
    def _generate_connections(self, services: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate logical connections between services."""
        connections = []
        
        # Connect applications to services
        app_services = [s for s in services if s['category'] == 'Application']
        db_services = [s for s in services if s['category'] == 'Database']
        other_services = [s for s in services if s['category'] == 'Service']
        
        # Connect applications to databases
        for app in app_services:
            for db in db_services:
                connections.append({
                    'from': app['id'],
                    'to': db['id'],
                    'type': 'data_flow',
                    'label': 'Uses'
                })
        
        # Connect applications to other services
        for app in app_services:
            for service in other_services:
                connections.append({
                    'from': app['id'],
                    'to': service['id'],
                    'type': 'integration',
                    'label': 'Integrates with'
                })
        
        return connections
    
    def _generate_service_panel(self, services: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate right panel with service details."""
        if not services:
            return {
                'title': 'No Services Selected',
                'description': 'Click on a service to view details',
                'services': []
            }
        
        # Show details for the first service as default
        primary_service = services[0]
        
        return {
            'title': f"{primary_service['name']} Configuration",
            'service_type': primary_service['name'],
            'description': primary_service['description'],
            'configuration': self._format_service_config(primary_service),
            'terraform_snippet': self._generate_terraform_snippet(primary_service),
            'use_cases': primary_service.get('use_cases', self._get_service_use_cases(primary_service['name'])),
            'characteristics': primary_service.get('characteristics', []),
            'integration_benefits': primary_service.get('integration_benefits', []),
            'all_services': services
        }
    
    def _format_service_config(self, service: Dict[str, Any]) -> Dict[str, Any]:
        """Format service configuration for display."""
        config = service.get('config', {})
        
        formatted_config = {
            'Resource Name': service.get('resource_name', 'N/A'),
            'Service Type': service['name']
        }
        
        # Add specific configuration based on service type
        if service['name'] == 'EC2':
            formatted_config.update({
                'Instance Type': config.get('instance_type', 'Not specified'),
                'AMI': config.get('ami', 'Not specified'),
                'Key Pair': config.get('key_name', 'Not specified')
            })
        elif service['name'] == 'S3':
            formatted_config.update({
                'Bucket Name': config.get('bucket', 'Not specified'),
                'Versioning': config.get('versioning', 'Not configured'),
                'Public Access': 'Blocked' if config.get('block_public_acls') else 'Allowed'
            })
        elif service['name'] == 'DynamoDB':
            formatted_config.update({
                'Table Name': config.get('name', 'Not specified'),
                'Billing Mode': config.get('billing_mode', 'Not specified'),
                'Hash Key': config.get('hash_key', 'Not specified')
            })
        
        # Add tags if available
        if 'tags' in config:
            formatted_config['Tags'] = config['tags']
        
        return formatted_config
    
    def _generate_terraform_snippet(self, service: Dict[str, Any]) -> str:
        """Generate Terraform code snippet for the service."""
        resource_type = service['type']
        resource_name = service['resource_name']
        config = service.get('config', {})
        
        snippet = f'resource "{resource_type}" "{resource_name}" {{\n'
        
        for key, value in config.items():
            if key == 'tags' and isinstance(value, dict):
                snippet += '  tags = {\n'
                for tag_key, tag_value in value.items():
                    snippet += f'    {tag_key} = "{tag_value}"\n'
                snippet += '  }\n'
            elif isinstance(value, str):
                snippet += f'  {key} = "{value}"\n'
            elif isinstance(value, bool):
                snippet += f'  {key} = {str(value).lower()}\n'
            else:
                snippet += f'  {key} = {value}\n'
        
        snippet += '}'
        
        return snippet
    
    def _get_service_use_cases(self, service_name: str) -> List[str]:
        """Get common use cases for AWS services."""
        use_cases = {
            'EC2': [
                'Web application hosting',
                'Development and testing environments',
                'High-performance computing',
                'Backup and disaster recovery'
            ],
            'S3': [
                'Static website hosting',
                'Data backup and archiving',
                'Content distribution',
                'Data lakes and analytics'
            ],
            'DynamoDB': [
                'Mobile and web applications',
                'Gaming applications',
                'IoT data storage',
                'Real-time analytics'
            ],
            'RDS': [
                'Web and mobile applications',
                'E-commerce platforms',
                'Online transaction processing',
                'Data warehousing'
            ],
            'Lambda': [
                'Serverless web applications',
                'Data processing',
                'Real-time file processing',
                'API backends'
            ]
        }
        
        return use_cases.get(service_name, ['General cloud computing tasks'])
    
    def _recommend_aws_services(self, languages: Dict, services: Dict) -> List[Dict[str, Any]]:
        """Create AWS services based on actual detected services and languages."""
        recommended = []
        
        # Map detected services to AWS equivalents
        service_mapping = {
            'AWS S3': 's3',
            'AWS Lambda': 'lambda', 
            'AWS EC2': 'ec2',
            'AWS RDS': 'rds',
            'AWS DynamoDB': 'dynamodb',
            'MongoDB': 'dynamodb',
            'PostgreSQL': 'rds',
            'MySQL': 'rds',
            'Redis': 'elasticache',
            'Docker': 'ecs',
            'Kubernetes': 'eks'
        }
        
        # Add detected languages as components
        for lang_name, count in languages.items():
            recommended.append(self._create_language_component(lang_name, count))
        
        # Add services based on actual detections
        for service_name in services.keys():
            aws_service = service_mapping.get(service_name)
            if aws_service:
                config = self._get_service_config(aws_service, service_name)
                recommended.append(self._create_service(aws_service, f'{aws_service}-service', config))
            else:
                # Add non-AWS services as-is
                recommended.append(self._create_generic_service(service_name, services[service_name]))
        
        # Only add compute if AWS services are detected
        aws_services_detected = any('AWS' in service for service in services.keys())
        
        if aws_services_detected and languages:
            primary_lang = max(languages.items(), key=lambda x: x[1])[0]
            
            # Only add hosting if S3 is detected
            if 'AWS S3' in services and primary_lang in ['JavaScript', 'TypeScript', 'HTML', 'CSS']:
                recommended.append(self._create_service('cloudfront', 'cdn', {'purpose': 'content delivery'}))
            
            # Only add EC2 if compute services are detected
            elif 'AWS EC2' in services or 'AWS Lambda' in services:
                if primary_lang in ['Python', 'Java', 'Go', 'C#', 'Ruby', 'PHP']:
                    recommended.append(self._create_service('ec2', 'app-server', {
                        'instance_type': 't3.micro',
                        'purpose': f'{primary_lang} application server'
                    }))
        
        # Add basic infrastructure only if multiple AWS services detected
        if len(recommended) > 1:
            recommended.extend([
                self._create_service('vpc', 'main-vpc', {'cidr_block': '10.0.0.0/16'}),
                self._create_service('security_group', 'app-sg', {'purpose': 'application security'})
            ])
        
        return recommended
    
    def _get_service_config(self, aws_service: str, original_service: str) -> Dict:
        """Get configuration for AWS service based on detected service."""
        configs = {
            's3': {'purpose': f'Storage for {original_service}'},
            'lambda': {'runtime': 'python3.9', 'purpose': f'Serverless functions'},
            'ec2': {'instance_type': 't3.micro', 'purpose': f'Compute for {original_service}'},
            'rds': {'engine': 'mysql' if 'MySQL' in original_service else 'postgres', 'instance_class': 'db.t3.micro'},
            'dynamodb': {'billing_mode': 'PAY_PER_REQUEST', 'purpose': f'NoSQL database'},
            'elasticache': {'node_type': 'cache.t3.micro', 'engine': 'redis'},
            'ecs': {'purpose': f'Container orchestration'},
            'eks': {'purpose': f'Kubernetes cluster'}
        }
        return configs.get(aws_service, {'purpose': f'Service for {original_service}'})
    
    def _create_language_component(self, language: str, count: int) -> Dict[str, Any]:
        """Create a language component for the diagram."""
        lang_info = self.desc_generator.get_language_description(language, count)
        
        # Merge generated config with file info
        config = lang_info.get('configuration', {})
        config.update({'file_count': count, 'purpose': f'{language} application'})
        
        return {
            'id': f'lang_{language.lower()}',
            'type': 'language',
            'name': language,
            'icon': '💻',
            'category': 'Application',
            'resource_name': lang_info.get('resource_name', f'{language.lower()}-app'),
            'config': config,
            'description': lang_info['description'],
            'use_cases': lang_info['use_cases'],
            'characteristics': lang_info.get('characteristics', []),
            'terraform_config': lang_info.get('terraform_config', f'# {language} application'),
            'inputs': [{'id': f'lang_{language.lower()}_input', 'label': 'Input'}],
            'outputs': [{'id': f'lang_{language.lower()}_output', 'label': 'Output'}]
        }
    
    def _create_generic_service(self, service_name: str, count: int) -> Dict[str, Any]:
        """Create a generic service component."""
        service_info = self.desc_generator.get_service_description(service_name, count)
        
        # Merge generated config with reference info
        config = service_info.get('configuration', {})
        config.update({'references': count, 'purpose': f'{service_name} integration'})
        
        return {
            'id': f'service_{service_name.lower().replace(" ", "_")}',
            'type': 'service',
            'name': service_name,
            'icon': '⚙️',
            'category': 'Service',
            'resource_name': service_info.get('resource_name', service_name.lower().replace(' ', '-')),
            'config': config,
            'description': service_info['description'],
            'use_cases': service_info['use_cases'],
            'integration_benefits': service_info.get('integration_benefits', []),
            'terraform_config': service_info.get('terraform_config', f'# {service_name} configuration'),
            'inputs': [{'id': f'service_{service_name.lower().replace(" ", "_")}_input', 'label': 'Input'}],
            'outputs': [{'id': f'service_{service_name.lower().replace(" ", "_")}_output', 'label': 'Output'}]
        }
    
    def _create_service(self, service_type: str, resource_name: str, config: Dict) -> Dict[str, Any]:
        """Create a service object for the diagram."""
        service_mapping = {
            'ec2': {'name': 'EC2', 'icon': '💻', 'category': 'Virtual Machine (VM)', 'aws_type': 'aws_instance'},
            's3': {'name': 'S3', 'icon': '🪣', 'category': 'Database', 'aws_type': 'aws_s3_bucket'},
            'dynamodb': {'name': 'DynamoDB', 'icon': '⚡', 'category': 'Database', 'aws_type': 'aws_dynamodb_table'},
            'rds': {'name': 'RDS', 'icon': '🗄️', 'category': 'Database', 'aws_type': 'aws_db_instance'},
            'lambda': {'name': 'Lambda', 'icon': '🔶', 'category': 'Database', 'aws_type': 'aws_lambda_function'},
            'cloudfront': {'name': 'CloudFront', 'icon': '🌐', 'category': 'Database', 'aws_type': 'aws_cloudfront_distribution'},
            'ecs': {'name': 'ECS', 'icon': '📦', 'category': 'Database', 'aws_type': 'aws_ecs_service'},
            'ecr': {'name': 'ECR', 'icon': '📦', 'category': 'Database', 'aws_type': 'aws_ecr_repository'},
            'vpc': {'name': 'VPC', 'icon': '🌐', 'category': 'Database', 'aws_type': 'aws_vpc'},
            'security_group': {'name': 'Security Group', 'icon': '🔒', 'category': 'Security', 'aws_type': 'aws_security_group'},
            'elasticache': {'name': 'ElastiCache', 'icon': '🔄', 'category': 'Database', 'aws_type': 'aws_elasticache_cluster'},
            'eks': {'name': 'EKS', 'icon': '📦', 'category': 'Database', 'aws_type': 'aws_eks_cluster'}
        }
        
        service_info = service_mapping.get(service_type, {'name': service_type, 'icon': '☁️', 'category': 'Database', 'aws_type': f'aws_{service_type}'})
        
        return {
            'id': f"{service_info['aws_type']}.{resource_name}",
            'type': service_info['aws_type'],
            'name': service_info['name'],
            'icon': service_info['icon'],
            'category': service_info['category'],
            'resource_name': resource_name,
            'config': config,
            'description': self._get_service_description_from_config(service_info['name'], config),
            'inputs': [{'id': f"{service_info['aws_type']}.{resource_name}_input", 'label': 'Input'}],
            'outputs': [{'id': f"{service_info['aws_type']}.{resource_name}_output", 'label': 'Output'}]
        }
    
    def _get_service_description_from_config(self, service_name: str, config: Dict) -> str:
        """Generate service description from configuration."""
        purpose = config.get('purpose', '')
        if purpose:
            return f"{service_name} for {purpose}"
        
        if service_name == 'EC2':
            return f"EC2 instance ({config.get('instance_type', 't3.micro')})"
        elif service_name == 'RDS':
            return f"RDS database ({config.get('engine', 'mysql')})"
        elif service_name == 'Lambda':
            return f"Lambda function ({config.get('runtime', 'python3.9')})"
        
        return f"{service_name} service"
    
    def _group_services(self, services: List[Dict]) -> Dict[str, List[Dict]]:
        """Group services by category."""
        groups = {'Application': [], 'Virtual Machine (VM)': [], 'Database': [], 'Service': [], 'Security': []}
        
        for service in services:
            category = service['category']
            if category in groups:
                groups[category].append(service)
        
        return groups
    
    def _generate_terraform_from_services(self, services: List[Dict], project_name: str) -> Dict[str, Any]:
        """Generate Terraform configuration from recommended services."""
        terraform_config = {}
        
        for service in services:
            resource_key = service['id']
            terraform_config[resource_key] = {
                'type': service['type'],
                'name': service['resource_name'],
                'config': {
                    **service['config'],
                    'tags': {
                        'Name': f"{project_name}-{service['resource_name']}",
                        'Environment': 'development',
                        'Project': project_name
                    }
                }
            }
        
        return terraform_config