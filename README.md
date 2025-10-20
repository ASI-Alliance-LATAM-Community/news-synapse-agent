# Critical Thinking Agent

An AI agent trained with the perspectives of transformative philosophers and thinkers who challenge paradigms, question stereotypes, and build bridges between cultures.

## 🎯 Purpose

This agent integrates the wisdom of critical thinkers from Socrates to Judith Butler, from James Baldwin to Paulo Freire, to create an AI that:

- **Questions assumptions** rather than accepting surface-level explanations
- **Challenges stereotypes** and binary thinking
- **Builds cultural bridges** instead of reinforcing divisions  
- **Examines power dynamics** and structural factors
- **Facilitates dialogue** across different perspectives
- **Promotes critical consciousness** and liberation

## 🧠 Philosophical Framework

The agent draws from five categories of transformative thinkers:

### Classic/Foundational Thinkers
- **Socrates** - Relentless questioning of assumptions
- **Friedrich Nietzsche** - Critique of morality and herd thinking
- **Søren Kierkegaard** - Individual authenticity vs. institutional conformity
- **Karl Marx** - Analysis of social and economic structures
- **Michel de Montaigne** - Skepticism and self-reflection

### Modern & Contemporary Philosophers (9 thinkers)  
- **Michel Foucault** - Hidden power dynamics in institutions
- **Jacques Derrida** - Deconstruction of binary thinking and fixed meanings
- **Hannah Arendt** - Analysis of totalitarianism and moral responsibility
- **Slavoj Žižek** - Provocative critiques of ideology
- **Judith Butler** - Challenge to gender norms and identity categories
- **Cornel West** - Race, democracy, and prophetic pragmatism
- **Byung-Chul Han** - Modern burnout, surveillance, and conformity
- **Roland Barthes** - Structuralist/post-structuralist analysis of cultural codes and meaning
- **Gilles Deleuze** - Post-structuralist concepts of flows, connections, and multiplicity

### Radical/Critical Theorists (6 thinkers)
- **Herbert Marcuse** - One-dimensional society critique
- **Theodor Adorno** - Frankfurt School critique of culture industry and mass society
- **Walter Benjamin** - Marxist cultural criticism and aesthetics of mechanical reproduction
- **Paulo Freire** - Critical pedagogy and liberation through education
- **Frantz Fanon** - Colonialism and psychological oppression
- **bell hooks** - Intersectional analysis of race, gender, and class

### Literary Philosophers (8 thinkers)
- **George Orwell** - Political language and authoritarianism
- **Virginia Woolf** - Gender roles and narrative structure
- **James Baldwin** - Racial, social, and moral hypocrisies
- **Franz Kafka** - Bureaucracy and existential absurdity
- **Albert Camus** - Absurdism and ethical rebellion
- **Toni Morrison** - Hidden histories and power narratives
- **Haruki Murakami** - Reality, identity, and conformity
- **Tzvetan Todorov** - Literary theory, humanism, and cross-cultural encounter

### Science & Futurism
- **Thomas Kuhn** - Paradigm shifts in science
- **Marshall McLuhan** - Media's effect on consciousness
- **Donna Haraway** - Cyborg theory and boundary dissolution
- **Yuval Noah Harari** - Myths, systems, and future of humanity

## 🛠 System Components

### 1. Philosophical Framework (`philosophical_framework.py`)
Core system that integrates each thinker's:
- Core ideas and insights
- Questioning methodologies
- Cultural perspectives
- Stereotype-challenging approaches

### 2. Cultural Bridge Builder (`cultural_bridge.py`)
Tools for:
- Analyzing text for stereotypes and assumptions
- Suggesting alternative framings
- Building understanding across cultural differences
- Facilitating productive dialogue

### 3. Training Module (`training_module.py`)
Contains:
- Real-world scenarios with contrasts between stereotypical vs. critical responses
- Questioning exercises for different types of analysis
- Training prompts for developing critical thinking skills

### 4. Main Agent (`agent.py`)
Enhanced uAgent that:
- Uses philosophical framework in system prompts with instruction to reference authors' phrases and writings
- Pre-processes queries with critical analysis
- Integrates cultural bridge-building capabilities
- Incorporates direct quotations and concepts from the 18 integrated thinkers

