from sqlalchemy.orm import declarative_base, registry

mapper_registry = registry()
Base = mapper_registry.generate_base()
