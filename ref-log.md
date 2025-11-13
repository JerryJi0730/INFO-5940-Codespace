# Reflection Log: Multi-Agent Travel Planner Implementation

## What I Learned from Implementing a Multi-Agent Workflow

Implementing a multi-agent workflow for the travel planner taught me the power of decomposing complex problems into specialized, communicative roles. The key insight was that separating concerns—Planner vs. Reviewer—creates natural quality gates. The Planner operates without internet constraints, focusing on creative itinerary generation, while the Reviewer acts as a grounded validator using real-time data. This division mirrors human collaboration: brainstorming first, fact-checking second.

I learned that prompt design is crucial for agent behavior. Clear role definitions, explicit output formats, and specific constraints (e.g., "do not invent facts") directly influence agent performance. The Reviewer's Delta List concept—a structured list of concrete changes with reasons—proved more actionable than vague corrections. Similarly, telling the Planner "you have no internet access" paradoxically improved output quality by forcing it to leverage its knowledge confidently rather than hedge uncertainties.

## Challenges and Solutions

**Challenge 1: API Key Authentication (401 Error)**
The devcontainer set OPENAI_API_KEY to an empty string, preventing load_dotenv() from overriding it. Solution: Added explicit override logic after load_dotenv() to check for empty values and load from .env directly using dotenv_values().

**Challenge 2: Prompt Ambiguity**
Initial instructions were vague ("validate the itinerary"). The Reviewer wasn't clear on what constituted a valid change or how to structure output. Solution: Redesigned prompts with explicit sections (Delta List, Search Log, Revised Itinerary) and concrete examples ("Source: internet_search for 'Louvre opening hours'").

**Challenge 3: Tool Integration**
Adding internet_search to the Reviewer required understanding how the agents framework passes tools.

## Design Choices

**Delta List Format**: Instead of showing a "validated itinerary" with inline notes, I adopted a structured Delta List format. This makes corrections transparent and actionable: each change shows original→revised with reasoning and confidence levels.

**Conservative Cost Estimates**: I instructed both agents to round cost estimates upward slightly, reducing the risk of budget overruns for users.

**Explicit Knowledge Boundaries**: By telling the Planner it has no internet access and the Reviewer it must verify facts via search, I created clear accountability and reduced hallucination risks.

## External Tools and Assistance

Used GitHub Copilot (Claude Haiku 4.5) for:
- Debugging the environment variable loading issue
- Refining prompt language for clarity
- Structuring the Delta List output format

Why: Iterating on prompts and troubleshooting environment quirks required rapid feedback and multiple revisions—areas where AI assistance significantly accelerated development.
