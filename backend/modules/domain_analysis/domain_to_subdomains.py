from core.transform import Transform
from core.entity import Entity
import aiohttp
import dns.resolver
from typing import List


class DomainToSubdomains(Transform):
	"""
	Enumera subdominios de un dominio usando múltiples técnicas
	"""
	def __init__(self):
		super().__init__(
			name="Domain to Subdomains",
			input_type="Domain",
			output_types=["Domain"],
			description="Enumera subdominios de un dominio principal"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		domain = entity.properties.get('url', '').replace('www.', '').replace('http://', '').replace('https://', '')
		results: List[Entity] = []
		
		# Método 1: crt.sh (certificados SSL)
		subdomains = await self._search_crtsh(domain)
		
		# Método 2: DNS brute force (subdominios comunes)
		subdomains += await self._dns_bruteforce(domain)
		
		for subdomain in set(subdomains):
			subdomain_entity = Entity(
				entity_type='Domain',
				properties={
					'url': subdomain,
					'parent_domain': domain,
					'type': 'subdomain',
					'source': 'crt.sh & DNS'
				}
			)
			results.append(subdomain_entity)
		
		return results
	
	async def _search_crtsh(self, domain: str) -> List[str]:
		"""
		Busca subdominios en crt.sh (certificados SSL públicos)
		"""
		if not domain:
			return []
		url = f"https://crt.sh/?q=%.{domain}&output=json"
		subdomains: List[str] = []
		
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(url, timeout=10) as response:
					if response.status == 200:
						data = await response.json()
						for entry in data:
							name = entry.get('name_value', '')
							if name and '*' not in name:
								subdomains.append(name)
		except Exception as e:
			print(f"Error en crt.sh: {e}")
		
		return list(set(subdomains))[:20]
	
	async def _dns_bruteforce(self, domain: str) -> List[str]:
		"""
		Prueba subdominios comunes mediante DNS
		"""
		if not domain:
			return []
		common_subdomains = [
			'www', 'mail', 'ftp', 'admin', 'blog', 'dev', 'test',
			'staging', 'api', 'portal', 'shop', 'store', 'mobile',
			'vpn', 'remote', 'secure', 'login', 'accounts'
		]
		
		found_subdomains: List[str] = []
		resolver = dns.resolver.Resolver()
		resolver.timeout = 2
		resolver.lifetime = 2
		
		for sub in common_subdomains:
			try:
				subdomain = f"{sub}.{domain}"
				answers = resolver.resolve(subdomain, 'A')
				if answers:
					found_subdomains.append(subdomain)
			except Exception:
				continue
		
		return found_subdomains
