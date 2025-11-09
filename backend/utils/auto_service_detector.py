import re
from collections import defaultdict

def clean_service_name(service_name):
    """Clean and normalize service names to prevent concatenation."""
    service_name = service_name.strip()
    parts = service_name.replace('_', ' ').replace('-', ' ').split()
    if len(parts) > 3:
        meaningful_parts = []
        for part in parts[:3]:
            if len(part) > 2 and part.lower() not in ['aws', 'amazon', 'service']:
                meaningful_parts.append(part)
        if meaningful_parts:
            return ' '.join(meaningful_parts[:2])
    
    if len(service_name) > 30:
        return service_name[:30] + '...'
    
    return service_name

def auto_detect_services_with_references(content, file_path):
    """Detect services and track their code references."""
    services = defaultdict(lambda: {'count': 0, 'references': []})
    lines = content.split('\n')
    
    aws_service_map = {
        'lambda': 'AWS Lambda',
        's3': 'AWS S3',
        'ec2': 'AWS EC2',
        'rds': 'AWS RDS',
        'dynamodb': 'AWS DynamoDB',
        'iot': 'AWS IoT Core',
        'kinesis': 'AWS Kinesis',
        'firehose': 'AWS Kinesis Data Firehose',
        'greengrass': 'AWS IoT Greengrass',
        'lex': 'Amazon Lex',
        'sqs': 'AWS SQS',
        'sns': 'AWS SNS',
        'cloudformation': 'AWS CloudFormation',
        'cloudwatch': 'AWS CloudWatch'
    }
    
    aws_patterns = [
        r'aws[_-]([a-zA-Z0-9]+)',
        r'amazonaws\.com/([a-zA-Z0-9-]+)',
        r'\b(lambda|s3|ec2|rds|dynamodb|iot|kinesis|firehose|greengrass|lex|sqs|sns|cloudformation|cloudwatch|apigateway|cognito|amplify)\b',
        r'@aws-sdk/([a-zA-Z0-9-]+)',
        r'boto3\.',
        r'aws\s+([a-zA-Z0-9]+)',
        r'AWS::([a-zA-Z0-9:]+)'
    ]
    
    for line_num, line in enumerate(lines, 1):
        for pattern in aws_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                match_text = match.group(1) if match.groups() else match.group(0)
                clean_name = aws_service_map.get(match_text.lower(), f'AWS {match_text.capitalize()}')
                clean_name = clean_service_name(clean_name)
                
                services[clean_name]['count'] += 1
                services[clean_name]['references'].append({
                    'file': file_path,
                    'line': line_num,
                    'code': line.strip(),
                    'match': match.group(0)
                })
    
    cloud_patterns = {
        r'\.s3\.': 'AWS S3',
        r'\.ec2\.': 'AWS EC2', 
        r'\.lambda\.': 'AWS Lambda',
        r'\.rds\.': 'AWS RDS',
        r'\.dynamodb\.': 'AWS DynamoDB',
        r'azure\.': 'Microsoft Azure',
        r'gcp\.': 'Google Cloud Platform',
        r'kubernetes': 'Kubernetes',
        r'docker': 'Docker',
        r'redis': 'Redis',
        r'mongodb': 'MongoDB',
        r'postgresql': 'PostgreSQL',
        r'mysql': 'MySQL',
        r'nginx': 'Nginx',
        r'apache': 'Apache',
        r'terraform': 'Terraform',
        r'express': 'Express.js',
        r'fastapi': 'FastAPI',
        r'django': 'Django',
        r'flask': 'Flask',
        r'react': 'React',
        r'vue': 'Vue.js',
        r'angular': 'Angular'
    }
    
    for line_num, line in enumerate(lines, 1):
        for pattern, service in cloud_patterns.items():
            matches = list(re.finditer(pattern, line, re.IGNORECASE))
            for match in matches:
                clean_name = clean_service_name(service)
                services[clean_name]['count'] += 1
                services[clean_name]['references'].append({
                    'file': file_path,
                    'line': line_num,
                    'code': line.strip(),
                    'match': match.group(0)
                })
    
    # Also check import patterns for additional references
    import_patterns = [
        (r'import\s+([a-zA-Z0-9_-]+)', 'Import'),
        (r'from\s+([a-zA-Z0-9_.-]+)', 'Import'),
        (r'require\([\'"]([a-zA-Z0-9_.-]+)[\'"]', 'Require'),
        (r'@([a-zA-Z0-9_-]+)/', 'NPM Package'),
    ]
    
    for line_num, line in enumerate(lines, 1):
        for pattern, import_type in import_patterns:
            matches = re.finditer(pattern, line)
            for match in matches:
                match_text = match.group(1)
                if 'aws' in match_text.lower():
                    clean_name = clean_service_name('AWS SDK')
                    services[clean_name]['count'] += 1
                    services[clean_name]['references'].append({
                        'file': file_path,
                        'line': line_num,
                        'code': line.strip(),
                        'match': match.group(0)
                    })
                elif 'react' in match_text.lower():
                    clean_name = clean_service_name('React')
                    services[clean_name]['count'] += 1
                    services[clean_name]['references'].append({
                        'file': file_path,
                        'line': line_num,
                        'code': line.strip(),
                        'match': match.group(0)
                    })
                elif 'vue' in match_text.lower():
                    clean_name = clean_service_name('Vue.js')
                    services[clean_name]['count'] += 1
                    services[clean_name]['references'].append({
                        'file': file_path,
                        'line': line_num,
                        'code': line.strip(),
                        'match': match.group(0)
                    })
    
    # Remove services with no references
    return {name: data for name, data in services.items() if data['references']}

