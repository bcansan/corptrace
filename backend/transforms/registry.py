from backend.modules.company_search.company_to_domains import CompanyToDomains
from backend.modules.domain_analysis.domain_to_subdomains import DomainToSubdomains
from backend.modules.domain_analysis.domain_to_ips import DomainToIPs
from backend.modules.social_media.company_to_linkedin import CompanyToLinkedIn
from backend.modules.social_media.company_to_twitter import CompanyToTwitter
from backend.modules.company_search.company_to_emails import CompanyToEmails
from backend.modules.domain_analysis.domain_to_technologies import DomainToTechnologies
from backend.modules.people_search.person_to_email import PersonToEmail
from backend.modules.people_search.person_to_social import PersonToSocial


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
		transforms = [
			CompanyToDomains(),
			DomainToSubdomains(),
			DomainToIPs(),
			CompanyToLinkedIn(),
			CompanyToTwitter(),
			CompanyToEmails(),
			DomainToTechnologies(),
			PersonToEmail(),
			PersonToSocial(),
		]
		for transform in transforms:
			self.transforms[transform.name] = transform
	
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
