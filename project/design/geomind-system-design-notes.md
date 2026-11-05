# GeoMind — GeoHackathon System Design Notes

## 1. Project Context

**GeoMind** is the proposed Agentic AI system for the **SPE Europe Energy GeoHackathon**.

The hackathon has two main challenges:

### Challenge 1 — Agentic AI Engineering Workflow
The system should be able to:

- understand the engineering problem
- interact with the GEMINI digital twin
- select and execute appropriate models/tools
- identify missing modelling capabilities
- integrate additional calculations/tools when required
- compare alternatives
- explain the reasoning behind the final configuration

### Challenge 2 — Integrated Heating and Cooling System Design
The system should help design an integrated geothermal energy system using:

- deep geothermal energy for direct heating
- heat exchangers
- heat pumps
- absorption/sorption cooling where useful
- chillers
- thermal storage
- auxiliary systems

The final result should include:

- realized heating capacity
- realized cooling capacity
- selected system configuration
- component sizing
- comparison of alternatives
- interaction with the agent
- prompts / answers / token usage

### Bonus Directions

Possible extensions include:

- multi-agent collaboration
- automated optimization
- uncertainty analysis
- techno-economic assessment
- automatic model generation
- autonomous verification

---

# 2. Main Interpretation of the Task

The main problem is **system design**, not primarily a control problem.

The system should:

1. create candidate geothermal system designs
2. size components
3. simulate/evaluate them
4. compare alternatives
5. optimize design variables
6. justify the final design

A useful high-level loop is:

```text
Design
  ↓
Optimize
  ↓
Simulate
  ↓
Evaluate
  ↓
Critique / Adapt
  └──────────────→ Design
```

Reinforcement Learning is **not required** for the core task.

RL could become useful later for dynamic operation/control, for example:

- hourly energy demand
- storage dispatch
- geothermal flow control
- heat-pump operation
- dynamic electricity prices

For the current hackathon, conventional and black-box optimization are more natural.

---

# 3. Level 1 — Maximum Abstraction

The highest-level representation is:

```text
Problem
   ↓
GeoMind Agentic AI System
   ↓
Solution
```

### Problem
May contain:

- user goals
- constraints
- engineering inputs
- files
- system data
- questions
- preferences

### Solution
May contain:

- final system design
- equipment sizing
- simulation results
- optimized parameters
- comparison of alternatives
- explanations
- reports/files/visualizations

---

# 4. Architecture Philosophy

We do **not** want:

- a rigid traditional stack
- hundreds of tiny modules from the beginning
- an architecture diagram that looks artificially complicated

We do want:

- a **module-based architecture**
- some logical layering for clarity
- each layer to contain multiple modules
- each module to potentially contain several agents/tools

The hierarchy is therefore:

```text
Layer
  └── Module
        ├── Agent
        ├── Agent
        └── Tool / Algorithm
```

Example:

```text
Design & Optimization Layer
  └── Optimization Module
        ├── Optimizer Selector Agent
        ├── SLSQP
        ├── Differential Evolution
        ├── Genetic Algorithm
        ├── Bayesian Optimization
        └── NSGA-II
```

Important principle:

> Layers are organizational boundaries, not hard communication barriers.

Modules can communicate with other modules when needed.

---

# 5. User-Facing Architecture

One important decision is that **the User and UI should be at the top of the architecture**.

Current high-level flow:

```text
User
  ↓
UI
  ↓
API
  ↓
GeoMind Core
  ↓
Engineering Capabilities
  ↓
Data / Knowledge / Tools
```

This is not intended to be a strict software stack. It is a useful architectural organization.

---

# 6. UI Layer

The UI should not be only a chatbot.

It should behave like a **workspace for autonomous engineering tasks**.

The user should be able to:

- start a design task
- start an optimization task
- monitor simulations
- inspect results
- change constraints
- ask questions
- interrupt or modify an ongoing workflow
- understand what GeoMind is currently doing

A good UI concept is:

```text
Chat + Task Workspace + Results Dashboard
```

## Core UI Areas

### Chat / Assistant
User can:

- describe the problem
- ask questions
- change goals
- modify constraints
- request explanations
- interact during execution

### Design Tasks
The user should see:

- task ID
- task description
- status
- created time
- candidate designs
- current design parameters
- which agent/module is working on it
- result / progress

