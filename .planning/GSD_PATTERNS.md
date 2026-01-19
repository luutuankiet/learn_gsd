# GSD Context Engineering Patterns

**Created:** 2026-01-19
**Purpose:** Analysis of Get-Shit-Done patterns from glittercowboy/get-shit-done and application to this project's session handoff and context engineering work

## Overview

This document analyzes the core patterns from the GSD framework and provides concrete suggestions for applying them to our data engineering copilot patterns project, specifically for Phase 2 (Session Handoff) and Phase 3 (Context Engineering).

---

## Pattern 1: XML-Structured Instructions

### What It Is

GSD uses XML elements with semantic tags instead of pure markdown for agent instructions. Workflows, plan files, and templates structure content with explicit semantic boundaries.

**Example:**
```xml
<task type="auto">
  <name>Deploy to Vercel</name>
  <files>.vercel/, vercel.json</files>
  <action>Run `vercel --yes` to deploy</action>
  <verify>vercel ls shows deployment</verify>
  <done>App deployed, URL captured</done>
</task>
```

### Why It Works

1. **Parsing clarity**: Agents can extract structured information without ambiguous markdown parsing
2. **Semantic meaning**: `<action>` vs `<verify>` vs `<done>` are explicit, not inferred from section headers
3. **Nested context**: XML allows hierarchical structure - tasks contain actions, checkpoints have typed attributes
4. **Attribute metadata**: `type="auto"`, `gate="blocking"`, `tdd="true"` provide execution hints without polluting content

### Application to This Project

**Phase 2 (Session Handoff):**
- LOOPS.md template could use `<loop status="open|clarifying|closed">` instead of markdown status tags
- CONTEXT.md token tracking: `<context_loaded budget="2500" used="1847">` with nested file elements
- Session summary format: `<session><loops>...</loops><decisions>...</decisions></session>`

**Phase 3 (Context Engineering):**
- Context scoping framework: `<scope type="lineage" root_model="..."><included>...</included><excluded reason="...">...</excluded></scope>`
- Progressive loading strategy: `<load phase="initial|expanded"><files>...</files></load>`
- Token budget tracking: `<budget total="5000" loaded="2300" remaining="2700" threshold="warning">`

**Benefits for data engineering:**
- dbt model lineage: `<lineage depth="3" direction="downstream"><models>...</models></lineage>`
- Context decisions become queryable: grep for `<excluded reason="test_files">` to review what was cut
- Clearer handoff protocol: `<handoff><prior_session>...</prior_session><continuation>...</continuation></handoff>`

---

## Pattern 2: Context Layering

### What It Is

GSD maintains separate artifact files that layer context from broad to specific:
1. **PROJECT.md** - Vision, core value, constraints (rarely changes)
2. **REQUIREMENTS.md** - What must be true (stable requirements)
3. **ROADMAP.md** - Phases and plans (updated as phases complete)
4. **STATE.md** - Current position, recent decisions, session continuity (changes every session)

Each layer references the prior layer but doesn't duplicate it.

### Why It Works

1. **Stable base**: PROJECT.md loaded once, provides consistent foundation
2. **Selective loading**: STATE.md changes frequently but is small (~150 lines), so loading it every session is cheap
3. **Context accumulation**: Decisions from completed phases flow into STATE.md, not buried in chat history
4. **Fresh context windows**: Agents read these files at session start instead of reconstructing from conversation

### Application to This Project

**Phase 2 (Session Handoff):**

Our equivalent layering for data engineering work:
1. **PROJECT_CONTEXT.md** - Problem being solved, business context, data domain (changes rarely)
2. **LOOPS.md** - Open questions, blockers, clarifications needed (ephemeral working memory)
3. **CONTEXT.md** - What's loaded this session, token budget, exclusion decisions (session-specific)
4. **SESSION_SUMMARY.md** - Export format for TickTick (captures loops + context decisions)

