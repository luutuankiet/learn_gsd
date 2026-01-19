# Roadmap: Data Engineering Copilot Patterns

## Overview

Build a knowledge base of vendor-agnostic patterns for using AI copilots in data engineering workflows. Establish file-based protocols and heavily-commented templates that teach both GSD mechanics and data engineering patterns. Ship session handoff system first (eliminate 15-30 min context reconstruction), then layer in context engineering patterns (handling 200+ model lineages), and validate on real dbt refactoring work.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation & Templates** - File-based protocol and template structure
- [ ] **Phase 2: Session Handoff System** - Eliminate context reconstruction between sessions
- [ ] **Phase 3: Context Engineering Patterns** - Token budget management and context optimization
- [ ] **Phase 4: Educational Integration & Validation** - Teach through templates and validate on real work

## Phase Details

### Phase 1: Foundation & Templates
**Goal**: Establish file-based protocol and heavily-commented template approach that works across all agent types
**Depends on**: Nothing (first phase)
**Requirements**: META-01, META-02
**Success Criteria** (what must be TRUE):
  1. Templates have inline explanations of GSD mechanics (why artifacts exist, how they work)
  2. File-based protocol works via both MCP and copy/paste without modification
  3. User can read any template and understand both what to do and why
**Plans**: TBD

Plans:
- TBD (to be defined during phase planning)

### Phase 2: Session Handoff System
**Goal**: Create ephemeral working memory system that exports to GTD and eliminates 15-30 min context reconstruction
**Depends on**: Phase 1
**Requirements**: HANDOFF-01, HANDOFF-02, HANDOFF-03, HANDOFF-04, HANDOFF-05, HANDOFF-06
**Success Criteria** (what must be TRUE):
  1. User can capture loops during session (agent proposes, user approves workflow)
  2. User can generate session summary showing loops and context decisions
  3. User can export session working memory to TickTick for GTD processing
  4. User can import clarified loops from GTD back into future sessions
  5. User can track token budget (what's loaded, what's excluded, why)
**Plans**: TBD

Plans:
- TBD (to be defined during phase planning)

### Phase 3: Context Engineering Patterns
**Goal**: Enable context optimization for large codebases (200+ file lineages) while staying within 1k-5k token budgets
**Depends on**: Phase 2
**Requirements**: CONTEXT-01, CONTEXT-02, CONTEXT-03, CONTEXT-04, CONTEXT-05, CONTEXT-06
**Success Criteria** (what must be TRUE):
  1. User can scope context for any project type (not just dbt)
  2. User can stay within token budget across different scenarios
  3. User can start narrow and expand context progressively when needed
  4. User can document context decisions (why this scope? what was excluded?)
  5. User can navigate large codebases using dbt-mp and similar AEOps patterns
**Plans**: TBD

Plans:
- TBD (to be defined during phase planning)

### Phase 4: Educational Integration & Validation
**Goal**: Thread educational content through all templates and validate patterns on real dbt refactoring work
**Depends on**: Phase 3
**Requirements**: EDUC-01, EDUC-02, EDUC-03, META-03
**Success Criteria** (what must be TRUE):
  1. Every template explains both GSD mechanics and data engineering patterns
  2. 30-minute onboarding guide enables colleague to do and understand
  3. Patterns validated on real dbt refactoring (200+ model lineage scenario)
  4. User can produce PR narrative with reasoning, not just code changes
**Plans**: TBD

Plans:
- TBD (to be defined during phase planning)

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Templates | 0/TBD | Not started | - |
| 2. Session Handoff System | 0/TBD | Not started | - |
| 3. Context Engineering Patterns | 0/TBD | Not started | - |
| 4. Educational Integration & Validation | 0/TBD | Not started | - |

---
*Roadmap created: 2026-01-19*
*Last updated: 2026-01-19*