Example:

```text
D-001 | Baseline system         | Completed
D-002 | Heat-pump configuration | Running
D-003 | Storage-assisted design | Pending
```

### Optimization Tasks
The user should see:

- optimization objective
- optimizer
- current iteration
- best objective value
- convergence curve
- candidate designs
- running/completed/failed status

### Simulation Tasks
The UI should show:

- simulation ID
- linked design
- current status
- progress
- input
- output
- errors/failures

### Task Timeline / Activity
The user should understand the workflow state:

```text
Problem interpreted
        ↓
Candidate systems generated
        ↓
Simulation started
        ↓
Optimization iteration 12
        ↓
Best design updated
        ↓
Final evaluation
```

This is important because the hackathon explicitly focuses on an **Agentic AI workflow**. The autonomous process should therefore be visible.

---

# 7. API Layer

The API is the boundary between the UI and the intelligent system.

Current architectural preference:

> Keep the API focused on communication and task management; keep agentic intelligence inside GeoMind Core.

Possible API responsibilities:

- authentication
- request handling
- user/session management
- task creation
- task status
- task cancellation
- file upload/download
- results retrieval
- WebSocket / real-time updates
- external API integration

Conceptually:

```text
UI
 ↕
REST API / WebSocket
 ↕
GeoMind Core
```

---

# 8. GeoMind Core

This is the intelligent center of the system.

The exact internal structure is **not finalized yet**.

Current candidate modules include:

- Interaction Module
- Problem Module
- Orchestration Module
- Design Module
- Optimization Module
- Memory / Context Module

We intentionally do not want to over-specify these too early.

---

# 9. Problem Representation

A major design requirement is that GeoMind needs an **internal representation of the engineering design problem**.

The system should transform:

```text
User messages
Files
Inputs
Constraints
Preferences
Engineering data
```

into a shared structured representation.

Possible names:

- Design Problem Specification
- Canonical Design Problem Representation
- Shared Design Problem State

Current preferred concept:

```text
Problem Interpreter
        ↓
Shared Design Problem State
```

The shared state can later contain:

- objectives
- constraints
- design variables
- available technologies/components
- models/tools
- uncertain parameters
- evaluation metrics
- user preferences

The exact schema should be defined at a lower abstraction level.

---

# 10. Problem Interpreter

Instead of calling the input component an **Encoder**, a clearer engineering name is:

**Problem Interpreter**

Alternatives considered:

- Problem Compiler
- Problem Normalizer

Its purpose is:

```text
User / Files / Inputs
        ↓
Problem Interpreter
        ↓
Design Problem Specification
```

---

# 11. Solution Output

Instead of calling the output component a **Decoder**, a better name is:

**Solution Composer**

Alternatives:

- Solution Synthesizer
- Result Interpreter

Its purpose is to transform internal results into something understandable and useful:

```text
Design Results
Simulation Results
Optimization Results
Trade-offs
        ↓
Solution Composer
        ↓
Final Engineering Solution
```

---

# 12. Two Main Operating Branches

## A. Human Interaction Branch
The user can:

- chat with GeoMind
- ask why a design was chosen
- change objectives
- add/remove constraints
- inspect results
- modify the problem while the system is running

## B. Autonomous Design Branch
GeoMind can independently:

- generate designs
- evaluate alternatives
- simulate designs
- optimize parameters
- compare candidates
- improve the design
- converge toward a solution

Both branches should interact with the same **Shared Design Problem State**.

Conceptually:

```text
            User / Chat
                ↕
        Shared Problem State
                ↕
     Autonomous Design System
```

Example: if the user says “Cost is now more important than efficiency,” the shared problem state updates and the autonomous design process continues using the new preference.

---

# 13. Design Module

The Design Module should generate candidate engineering configurations.

Possible responsibilities:

- generate system topology
- choose component combinations
- create candidate configurations
- modify existing designs
- create alternatives
- maintain candidate designs

Example geothermal design choices:

- direct geothermal heating
- geothermal + heat pump
- geothermal + heat pump + storage
- geothermal + absorption chiller
- geothermal + electric chiller
- hybrid heating/cooling system

The actual design-agent structure will be defined later.

---

# 14. Optimization Module

Optimization should be its **own module**.

Reason:

- optimization methods should be swappable
- new optimizers should be easy to add
- different problems may require different algorithms