**Key insight from GSD:**
- STATE.md's "Accumulated Context" section = our SESSION_SUMMARY.md export to GTD
- Fresh agent reads STATE.md to resume = our handoff agent reads prior SESSION_SUMMARY.md
- Decisions don't pollute working memory - they live in structured artifacts

**Phase 3 (Context Engineering):**

Context layering for large codebases:
1. **CODEBASE_MAP.md** - High-level architecture, conventions (stable)
2. **LINEAGE.md** - Relevant models/files for current task (task-specific)
3. **CONTEXT_DECISIONS.md** - Why this scope? What was excluded? (audit trail)
4. **SLIM_MANIFEST.json** - Token-optimized dbt manifest (generated via dbt-mp)

**Benefits:**
- Token budget stays in budget: load full CODEBASE_MAP (1k tokens) + task-specific LINEAGE (2k tokens) vs dumping full manifest (500k tokens)
- Progressive loading: start with LINEAGE, expand to full manifest only if agent hits unknown dependency
- Decisions preserved: "Why did we exclude test files?" → CONTEXT_DECISIONS.md has rationale

---

## Pattern 3: Fresh Context Windows via Multi-Agent Orchestration

### What It Is

GSD orchestrator spawns subagents for autonomous work segments, then aggregates results. Each subagent gets fresh 200k context window (0% utilization at start).

**Pattern A (Fully Autonomous):**
- Plan has no checkpoints
- Spawn single subagent for entire plan
- Subagent executes all tasks, creates SUMMARY, commits
- Main context usage: ~5% (just orchestration)

**Pattern B (Segmented):**
- Plan has verify-only checkpoints
- Spawn subagent per segment (tasks between checkpoints)
- Main context handles checkpoints (~20% usage total)
- Each subagent: fresh 0-30% usage

### Why It Works

1. **Quality preservation**: Autonomous work never degrades - fresh context every time
2. **Scale beyond limits**: Can handle 10+ task plans if properly segmented
3. **Main context efficiency**: Orchestrator stays lean, only loads planning artifacts
4. **Checkpoint isolation**: Human interactions don't pollute task execution context

### Application to This Project

**Phase 2 (Session Handoff):**

We're building single-session patterns (no orchestration), but the principle applies:
- **Session working memory** (LOOPS.md, CONTEXT.md) = ephemeral, cleared between sessions
- **Handoff protocol** = export to GTD, fresh agent imports clarified items
- Each new session starts with fresh context window (0% usage) by reading STATE files

**Key insight from GSD:**
- Don't accumulate context within a session - export and reimport
- SESSION_SUMMARY.md = checkpoint between sessions
- Fresh agent reads summary to continue = GSD's continuation agent pattern

**Phase 3 (Context Engineering):**

For large dbt refactors (200+ model lineage):
- **Initial load** (narrow scope): Root model + immediate parents/children (2k tokens)
- **If agent needs more**: Expand to full lineage progressively
- **Token budget pattern**: Start at 20% usage, only expand to 50% if actually needed
- **Context decision log**: Document each expansion (why? what was added?)

**Pattern for 200+ model lineage:**
1. Load SLIM_MANIFEST (dbt-mp output: 15k tokens for 400 models)
2. Agent identifies relevant subset (20 models)
3. Load full metadata for those 20 models only
4. If agent encounters unknown dependency → expand scope, log decision
5. Session summary documents: "Started with 20 models, expanded to 35 after discovering dependency X"

---

## Pattern 4: Wave-Based Parallel Execution

### What It Is

Plans within a phase can execute in parallel if they have no dependencies. Dependency graph (`depends_on` in frontmatter) ensures correct ordering.

**Example:**
```yaml
# Plan 01-01: Foundation
depends_on: []

# Plan 01-02: Auth (can run parallel with 01-03)
depends_on: [01-01]

# Plan 01-03: Database (can run parallel with 01-02)
depends_on: [01-01]

# Plan 01-04: Integration (waits for both)
depends_on: [01-02, 01-03]
```

Wave 1: 01-01
Wave 2: 01-02, 01-03 (parallel)
Wave 3: 01-04

### Why It Works

