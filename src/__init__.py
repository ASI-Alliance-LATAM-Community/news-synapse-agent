"""
Critical Thinking Agent Package
Integrates philosophical frameworks for enhanced reasoning and cultural bridge-building
"""

from .philosophical_framework import PhilosophicalFramework, PhilosophicalPerspective, ThinkingCategory
from .cultural_bridge import CulturalBridgeBuilder, DialogueFacilitator
from .training_module import AgentTrainingModule, TrainingScenario

__version__ = "1.0.0"
__all__ = [
    "PhilosophicalFramework",
    "PhilosophicalPerspective", 
    "ThinkingCategory",
    "CulturalBridgeBuilder",
    "DialogueFacilitator",
    "AgentTrainingModule",
    "TrainingScenario"
]