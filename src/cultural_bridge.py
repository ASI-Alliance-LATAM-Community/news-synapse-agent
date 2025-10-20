"""
Cultural Bridge Builder and Stereotype Analyzer
Tools for facilitating cross-cultural understanding and challenging assumptions
"""

import re
from typing import List, Dict, Tuple
from philosophical_framework import PhilosophicalFramework

class CulturalBridgeBuilder:
    """Facilitates cross-cultural understanding and challenges stereotypes"""
    
    def __init__(self):
        self.framework = PhilosophicalFramework()
        self.stereotype_patterns = self._build_stereotype_patterns()
        self.cultural_bridge_strategies = self._build_bridge_strategies()
    
    def _build_stereotype_patterns(self) -> Dict[str, List[str]]:
        """Common stereotype patterns to watch for"""
        return {
            "cultural_essentialism": [
                r"\b(all|most) .+ (people|cultures?) (are|do|have)",
                r".+ (people|culture) is (inherently|naturally|typically)",
                r"they (always|never|tend to)",
                r"their nature is",
                r"(naturally|inherently) (good|bad|better|worse) at"
            ],
            "binary_thinking": [
                r"(civilized|advanced|modern|developed) (vs|versus) (savage|primitive|backward|traditional)",
                r"(rational|logical) (vs|versus) (emotional|irrational)",
                r"(individual|western) (vs|versus) (collective|eastern)",
                r"(superior|better) to (traditional|indigenous)"
            ],
            "deficit_framing": [
                r"(lacks?|missing|without) (technology|advancement|development)",
                r"(underdeveloped|behind|backward)",
                r"needs? to (catch up|modernize|advance)",
                r"(primitive|outdated) (culture|practices|thinking)"
            ],
            "power_blindness": [
                r"(color.?blind|post.?racial)",
                r"(merit.?based|equal opportunity)",
                r"level playing field",
                r"pull themselves up"
            ]
        }
    
    def _build_bridge_strategies(self) -> Dict[str, List[str]]:
        """Strategies for building cultural understanding"""
        return {
            "perspective_taking": [
                "Consider how this looks from [other culture's] perspective",
                "What assumptions are embedded in this viewpoint?",
                "How might historical context shape this cultural practice?",
                "What knowledge systems inform this approach?"
            ],
            "common_ground": [
                "What human concerns are shared across cultures here?",
                "How do different cultures address similar challenges?",
                "What can we learn from this cultural approach?",
                "Where might creative synthesis be possible?"
            ],
            "power_analysis": [
                "Who has the power to define 'normal' in this context?",
                "How do historical power relations affect this interaction?",
                "Whose voices are centered vs. marginalized here?",
                "What structural factors shape these cultural differences?"
            ],
            "complexity_embrace": [
                "How is this culture internally diverse?",
                "What tensions exist within this cultural group?",
                "How are traditions being reinterpreted by new generations?",
                "What hybrid forms are emerging from cultural contact?"
            ]
        }
    
    def analyze_for_stereotypes(self, text: str) -> Dict[str, List[str]]:
        """Analyze text for potential stereotypes and problematic patterns"""
        identified_patterns = {}
        
        for pattern_type, patterns in self.stereotype_patterns.items():
            matches = []
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    matches.append(pattern)
            if matches:
                identified_patterns[pattern_type] = matches
        
        return identified_patterns
    
    def suggest_alternative_framings(self, text: str, identified_stereotypes: Dict[str, List[str]]) -> List[str]:
        """Suggest alternative ways to frame statements that contain stereotypes"""
        suggestions = []
        
        if "cultural_essentialism" in identified_stereotypes:
            suggestions.extend([
                "Consider: 'Some people in [culture] tend to...' rather than 'All [culture] people are...'",
                "Ask: What historical and structural factors might influence these patterns?",
                "Frame: 'In certain contexts, [cultural practice] serves the function of...'",
                "Explore: How do individuals within this culture vary in their practices?"
            ])
        
        if "binary_thinking" in identified_stereotypes:
            suggestions.extend([
                "Question the binary: What exists between these supposed opposites?",
                "Consider: How might both approaches have value in different contexts?",
                "Explore: What would a synthesis of these approaches look like?",
                "Ask: Who benefits from maintaining this either/or framing?"
            ])
        
        if "deficit_framing" in identified_stereotypes:
            suggestions.extend([
                "Reframe as difference rather than deficit: What does this culture excel at?",
                "Ask: What knowledge or skills does this approach cultivate?",
                "Consider: How might this be adaptive to particular environmental/social conditions?",
                "Explore: What can dominant cultures learn from this approach?"
            ])
        
        if "power_blindness" in identified_stereotypes:
            suggestions.extend([
                "Acknowledge structural inequalities: How do power differences affect this situation?",
                "Consider historical context: What legacy effects are still operating?",
                "Examine institutional barriers: What systemic factors create disparate outcomes?",
                "Ask: How do current policies and practices perpetuate or challenge inequalities?"
            ])
        
        return suggestions
    
    def build_cultural_bridge_response(self, topic: str, cultural_perspectives: List[str]) -> str:
        """Generate a response that builds bridges between cultural perspectives"""
        
        questioning_methods = self.framework.get_questioning_methods_for_topic(topic)
        cultural_insights = self.framework.get_cultural_insights_for_topic(topic)
        
        bridge_response = f"""
CULTURAL BRIDGE-BUILDING ANALYSIS FOR: {topic}

MULTIPLE PERSPECTIVES TO CONSIDER:
{chr(10).join(f"• {perspective}" for perspective in cultural_perspectives)}

CRITICAL QUESTIONS TO EXPLORE:
{chr(10).join(f"• {method}" for method in questioning_methods[:5])}

CULTURAL INSIGHTS TO REMEMBER:
{chr(10).join(f"• {insight}" for insight in cultural_insights[:5])}

BRIDGE-BUILDING STRATEGIES:
"""
        
        for strategy_type, strategies in self.cultural_bridge_strategies.items():
            bridge_response += f"\n{strategy_type.replace('_', ' ').title()}:\n"
            bridge_response += chr(10).join(f"  • {strategy}" for strategy in strategies[:2])
            bridge_response += "\n"
        
        return bridge_response
    
    def generate_philosophical_inquiry(self, query: str) -> str:
        """Generate philosophical inquiry based on the original query"""
        
        stereotypes = self.analyze_for_stereotypes(query)
        
        response = "PHILOSOPHICAL ANALYSIS AND CULTURAL BRIDGE-BUILDING:\n\n"
        
        if stereotypes:
            response += "⚠️  POTENTIAL ASSUMPTIONS TO EXAMINE:\n"
            for pattern_type, patterns in stereotypes.items():
                response += f"• {pattern_type.replace('_', ' ').title()}: Found patterns suggesting stereotypical thinking\n"
            
            suggestions = self.suggest_alternative_framings(query, stereotypes)
            response += "\n🌉 ALTERNATIVE FRAMINGS TO CONSIDER:\n"
            for suggestion in suggestions[:3]:
                response += f"• {suggestion}\n"
        
        response += "\n🤔 PHILOSOPHICAL QUESTIONS TO EXPLORE:\n"
        questions = [
            "What assumptions underlie this question?",
            "Whose perspectives are centered vs. marginalized?", 
            "How might different cultural contexts shape this issue?",
            "What power dynamics are at play here?",
            "How could we reframe this to build understanding rather than division?"
        ]
        
        for question in questions:
            response += f"• {question}\n"
        
        return response