Common conceptual interface:

```text
Design Variables
Objectives
Constraints
Evaluator
      ↓
Optimization Module
      ↓
Candidate Designs
```

Potential algorithms:

- SLSQP
- Differential Evolution
- Genetic Algorithm
- Bayesian Optimization
- CMA-ES
- NSGA-II

Potential future component: **Optimizer Selector**.

It can choose an optimization strategy based on:

- continuous vs discrete variables
- expensive simulations
- number of objectives
- constraint complexity
- design-space size

Example design variables:

- heat pump capacity
- chiller capacity
- thermal storage size
- geothermal flow rate
- reinjection temperature
- heat exchanger sizing

Example objectives:

- minimize CAPEX
- minimize OPEX
- minimize electricity usage
- maximize efficiency
- maximize geothermal utilization
- minimize emissions

---

# 15. Simulation Module

The Simulation Module should execute engineering models.

Possible responsibilities:

- call GEMINI models
- run component models
- run system calculations
- execute simulations
- collect simulation outputs
- manage failed runs
- support parallel execution

---

# 16. Evaluation Module

The Evaluation Module evaluates a candidate design.

Possible metrics:

- heating capacity
- cooling capacity
- electricity consumption
- geothermal utilization
- efficiency
- CAPEX
- OPEX
- emissions
- feasibility
- constraint violations
- reliability

Conceptually:

```text
Candidate Design
      ↓
Simulation
      ↓
Evaluation
      ↓
Score / Metrics
```

---

# 17. Verification

A possible dedicated Verification capability can check:

- engineering feasibility
- physical constraints
- component limits
- invalid configurations
- unrealistic values
- constraint violations

This may later be a separate module or part of Evaluation. That decision is still open.

---

# 18. Memory and Context

GeoMind should keep useful system state, such as:

- user conversation
- previous task decisions
- generated designs
- optimization history
- simulation results
- rejected candidates
- current best design
- user preference changes

Possible future distinction:

```text
Short-term task context
+
Long-term project memory
```

---

# 19. Engineering Capability Layer

Possible modules:

- Simulation Module
- Evaluation Module
- Verification Module
- Visualization Module
- Tool Integration Module

These modules may use:

- GEMINI
- numerical algorithms
- engineering equations
- optimization libraries
- external tools/APIs
- data-processing functions

---

# 20. LLM vs Non-LLM Responsibilities

The architecture should not force everything through an LLM.

## Good tasks for LLM agents

- understanding user intent
- interpreting the engineering problem
- planning
- deciding which tool to call
- generating design alternatives
- critiquing results
- explaining trade-offs
- interacting with the user
- composing final explanations

## Good tasks for deterministic / numerical tools

- simulation
- heat and mass balance
- component sizing
- optimization
- constraint checking
- economic calculation
- uncertainty calculation
- KPI computation

Key principle:

> LLMs reason and orchestrate; numerical tools calculate and verify.

---

# 21. Agent Harness

We want GeoMind to behave as a **large orchestration harness**, not just a single chatbot.

The harness can eventually manage:

- agents
- tools
- workflows
- state
- task scheduling
- optimization loops
- simulation calls
- feedback loops
- logs
- parallel exploration
- user intervention

But we do **not** want to define every internal agent yet.

---

# 22. GEMINI Role

GEMINI should be treated as an engineering modelling/simulation backend.

It is **not simply a large 3D reservoir simulator like CMG or OPM**.

It provides engineering and plant-level capabilities and includes models such as:

- production wells
- injection wells
- ESP
- injection pump
- booster pump
- heat exchanger
- reservoir
- degasser
- filter
- gas boiler

Templates also exist for components such as:

- heat pump
- electric boiler
- CHP
- heat demand

However, presence of a template does not automatically mean the component is fully implemented in the current runtime.

Therefore:

```text
GeoMind
   ↓
GEMINI + Additional Engineering Models
```

may be required.

---

# 23. Current GEMINI AI Capability

The existing GEMINI repository includes AI/RAG functionality using tools such as:

- Ollama
- ChromaDB
- LangChain

The current chat functionality is mainly:

```text
Documents
   ↓
Embedding / Retrieval
   ↓
LLM
   ↓
Answer
```

This is not yet the autonomous multi-agent workflow required for the hackathon.

