import asyncio
from backend.core.entity import Entity
from backend.transforms.registry import transform_registry


async def test_company_to_domains():
	print("\n=== Testing Company to Domains ===")
	company = Entity(
		entity_type='Company',
		properties={
			'name': 'Google',
			'industry': 'Technology'
		}
	)
	transform = transform_registry.get_transform("Company to Domains")
	results = await transform.execute(company)
	print(f"Found {len(results)} domains:")
	for domain in results:
		print(f"  - {domain.properties['url']}")


async def test_domain_to_subdomains():
	print("\n=== Testing Domain to Subdomains ===")
	domain = Entity(
		entity_type='Domain',
		properties={
			'url': 'google.com'
		}
	)
	transform = transform_registry.get_transform("Domain to Subdomains")
	results = await transform.execute(domain)
	print(f"Found {len(results)} subdomains:")
	for subdomain in results[:10]:
		print(f"  - {subdomain.properties['url']}")


async def main():
	await test_company_to_domains()
	await test_domain_to_subdomains()
	print("\n=== Available Transforms ===")
	all_transforms = transform_registry.list_all()
	for t in all_transforms:
		print(f"  - {t['name']}: {t['input_type']} → {t['output_types']}")


if __name__ == "__main__":
	asyncio.run(main())