def auto_detect_services(content):
    """Legacy function for backward compatibility."""
    services = defaultdict(int)
    
    aws_service_map = {
        'lambda': 'AWS Lambda',
        's3': 'AWS S3',
        'ec2': 'AWS EC2',
        'rds': 'AWS RDS',
        'dynamodb': 'AWS DynamoDB',
        'iot': 'AWS IoT Core',
        'kinesis': 'AWS Kinesis',
        'firehose': 'AWS Kinesis Data Firehose',
        'greengrass': 'AWS IoT Greengrass',
        'lex': 'Amazon Lex',
        'sqs': 'AWS SQS',
        'sns': 'AWS SNS',
        'cloudformation': 'AWS CloudFormation',
        'cloudwatch': 'AWS CloudWatch'
    }
    
    aws_patterns = [
        r'aws[_-]([a-zA-Z0-9]+)',
        r'amazonaws\.com/([a-zA-Z0-9-]+)',
        r'\b(lambda|s3|ec2|rds|dynamodb|iot|kinesis|firehose|greengrass|lex|sqs|sns|cloudformation|cloudwatch|apigateway|cognito|amplify)\b',
        r'@aws-sdk/([a-zA-Z0-9-]+)',
        r'boto3\.',
        r'aws\s+([a-zA-Z0-9]+)',
        r'AWS::([a-zA-Z0-9:]+)'
    ]
    
    for pattern in aws_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                match = match[0] if match[0] else match[1]
            clean_name = aws_service_map.get(match.lower(), f'AWS {match.capitalize()}')
            clean_name = clean_service_name(clean_name)
            services[clean_name] += 1
    
    cloud_patterns = {
        r'\.s3\.': 'AWS S3',
        r'\.ec2\.': 'AWS EC2', 
        r'\.lambda\.': 'AWS Lambda',
        r'\.rds\.': 'AWS RDS',
        r'\.dynamodb\.': 'AWS DynamoDB',
        r'azure\.': 'Microsoft Azure',
        r'gcp\.': 'Google Cloud Platform',
        r'kubernetes': 'Kubernetes',
        r'docker': 'Docker',
        r'redis': 'Redis',
        r'mongodb': 'MongoDB',
        r'postgresql': 'PostgreSQL',
        r'mysql': 'MySQL',
        r'nginx': 'Nginx',
        r'apache': 'Apache',
        r'terraform': 'Terraform',
        r'express': 'Express.js',
        r'fastapi': 'FastAPI',
        r'django': 'Django',
        r'flask': 'Flask',
        r'react': 'React',
        r'vue': 'Vue.js',
        r'angular': 'Angular'
    }
    
    for pattern, service in cloud_patterns.items():
        if re.search(pattern, content, re.IGNORECASE):
            clean_name = clean_service_name(service)
            services[clean_name] += 1
    
    import_patterns = [
        r'import\s+([a-zA-Z0-9_-]+)',
        r'from\s+([a-zA-Z0-9_.-]+)',
        r'require\([\'"]([a-zA-Z0-9_.-]+)[\'"]',
        r'@([a-zA-Z0-9_-]+)/',
        r'pip\s+install\s+([a-zA-Z0-9_-]+)',
        r'npm\s+install\s+([a-zA-Z0-9_-]+)',
        r'yarn\s+add\s+([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if 'aws' in match.lower():
                clean_name = clean_service_name('AWS SDK')
                services[clean_name] += 1
            elif 'azure' in match.lower():
                clean_name = clean_service_name('Microsoft Azure')
                services[clean_name] += 1
            elif any(x in match.lower() for x in ['gcp', 'google-cloud']):
                clean_name = clean_service_name('Google Cloud Platform')
                services[clean_name] += 1
    
    return dict(services)

def detect_all_services_with_references(folder_path):
    """Scan all files and detect services with code references."""
    import os
    all_services = defaultdict(lambda: {'count': 0, 'references': []})
    
    # Skip binary file extensions
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg', '.webp',
                        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm',
                        '.mp3', '.wav', '.ogg', '.flac', '.aac',
                        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                        '.zip', '.tar', '.gz', '.rar', '.7z',
                        '.exe', '.dll', '.so', '.dylib', '.bin'}
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith('.'):
                continue
                
            # Skip binary files
            _, ext = os.path.splitext(file.lower())
            if ext in binary_extensions:
                continue
                
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    services = auto_detect_services_with_references(content, relative_path)
                    
                    for service, data in services.items():
                        all_services[service]['count'] += data['count']
                        all_services[service]['references'].extend(data['references'])
            except:
                continue
    
    return dict(all_services)

def detect_all_services(folder_path):
    """Legacy function - scan all files and auto-detect services."""
    import os
    all_services = defaultdict(int)
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith('.'):
                continue
                
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    services = auto_detect_services(content)
                    for service, count in services.items():
                        all_services[service] += count
            except:
                continue
    
    return dict(all_services)