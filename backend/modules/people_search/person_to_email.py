from backend.core.transform import Transform
from backend.core.entity import Entity
from typing import List


class PersonToEmail(Transform):
	"""
	Genera posibles emails de una persona basado en patrones comunes
	"""
	def __init__(self):
		super().__init__(
			name="Person to Email Pattern",
			input_type="Person",
			output_types=["Email"],
			description="Genera posibles direcciones de email corporativo"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		first_name = entity.properties.get('first_name', '').lower()
		last_name = entity.properties.get('last_name', '').lower()
		company_domain = entity.properties.get('company_domain', '')
		results: List[Entity] = []
		if first_name and last_name and company_domain:
			for email in self._generate_email_patterns(first_name, last_name, company_domain):
				email_entity = Entity(
					entity_type='Email',
					properties={
						'address': email,
						'person': f"{first_name} {last_name}",
						'domain': company_domain,
						'pattern': email.split('@')[0],
						'verified': False
					}
				)
				results.append(email_entity)
		return results
	
	def _generate_email_patterns(self, first: str, last: str, domain: str) -> List[str]:
		"""
		Genera patrones comunes de email corporativo
		"""
		patterns = [
			f"{first}.{last}@{domain}",
			f"{first}{last}@{domain}",
			f"{first[0]}{last}@{domain}",
			f"{first}_{last}@{domain}",
			f"{last}.{first}@{domain}",
			f"{first}@{domain}",
			f"{last}@{domain}",
		]
		return patterns