1. **Faster execution**: Independent work happens concurrently
2. **File ownership**: Each plan owns specific files, no conflicts
3. **Clear dependencies**: Explicit graph prevents ordering issues
4. **Milestone velocity**: Multiple agents can work simultaneously

### Application to This Project

**Not directly applicable** - We're building documentation/templates, not executing parallel work.

**However, the dependency pattern is valuable:**

**Phase 2 plans could be:**
- Plan 2-01: LOOPS.md template (no dependencies)
- Plan 2-02: CONTEXT.md template (no dependencies)
- Plan 2-03: Session summary format (depends on 2-01, 2-02)
- Plan 2-04: TickTick export protocol (depends on 2-03)

**Phase 3 plans:**
- Plan 3-01: Context scoping framework (no dependencies)
- Plan 3-02: Token budget patterns (depends on 2-02 CONTEXT.md template)
- Plan 3-03: dbt-mp integration guide (depends on 3-01, 3-02)
- Plan 3-04: Progressive loading strategy (depends on 3-01, 3-02)

**Benefit:**
- ROADMAP.md can show dependency graph visually
- Future execution: Could validate plans against dependencies
- Documentation clarity: Readers understand prerequisites

---

## Pattern 5: Artifact Organization in .planning/

### What It Is

GSD maintains all planning artifacts in `.planning/` directory with clear structure:
```
.planning/
├── PROJECT.md              # Vision, constraints
├── REQUIREMENTS.md         # What must be true
├── ROADMAP.md              # Phases and plans
├── STATE.md                # Current position, decisions
├── phases/
│   ├── 01-foundation/
│   │   ├── 01-01-PLAN.md
│   │   ├── 01-01-SUMMARY.md
│   │   ├── 01-02-PLAN.md
│   │   └── 01-02-SUMMARY.md
│   └── 02-auth/
│       ├── 02-01-PLAN.md
│       └── 02-01-SUMMARY.md
```

### Why It Works

1. **Context rot prevention**: Old plans/summaries in dated directories, not polluting working context
2. **Git history**: Planning decisions visible in commit log
3. **Pattern consistency**: Every project has same structure
4. **Agent navigation**: Agents know where to find artifacts
5. **Human readability**: Directory structure = execution timeline

### Application to This Project

**We already use this pattern!** Our `.planning/` has:
- PROJECT.md
- REQUIREMENTS.md
- ROADMAP.md
- STATE.md
- phases/ (ready for phase directories)

**Enhancement for Phase 2:**
Add session artifacts to structure:
```
.planning/
├── PROJECT.md
├── REQUIREMENTS.md
├── ROADMAP.md
├── STATE.md
├── sessions/               # NEW: Session handoff artifacts
│   ├── 2026-01-19-refactor-models/
│   │   ├── LOOPS.md
│   │   ├── CONTEXT.md
│   │   └── SUMMARY.md
│   └── 2026-01-20-fix-tests/
│       ├── LOOPS.md
│       ├── CONTEXT.md
│       └── SUMMARY.md
└── phases/
    └── ...
```

**Benefits:**
- Session artifacts don't pollute project-level .planning/
- Historical sessions preserved for learning
- Each session = dated directory with complete handoff state
- Can review past context decisions: "How did we scope the refactor last time?"

---

## Pattern 6: Goal-Backward Methodology (Truths → Artifacts → Key Links)

### What It Is

Plan frontmatter defines success via `must_haves` section:
```yaml
must_haves:
  truths:
    - "Auth middleware protects /api/dashboard routes"
    - "Invalid tokens return 401 with error message"
  artifacts:
    - path: "src/middleware/auth.ts"
      provides: "JWT validation middleware"
      min_lines: 50
  key_links:
    - from: "middleware.ts"
      to: "auth API routes"
      via: "JWT validation"
```

### Why It Works

1. **Verifiable outcomes**: "Does auth middleware exist?" vs "Implement auth" (how do you verify?)
2. **File existence checks**: Agents can verify artifacts were created
3. **Relationship validation**: key_links ensure integration, not just file creation
4. **Pattern detection**: Can grep for specific implementation patterns

