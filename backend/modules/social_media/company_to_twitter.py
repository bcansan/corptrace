from core.transform import Transform
from core.entity import Entity
from typing import List


class CompanyToTwitter(Transform):
	"""
	Encuentra el perfil de Twitter/X de una empresa
	"""
	def __init__(self):
		super().__init__(
			name="Company to Twitter Profile",
			input_type="Company",
			output_types=["SocialProfile"],
			description="Busca el perfil de Twitter/X de la empresa"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		company_name = entity.properties.get('name', '')
		results: List[Entity] = []
		twitter_handle = await self._search_twitter(company_name)
		if twitter_handle:
			profile_entity = Entity(
				entity_type='SocialProfile',
				properties={
					'platform': 'Twitter',
					'handle': twitter_handle,
					'url': f"https://twitter.com/{twitter_handle}",
					'company': company_name
				}
			)
			results.append(profile_entity)
		return results
	
	async def _search_twitter(self, company_name: str) -> str:
		"""
		Intenta encontrar el handle de Twitter (no verificado)
		"""
		if not company_name:
			return ""
		return company_name.replace(' ', '').replace('.', '')
