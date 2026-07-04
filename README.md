# AI Career Coach

An intelligent multi-agent system that generates personalized, professional career roadmaps. Built with Google Gemini and a modular agent pipeline, it analyzes a user's career goal and produces a structured learning plan with technical recommendations, certifications, projects, and timelines.

---

## Architecture

The system follows a **sequential agent pipeline** where each agent specializes in one phase of roadmap generation. Agents communicate through an in-memory shared store, keeping them decoupled and independently testable.

```
User Query
    │
    ▼
┌─────────────┐
│  Planner    │  Creates a structured learning plan
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Researcher │  Identifies skills, tools, certifications, trends
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Writer     │  Formats a professional roadmap document
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Reviewer   │  Polishes, deduplicates, and improves flow
└──────┬──────┘
       │
       ▼
  Final Roadmap
```

### Agent Responsibilities

| Agent | Role | Prompt Focus |
|-------|------|-------------|
| **Planner** | Analyze the career goal and break it into logical learning phases | Structured execution plan |
| **Researcher** | Research required skills, technologies, certifications, and industry trends | Technical depth and relevance |
| **Writer** | Convert research into a clean, readable roadmap with headings, timelines, and projects | Formatting and clarity |
| **Reviewer** | Review and polish the final roadmap — remove duplicates, improve flow and completeness | Quality assurance |

---

## Project Structure

```
ai-career-coach/
├── app.py                    # Entry point — runs the full agent pipeline
├── config.py                 # Environment variable loading and validation
├── .env.example              # Template for environment configuration
├── .gitignore
├── README.md
│
├── agents/
│   ├── base_agent.py         # Abstract base class for all agents
│   ├── planner_agent.py      # Career plan generation
│   ├── research_agent.py     # Skills and technology research
│   ├── writer_agent.py       # Roadmap writing and formatting
│   └── reviewer_agent.py     # Roadmap review and refinement
│
├── prompts/
│   ├── planner_prompt.py     # Prompt template for the Planner
│   ├── researcher_prompt.py  # Prompt template for the Researcher
│   ├── writer_prompt.py      # Prompt template for the Writer
│   └── reviewer_prompt.py    # Prompt template for the Reviewer
│
├── services/
│   └── gemini_service.py     # Google Gemini API wrapper
│
├── memory/
│   └── shared_memory.py      # In-memory key-value store for agent communication
│
└── models/
    └── agent_response.py     # Standardised AgentResponse dataclass
```

### Key Components

**`app.py`** — The entry point. Captures the user's career goal, initialises shared memory and the Gemini service, then runs the four agents sequentially. Prints the final roadmap to the console.

**`config.py`** — Loads `GEMINI_API_KEY` and `MODEL_NAME` from the environment (`.env` file). Validates that the API key is present on startup.

**`services/gemini_service.py`** — Thin wrapper around the `google-genai` SDK. Provides a single `generate_response(prompt)` method that all agents call. Keeps API-specific logic isolated from business logic.

**`memory/shared_memory.py`** — A simple in-memory dictionary shared across all agents. Each agent reads the previous agent's output and writes its own result, forming the communication backbone of the pipeline.

**`models/agent_response.py`** — A `@dataclass` that standardises every agent's output with fields: `agent_name`, `output`, `status`, `error`, `timestamp`.

**`agents/base_agent.py`** — Abstract base class. Defines the `execute()` workflow: build prompt → call Gemini → wrap response in `AgentResponse` → store in shared memory. Concrete agents only implement `get_agent_name()`, `get_memory_key()`, and `build_prompt()`.

---

## Prerequisites

- Python 3.10+
- A Google Gemini API key ([get one here](https://aistudio.google.com/apikey))

---

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/Anhad-01/AI-career-coach.git
   cd ai-career-coach
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install google-genai python-dotenv
   ```

4. **Configure environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set your Gemini API key:

   ```
   GEMINI_API_KEY=your_actual_api_key
   MODEL_NAME=gemini-2.5-flash
   ```

   > `MODEL_NAME` defaults to `gemini-2.5-flash` if not specified.

---

## Usage

Run the application:

```bash
python app.py
```

You will be prompted to enter a career goal. For example:

```
Enter your career goal:
I am a Java developer with 3 years of experience. I want to become a Machine Learning Engineer.
```

The system runs all four agents and prints the final career roadmap to the console.

---

## Example Workflow

```
======================================================================
AI Career Coach
======================================================================
Enter your career goal:
> I am a frontend developer wanting to transition to DevOps

 Planning career roadmap...
 Researching latest technologies...
 Writing professional roadmap...
 Reviewing final roadmap...
======================================================================
FINAL CAREER ROADMAP:
======================================================================
[Gemini-generated roadmap with phases, skills, tools, certifications,
projects, and a timeline]
```

---

## Extending the System

### Adding a new agent

1. Create a prompt template in `prompts/`.
2. Create an agent class in `agents/` that inherits from `BaseAgent`.
3. Implement `get_agent_name()`, `get_memory_key()`, and `build_prompt()`.
4. Register the agent in `app.py` — instantiate it and call `execute()` at the desired point in the pipeline.

### Swapping the LLM

Replace `services/gemini_service.py` with a wrapper for another provider (OpenAI, Anthropic, etc.). The rest of the system is unaffected as long as the `generate_response(prompt)` interface is preserved.