### Application to This Project

**Phase 2 (Session Handoff):**

Templates as must_haves:
```yaml
must_haves:
  truths:
    - "LOOPS.md template has clear status transitions (open → clarifying → closed)"
    - "CONTEXT.md tracks token budget with loaded/excluded breakdown"
    - "Session summary exports to TickTick-compatible format"
  artifacts:
    - path: "templates/LOOPS.md"
      provides: "Loop capture template with status workflow"
      min_lines: 30
    - path: "templates/CONTEXT.md"
      provides: "Token budget tracking template"
      min_lines: 40
  key_links:
    - from: "LOOPS.md"
      to: "SESSION_SUMMARY.md"
      via: "Loop export format"
      pattern: "status.*closed.*→.*summary"
```

**Phase 3 (Context Engineering):**

Patterns as must_haves:
```yaml
must_haves:
  truths:
    - "Context scoping framework works for any project type (not dbt-specific)"
    - "Token budget stays within 1k-5k range across scenarios"
    - "Progressive loading documents why scope expanded"
  artifacts:
    - path: "guides/context-scoping.md"
      provides: "Framework for deciding what to load vs exclude"
      min_lines: 100
    - path: "guides/progressive-loading.md"
      provides: "Strategy for starting narrow and expanding when needed"
      min_lines: 80
  key_links:
    - from: "context-scoping.md"
      to: "dbt-mp integration guide"
      via: "Token budget enforcement"
      pattern: "budget.*5000.*dbt-mp"
```

**Benefits:**
- Verifiable success criteria (not subjective "good enough")
- Agent can check: "Does this artifact exist? Does it have min_lines? Does it contain pattern?"
- Key_links ensure templates integrate, not exist in isolation

---

## Pattern 7: Task Sizing and Context Budgets (50% Rule)

### What It Is

GSD uses quality degradation curve to size work:
- **0-30% context**: Peak quality, all capabilities available
- **30-50% context**: Still good, start being conservative
- **50-70% context**: Quality degrades, simple tasks only
- **70%+ context**: Avoid - high error rate

**Planning heuristic:**
- Phases: 2-4 plans each
- Plans: 3-6 tasks each
- Target: Stay under 50% context per plan execution

### Why It Works

1. **Quality preservation**: Work completes before context degradation
2. **Predictable execution**: Know when to stop and spawn fresh context
3. **Scope forcing function**: Can't cram 20 tasks into one plan - forces decomposition
4. **Error prevention**: Stop before quality cliff

### Application to This Project

**Not directly applicable** - We're focused on single-session optimization, not multi-plan execution.

**However, the principle applies to data engineering work:**

**Phase 3 context engineering patterns:**

Token budget for dbt refactoring:
- **Start narrow** (20% budget): Root model + immediate dependencies
- **Conservative expansion** (40% budget): Add downstream models if needed
- **Warning threshold** (50% budget): Document why expansion needed, consider stopping
- **Red line** (60%+): Do NOT load more - split into multiple sessions

**Example scenario: Refactoring grain change**
1. Load root model + 2 parents + 5 children (2k tokens, 20% budget)
2. Agent discovers dependency → add 10 more models (4k tokens, 40% budget)
3. Agent hits another dependency → STOP, document, export to next session
4. Next session: Fresh context, load expanded scope from the start

**Documentation in templates:**
```
## Token Budget Guidelines

**Conservative thresholds (data engineering focus):**
- 0-2k tokens (20%): Comfortable, can explore freely
- 2k-4k tokens (40%): Good, be deliberate about expansions
- 4k-5k tokens (50%): Warning zone, document if you expand
- 5k+ tokens (60%+): Stop - export to fresh session

**Why conservative?** Data engineering involves complex reasoning:
- Model dependencies (graph traversal)
- SQL transformations (semantic understanding)
- Data quality implications (impact analysis)

Stay under 50% to preserve reasoning quality.
```

---

## Pattern 8: Checkpoint Patterns (human-verify, decision, human-action)