Therefore GeoMind should build the agentic layer around/above GEMINI.

---

# 24. Current Proposed Logical Organization

```text
┌──────────────────────────────────────────────┐
│                    USER                      │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│                 UI LAYER                     │
│ Chat | Tasks | Results | Dashboard          │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│                 API LAYER                    │
│ Requests | Tasks | Files | Real-time Updates│
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│              GEOMIND CORE                    │
│ Problem | Design | Optimization |           │
│ Orchestration | Memory                      │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│          ENGINEERING CAPABILITIES            │
│ Simulation | Evaluation | Verification      │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│             DATA & KNOWLEDGE                 │
│ Models | Files | Results | Knowledge | Data │
└──────────────────────────────────────────────┘
```

This is **not final**. It is the current architectural direction.

---

# 25. Important Architectural Principles

We want the system to be:

### Modular
Each capability can evolve independently.

### Observable
The user can see what the autonomous system is doing.

### Interactive
The user can intervene during execution.

### Agentic
The system can independently plan and execute engineering workflows.

### Tool-driven
LLMs should use engineering tools rather than invent numerical answers.

### Extensible
New tools, optimizers, models, and agents can be plugged in.

### Closed-loop
Results should influence the next design decision.

---

# 26. Current Architecture Decisions

Decisions that are relatively established:

- Project name: **GeoMind**
- GeoMind is an **Agentic AI System**
- Highest-level abstraction: `Problem → GeoMind → Solution`
- Architecture should be **module-based**
- We still want some logical layering
- Each layer contains multiple modules
- Each module may contain multiple agents/tools
- User should be at the top
- UI comes before API
- UI must expose autonomous tasks
- Design and Optimization tasks should be visible
- API should mostly handle communication/task management
- Core intelligence should stay inside GeoMind
- Design and Optimization should remain separate conceptual modules
- Optimization algorithms should be plug-and-play
- System should support human interaction and autonomous design simultaneously
- A shared problem representation/state is required
- GEMINI is an engineering backend/tool, not the whole agentic system

---

# 27. Things Intentionally Not Finalized Yet

We have intentionally **not** finalized:

- exact number of layers
- exact number of modules
- exact agents inside each module
- precise module-to-module interfaces
- event bus/message protocol
- database choice
- backend framework
- frontend framework
- task scheduler
- agent framework
- workflow engine
- optimizer-selection logic
- final problem-state schema
- whether Verification is independent or part of Evaluation
- exact GEMINI extensions required

These should be designed gradually rather than invented all at once.

---

# 28. Recommended Next Design Step

The next step should **not** be adding more boxes.

The next step should be to define the responsibilities of the major modules one by one.

Suggested order:

```text
1. UI / Task interaction
2. API boundary
3. Problem Module
4. Orchestration Module
5. Design Module
6. Optimization Module
7. Simulation + Evaluation
8. Shared state / memory
```

For each module, define only:

```text
Purpose
Inputs
Outputs
Who calls it
What it calls
State it owns
```

Only after that should we define internal agents.

---

# 29. Working Design Principle

> **Do not create an agent just because something can be an agent.**

First ask:

- Is this reasoning-heavy?
- Does it need autonomy?
- Does it need language understanding?
- Does it need to select among tools?

If not, it should probably be:

- a normal module
- deterministic function
- numerical algorithm
- service
- optimizer
- simulator

This keeps GeoMind technically credible and prevents an unnecessarily complicated multi-agent architecture.

---

# 30. Current Mental Model

```text
                         USER
                          │
                          ▼
                   ┌────────────┐
                   │     UI     │
                   │ Chat/Tasks │
                   └─────┬──────┘
                         │
                         ▼
                   ┌────────────┐
                   │    API     │
                   └─────┬──────┘
                         │
                         ▼
              ┌──────────────────────┐
              │     GEOMIND CORE     │
              │                      │
              │ Problem              │
              │ Orchestration        │
              │ Design               │
              │ Optimization         │
              │ Memory / Context     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ ENGINEERING MODULES  │
              │                      │
              │ Simulation           │
              │ Evaluation           │
              │ Verification         │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   TOOLS / DATA / KB  │
              │ GEMINI / Models /    │
              │ Files / Results      │
              └──────────────────────┘
```

The architecture will evolve from this point **incrementally**.
