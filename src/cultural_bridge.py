"""
Cultural Bridge Builder and Stereotype Analyzer
Tools for facilitating cross-cultural understanding and challenging assumptions
Includes offensive language detection and filtering capabilities
"""

import re
from typing import List, Dict, Tuple, Optional
from typing import List, Dict, Tuple, Optional, Any
from philosophical_framework import PhilosophicalFramework

class OffensiveLanguageDetector:
    """Detects and filters offensive, racist, or misogynistic language and suggests alternatives"""
    
    def __init__(self):
        self.offensive_patterns = self._build_offensive_patterns()
        self.alternative_suggestions = self._build_alternative_suggestions()
    
    def _build_offensive_patterns(self) -> Dict[str, List[str]]:
        """Patterns to detect offensive language categories"""
        return {
            "racist_language": [
                r"\b(urban|inner.?city)\b.*\b(crime|violence|problems|youth)\b",
                r"\b(articulate|well.?spoken)\b.*\b(black|african.?american)\b",
                r"\b(model minority|credit to (their|your) race)\b",
                r"\b(exotic|oriental|primitive)\b",
                r"\b(ghetto|hood|thug)\b(?!.*neighborhood)",
                r"\b(savages?|uncivilized|backwards?)\b",
                r"\b(illegals?|anchor babies?)\b",
                r"\b(go back (to )?where (they|you) came from)\b",
                r"\b(those people|these people)\b.*\b(need to|should)\b"
            ],
            "misogynistic_language": [
                r"\b(women|females?|girls?)\b.*\b(too )?(emotional|hysterical|irrational)\b",
                r"\b(women|females?)\b.*\b(can't|unable|not suited)\b.*\b(lead|leadership)\b",
                r"\b(bossy|shrill|nagging)\b.*\b(women|female)\b",
                r"\b(gold.?digger|attention.?seeking)\b",
                r"\b(asking for it|she was dressed)\b",
                r"\b(biological clock|baby crazy)\b",
                r"\b(catty|bitchy|crazy ex)\b",
                r"\b(naturally|biologically)\b.*\b(women|females?)\b.*\b(worse|bad|inferior)\b"
            ],
            "homophobic_language": [
                r"\b(that's so gay|no homo)\b",
                r"\b(lifestyle choice|sexual preference)\b",
                r"\b(recruiting|agenda|indoctrinating)\b.*\b(gay|lgbt|queer)\b",
                r"\b(unnatural|against nature)\b.*\b(homosexual|gay)\b"
            ],
            "transphobic_language": [
                r"\b(real (wo)?man|biological (wo)?man)\b",
                r"\b(born (wo)?man|actual gender)\b",
                r"\b(gender ideology|trans agenda)\b",
                r"\b(mutilating|chopping off)\b"
            ],
            "ableist_language": [
                r"\b(retarded|mentally deficient)\b",
                r"\b(psycho|crazy|insane)\b.*\b(people|person)\b",
                r"\b(wheelchair.?bound|suffers from)\b",
                r"\b(normal people|able.?bodied)\b.*\b(vs|compared to)\b"
            ],
            "classist_language": [
                r"\b(white trash|trailer trash)\b",
                r"\b(welfare queen|moocher)\b",
                r"\b(pull yourself up|bootstrap)\b",
                r"\b(deserve to be poor|chosen poverty)\b"
            ],
            "xenophobic_language": [
                r"\b(go back to|send them back)\b",
                r"\b(real americans?|true patriots?)\b",
                r"\b(invasion|swarm|horde)\b.*\b(immigrants?|refugees?)\b",
                r"\b(taking our jobs|stealing benefits)\b"
            ]
        }
    
    def _build_alternative_suggestions(self) -> Dict[str, Dict[str, List[str]]]:
        """Alternative phrasings for offensive language patterns with specific examples"""
        return {
            "racist_language": {
                "general_guidance": [
                    "Consider discussing specific policies or systemic issues rather than coded language",
                    "Focus on individual actions rather than group generalizations",
                    "Use person-first language that doesn't reduce people to stereotypes",
                    "Acknowledge the complexity and diversity within any cultural group"
                ],
                "specific_examples": [
                    "Instead of 'urban youth are causing problems' → 'What systemic factors contribute to challenges in underresourced neighborhoods?'",
                    "Instead of 'those people need to go back' → 'How can we work together to address community concerns?'",
                    "Instead of 'articulate for a Black person' → simply 'articulate' (without racial qualifiers)",
                    "Instead of 'exotic' → 'from [specific place]' or 'unfamiliar to me'"
                ]
            },
            "misogynistic_language": {
                "general_guidance": [
                    "Consider if you would use the same language to describe a man in this situation",
                    "Focus on specific behaviors rather than gendered assumptions",
                    "Avoid language that polices women's emotions or autonomy",
                    "Use neutral descriptors that don't carry gender-based judgment"
                ],
                "specific_examples": [
                    "Instead of 'women are too emotional for leadership' → 'effective leadership requires both analytical and empathetic skills'",
                    "Instead of 'women naturally can't handle technical work' → 'what barriers prevent equal participation in technical fields?'",
                    "Instead of 'she's being hysterical' → 'she seems upset' or 'she's expressing strong concerns'",
                    "Instead of 'bossy woman' → 'assertive leader' or 'direct communicator'"
                ]
            },
            "homophobic_language": {
                "general_guidance": [
                    "Use 'sexual orientation' instead of 'preference' or 'lifestyle'",
                    "Avoid using 'gay' as a synonym for 'bad' or 'weird'",
                    "Focus on acceptance and inclusion rather than tolerance",
                    "Recognize LGBTQ+ identities as natural human diversity"
                ],
                "specific_examples": [
                    "Instead of 'that's so gay' → 'that's frustrating' or 'that's disappointing'",
                    "Instead of 'lifestyle choice' → 'sexual orientation' or 'identity'",
                    "Instead of 'homosexual agenda' → 'LGBTQ+ rights advocacy'",
                    "Instead of 'tolerating' LGBTQ+ people → 'welcoming' or 'celebrating diversity'"
                ]
            },
            "transphobic_language": {
                "general_guidance": [
                    "Use the pronouns and names people prefer for themselves",
                    "Avoid focusing on biology when discussing gender identity",
                    "Recognize gender identity as a core aspect of human experience",
                    "Use inclusive language that doesn't exclude trans people"
                ],
                "specific_examples": [
                    "Instead of 'real woman/man' → simply 'woman/man' (all women and men are real)",
                    "Instead of 'born male/female' → 'assigned male/female at birth' (when relevant)",
                    "Instead of 'gender ideology' → 'understanding of gender diversity'",
                    "Instead of focusing on biology → focus on the person's identity and experience"
                ]
            },
            "ableist_language": {
                "general_guidance": [
                    "Use person-first language (person with disability, not disabled person)",
                    "Avoid using mental health terms as insults",
                    "Focus on accessibility and inclusion rather than 'normalcy'",
                    "Recognize disability as part of human diversity"
                ],
                "specific_examples": [
                    "Instead of 'wheelchair-bound' → 'uses a wheelchair' or 'wheelchair user'",
                    "Instead of 'suffers from autism' → 'is autistic' or 'has autism'",
                    "Instead of 'normal people vs disabled' → 'non-disabled people and disabled people'",
                    "Instead of 'crazy idea' → 'surprising idea' or 'unexpected suggestion'"
                ]
            },
            "classist_language": {
                "general_guidance": [
                    "Examine systemic factors that contribute to economic inequality",
                    "Avoid language that blames individuals for structural problems",
                    "Recognize the dignity and worth of all people regardless of economic status",
                    "Consider how privilege affects opportunities and outcomes"
                ],
                "specific_examples": [
                    "Instead of 'pull yourself up by bootstraps' → 'what support systems help people advance?'",
                    "Instead of 'welfare queen' → 'person receiving social assistance'",
                    "Instead of 'trailer trash' → avoid class-based insults entirely",
                    "Instead of 'they deserve to be poor' → 'what systemic factors create economic barriers?'"
                ]
            },
            "xenophobic_language": {
                "general_guidance": [
                    "Focus on shared human values and experiences",
                    "Recognize the contributions immigrants make to society",
                    "Avoid dehumanizing language when discussing immigration",
                    "Consider the complex factors that drive migration"
                ],
                "specific_examples": [
                    "Instead of 'invasion of immigrants' → 'increase in immigration' or 'migration patterns'",
                    "Instead of 'real Americans' → 'long-term residents' or avoid exclusive language",
                    "Instead of 'taking our jobs' → 'how can we create more opportunities for everyone?'",
                    "Instead of 'send them back' → 'comprehensive immigration policy reform'"
                ]
            }
        }
    
    def detect_offensive_language(self, text: str) -> Dict[str, List[str]]:
        """Detect offensive language patterns in text"""
        detected_issues = {}
        
        for category, patterns in self.offensive_patterns.items():
            matches = []
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    matches.append(pattern)
            if matches:
                detected_issues[category] = matches
        
        return detected_issues
    
    def suggest_alternatives(self, text: str, detected_issues: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Suggest alternative phrasings for detected offensive language with specific examples"""
        suggestions = {
            "specific_examples": [],
            "general_guidance": [],
            "philosophical_insights": []
        }
        
        for category in detected_issues.keys():
            if category in self.alternative_suggestions:
                category_data = self.alternative_suggestions[category]
                suggestions["specific_examples"].extend(category_data.get("specific_examples", []))
                suggestions["general_guidance"].extend(category_data.get("general_guidance", []))
        
        suggestions["philosophical_insights"].extend([
            "Consider the humanity and dignity of all people involved",
            "Ask whose voices and experiences are being centered or marginalized",
            "Examine how language can perpetuate or challenge systems of oppression",
            "Focus on building understanding rather than reinforcing divisions"
        ])
        
        for key in suggestions:
            suggestions[key] = list(dict.fromkeys(suggestions[key])) 
        
        return suggestions
    
    def filter_and_suggest(self, text: str) -> Dict[str, Any]:
        """Complete analysis with detection and suggestions"""
        detected = self.detect_offensive_language(text)
        suggestions = self.suggest_alternatives(text, detected) if detected else {
            "specific_examples": [],
            "general_guidance": [],
            "philosophical_insights": []
        }
        
        return {
            "has_offensive_content": bool(detected),
            "detected_issues": detected,
            "suggestions": suggestions,
            "severity": self._assess_severity(detected)
        }
    
    def _assess_severity(self, detected_issues: Dict[str, List[str]]) -> str:
        """Assess the severity of detected issues"""
        if not detected_issues:
            return "none"
        elif len(detected_issues) == 1 and len(list(detected_issues.values())[0]) == 1:
            return "mild"
        elif len(detected_issues) <= 2:
            return "moderate"
        else:
            return "severe"

class CulturalBridgeBuilder:
    """Facilitates cross-cultural understanding and challenges stereotypes"""
    
    def __init__(self):
        self.framework = PhilosophicalFramework()
        self.stereotype_patterns = self._build_stereotype_patterns()
        self.cultural_bridge_strategies = self._build_bridge_strategies()
        self.offensive_detector = OffensiveLanguageDetector() 
    
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
        
        offensive_analysis = self.offensive_detector.filter_and_suggest(query)
        
        response = "PHILOSOPHICAL ANALYSIS AND CULTURAL BRIDGE-BUILDING:\n\n"
        
        if offensive_analysis["has_offensive_content"]:
            response += "🚨 OFFENSIVE LANGUAGE DETECTED:\n"
            severity_emoji = {"mild": "⚠️", "moderate": "🛑", "severe": "🚨"}
            response += f"{severity_emoji.get(offensive_analysis['severity'], '⚠️')} Severity: {offensive_analysis['severity'].title()}\n"
            
            for category, patterns in offensive_analysis["detected_issues"].items():
                response += f"• {category.replace('_', ' ').title()}: Language that may be harmful or exclusionary\n"
            
            suggestions = offensive_analysis["suggestions"]
            
            if suggestions["specific_examples"]:
                response += "\n� BETTER WAYS TO SAY IT - SPECIFIC EXAMPLES:\n"
                for example in suggestions["specific_examples"][:3]:
                    response += f"• {example}\n"
            
            if suggestions["general_guidance"]:
                response += "\n💡 GENERAL GUIDANCE:\n"
                for guidance in suggestions["general_guidance"][:3]:
                    response += f"• {guidance}\n"
            
            if suggestions["philosophical_insights"]:
                response += "\n🤔 PHILOSOPHICAL INSIGHTS:\n"
                for insight in suggestions["philosophical_insights"][:2]:
                    response += f"• {insight}\n"
            
            response += "\n"
        
        if stereotypes:
            response += "⚠️  POTENTIAL ASSUMPTIONS TO EXAMINE:\n"
            for pattern_type, patterns in stereotypes.items():
                response += f"• {pattern_type.replace('_', ' ').title()}: Found patterns suggesting stereotypical thinking\n"
            
            suggestions = self.suggest_alternative_framings(query, stereotypes)
            response += "\n🌉 ALTERNATIVE FRAMINGS TO CONSIDER:\n"
            for suggestion in suggestions[:3]:
                response += f"• {suggestion}\n"
            
            response += "\n"
        
        response += "🤔 PHILOSOPHICAL QUESTIONS TO EXPLORE:\n"
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