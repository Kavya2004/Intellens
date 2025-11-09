"""
Cost estimation utility for cloud services and technologies.
Provides projected monthly and yearly costs based on typical usage patterns.
"""

from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass
class CostEstimate:
    monthly_min: float
    monthly_max: float
    yearly_min: float
    yearly_max: float
    unit: str
    assumptions: str

class CostEstimator:
    """Estimates costs for detected services based on typical usage patterns."""
    
    def __init__(self):
        # Cost data based on current pricing (USD, as of 2024)
        self.service_costs = {
            # AWS Services
            'AWS Lambda': CostEstimate(5, 50, 60, 600, 'USD', '1M requests/month, 128MB memory'),
            'AWS S3': CostEstimate(10, 100, 120, 1200, 'USD', '100GB storage, standard tier'),
            'AWS EC2': CostEstimate(20, 200, 240, 2400, 'USD', 't3.micro to t3.medium instances'),
            'AWS RDS': CostEstimate(25, 300, 300, 3600, 'USD', 'db.t3.micro to db.t3.medium'),
            'AWS DynamoDB': CostEstimate(15, 150, 180, 1800, 'USD', '25GB storage, on-demand'),
            'AWS IoT Core': CostEstimate(10, 80, 120, 960, 'USD', '1M messages/month'),
            'AWS Kinesis': CostEstimate(20, 200, 240, 2400, 'USD', '1 shard, 1M records/month'),
            'AWS SQS': CostEstimate(1, 20, 12, 240, 'USD', '1M requests/month'),
            'AWS SNS': CostEstimate(2, 25, 24, 300, 'USD', '1M notifications/month'),
            'AWS CloudWatch': CostEstimate(5, 50, 60, 600, 'USD', 'Basic monitoring'),
            'AWS API Gateway': CostEstimate(10, 100, 120, 1200, 'USD', '1M API calls/month'),
            
            # Databases
            'PostgreSQL': CostEstimate(0, 50, 0, 600, 'USD', 'Self-hosted or managed service'),
            'MySQL': CostEstimate(0, 40, 0, 480, 'USD', 'Self-hosted or managed service'),
            'MongoDB': CostEstimate(0, 60, 0, 720, 'USD', 'Atlas M10 cluster or self-hosted'),
            'Redis': CostEstimate(0, 30, 0, 360, 'USD', 'ElastiCache or self-hosted'),
            
            # Frameworks & Tools (hosting costs)
            'FastAPI': CostEstimate(5, 50, 60, 600, 'USD', 'Container hosting (1-4 instances)'),
            'Django': CostEstimate(10, 80, 120, 960, 'USD', 'Web hosting with database'),
            'Flask': CostEstimate(5, 40, 60, 480, 'USD', 'Basic web hosting'),
            'Express.js': CostEstimate(5, 50, 60, 600, 'USD', 'Node.js hosting'),
            'React': CostEstimate(0, 20, 0, 240, 'USD', 'Static hosting (Netlify/Vercel)'),
            'Vue.js': CostEstimate(0, 20, 0, 240, 'USD', 'Static hosting'),
            'Angular': CostEstimate(0, 25, 0, 300, 'USD', 'Static hosting'),
            
            # Infrastructure
            'Docker': CostEstimate(10, 100, 120, 1200, 'USD', 'Container registry + hosting'),
            'Kubernetes': CostEstimate(50, 500, 600, 6000, 'USD', 'Managed cluster (EKS/GKE/AKS)'),
            'Terraform': CostEstimate(0, 10, 0, 120, 'USD', 'Terraform Cloud (free tier available)'),
            'Nginx': CostEstimate(0, 20, 0, 240, 'USD', 'Load balancer service'),
            'Apache': CostEstimate(0, 15, 0, 180, 'USD', 'Web server hosting'),
            
            # Cloud Platforms (base costs)
            'Microsoft Azure': CostEstimate(25, 250, 300, 3000, 'USD', 'Basic compute + storage'),
            'Google Cloud Platform': CostEstimate(25, 250, 300, 3000, 'USD', 'Basic compute + storage'),
        }
    
    def estimate_service_cost(self, service_name: str, usage_count: int = 1) -> Dict:
        """Estimate cost for a specific service."""
        if service_name not in self.service_costs:
            # Default estimate for unknown services
            cost = CostEstimate(5, 50, 60, 600, 'USD', 'Estimated based on typical service costs')
        else:
            cost = self.service_costs[service_name]
        
        # Scale costs based on usage count (detected occurrences)
        scale_factor = min(usage_count * 0.5 + 0.5, 3.0)  # Cap at 3x for high usage
        
        return {
            'service': service_name,
            'monthly_cost_range': f"${cost.monthly_min * scale_factor:.0f} - ${cost.monthly_max * scale_factor:.0f}",
            'yearly_cost_range': f"${cost.yearly_min * scale_factor:.0f} - ${cost.yearly_max * scale_factor:.0f}",
            'monthly_min': cost.monthly_min * scale_factor,
            'monthly_max': cost.monthly_max * scale_factor,
            'yearly_min': cost.yearly_min * scale_factor,
            'yearly_max': cost.yearly_max * scale_factor,
            'currency': cost.unit,
            'assumptions': cost.assumptions,
            'usage_detected': usage_count
        }
    
    def estimate_project_costs(self, detected_services: Dict[str, int]) -> Dict:
        """Estimate total project costs based on detected services."""
        service_estimates = []
        total_monthly_min = 0
        total_monthly_max = 0
        total_yearly_min = 0
        total_yearly_max = 0
        
        for service_name, usage_count in detected_services.items():
            estimate = self.estimate_service_cost(service_name, usage_count)
            service_estimates.append(estimate)
            
            total_monthly_min += estimate['monthly_min']
            total_monthly_max += estimate['monthly_max']
            total_yearly_min += estimate['yearly_min']
            total_yearly_max += estimate['yearly_max']
        
        return {
            'service_estimates': service_estimates,
            'total_costs': {
                'monthly_range': f"${total_monthly_min:.0f} - ${total_monthly_max:.0f}",
                'yearly_range': f"${total_yearly_min:.0f} - ${total_yearly_max:.0f}",
                'monthly_min': total_monthly_min,
                'monthly_max': total_monthly_max,
                'yearly_min': total_yearly_min,
                'yearly_max': total_yearly_max,
                'currency': 'USD'
            },
            'cost_breakdown': {
                'infrastructure': sum(e['monthly_max'] for e in service_estimates 
                                   if any(x in e['service'].lower() for x in ['aws', 'azure', 'google', 'kubernetes'])),
                'databases': sum(e['monthly_max'] for e in service_estimates 
                               if any(x in e['service'].lower() for x in ['sql', 'mongo', 'redis', 'dynamo'])),
                'frameworks': sum(e['monthly_max'] for e in service_estimates 
                                if any(x in e['service'].lower() for x in ['api', 'django', 'flask', 'react', 'vue', 'angular']))
            },
            'recommendations': self._generate_cost_recommendations(service_estimates, total_monthly_max)
        }
    
    def _generate_cost_recommendations(self, service_estimates: list, total_monthly_max: float) -> list:
        """Generate cost optimization recommendations."""
        recommendations = []
        
        if total_monthly_max > 500:
            recommendations.append("Consider using reserved instances or savings plans for long-term deployments")
        
        if any('AWS' in e['service'] for e in service_estimates):
            recommendations.append("Use AWS Free Tier for development and testing")
            recommendations.append("Implement auto-scaling to optimize costs based on demand")
        
        if any('Kubernetes' in e['service'] for e in service_estimates):
            recommendations.append("Consider spot instances for non-critical workloads")
        
        if len(service_estimates) > 5:
            recommendations.append("Review service dependencies to identify potential consolidation opportunities")
        
        recommendations.append("Monitor usage with cost alerts to prevent unexpected charges")
        recommendations.append("Use infrastructure as code (Terraform) for consistent and cost-effective deployments")
        
        return recommendations

def estimate_costs_for_services(detected_services: Dict[str, int]) -> Dict:
    """Main function to estimate costs for detected services."""
    estimator = CostEstimator()
    return estimator.estimate_project_costs(detected_services)