### What It Is

GSD formalizes human-in-the-loop points with typed checkpoints:
- **checkpoint:human-verify** (90%): Claude automated work, human confirms visual/functional correctness
- **checkpoint:decision** (9%): Human makes architectural/technology choices
- **checkpoint:human-action** (1%): Truly unavoidable manual steps OR authentication gates

**Golden rule:** If Claude CAN automate it, Claude MUST automate it.

### Why It Works

1. **Automation first**: Checkpoints come AFTER Claude did everything automatable
2. **Clear expectations**: User knows what they need to do (verify, decide, or act)
3. **Verification specificity**: Numbered steps, exact URLs, expected outcomes
4. **Gate handling**: Auth errors become checkpoints, not failures

### Application to This Project

**Phase 2 (Session Handoff):**

Loop capture protocol has implicit checkpoints:
- Agent proposes loop → **checkpoint:decision** → user approves/rejects
- Agent generates session summary → **checkpoint:human-verify** → user confirms before export

**Make them explicit in templates:**
```xml
<!-- In loop capture workflow -->
<step name="propose_loop">
  Agent identifies potential loop and proposes to user.
</step>

<step type="checkpoint:decision">
  <decision>Should this be captured as a loop?</decision>
  <context>Agent detected: [description of potential loop]</context>
  <options>
    <option id="capture">Yes, capture as loop</option>
    <option id="skip">No, continue without capturing</option>
  </options>
  <resume-signal>Select: capture or skip</resume-signal>
</step>
```

**Phase 3 (Context Engineering):**

Progressive loading has checkpoints:
```xml
<step name="initial_load">
  Load slim context (root model + immediate deps)
</step>

<step type="checkpoint:human-verify">
  <what-built>Loaded 15 models (2.3k tokens, 23% budget)</what-built>
  <how-to-verify>
    Review CONTEXT.md:
    - Token budget shows 2.3k/10k used
    - Loaded models list matches expected scope
    - No unexpected files loaded
  </how-to-verify>
  <resume-signal>Type "approved" to continue</resume-signal>
</step>
```

**Benefits:**
- User knows when they're needed (verification, not execution)
- Templates teach "checkpoint thinking" - when to pause and verify
- Clear distinction: agent proposes, user approves (ownership preservation)

---

## Integration Roadmap

### Phase 1: Foundation & Templates

**Apply GSD patterns to template design:**

1. **XML structure** for heavily-commented templates:
   - Use XML elements for semantic clarity in teaching examples
   - Show both XML and markdown versions (teach pattern flexibility)

2. **Artifact organization**:
   - Establish `.project/` directory structure (equivalent to `.planning/`)
   - SESSION_SUMMARY.md, LOOPS.md, CONTEXT.md in dated subdirectories

3. **Goal-backward methodology**:
   - Template success criteria as must_haves (verifiable outcomes)
   - Key_links show how templates integrate with each other

**Concrete actions:**
- Add `.project/` directory structure diagram to PROJECT.md
- Create template for must_haves frontmatter in planning documents
- Document XML vs markdown tradeoffs (when to use which)

### Phase 2: Session Handoff System

**Apply GSD patterns to handoff artifacts:**

1. **Context layering**:
   ```
   PROJECT_CONTEXT.md (stable)
   └─ LOOPS.md (ephemeral working memory)
      └─ CONTEXT.md (session-specific)
         └─ SESSION_SUMMARY.md (export to GTD)
   ```

