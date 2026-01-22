# Phase 1.2 Context: Audit and Fix Template Coherence

> Decisions captured from discuss-phase session 2025-01-22

---

## Phase Goal

Refactor GSD-lite templates from scattered, inconsistent documents into a **foolproof 5-file structure** optimized for single-agent sessions with weaker reasoning models.

---

## Core Philosophy Confirmed

| Principle | Decision |
|-----------|----------|
| GSD-lite purpose | Comprehensive TODO list, NOT documentation repository |
| Phase creation | Incremental (phases grow as we work), NOT upfront roadmap |
| Artifact lifecycle | Verbose logging → Promote externally → Aggressive trim |
| Target agent | Single agent, single context window, sequential tool calls |
| Single-read constraint | Agent can only read files at first turn |

---

## 5-File Structure (Final Decision)

```
gsd-lite/
  PROTOCOL.md      ← Single entrypoint. Agent reads FIRST.
  STATE.md         ← Current phase, task, decisions, session log
  WORK.md          ← Verbose execution log (deleted after promotion)
  INBOX.md         ← Quick capture for loops from user AND agent
  HISTORY.md       ← Minimal record of completed phases
```

**All other files (README, INIT_PROMPT, BOOTLOADER_TEMPLATE, etc.) will be consolidated or removed.**

---

## PROTOCOL.md Requirements

### Must Include
1. **Session start checklist** - Explicitly tell agent to read PROTOCOL + STATE (+ WORK if resuming)
2. **File guide table** - What each file is for, when to read/write
3. **Planning mode with moodboard** - 10x emoji banner, visual boxes, interview until human confirms understanding
4. **Execution mode** - Log everything to WORK.md
5. **Loop capture** - Loops from BOTH user (non-linear thinker) and agent
6. **Sticky reminder** - End of every turn: status, loops captured, next action
7. **Scope discipline** - No scope creep mid-phase; defer to INBOX
8. **Promotion workflow** - Promote → Record to HISTORY → Delete WORK

### Behavioral Rules
- Interview before acting
- Present moodboard in planning (DO NOT SKIP)
- Log verbosely during execution
- Capture ALL loops immediately
- Never expand scope mid-phase

---

## STATE.md Requirements

**Depth: Moderate** - Enough for weak agent to resume without reading full WORK.md

Must contain:
- **Active Phase** - Name and goal
- **Current Task** - Task name, status, blocked status
- **Key Decisions Made** - So agent doesn't re-ask same questions
- **Session Log** - Brief history of what happened when
- **Open Loops** - Reference to INBOX items for awareness

---

## Hierarchy Confirmed

```
Phase 1 ──┬── Session 1 ──┬── Task A
          │               └── Task B
          ├── Session 2 ──┬── Task B (continued)
          │               └── Task C
          └── Session 3 ──── Task D
```

- **Phase**: Logical chunk of work (created incrementally, not planned upfront)
- **Session**: Time-bounded work period (natural breakpoints)
- **Task**: Atomic unit of work within a phase

**Artifacts live in phase scope, not session scope.** Sessions are just time markers in STATE.md log.

---

## Promote & Trim Workflow

| Step | Action | Example |
|------|--------|---------|
| 1. Complete | Phase work is done | CI passes, code works |
| 2. Promote | Extract to external artifact | Write PR description from WORK.md |
| 3. Record | Add to HISTORY.md | "Phase 3: Refactor model - PR #42" |
| 4. Trim | **Aggressive** - delete WORK.md content | WORK.md is now empty |
| 5. Clear | STATE.md shows no active phase | Ready for next phase |

---

## Out of Scope (Deferred)

These were mentioned but are NOT part of Phase 1.2:

- [ ] Multi-agent orchestration patterns
- [ ] Complex project roadmapping
- [ ] Integration with external tools
- [ ] Template versioning system

---

## Success Criteria for This Phase

- [ ] Consolidate all scattered templates into 5-file structure
- [ ] PROTOCOL.md is self-contained and foolproof for weak agents
- [ ] STATE.md template captures moderate depth
- [ ] INBOX.md template supports loop capture from both sides
- [ ] WORK.md and HISTORY.md templates are simple and clear
- [ ] No redundant files (README, INIT_PROMPT, BOOTLOADER removed/consolidated)
- [ ] A human can read the protocol and understand the entire workflow

---

## Key Quotes from Discussion

> "GSD-lite is a comprehensive TODO list, not a place to document."

> "The need to keep verbose, detailed logs is needed to serve its purpose up to the point where one phase is completed, after which can be trimmed."

> "User thinks non-linear so they will ask as they go; they are loops that agent must also capture."

> "The moodboard and the visual verbose 10x emoji banner is the top requirement to nudge both agent and user."
