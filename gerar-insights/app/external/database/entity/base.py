"""
Base declarativa centralizada para todas as entities do projeto.
Garante consistência e evita conflitos em migrações.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