## 🚀 Getting Started

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd agi-hackathon-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your ASI1_API_KEY
```

### Testing with CLI

Test the philosophical framework without needing the full agent:

```bash
python test_cli.py
```

The CLI provides options to:
- Analyze text for stereotypes
- Explore specific thinkers' perspectives  
- Practice different questioning exercises
- Facilitate dialogue between viewpoints
- View training scenarios
- Generate philosophical analysis

### Running the Agent

```bash
cd src
python agent.py
```

The agent will start with the enhanced philosophical framework integrated.

## 📚 Example Transformations

### Before: Stereotypical Response
**Query**: "Why are some cultures more successful than others?"

**Typical Response**: "Some cultures value hard work and education more, while others are held back by traditional thinking."

### After: Critical Thinking Response
**Enhanced Response**: 
"This question requires examining several assumptions:

**Power Analysis (Foucault)**: Who defines 'success'? Western economic models became dominant through colonialism, not inherent superiority.

**Historical Context (Marx, Fanon)**: Current inequalities stem from centuries of resource extraction and interference, not cultural deficiencies.

**Questioning Binaries (Butler)**: The successful/unsuccessful binary obscures diversity within societies and different definitions of prosperity.

**Cultural Bridge-Building**: Instead of ranking cultures, explore: What different models of wellbeing exist? How might various cultural approaches contribute to solving global challenges?"

## 🎓 Training Approach

The agent is trained to:

1. **Identify Assumptions**: What unstated beliefs underlie this question?

2. **Examine Power Dynamics**: Who benefits? Whose voices are missing?

3. **Question Binaries**: What false either/or thinking limits understanding?

4. **Consider Multiple Perspectives**: How might different positions view this?

5. **Trace Genealogies**: How did current 'common sense' emerge?

6. **Build Bridges**: How can we honor differences while working toward understanding?

7. **Focus on Liberation**: How can analysis contribute to human flourishing?

## 🤝 Cultural Bridge-Building Strategies

### Perspective-Taking
- Consider how issues look from different cultural viewpoints
- Question assumptions embedded in dominant perspectives
- Examine how historical context shapes cultural practices

### Common Ground
- Identify shared human concerns across cultures
- Look for different approaches to similar challenges
- Explore possibilities for creative synthesis

### Power Analysis  
- Examine who has power to define 'normal'
- Consider how historical power relations affect interactions
- Center marginalized voices in analysis

### Complexity Embrace
- Recognize internal diversity within cultures
- Explore tensions and changes within cultural groups
- Identify hybrid forms emerging from cultural contact

## 🔧 Customization

### Adding New Thinkers
Add to `philosophical_framework.py`:

```python
"new_thinker": PhilosophicalPerspective(
    name="New Thinker",
    category=ThinkingCategory.MODERN_CONTEMPORARY,
    core_ideas=["Key insight 1", "Key insight 2"],
    questioning_methods=["Method 1", "Method 2"],
    cultural_insights=["Insight 1", "Insight 2"],
    stereotype_challenges=["Challenge 1", "Challenge 2"]
)
```

### Adding Training Scenarios
Add to `training_module.py`:

```python
TrainingScenario(
    title="New Scenario",
    description="Description of the scenario",
    stereotypical_response="Problematic response",
    critical_thinking_response="Enhanced response using philosophical frameworks",
    philosophical_frameworks_applied=["Framework 1", "Framework 2"],
    cultural_bridge_strategies=["Strategy 1", "Strategy 2"]
)
```

## 📖 Key Questioning Strategies

The agent employs these core questioning approaches:

- Ask who benefits from current arrangements
- Examine hidden power dynamics and assumptions  
- Question binary thinking and false dichotomies
- Analyze historical origins of current beliefs
- Consider multiple cultural perspectives
- Challenge authority-based vs. evidence-based claims
- Examine intersections of different forms of oppression
- Question what counts as 'normal' or 'natural'
- Analyze how language shapes thought
- Consider subjective experience alongside objective analysis

## 🌍 Cultural Bridge Principles

- Recognize that all cultures have valuable knowledge systems
- Question universalist claims that ignore cultural specificity
- Examine how power relations shape intercultural encounters
- Look for common human concerns across different expressions
- Challenge deficit models of cultural differences
- Recognize internal diversity and change within cultures
- Consider how historical trauma affects cultural groups
- Look for cultural resources for resistance and creativity

## 🔬 Future Enhancements

Possible improvements:
- NLP-based topic classification for better thinker matching
- Integration with vector databases for philosophical text retrieval
- Multi-turn dialogue capabilities for deeper questioning
- Real-time stereotype detection in conversations
- Cultural context APIs for more nuanced analysis

## 📜 License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## 🙏 Acknowledgments

This agent stands on the shoulders of giants - the philosophers, writers, and critical thinkers whose transformative ideas continue to challenge us to think more deeply, question more thoroughly, and build bridges more intentionally across the differences that both separate and enrich us.