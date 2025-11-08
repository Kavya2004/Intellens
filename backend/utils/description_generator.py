import os
import anthropic
from typing import Dict, List

class DescriptionGenerator:
    """Generate descriptions for programming languages and services using Claude."""
    
    def __init__(self):
        # Configure Claude API
        api_key = os.getenv('CLAUDE_API_KEY')
        if api_key:
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            self.client = None
    
    def get_language_description(self, language: str, file_count: int) -> Dict[str, any]:
        """Get comprehensive description for a programming language."""
        if not self.client:
            return self._get_fallback_language_description(language, file_count)
        
        try:
            prompt = f"""
            Provide a comprehensive description for the programming language: {language}
            
            Format your response as JSON with these exact keys:
            {{
                "description": "Brief 2-3 sentence description of what {language} is and its main purpose",
                "use_cases": ["use case 1", "use case 2", "use case 3", "use case 4"],
                "characteristics": ["key feature 1", "key feature 2", "key feature 3"],
                "configuration": {{"key1": "value1", "key2": "value2"}},
                "resource_name": "suggested-resource-name",
                "terraform_config": "Complete terraform resource block for {language} deployment"
            }}
            
            Keep descriptions concise and practical. Focus on real-world applications.
            """
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse JSON response
            import json
            try:
                result = json.loads(response.content[0].text.strip())
                return {
                    'description': result['description'],
                    'use_cases': result['use_cases'],
                    'characteristics': result['characteristics'],
                    'configuration': result.get('configuration', {}),
                    'resource_name': result.get('resource_name', f'{language.lower()}-app'),
                    'terraform_config': result.get('terraform_config', f'# {language} application configuration')
                }
            except (json.JSONDecodeError, KeyError):
                return self._get_fallback_language_description(language, file_count)
            
        except Exception as e:
            print(f"Claude API error for {language}: {e}")
            return self._get_fallback_language_description(language, file_count)
    
    def get_service_description(self, service: str, reference_count: int) -> Dict[str, any]:
        """Get comprehensive description for a service or technology."""
        if not self.client:
            return self._get_fallback_service_description(service, reference_count)
        
        try:
            prompt = f"""
            Provide a comprehensive description for the technology/service: {service}
            
            Format your response as JSON with these exact keys:
            {{
                "description": "Brief 2-3 sentence description of what {service} is and its main purpose",
                "use_cases": ["use case 1", "use case 2", "use case 3", "use case 4"],
                "integration_benefits": ["benefit 1", "benefit 2", "benefit 3"],
                "configuration": {{"key1": "value1", "key2": "value2"}},
                "resource_name": "suggested-resource-name",
                "terraform_config": "Complete terraform resource block for {service} deployment"
            }}
            
            Keep descriptions concise and practical. Focus on real-world applications and integration benefits.
            """
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse JSON response
            import json
            try:
                result = json.loads(response.content[0].text.strip())
                return {
                    'description': result['description'],
                    'use_cases': result['use_cases'],
                    'integration_benefits': result['integration_benefits'],
                    'configuration': result.get('configuration', {}),
                    'resource_name': result.get('resource_name', service.lower().replace(' ', '-')),
                    'terraform_config': result.get('terraform_config', f'# {service} configuration')
                }
            except (json.JSONDecodeError, KeyError):
                return self._get_fallback_service_description(service, reference_count)
            
        except Exception as e:
            print(f"Claude API error for {service}: {e}")
            return self._get_fallback_service_description(service, reference_count)
    
    def _get_fallback_language_description(self, language: str, file_count: int) -> Dict[str, any]:
        """Fallback descriptions when Gemini is unavailable."""
        fallbacks = {
            'Python': {
                'description': 'Python is a high-level, interpreted programming language known for its simplicity and readability. It\'s widely used for web development, data science, automation, and artificial intelligence applications.',
                'use_cases': ['Web development with Django/Flask', 'Data science and machine learning', 'Automation and scripting', 'API development'],
                'characteristics': ['Easy to learn and read', 'Extensive library ecosystem', 'Cross-platform compatibility']
            },
            'JavaScript': {
                'description': 'JavaScript is a dynamic programming language primarily used for web development. It enables interactive web pages and is essential for front-end development, with growing use in back-end development through Node.js.',
                'use_cases': ['Frontend web development', 'Backend development with Node.js', 'Mobile app development', 'Desktop applications'],
                'characteristics': ['Dynamic and flexible', 'Event-driven programming', 'Large ecosystem of frameworks']
            },
            'Go': {
                'description': 'Go is a statically typed, compiled programming language developed by Google. It\'s designed for simplicity, efficiency, and excellent concurrency support, making it ideal for system programming and cloud services.',
                'use_cases': ['Microservices and APIs', 'Cloud infrastructure tools', 'System programming', 'Network programming'],
                'characteristics': ['Fast compilation and execution', 'Built-in concurrency support', 'Simple and clean syntax']
            },
            'Rust': {
                'description': 'Rust is a systems programming language focused on safety, speed, and concurrency. It prevents common programming errors like null pointer dereferences and buffer overflows while maintaining high performance.',
                'use_cases': ['System programming', 'Web assembly applications', 'Blockchain development', 'Game engine development'],
                'characteristics': ['Memory safety without garbage collection', 'Zero-cost abstractions', 'Excellent performance']
            },
            'JSON': {
                'description': 'JSON (JavaScript Object Notation) is a lightweight, text-based data interchange format. It\'s easy for humans to read and write, and easy for machines to parse and generate.',
                'use_cases': ['API data exchange', 'Configuration files', 'Data storage', 'Web application communication'],
                'characteristics': ['Human-readable format', 'Language-independent', 'Lightweight and efficient']
            },
            'SQL': {
                'description': 'SQL (Structured Query Language) is a domain-specific language for managing and querying relational databases. It\'s the standard language for relational database management systems.',
                'use_cases': ['Database queries and management', 'Data analysis and reporting', 'Database schema design', 'Data migration'],
                'characteristics': ['Declarative syntax', 'Standardized across databases', 'Powerful data manipulation']
            },
            'YAML': {
                'description': 'YAML is a human-readable data serialization standard commonly used for configuration files and data exchange. It\'s designed to be easily readable by both humans and machines.',
                'use_cases': ['Configuration files', 'CI/CD pipelines', 'Docker Compose files', 'Kubernetes manifests'],
                'characteristics': ['Human-readable format', 'Indentation-based structure', 'Supports complex data types']
            },
            'PHP': {
                'description': 'PHP is a server-side scripting language designed for web development. It\'s embedded in HTML and is particularly suited for creating dynamic web pages and web applications.',
                'use_cases': ['Web development', 'Content management systems', 'E-commerce platforms', 'Server-side scripting'],
                'characteristics': ['Easy to learn and deploy', 'Large community and ecosystem', 'Built-in web development features'],
                'resource_name': 'php-app',
                'terraform_config': '# PHP application\nresource "aws_instance" "php-app" {\n  ami = "ami-12345678"\n  instance_type = "t3.micro"\n}'
            },
            'TypeScript': {
                'description': 'TypeScript is a strongly typed programming language that builds on JavaScript by adding static type definitions. It helps catch errors early and makes JavaScript development more robust.',
                'use_cases': ['Large-scale JavaScript applications', 'Frontend frameworks', 'Node.js backend development', 'Enterprise applications'],
                'characteristics': ['Static typing for JavaScript', 'Enhanced IDE support', 'Compiles to clean JavaScript'],
                'resource_name': 'typescript-app',
                'terraform_config': '# TypeScript application\nresource "aws_s3_bucket" "typescript-app" {\n  bucket = "my-typescript-app"\n}'
            },
            'Ruby': {
                'description': 'Ruby is a dynamic, object-oriented programming language focused on simplicity and productivity. It has an elegant syntax that is natural to read and easy to write.',
                'use_cases': ['Web development with Ruby on Rails', 'Automation and scripting', 'Prototyping', 'DevOps tools'],
                'characteristics': ['Elegant and expressive syntax', 'Object-oriented design', 'Strong community and gems ecosystem']
            }
        }
        

        
        return fallbacks.get(language, {
            'description': f'{language} is a programming language used in this project.',
            'use_cases': ['Software development', 'Application building', 'Problem solving', 'System implementation'],
            'characteristics': ['Programming language', 'Used in software development', 'Part of this project'],
            'configuration': {'type': language.lower(), 'files': file_count},
            'resource_name': f'{language.lower()}-app',
            'terraform_config': f'# {language} application\nresource "aws_instance" "{language.lower()}-app" {{\n  ami = "ami-12345678"\n  instance_type = "t3.micro"\n}}'
        })
    
    def _get_fallback_service_description(self, service: str, reference_count: int) -> Dict[str, any]:
        """Fallback descriptions for services when Gemini is unavailable."""
        fallbacks = {
            'Docker': {
                'description': 'Docker is a containerization platform that packages applications and their dependencies into lightweight, portable containers. It ensures consistent deployment across different environments.',
                'use_cases': ['Application containerization', 'Microservices deployment', 'Development environment consistency', 'CI/CD pipelines'],
                'integration_benefits': ['Consistent deployments', 'Resource efficiency', 'Scalability and portability']
            },
            'Redis': {
                'description': 'Redis is an in-memory data structure store used as a database, cache, and message broker. It supports various data structures and provides high performance for real-time applications.',
                'use_cases': ['Caching layer', 'Session storage', 'Real-time analytics', 'Message queuing'],
                'integration_benefits': ['Improved application performance', 'Reduced database load', 'Fast data access']
            },
            'PostgreSQL': {
                'description': 'PostgreSQL is a powerful, open-source relational database system known for its reliability, feature robustness, and performance. It supports both SQL and JSON querying.',
                'use_cases': ['Web applications', 'Data warehousing', 'Geospatial applications', 'Financial systems'],
                'integration_benefits': ['ACID compliance', 'Advanced SQL features', 'Extensibility and reliability']
            },
            'MongoDB': {
                'description': 'MongoDB is a NoSQL document database that stores data in flexible, JSON-like documents. It\'s designed for scalability and developer productivity.',
                'use_cases': ['Content management', 'Real-time analytics', 'IoT applications', 'Mobile applications'],
                'integration_benefits': ['Flexible schema design', 'Horizontal scalability', 'Developer-friendly']
            }
        }
        
        service_fallbacks = {
            'React': {
                'description': 'React is a JavaScript library for building user interfaces with a component-based architecture. It enables developers to create interactive and dynamic web applications efficiently.',
                'use_cases': ['Single-page applications', 'Interactive web interfaces', 'Component-based UI development', 'Progressive web apps'],
                'integration_benefits': ['Reusable components', 'Virtual DOM performance', 'Large ecosystem'],
                'configuration': {'framework': 'react', 'build_tool': 'webpack'},
                'resource_name': 'react-app',
                'terraform_config': '# React application deployment\nresource "aws_s3_bucket" "react-app" {\n  bucket = "my-react-app"\n  website {\n    index_document = "index.html"\n  }\n}'
            }
        }
        

        
        return service_fallbacks.get(service, fallbacks.get(service, {
            'description': f'{service} is a technology or service integrated into this project.',
            'use_cases': ['System integration', 'Application enhancement', 'Service provision', 'Technology implementation'],
            'integration_benefits': ['Enhanced functionality', 'Improved capabilities', 'System integration'],
            'configuration': {'type': service.lower().replace(' ', '_'), 'references': reference_count},
            'resource_name': service.lower().replace(' ', '-'),
            'terraform_config': f'# {service} configuration\nresource "null_resource" "{service.lower().replace(" ", "_")}" {{\n  # Configuration for {service}\n}}'
        }))