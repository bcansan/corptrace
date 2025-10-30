import socket
import dns.resolver
from typing import List
from core.transform import Transform
from core.entity import Entity


class DomainToIPs(Transform):
	"""
	Resuelve direcciones IP de un dominio
	"""
	def __init__(self):
		super().__init__(
			name="Domain to IP Addresses",
			input_type="Domain",
			output_types=["IPAddress"],
			description="Resuelve las IPs asociadas a un dominio"
		)
	
	async def execute(self, entity: Entity) -> List[Entity]:
		domain = entity.properties.get('url', '').replace('www.', '').replace('http://', '').replace('https://', '')
		results: List[Entity] = []
		
		ips = self._resolve_ips(domain)
		
		for ip in ips:
			ip_entity = Entity(
				entity_type='IPAddress',
				properties={
					'address': ip,
					'domain': domain,
					'type': 'IPv4',
					'source': 'DNS Resolution'
				}
			)
			results.append(ip_entity)
		
		return results
	
	def _resolve_ips(self, domain: str) -> List[str]:
		"""
		Resuelve IPs usando DNS
		"""
		ips: List[str] = []
		if not domain:
			return ips
		try:
			ip = socket.gethostbyname(domain)
			ips.append(ip)
		except Exception:
			pass
		try:
			resolver = dns.resolver.Resolver()
			answers = resolver.resolve(domain, 'A')
			for rdata in answers:
				ips.append(str(rdata))
		except Exception:
			pass
		return list(set(ips))
