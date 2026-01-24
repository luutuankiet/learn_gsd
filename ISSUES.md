# GSD-Lite Protocol Issues

## GAP 2: Hallucination Prevention (Critical)

**Session Evidence:** T4-T6
- T4: Agent proposed PHASE-001 but **claimed to write files without executing tool calls**
- T5: User caught the hallucination
- T6: Agent corrected and actually wrote files

**Protocol Issue:**
No guidance on verifying tool execution actually happened.

**Recommendation:**
```markdown
## Anti-Hallucination Protocol

After EVERY turn, before sticky reminder:
- [ ] Self-check: Did I EXECUTE tool calls or just DESCRIBE them?
- [ ] Verify: Are file updates CONFIRMED in tool results?
- [ ] Validate: Can I reference specific line numbers from Read results?

If uncertain, re-read the file to confirm changes persisted.
```

**Impact:** High - Breaks user trust, creates phantom state

---

## GAP 3: No Research/Verification Mode (Critical)

**Session Evidence:** T9-T16
- User initiated `/discuss` to verify logic before implementing
- Agent entered "Verification" mode (not defined in protocol)
- Investigated source code (T13-T15)
- Confirmed logic (T16)
- **This entire workflow is missing from protocol**

**Protocol Issue:**
Protocol jumps from MOODBOARD → WHITEBOARD → EXECUTION.
No coverage for "Let me investigate before planning."

**Recommendation:**
```markdown
## RESEARCH Mode (Optional Pre-Planning Phase)

When user requests investigation before implementation:

**Trigger phrases:**
- "Can you verify..."
- "Let's investigate..."
- "Check if this is possible..."
- "/discuss [topic]"

**Protocol:**
1. Update STATE.md: `Current Mode: Research`
2. Investigate codebase/dependencies/source code
3. Document findings in WORK.md with evidence
4. Propose WHITEBOARD based on research findings
5. Update STATE.md: `Current Mode: Planning` (proceed to MOODBOARD)

**Example WORK.md entry:**
```
### [2026-01-24] Research: Attribution Variable
**Objective:** Verify $options->message_to_prepend exists in codebase
**Evidence:** Found in makefulltextfeed.php:127
**Conclusion:** Safe to use {url} or {effective-url} substitution
```
```

**Impact:** High - Real-world sessions need investigation phase before committing to plan

---

## Root Cause Analysis (Hypothesis)

**Issue:** Agent doesn't follow protocol strictly

**User's Hunch:**
- System instruction + MCP tool definitions too long (6-7k tokens initially)
- Not optimal for Gemini with 1M token context
- Even with large context, this isn't best practice

**Investigation Needed:**
1. Review upstream OG GSD at `./.claude/get-shit-done/workflows/discuss-phase.md`
2. Review roadmap at `./.planning`
3. Analyze if protocol needs to be more concise/focused
4. Consider if protocol should be broken into smaller, mode-specific instructions

**Next Steps:**
- [ ] Review upstream GSD implementation
- [ ] Review project roadmap
- [ ] Determine optimal protocol length/structure for LLM adherence
- [ ] Test if shorter, focused instructions improve protocol compliance
