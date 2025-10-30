from core.transform import Transform
from core.entity import Entity
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict


class DomainToTechnologies(Transform):
	"""
	Detecta tecnologías usadas en un sitio web
	"""
	def __init__(self):
		super().__init__(
			name="Domain to Technologies",
			input_type="Domain",
			output_types=["Technology"],
			description="Detecta tecnologías web, frameworks y servicios"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		domain = entity.properties.get('url', '')
		if domain and not domain.startswith('http'):
			domain = f"https://{domain}"
		results: List[Entity] = []
		
		technologies = await self._detect_technologies(domain) if domain else []
		
		for tech in technologies:
			tech_entity = Entity(
				entity_type='Technology',
				properties={
					'name': tech['name'],
					'category': tech['category'],
					'domain': domain,
					'confidence': tech.get('confidence', 'medium')
				}
			)
			results.append(tech_entity)
		
		return results
	
	async def _detect_technologies(self, url: str) -> List[Dict]:
		"""
		Detecta tecnologías analizando HTML y headers
		"""
		technologies: List[Dict] = []
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(url, timeout=10) as response:
					html = await response.text()
					headers = response.headers
					if 'X-Powered-By' in headers:
						technologies.append({
							'name': headers['X-Powered-By'],
							'category': 'Web Server',
							'confidence': 'high'
						})
					soup = BeautifulSoup(html, 'html.parser')
					lower = html.lower()
					if 'react' in lower or soup.find('div', {'id': 'root'}):
						technologies.append({'name': 'React', 'category': 'JavaScript Framework', 'confidence': 'medium'})
					if 'wp-content' in html or 'wordpress' in lower:
						technologies.append({'name': 'WordPress', 'category': 'CMS', 'confidence': 'high'})
					if 'google-analytics' in lower or 'gtag' in lower:
						technologies.append({'name': 'Google Analytics', 'category': 'Analytics', 'confidence': 'high'})
		except Exception as e:
			print(f"Error detecting technologies: {e}")
		return technologies
