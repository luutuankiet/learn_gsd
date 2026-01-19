# GSD Prompt Design Integration Analysis

**Created:** 2026-01-19
**Context:** Analyzing how to leverage GSD prompt design patterns for the Data Engineering Copilot Patterns project

## Executive Summary

The GSD framework in `gsd_reference/` demonstrates sophisticated context engineering and prompt architecture patterns that directly address the problems this project aims to solve. This analysis identifies key GSD patterns and proposes how to integrate them into our documentation and templates.

---

## GSD Core Architecture Patterns

### 1. Multi-Layered Document System

**Pattern:**
```
PROJECT.md     → Persistent vision (never grows)
REQUIREMENTS.md → Scoped deliverables with phase traceability
ROADMAP.md     → Progress tracking and phase sequencing
STATE.md       → Decisions, blockers, cross-session memory
research/      → Domain investigation
```

**Why it works:**
- Each document has a single responsibility
- STATE.md prevents "forwarder problem" by capturing decisions
- Ephemeral working memory (plans, summaries) separate from persistent context
- Prevents document sprawl through strict boundaries

**Application to our project:**
- **SESSION_HANDOFF.md template** should mirror STATE.md structure
- **CONTEXT.md template** should track what's loaded/excluded like GSD's plan frontmatter
- **LOOPS.md template** should capture non-linear reasoning (open questions from turn 10)

---

### 2. Plans Are Prompts (Not Documents)

**Pattern:**
```xml
<objective>
What this accomplishes + Why it matters + Output artifacts
</objective>

<context>
@.planning/PROJECT.md
@path/to/relevant/source.ts
</context>

<task type="auto">
  <name>Task 1: Action-oriented name</name>
  <files>exact/file/path.ext</files>
  <action>Specific implementation with rationale for choices</action>
  <verify>Command or check</verify>
  <done>Acceptance criteria</done>
</task>
```

**Why it works:**
- XML structure is Claude-optimal (training data heavy on XML for structured tasks)
- Eliminates interpretation layer - executor reads plan AS prompt
- Verification baked into task definition
- File paths eliminate ambiguity

**Application to our project:**
- **TASK_BREAKDOWN.md template** should use XML structure for common data work
- Templates should include inline examples showing XML task definitions
- Refactor template: `<task>` for each model change with downstream dependency tracking

---

### 3. Goal-Backward Verification

**Pattern:**
```yaml
must_haves:
  truths:
    - "User can see existing messages"
    - "User can send a message"
  artifacts:
    - path: "src/components/Chat.tsx"
      provides: "Message list rendering"
      min_lines: 30
  key_links:
    - from: "src/components/Chat.tsx"
      to: "/api/chat"
      via: "fetch in useEffect"
      pattern: "fetch.*api/chat"
```

