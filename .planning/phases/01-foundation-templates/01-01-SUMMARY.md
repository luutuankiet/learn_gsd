---
phase: 01-foundation-templates
plan: 01
subsystem: templates
tags: [markdown, xml, gsd-patterns, loop-capture, token-budgets, session-state]

# Dependency graph
requires:
  - phase: 00-gsd-pattern-analysis
    provides: GSD_PATTERNS.md with 8 core patterns and XML structure guidance
provides:
  - LOOPS_TEMPLATE.md with systematic ID format (LOOP-NNN) and XML structure for loop capture
  - CONTEXT_TEMPLATE.md with token budget thresholds (20/40/50%) and progressive loading strategy
  - STATE_TEMPLATE.md with session state structure and available actions menu
affects: [01-02-session-templates, 02-session-handoff, phase-planning, plan-execution]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Systematic ID coding (TYPE-NNN format for global unique references)
    - XML elements in markdown for semantic clarity
    - Token budget thresholds (comfortable/deliberate/warning/stop at 0-20/20-40/40-50/50%+)
    - Progressive loading strategy (start narrow, expand deliberately, exclude proactively)
    - Available actions menu (core + contextual slash commands)
    - Context stack for non-linear reasoning support

key-files:
  created:
    - .planning/templates/LOOPS_TEMPLATE.md
    - .planning/templates/CONTEXT_TEMPLATE.md
    - .planning/templates/STATE_TEMPLATE.md
  modified: []

key-decisions:
  - "Loop lifecycle: open → clarifying → closed with status tracking"
  - "Token budget red line at 50% based on quality degradation research"
  - "Progressive loading over upfront loading to maintain comfortable/deliberate zones"
  - "Single-level context stack depth limit to prevent cognitive overload"
  - "Recovery protocol via user prompt 'update artifacts' for protocol drift"

patterns-established:
  - "Systematic ID format: TYPE-NNN (e.g., LOOP-007, TASK-003, DECISION-008)"
  - "XML semantic elements: <loop id= status=>, <context_loaded budget= threshold=>"
  - "Token budget phases: comfortable (0-20%), deliberate (20-40%), warning (40-50%), stop (50%+)"
  - "Available actions: Core actions always present + contextual actions based on state"
  - "Educational inline comments: Explain both 'what' and 'why' for GSD mechanics"

# Metrics
duration: 6min
completed: 2026-01-21
---

# Phase 1 Plan 01: Core Templates Summary

**Three production-ready templates (LOOPS, CONTEXT, STATE) with systematic ID format, XML structure, token budget thresholds, and inline GSD education**

## Performance

- **Duration:** 6 min
- **Started:** 2026-01-21T16:25:07Z
- **Completed:** 2026-01-21T16:31:11Z
- **Tasks:** 3
- **Files created:** 3

## Accomplishments

- Loop capture template with systematic ID format (LOOP-NNN) and XML structure for status tracking
- Token budget template with four-phase thresholds (comfortable/deliberate/warning/stop) and progressive loading strategy
- Session state template with available actions menu, context stack support, and recovery protocol
- All templates include inline educational comments explaining GSD mechanics and data engineering patterns
- Templates designed for both MCP (file access) and copy-paste workflows

## Task Commits

Each task was committed atomically:

1. **Task 1: Create LOOPS_TEMPLATE.md with systematic ID structure** - `385b1fa` (feat)
2. **Task 2: Create CONTEXT_TEMPLATE.md with token budget tracking** - `f568aeb` (feat)
3. **Task 3: Create STATE_TEMPLATE.md with session state structure** - `36e16d2` (feat)

## Files Created/Modified

**Created:**
- `.planning/templates/LOOPS_TEMPLATE.md` (312 lines) - Loop capture with systematic IDs, XML structure, lifecycle transitions, 3 data engineering examples
- `.planning/templates/CONTEXT_TEMPLATE.md` (581 lines) - Token budget tracking with thresholds, progressive loading, 3 dbt scenarios, exclusion rationale
- `.planning/templates/STATE_TEMPLATE.md` (618 lines) - Session state with current context, active loops, token budget snapshot, available actions menu, context stack

## Decisions Made

**1. Systematic ID format: TYPE-NNN**
- Rationale: Global unique references enable quick lookup, artifact linking via grep, unambiguous cross-references
- Pattern: LOOP-001, TASK-003, DECISION-008 (zero-padded three digits)
- Scope: Global unique - IDs never repeat even after closure

**2. Token budget thresholds: 20/40/50%**
- Rationale: Based on GSD Pattern 7 (conservative budgets) and quality degradation research
- Comfortable (0-20%): Exploratory work, room to load freely
- Deliberate (20-40%): Focused work, justify additions
- Warning (40-50%): Quality degradation zone, seek exclusions
- Stop (50%+): Red line - must reduce context before proceeding

**3. Progressive loading strategy**
- Rationale: You don't know what context you need until you start working
- Phase 1: Start narrow (core files + direct deps, 0-20% budget)
- Phase 2: Expand when needed (tests, downstream models, 20-40% budget)
- Phase 3: Exclude and refocus (remove unreferenced files, stay under 40%)

**4. XML elements in markdown**
- Rationale: Semantic clarity, attribute metadata, greppable structure, machine-parseable
- Use cases: Loop status tracking, token budgets, checkpoint events
- When NOT to use: Long-form prose, simple lists, visual formatting

**5. Available actions menu**
- Rationale: Reduces cognitive load - user always knows options
- Core actions: Always present (/continue, /pause, /status, /add-loop, /discuss)
- Contextual actions: Vary by state (plan approval, loop closure, phase completion)
- Format: Slash commands (familiar from Slack/Discord)

**6. Context stack depth limit: 1 level**
- Rationale: Prevents cognitive overload from nested discussions
- Depth 0: Normal work
- Depth 1: One tangent (manageable)
- Depth 2+: Lost track of primary goal (avoid)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - all three templates created successfully following RESEARCH.md patterns and CONTEXT.md decisions.

## Next Phase Readiness

**Ready for Phase 1 Plan 02:** Session Templates (BOOTLOADER, SUMMARY, README)
- Core artifact templates complete (LOOPS, CONTEXT, STATE)
- Systematic ID format established for cross-template references
- Token budget thresholds defined for session management
- Available actions menu pattern ready for BOOTLOADER integration

**No blockers or concerns.**

---
*Phase: 01-foundation-templates*
*Completed: 2026-01-21*
