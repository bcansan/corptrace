from core.transform import Transform
from core.entity import Entity
from typing import List


class CompanyToLinkedIn(Transform):
	"""
	Encuentra el perfil de LinkedIn de una empresa
	"""
	def __init__(self):
		super().__init__(
			name="Company to LinkedIn Profile",
			input_type="Company",
			output_types=["SocialProfile"],
			description="Busca el perfil corporativo de LinkedIn"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		company_name = entity.properties.get('name', '')
		results: List[Entity] = []
		linkedin_url = await self._search_linkedin(company_name)
		if linkedin_url:
			profile_entity = Entity(
				entity_type='SocialProfile',
				properties={
					'platform': 'LinkedIn',
					'url': linkedin_url,
					'company': company_name,
					'type': 'Company Page'
				}
			)
			results.append(profile_entity)
		return results
	
	async def _search_linkedin(self, company_name: str) -> str:
		"""
		Construye URL probable de LinkedIn (verificación pendiente)
		"""
		if not company_name:
			return ""
		slug = company_name.lower().replace(' ', '-').replace('.', '')
		return f"https://www.linkedin.com/company/{slug}"