**Why it works:**
- Existence ≠ Implementation (file exists doesn't mean feature works)
- Programmatic verification of wiring (grep patterns for connections)
- Prevents stub code from passing as done
- Links are where systems break

**Application to our project:**
- **VERIFICATION.md template** for dbt refactoring should check:
  - Truth: "Downstream models compile after refactor"
  - Artifact: `models/refactored_model.sql` with specific structure
  - Key link: Column refs in downstream models match new schema
- dbt-mp manifest should include verification grep patterns
- Proof of correctness template should use goal-backward methodology

---

### 4. Questioning as Dream Extraction

**Pattern:**
```
Philosophy: You are a thinking partner, not an interviewer

Process:
1. Start open (let them dump mental model)
2. Follow energy (what excited them?)
3. Challenge vagueness ("Good" means what?)
4. Make abstract concrete ("Walk me through using this")
5. Know when to stop (when you can write clear PROJECT.md)

Anti-patterns:
- Checklist walking
- Corporate speak ("success criteria", "stakeholders")
- Shallow acceptance of vague answers
```

**Why it works:**
- Avoids "forwarder problem" - user articulates vision, maintains ownership
- Surfaces hidden assumptions early
- Creates shared mental model
- Prevents downstream ambiguity in plans

**Application to our project:**
- **PAIR_PROGRAMMING.md template** should include questioning protocol
- Problem articulation before solution (GSD's "start open")
- Loop capture should use "agent proposes loops, user approves" pattern
- Context decisions documented with "why this scope?" questioning

---

### 5. Checkpoint Protocol (Automation-First)

**Pattern:**
```xml
<task type="auto">
  <name>Deploy to Vercel</name>
  <action>Run `vercel --yes`, capture URL</action>
  <verify>curl returns 200</verify>
</task>

<task type="checkpoint:human-verify">
  <what-built>Deployed to https://url</what-built>
  <how-to-verify>
    1. Visit URL
    2. Check homepage loads
    3. No console errors
  </how-to-verify>
  <resume-signal>Type "approved"</resume-signal>
</task>
```

**Why it works:**
- Claude automates everything with CLI/API first
- Human verifies visual/functional correctness after automation
- Authentication gates handled dynamically (not pre-planned)
- Prevents asking humans to do automatable work

**Application to our project:**
- **DBT_REFACTOR.md template** checkpoints:
  - Auto: Run `dbt run --select +refactored_model+`
  - Verify: Human checks data looks correct in warehouse
- **TEST_FAILURE.md template** checkpoints:
  - Auto: Fix identified in code, tests re-run
  - Verify: Human confirms root cause addressed (not just symptom)

---

### 6. Context Budget Management

**Pattern:**
```
Plans target ~50% context (not 80%)
- No context anxiety possible
- Quality maintained start to finish
- Room for unexpected complexity

Aggressive atomicity: 2-3 tasks max per plan

Quality degradation curve:
0-30%:  PEAK (thorough, comprehensive)
30-50%: GOOD (confident, solid work)
50-70%: DEGRADING (efficiency mode begins)
70%+:   POOR (rushed, minimal)
```

**Why it works:**
- Stops BEFORE quality degrades
- Fresh context per phase prevents accumulated rot
- Smaller plans = consistent quality
- TDD plans target even lower (40%) due to iteration overhead

**Application to our project:**
- **CONTEXT.md template** should track token budget:
  - Loaded: dbt manifest (slim via dbt-mp) = 5k tokens
  - Excluded: Full DAG (500k) - using lineage subset instead
  - Why: Focus on immediate refactor, not entire warehouse
- Progressive context loading strategy:
  - Start: Narrow (single model + 1-hop dependencies)
  - Expand: If blocked, load 2-hop or related models
  - Document: Why each expansion happened

---

### 7. Fresh Context Per Agent (Parallel Execution)

**Pattern:**
```
Orchestrator spawns specialized agents:
- gsd-planner: Creates PLAN.md (fresh 200k context)
- gsd-executor: Executes plan (fresh 200k context)
- gsd-verifier: Checks goal achieved (fresh 200k context)

Each agent:
1. Loads STATE.md first (accumulated decisions)
2. Reads only relevant prior work
3. Writes results immediately
4. Updates STATE.md with new decisions
5. Returns structured completion message
```

**Why it works:**
- Avoids context rot from long conversations
- Each agent gets full working memory
- State persistence via files, not conversation history
- Parallel execution possible (multiple fresh contexts)

**Application to our project:**
- **Multi-session workflow:**
  - Session 1: Problem articulation (user + agent)
  - Export loops to TickTick
  - Session 2: Implementation (fresh agent, imports clarified loops)
- Agent proposes loops during work, user approves
- Session summary captures loops + context decisions for GTD export

---

## Key Gaps in Current Planning

### Gap 1: No XML Task Structure
**Current state:** ROADMAP.md has prose task descriptions
**GSD pattern:** XML `<task>` with `<files>`, `<action>`, `<verify>`, `<done>`
**Fix:** Add TASK_TEMPLATE.md showing XML structure for data work scenarios

### Gap 2: No Goal-Backward Must-Haves
**Current state:** Requirements are forward-looking (what to build)
**GSD pattern:** Derive observable truths, required artifacts, key links
**Fix:** Update Phase 1 plan to include must-haves derivation for template structure

### Gap 3: No Questioning Protocol Reference
**Current state:** Templates lack guidance on problem articulation
**GSD pattern:** `questioning.md` with philosophy + techniques
**Fix:** Embed questioning patterns in PAIR_PROGRAMMING.md requirements

### Gap 4: No State Persistence Design
**Current state:** Loop capture and session handoff described, not structured
**GSD pattern:** STATE.md with decisions table, blockers, session continuity
**Fix:** Create STATE.md equivalent (SESSION_STATE.md) for ephemeral working memory

### Gap 5: No Verification Patterns
**Current state:** "Proof of correctness" requirement lacks specifics
**GSD pattern:** `verification-patterns.md` with stub detection, wiring checks
**Fix:** Add DBT_VERIFICATION.md showing how to verify refactors aren't stubs

---

## Integration Recommendations by Phase

### Phase 1: Foundation & Templates

**Add to requirements:**
- **META-04**: Templates use XML task structure (example: dbt refactor scenario)
- **META-05**: Templates include verification patterns (stub detection for SQL)
- **META-06**: Reference GSD prompt patterns in template comments

**Template enhancements:**
```markdown
# TASK_BREAKDOWN.md Template

## Refactor Scenario: Changing Model Grain

<task type="auto">
  <name>Update model SQL to new grain</name>
  <files>models/marts/fct_orders.sql</files>
  <action>
    Change grain from order to order_line_item.
    Update primary key: id → order_line_item_id
    Remove aggregations (now atomic level).
    Preserve all columns needed by downstream models.
  </action>
  <verify>
    dbt compile --select fct_orders
    dbt run --select fct_orders
    Row count check: SELECT COUNT(*) should be ~10x higher
  </verify>
  <done>
    Model compiles, runs successfully, row count validates grain change
  </done>
</task>

<task type="auto">
  <name>Update downstream model references</name>
  <files>models/marts/fct_customer_ltv.sql</files>
  <action>
    Update JOIN: fct_orders o → fct_orders oli
    Add GROUP BY: oli.order_id (since oli is now at line item grain)
    Verify all fct_orders.* column refs still valid
  </action>
  <verify>
    dbt compile --select fct_customer_ltv
    dbt run --select fct_customer_ltv
    Comparison query: Old vs new aggregated values should match
  </verify>
  <done>
    Downstream model compiles, runs, produces same results as before refactor
  </done>
</task>

<task type="checkpoint:human-verify">
  <what-built>
    Refactored fct_orders to line-item grain, updated downstream dependencies
  </what-built>
  <how-to-verify>
    1. Run: dbt run --select +fct_customer_ltv+
    2. Query: SELECT COUNT(*) FROM analytics.fct_customer_ltv
    3. Compare to baseline (before refactor)
    4. Spot-check: Sample customer LTV values match expected
  </how-to-verify>
  <resume-signal>Type "approved" or describe data issues</resume-signal>
</task>

<!-- Why this structure:
- XML makes tasks unambiguous (agent doesn't interpret)
- Files explicitly listed (no "relevant files" vagueness)
- Verify includes actual commands (reproducible)
- Checkpoint after automation completes (not asking human to run dbt)
-->
```

### Phase 2: Session Handoff System

**Integrate GSD patterns:**

**LOOPS.md template:**
```markdown
# Session Loops

## Open Loops
(Agent proposes, user approves)

| ID | Loop | Proposed By | Status | Next Action |
|----|------|-------------|--------|-------------|
| L1 | Should we add incremental materialization? | Agent (turn 12) | Approved | Implement in next session |
| L2 | Unclear if downstream BI tool can handle new grain | Agent (turn 18) | Clarifying | User to check with BI team |
| L3 | Test coverage only validates row count, not logic | Agent (turn 22) | Pending | User decision needed |

## Closed Loops
(Resolved this session)

| ID | Loop | Resolution | When |
|----|------|------------|------|
| L4 | Which column to use for surrogate key? | Use dbt_utils.generate_surrogate_key on [order_id, line_number] | Turn 15 |

<!-- Pattern from GSD:
- Agent proposes loops when encountering ambiguity
- User approves/clarifies/adds context
- Export to TickTick: Open loops become GTD clarify tasks
- Import back: Clarified loops provide context for next session
-->
```

**CONTEXT.md template:**
```markdown
# Session Context Budget

## Loaded Context (1k-5k tokens target)

### Slim Manifest
- **File:** `.dbt/manifest_slim.json` (via dbt-mp)
- **Size:** 5,234 tokens
- **Contains:** fct_orders + 1-hop upstream/downstream dependencies
- **Excludes:** Full DAG (500k tokens), staging models (not relevant)

### Model Files
- `models/marts/fct_orders.sql` (234 tokens)
- `models/marts/fct_customer_ltv.sql` (187 tokens)

### Test Baseline
- `tests/baseline_row_counts.csv` (156 tokens)

**Total loaded: 5,811 tokens (~3% of context window)**

## Excluded Context

| Item | Size | Reason |
|------|------|--------|
| Full manifest | 500k | Using slim manifest with dbt-mp instead |
| Staging models | 50k | Not involved in this refactor |
| Source YAML | 20k | Grain change happens in mart layer |

## Context Decisions

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Load only 1-hop dependencies | Refactor isolated to fct_orders, known downstream | If blocked, can expand to 2-hop |
| Use dbt-mp slim manifest | 97% token reduction, includes lineage | Tradeoff: Lose column-level detail |
| Exclude tests folder | Baseline CSV sufficient for validation | Can load full tests if verification fails |

<!-- Pattern from GSD:
- Track what's loaded AND what's excluded (both matter)
- Document WHY for each decision (not just what)
- Progressive loading strategy (start narrow, expand if blocked)
- Token budget explicit (prevents context anxiety)
-->
```

### Phase 3: Context Engineering Patterns

**Integrate GSD patterns:**

**DBT_CONTEXT_SCOPING.md:**
```markdown
# dbt Project Context Scoping

## Scoping Framework (from GSD)

### Level 0: Minimal (1k tokens)
**When:** Bug fix in single model, no downstream changes
**Load:**
- Target model SQL only
- Immediate upstream refs (1-hop)
- Baseline test data

**Example:**
```bash
dbt-mp slim-manifest --select model_name --scope 1-hop
```

### Level 1: Focused (3k tokens)
**When:** Refactor with known downstream dependencies
**Load:**
- Target model SQL
- 1-hop upstream/downstream
- Related tests
- dbt_project.yml config for target

**Example:**
```bash
dbt-mp slim-manifest --select +model_name+ --scope 1-hop
```

### Level 2: Extended (5k tokens)
**When:** Schema change affecting multiple models
**Load:**
- Target model + downstream cascade
- 2-hop dependencies
- All related tests
- Macros used

**Example:**
```bash
dbt-mp slim-manifest --select +model_name+2 --include-macros
```

### Level 3: Full Lineage (10k+ tokens)
**When:** Architectural change, uncertain blast radius
**Load:**
- Complete lineage tree
- All tests
- Source definitions
- Macros + snapshots

**Example:**
```bash
dbt-mp full-lineage --select +model_name+
```

<!-- Pattern from GSD:
- Start narrow (Level 0-1) by default
- Expand progressively when blocked
- Document expansion decisions (why Level 2 became necessary)
- Token budgets explicit at each level
-->
```

### Phase 4: Educational Integration & Validation

**Integrate GSD patterns:**

**ONBOARDING.md (30-minute guide):**
```markdown
# 30-Minute Onboarding: Data Engineering Copilot Patterns

## Part 1: The Problem (5 min)

**Five ways current copilot workflow breaks:**
1. Context optimization: 500k token manifests with no strategy
2. Forwarder problem: Agent fixes, you don't learn why
3. Non-linear reasoning: Turn 10 loops buried by turn 20
4. Document sprawl: PROJECT.md grows forever
5. Cross-session continuity: 15-30 min manual reconstruction

*These map to GSD's core problems and solutions*

## Part 2: The Patterns (15 min)

### Pattern 1: Session Handoff (from GSD STATE.md)
**Problem:** Every new session starts cold
**Solution:** LOOPS.md + CONTEXT.md + SESSION_SUMMARY.md

**Try it:**
1. Start session, encounter ambiguity
2. Agent proposes loop: "Should we use incremental?"
3. You approve or clarify
4. Session ends → Export loops to TickTick
5. You clarify async: "Yes, incremental for tables >1M rows"
6. Next session → Import loop → Fresh context with answer

**Learning:** Agent proposes, you approve. You stay in key reasoning.

### Pattern 2: Context Budget (from GSD 50% rule)
**Problem:** Dumping full dbt manifest (500k tokens)
**Solution:** dbt-mp + progressive loading

**Try it:**
1. Start narrow: `dbt-mp slim-manifest --select model_name`
2. Load 1-hop deps only (5k tokens)
3. If blocked → Expand to 2-hop
4. Document WHY expansion needed

**Learning:** Start narrow, expand when blocked. Token budget explicit.

### Pattern 3: Goal-Backward Verification (from GSD must-haves)
**Problem:** Agent says "refactor complete" but tests don't validate logic
**Solution:** Derive observable truths before starting

**Try it:**
1. Before refactor, define truths:
   - "Downstream models compile"
   - "Customer LTV values match baseline"
   - "Row count validates new grain"
2. For each truth, derive required artifacts:
   - fct_customer_ltv.sql must reference new grain correctly
3. Check key links:
   - grep "fct_orders" downstream models → all JOINs updated

**Learning:** Existence ≠ Implementation. Check wiring, not just files.

## Part 3: Practice Exercise (10 min)

**Scenario:** You need to refactor fct_orders from order-grain to line-item-grain.

**Exercise:**
1. Use TASK_BREAKDOWN.md template
2. Write XML tasks for:
   - Update model SQL
   - Update downstream refs
   - Verification checkpoint
3. Define must-haves (truths, artifacts, key links)
4. Scope context (which level: 0-3?)

**Check your work:**
- Are tasks specific? (Files listed, verify commands included)
- Did you derive truths first? (Not just "tasks complete")
- Is context scoped appropriately? (Token budget documented)

<!-- Pattern from GSD:
- Learn by doing (not just reading)
- Templates as teaching tools (heavily commented)
- Real scenario (not toy example)
- Self-check criteria (you validate own work)
-->
```

---

## Recommended File Additions

### New Templates to Create

1. **TASK_TEMPLATE.md**
   - XML structure examples for data engineering scenarios
   - Refactor, test failure, new model, pipeline debugging
   - Includes verification patterns (GSD wiring checks adapted for dbt)

2. **SESSION_STATE.md**
   - Equivalent of GSD STATE.md but for ephemeral sessions
   - Loops table, context budget tracker, decisions log
   - Export format for TickTick integration

3. **DBT_VERIFICATION.md**
   - Goal-backward verification for dbt projects
   - Stub detection patterns (SQL edition)
   - Wiring verification (column refs, joins, CTEs)
   - Key links (model → downstream, macro → invocation)

4. **CONTEXT_SCOPING_FRAMEWORK.md**
   - Four levels (minimal/focused/extended/full) with token budgets
   - dbt-mp commands for each level
   - Decision tree: Which level for which scenario?
   - Progressive expansion protocol

5. **QUESTIONING_FOR_DATA_WORK.md**
   - GSD questioning.md adapted for data engineering
   - "Walk me through the lineage" (make abstract concrete)
   - "What does 'clean data' mean here?" (challenge vagueness)
   - Problem articulation protocol for pair programming

### Updates to Existing Files

**PROJECT.md:**
- Add "GSD Inspiration" section referencing prompt patterns learned
- Update "Problems to Solve" with GSD framing (context rot, forwarder problem)

**REQUIREMENTS.md:**
- Add verification requirements:
  - VERIFY-01: Templates demonstrate stub detection patterns
  - VERIFY-02: Wiring verification examples for dbt projects
- Add context requirements:
  - CONTEXT-07: Four-level scoping framework (minimal → full)
  - CONTEXT-08: Progressive loading decision protocol

**ROADMAP.md:**
- Update Phase 1 success criteria to include XML task examples
- Update Phase 2 to include "agent proposes loops" workflow
- Update Phase 3 to include four-level scoping framework
- Update Phase 4 to include GSD pattern explanations in templates

---

## Pattern Priorities for Each Requirement

### HANDOFF Requirements

| Requirement | GSD Pattern to Integrate |
|-------------|-------------------------|
| HANDOFF-01 (LOOPS.md) | STATE.md structure + "agent proposes, user approves" |
| HANDOFF-02 (Loop capture) | Questioning techniques (surface loops during work) |
| HANDOFF-03 (CONTEXT.md) | Plan frontmatter (loaded/excluded/why) |
| HANDOFF-04 (Session summary) | Continuation format (structured next steps) |
| HANDOFF-05 (TickTick export) | SESSION_STATE format |
| HANDOFF-06 (Context import) | Fresh context per agent pattern |

### CONTEXT Requirements

| Requirement | GSD Pattern to Integrate |
|-------------|-------------------------|
| CONTEXT-01 (Scoping framework) | 50% context budget rule + progressive loading |
| CONTEXT-02 (Token budget) | Context budget tracking from plan frontmatter |
| CONTEXT-03 (Progressive loading) | Start narrow → expand when blocked |
| CONTEXT-04 (Decision documentation) | Context decisions table (what excluded, why) |
| CONTEXT-05 (Optimization tools) | dbt-mp as AEOps pattern (97% reduction) |
| CONTEXT-06 (Large codebase nav) | Slim manifest + lineage subset strategy |

### EDUC Requirements

| Requirement | GSD Pattern to Integrate |
|-------------|-------------------------|
| EDUC-01 (GSD mechanics) | Why artifacts exist (multi-layer doc system purpose) |
| EDUC-02 (Data patterns) | XML tasks adapted for dbt scenarios |
| EDUC-03 (30-min onboarding) | Learn by doing (practice exercise with templates) |

### META Requirements

| Requirement | GSD Pattern to Integrate |
|-------------|-------------------------|
| META-01 (Heavily commented) | Template comments explain GSD pattern inspiration |
| META-02 (File-based protocol) | Works via Read/Write tools (like GSD .planning/ structure) |
| META-03 (Validate on real work) | Use GSD verification patterns (truths/artifacts/links) |

---

## Implementation Plan for Phase 1

### Step 1: Embed GSD References (2-3 tasks)
1. Create `.planning/references/` directory
2. Extract key GSD patterns:
   - `questioning-for-data.md` (adapted from gsd_reference)
   - `verification-for-dbt.md` (adapted from verification-patterns.md)
   - `xml-task-structure.md` (examples for data work)
3. Update templates to reference these patterns

### Step 2: Create Template Prototypes (2-3 tasks)
1. **TASK_BREAKDOWN.md**:
   - Refactor scenario with XML structure
   - Test failure scenario
   - Inline comments explaining GSD patterns
2. **SESSION_STATE.md**:
   - Loops table (agent proposes/user approves)
   - Context budget tracker
   - Decisions log with rationale
3. **CONTEXT_SCOPING.md**:
   - Four-level framework
   - dbt-mp commands
   - Decision protocol

### Step 3: Validate Templates (1-2 tasks)
1. Use refactor scenario template on real dbt model
2. Capture lessons learned (what worked, what didn't)
3. Update templates based on validation

---

## Long-Term Vision: GSD for Data Engineering

**Where this could go beyond v1:**

1. **Specialized Agents (v2):**
   - `dbt-refactor-planner`: Creates XML tasks for lineage changes
   - `dbt-executor`: Runs tasks with atomic commits per model
   - `dbt-verifier`: Goal-backward verification of refactors

2. **dbt-mp + GSD Integration (v2):**
   - `dbt-mp gsd-context --select model` auto-generates CONTEXT.md
   - Token budget calculated automatically
   - Progressive loading protocol built-in

3. **Session Orchestration (v2):**
   - `/data:refactor` command spawns specialized agents
   - Parallel execution: Multiple models refactored simultaneously
   - Fresh context per agent (like GSD execute-phase)

4. **PR Narrative Generation (v2):**
   - SESSION_SUMMARY.md → PR description template
   - Loops documented → "Open Questions" section
   - Context decisions → "Scope" section
   - Verification results → "Testing" section

---

## Next Steps

1. **Review this analysis** - Identify which patterns resonate most
2. **Prioritize integration** - Which patterns add most value to Phase 1?
3. **Update requirements** - Add specific verification/context requirements
4. **Start Phase 1 planning** - Use GSD patterns when creating detailed phase plan

## Reference

- **GSD Source:** `gsd_reference/` (full .claude directory copy)
- **Key Files Analyzed:**
  - `get-shit-done/references/questioning.md`
  - `get-shit-done/references/verification-patterns.md`
  - `get-shit-done/references/continuation-format.md`
  - `get-shit-done/references/checkpoints.md`
  - `agents/gsd-executor.md`
  - `agents/gsd-planner.md`
  - `commands/gsd/new-project.md`

---

*This analysis created by examining GSD prompt patterns from github.com/glittercowboy/get-shit-done*
