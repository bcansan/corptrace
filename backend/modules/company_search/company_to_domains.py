from backend.core.transform import Transform
from backend.core.entity import Entity
import aiohttp
from bs4 import BeautifulSoup
from typing import List


class CompanyToDomains(Transform):
	"""
	Busca dominios asociados a una empresa usando múltiples fuentes
	"""
	def __init__(self):
		super().__init__(
			name="Company to Domains",
			input_type="Company",
			output_types=["Domain"],
			description="Encuentra dominios web asociados a una empresa"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		company_name = entity.properties.get('name', '')
		results: List[Entity] = []
		
		# Método 1: Búsqueda simulada (reemplazar por Google CSE u otra fuente)
		domains = await self._search_domains_google(company_name)
		
		for domain in domains:
			domain_entity = Entity(
				entity_type='Domain',
				properties={
					'url': domain,
					'source': 'Google Search',
					'company': company_name
				}
			)
			results.append(domain_entity)
		
		return results
	
	async def _search_domains_google(self, company_name: str) -> List[str]:
		"""
		Simula búsqueda de dominios (en producción usar Google Custom Search API)
		"""
		if not company_name:
			return []
		name = company_name.lower().replace(' ', '')
		common_domains = [
			f"www.{name}.com",
			f"{name}.es",
		]
		return common_domains[:5]
