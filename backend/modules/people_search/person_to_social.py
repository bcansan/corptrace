from core.transform import Transform
from core.entity import Entity
from typing import List


class PersonToSocial(Transform):
	"""
	Busca perfiles sociales de una persona
	"""
	def __init__(self):
		super().__init__(
			name="Person to Social Profiles",
			input_type="Person",
			output_types=["SocialProfile"],
			description="Encuentra perfiles en redes sociales"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		full_name = entity.properties.get('full_name', '')
		first_name = entity.properties.get('first_name', '')
		last_name = entity.properties.get('last_name', '')
		if not full_name and first_name and last_name:
			full_name = f"{first_name} {last_name}"
		results: List[Entity] = []
		platforms = ['LinkedIn', 'Twitter', 'GitHub']
		for platform in platforms:
			url = self._generate_profile_url(platform, full_name, first_name, last_name)
			if url:
				profile_entity = Entity(
					entity_type='SocialProfile',
					properties={
						'platform': platform,
						'url': url,
						'person': full_name,
						'verified': False
					}
				)
				results.append(profile_entity)
		return results
	
	def _generate_profile_url(self, platform: str, full_name: str, first: str, last: str) -> str:
		"""
		Genera URLs probables de perfiles sociales
		"""
		name_slug = (full_name or '').lower().replace(' ', '-')
		if platform == 'LinkedIn':
			return f"https://www.linkedin.com/in/{name_slug}" if name_slug else ""
		elif platform == 'Twitter':
			handle = f"{first}{last}".lower()
			return f"https://twitter.com/{handle}" if handle else ""
		elif platform == 'GitHub':
			handle = f"{first}{last}".lower()
			return f"https://github.com/{handle}" if handle else ""
		return ""
