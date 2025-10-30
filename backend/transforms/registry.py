import sys
from pathlib import Path

# Ensure backend/ directory is on sys.path
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
	sys.path.insert(0, str(BACKEND_DIR))

# Import transforms with error tolerance
_transforms_modules = []

try:
	from modules.company_search.company_to_domains import CompanyToDomains  # type: ignore
	_transforms_modules.append(("CompanyToDomains", CompanyToDomains))
except Exception as e:
	print(f"[registry] Failed to load CompanyToDomains: {e}")

try:
	from modules.domain_analysis.domain_to_subdomains import DomainToSubdomains  # type: ignore
	_transforms_modules.append(("DomainToSubdomains", DomainToSubdomains))
except Exception as e:
	print(f"[registry] Failed to load DomainToSubdomains: {e}")

try:
	from modules.domain_analysis.domain_to_ips import DomainToIPs  # type: ignore
	_transforms_modules.append(("DomainToIPs", DomainToIPs))
except Exception as e:
	print(f"[registry] Failed to load DomainToIPs: {e}")

try:
	from modules.social_media.company_to_linkedin import CompanyToLinkedIn  # type: ignore
	_transforms_modules.append(("CompanyToLinkedIn", CompanyToLinkedIn))
except Exception as e:
	print(f"[registry] Failed to load CompanyToLinkedIn: {e}")

try:
	from modules.social_media.company_to_twitter import CompanyToTwitter  # type: ignore
	_transforms_modules.append(("CompanyToTwitter", CompanyToTwitter))
except Exception as e:
	print(f"[registry] Failed to load CompanyToTwitter: {e}")

try:
	from modules.company_search.company_to_emails import CompanyToEmails  # type: ignore
	_transforms_modules.append(("CompanyToEmails", CompanyToEmails))
except Exception as e:
	print(f"[registry] Failed to load CompanyToEmails: {e}")

try:
	from modules.domain_analysis.domain_to_technologies import DomainToTechnologies  # type: ignore
	_transforms_modules.append(("DomainToTechnologies", DomainToTechnologies))
except Exception as e:
	print(f"[registry] Failed to load DomainToTechnologies: {e}")

try:
	from modules.people_search.person_to_email import PersonToEmail  # type: ignore
	_transforms_modules.append(("PersonToEmail", PersonToEmail))
except Exception as e:
	print(f"[registry] Failed to load PersonToEmail: {e}")

try:
	from modules.people_search.person_to_social import PersonToSocial  # type: ignore
	_transforms_modules.append(("PersonToSocial", PersonToSocial))
except Exception as e:
	print(f"[registry] Failed to load PersonToSocial: {e}")


class TransformRegistry:
	"""
	Registro centralizado de todas las transformaciones disponibles
	"""
	def __init__(self):
		self.transforms = {}
		self._register_all()
	
	def _register_all(self):
		"""
		Registra todas las transformaciones disponibles
		"""
		for name, cls in _transforms_modules:
			try:
				instance = cls()
				self.transforms[instance.name] = instance
			except Exception as e:
				print(f"[registry] Failed to instantiate {name}: {e}")
	
	def get_transforms_for_entity(self, entity_type: str) -> list:
		"""
		Obtiene todas las transformaciones aplicables a un tipo de entidad
		"""
		available = []
		for _, transform in self.transforms.items():
			if transform.input_type == entity_type:
				available.append(transform)
		return available
	
	def get_transform(self, name: str):
		"""
		Obtiene una transformación específica por nombre
		"""
		return self.transforms.get(name)
	
	def list_all(self) -> list:
		"""
		Lista todas las transformaciones disponibles
		"""
		return [
			{
				'name': t.name,
				'input_type': t.input_type,
				'output_types': t.output_types,
				'description': t.description
			}
			for t in self.transforms.values()
		]


transform_registry = TransformRegistry()
