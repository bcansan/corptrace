from backend.core.transform import Transform
from backend.core.entity import Entity
from typing import List


class CompanyToEmails(Transform):
	"""
	Extrae emails asociados a una empresa
	"""
	def __init__(self):
		super().__init__(
			name="Company to Email Addresses",
			input_type="Company",
			output_types=["Email"],
			description="Encuentra direcciones de email asociadas a la empresa"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		company_name = entity.properties.get('name', '')
		domain = entity.properties.get('domain', '')
		results: List[Entity] = []
		if domain:
			for email in self._generate_common_emails(domain):
				email_entity = Entity(
					entity_type='Email',
					properties={
						'address': email,
						'domain': domain,
						'company': company_name,
						'source': 'Pattern Generation'
					}
				)
				results.append(email_entity)
		return results
	
	def _generate_common_emails(self, domain: str) -> List[str]:
		"""
		Genera patrones comunes de email corporativo
		"""
		common_patterns = [
			f"info@{domain}",
			f"contact@{domain}",
			f"admin@{domain}",
			f"support@{domain}",
			f"sales@{domain}",
			f"hello@{domain}",
			f"office@{domain}"
		]
		return common_patterns