2. **Fresh context windows**:
   - Each new session starts at 0% context
   - Read SESSION_SUMMARY.md from previous session (like GSD's STATE.md)
   - Import clarified loops from GTD
   - No accumulation within session - export and reimport pattern

3. **Checkpoint thinking**:
   - Loop capture: agent proposes → **checkpoint:decision** → user approves
   - Session summary: agent generates → **checkpoint:human-verify** → user exports

**Concrete actions:**
- LOOPS.md template uses `<loop status="...">` XML structure
- CONTEXT.md includes `<budget total="5000" used="2300" remaining="2700">`
- SESSION_SUMMARY.md export format compatible with TickTick markdown
- Document handoff protocol: export → fresh context → import clarified items

### Phase 3: Context Engineering Patterns

**Apply GSD patterns to context optimization:**

1. **Token budget management** (50% rule for data engineering):
   - 0-20% (0-2k): Comfortable exploration
   - 20-40% (2-4k): Deliberate expansions
   - 40-50% (4-5k): Warning zone, document decisions
   - 50%+ (5k+): Stop, export to fresh session

2. **Progressive loading** (GSD's segmentation principle):
   - Start narrow (root model + immediate deps)
   - Expand only when agent hits unknown dependency
   - Document each expansion in CONTEXT_DECISIONS.md
   - Session summary shows: "Started 20 models → expanded to 35 after X"

3. **Context decision documentation**:
   ```xml
   <scope type="lineage" root_model="fct_orders">
     <initial_load>
       <models>dim_customers, dim_products, stg_orders</models>
       <token_budget used="2300" total="5000" />
     </initial_load>
     <expansion reason="discovered_dependency">
       <added>int_order_items, int_payments</added>
       <token_budget used="3800" total="5000" />
     </expansion>
   </scope>
   ```

**Concrete actions:**
- Context scoping guide uses must_haves with verifiable budgets
- Progressive loading template documents decision points
- dbt-mp integration guide shows token budget in practice (400 models → 15k tokens)
- CONTEXT_DECISIONS.md template captures "why this scope?"

### Phase 4: Educational Integration & Validation

**Apply GSD's heavily-commented approach:**

1. **Inline GSD mechanics explanations**:
   - Why XML over markdown for certain patterns
   - Context layering rationale (stable → ephemeral)
   - Fresh context window benefits
   - Checkpoint thinking (when to pause and verify)

2. **Show, don't just tell**:
   - Templates include example XML structures with annotations
   - Context engineering guide has worked example (200+ model lineage)
   - Session handoff protocol shows full workflow with checkpoints

3. **Onboarding guide structure** (GSD-inspired):
   - Start with must_haves (what you'll be able to do)
   - Show artifact organization (where files live)
   - Walk through complete example (refactor with handoff)
   - Validate on real work (your dbt project)

**Concrete actions:**
- Every template includes "Why this pattern?" section
- 30-min guide follows: must_haves → artifacts → worked example → validate
- Validation scenario: Refactor dbt model grain change with 200+ downstream models
- Document GSD patterns we adopted and why (attribution + learning)

---

## Summary

**Core GSD patterns adopted:**

1. ✅ **XML structure** for semantic clarity in loop tracking and context budgets
2. ✅ **Context layering** (PROJECT_CONTEXT → LOOPS → CONTEXT → SUMMARY)
3. ✅ **Fresh context windows** via session export/import (no within-session accumulation)
4. ✅ **Artifact organization** in `.project/` with dated session subdirectories
5. ✅ **Goal-backward methodology** (must_haves with verifiable outcomes)
6. ✅ **Token budget management** (50% rule adapted for data engineering)
7. ✅ **Checkpoint patterns** (agent proposes, user approves - ownership preservation)

**Not adopted (out of scope for v1):**

- ❌ **Wave-based parallel execution** (documentation project, not concurrent work)
- ❌ **Multi-agent orchestration** (focused on single-session optimization first)

**Key adaptations for data engineering:**

- Conservative token budgets (20/40/50% thresholds vs GSD's 30/50/70%)
- Progressive loading pattern for model lineage (start narrow, expand deliberately)
- Context decision audit trail (CONTEXT_DECISIONS.md documents "why this scope?")
- Session handoff optimized for GTD integration (export to TickTick)

**Attribution:**

These patterns learned from glittercowboy/get-shit-done framework. We adapt them for data engineering workflows while preserving core principles: ownership, verifiable outcomes, fresh context, deliberate scope management.

---

*Analysis created: 2026-01-19*
*Reference: github.com/glittercowboy/get-shit-done*