class DialogueFacilitator:
    """Facilitates productive dialogue across different perspectives"""
    
    def __init__(self):
        self.bridge_builder = CulturalBridgeBuilder()
    
    def facilitate_perspective_exchange(self, viewpoint_a: str, viewpoint_b: str, topic: str) -> str:
        """Help facilitate understanding between two different viewpoints"""
        
        response = f"FACILITATING DIALOGUE ON: {topic}\n\n"
        
        response += "PERSPECTIVE A SUMMARY:\n"
        response += f"{viewpoint_a}\n\n"
        
        response += "PERSPECTIVE B SUMMARY:\n"
        response += f"{viewpoint_b}\n\n"
        
        response += "PHILOSOPHICAL ANALYSIS:\n"
        response += "• What values and assumptions underlie each perspective?\n"
        response += "• How might historical and cultural contexts shape these views?\n"
        response += "• Where might there be common ground or shared concerns?\n"
        response += "• What questions could help each side understand the other better?\n\n"
        
        response += "BRIDGE-BUILDING QUESTIONS:\n"
        response += "• What experiences led each side to their viewpoint?\n"
        response += "• What fears or concerns drive each perspective?\n"
        response += "• How might both sides be partially right about different aspects?\n"
        response += "• What would a solution look like that honors the valid concerns of both sides?\n\n"
        
        response += "NEXT STEPS FOR DIALOGUE:\n"
        response += "• Focus on understanding before being understood\n"
        response += "• Look for the human story behind each position\n"
        response += "• Identify shared values even amid different approaches\n"
        response += "• Explore creative solutions that transcend either/or thinking\n"
        
        return response