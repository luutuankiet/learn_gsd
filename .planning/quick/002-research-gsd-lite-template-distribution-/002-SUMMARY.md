---
phase: quick-002
plan: 002
subsystem: distribution
tags: [markdown, templates, github, npm, git-subtree, packaging]

# Dependency graph
requires:
  - phase: 01-04
    provides: "All templates complete and production-ready"
provides:
  - "Understanding of template distribution landscape"
  - "Clear guidance on appropriate distribution methods for markdown templates"
  - "Recommendation: Git clone + manual copy as primary, shell installer as optional"
affects: [future-phase-packaging, external-sharing]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Manual copy pattern for markdown template distribution"
    - "Shell script installer as convenience layer"

key-files:
  created:
    - ".planning/quick/002-research-gsd-lite-template-distribution-/002-SUMMARY.md"
  modified: []

key-decisions:
  - "Use manual git clone + copy as primary distribution method"
  - "Avoid npx/pip - wrong tools for markdown templates (code vs documentation)"
  - "Shell script installer optional for convenience"
  - "Git subtree as power-user option for maintaining update connection"

patterns-established:
  - "Template distribution: Match method to content type (code vs markdown)"
  - "Distribution simplicity: Minimize dependencies for broadest compatibility"

# Metrics
duration: 8min
completed: 2026-01-22
---

# Quick 002: Template Distribution Research Summary

**Clarified npx/pip are for executable code packages, not markdown templates - recommended manual copy as primary method with optional shell installer for convenience**

## Performance

- **Duration:** 8 min
- **Started:** 2026-01-21T19:39:43Z
- **Completed:** 2026-01-21T19:47:43Z
- **Tasks:** 3
- **Files modified:** 1

## Question Answered

**User question:** "how do i publish my gsd lite template for distribution ? is this through npx or pip `.planning/templates`"

**Answer:** No, npx and pip are the wrong tools. They're for distributing executable code packages (Node.js and Python respectively), not markdown documentation files. gsd-lite templates need a different distribution approach suited for static documentation.

## Key Insight

**Content type determines distribution method:**
- **Code packages** (executable, requires installation) → npm/pip/cargo
- **Markdown templates** (static files, copy-and-paste) → Git clone or download
- **Hybrid** (templates + scaffolding logic) → npm create/CLI installer

gsd-lite is pure markdown (8 files: 7 templates + AGENTS.md) with no code execution, so code package managers are overkill.

## Research Findings

### 1. GitHub Template Repository Pattern

**How it works:**
- GitHub's "Use this template" button on repo
- Creates NEW repository from template structure
- Best for: Full project scaffolding (entire repo becomes template)

**Pros:**
- Zero dependencies beyond GitHub account
- Low maintenance (just update template repo)
- Easy discovery via GitHub

**Cons:**
- Creates NEW repo, doesn't add to existing projects
- gsd-lite is drop-in addition, not full project scaffold
- **Not a fit for this use case**

**Examples:** create-react-app templates, cookiecutter templates

---

### 2. npm create / npx Pattern

**How it works:**
- JavaScript package published to npm registry as `@create-*` or `create-*`
- Contains executable code that scaffolds project
- User runs: `npm create gsd-lite` or `npx create-gsd-lite`
- Script copies files, prompts for config, customizes templates

**Pros:**
- Single command installation
- Can include prompts for customization
- Version management via npm

**Cons:**
- **Requires Node.js dependency** (problem for Python/Go-only projects)
- **Requires writing JavaScript wrapper** just to copy 8 markdown files
- **Overkill for static files** - npm is for executable packages
- Publishing/maintenance overhead (npm account, versioning, package.json)

**Why NOT for gsd-lite:**
- npx is for EXECUTABLE code, not documentation
- Would need JavaScript just to `fs.copyFileSync()` - absurd overhead
- Forces Node.js dependency on non-Node projects
- gsd-lite targets data engineers (Python, SQL, dbt) who may not have Node.js

**Examples:** create-next-app, create-vite, create-react-app

---

### 3. CLI Installer Pattern

**How it works:**
- Shell script that downloads and copies templates
- Distribution: GitHub releases, gist, or repo
- User runs: `curl -fsSL url/install.sh | bash`
- Script can prompt for target directory, check updates

**Pros:**
- One-liner installation
- Minimal dependencies (curl/wget, usually present)
- Can handle updates (script checks versions)
- Platform agnostic (works on any Unix-like system)

**Cons:**
- Medium maintenance burden (shell script to maintain)
- Security concern (curl | bash requires trust)
- Doesn't work on Windows without WSL/Git Bash

**Fit for gsd-lite:**
- Good as **optional convenience layer** on top of manual copy
- For users who want automation
- Not required as primary method (manual copy simpler)

**Examples:** oh-my-zsh installer, Homebrew formulas

---

### 4. Git Subtree / Submodule Pattern

**How it works:**
- User adds gsd-lite repo as subdirectory in their project
- Subtree: `git subtree add --prefix .gsd-lite https://github.com/user/gsd-lite main`
- Updates: `git subtree pull --prefix .gsd-lite https://github.com/user/gsd-lite main`
- Maintains connection to source repo

**Pros:**
- Updates are straightforward (git subtree pull)
- Maintains version history
- Only dependency: git (already required)

**Cons:**
- **Complex commands** - git subtree not beginner-friendly
- Steep learning curve for non-Git power users
- Merge conflicts on updates if user customized templates
- Submodules even more complex (separate .gitmodules config)

**Fit for gsd-lite:**
- Good for **power users** who want update tracking
- Not recommended as primary method (too complex for most)
- Document as "Advanced: Git Subtree" option

**Examples:** Embedded dependencies, vendored code

---

### 5. Manual Copy Pattern

**How it works:**
- User clones repo: `git clone https://github.com/user/gsd-lite`
- User copies templates: `cp -r gsd-lite/.planning/templates/ my-project/.gsd-lite/`
- User customizes templates for their project
- User deletes cloned repo (or keeps for reference)

**Pros:**
- **Simplest approach** - standard git commands
- **Zero dependencies** beyond git (projects already have)
- **Full control** - user sees exactly what they're copying
- **Platform agnostic** - works everywhere git works
- **No maintenance** - just maintain source repo

**Cons:**
- No automatic updates (user must re-clone and diff/merge)
- Manual process (not one-liner)
- User must know what directory to copy

**Fit for gsd-lite:**
- **BEST PRIMARY METHOD**
- Matches content type (static documentation)
- Minimal dependencies
- Works for all project types (Python, Node.js, Go, etc.)
- Clear instructions in README handle the "what to copy" question

**Examples:** Bootstrap starter templates, configuration file examples

---

## Comparison for gsd-lite Use Case

**Constraints:**
- Pure markdown files (no code execution)
- Target: Data engineers (may have Python-only or Go-only projects)
- Platform agnostic (works with any AI copilot)
- Drop-in addition to existing projects (not full project scaffold)
- 8 files total (7 templates + AGENTS.md)
- Users need to customize after installation (paths, project names)

**Evaluation:**

| Approach | Simplicity | Dependencies | Customization | Updates | Maintenance | Fit for gsd-lite |
|----------|------------|--------------|---------------|---------|-------------|------------------|
| GitHub Template Repo | Medium | None | Manual edit | None | Low | ❌ Creates new repo, not drop-in |
| npm create | High | Node.js + npm | Script prompts | Re-run | High | ❌ Node.js dependency, overkill |
| CLI Installer | High | curl/wget | Script prompts | Re-run | Medium | ⚠️ Optional convenience layer |
| Git Subtree | Low | Git only | Manual edit | `subtree pull` | Low | ⚠️ Power user option (complex) |
| Manual Copy | High | Git only | Manual edit | Manual merge | Low | ✅ Best primary method |

---

## Recommendation

### Primary Method: Manual Git Clone + Copy

**Why this approach:**
1. **Matches content type** - Markdown files don't need code package managers
2. **Minimal dependencies** - Only git (projects already have)
3. **Simplest for users** - Standard git clone + copy commands
4. **Platform agnostic** - Works for Python, Node.js, Go, any project
5. **Full transparency** - User sees exactly what they're getting
6. **Low maintenance** - Just maintain the source repo

**User workflow:**
```bash
# 1. Clone the repository
git clone https://github.com/your-username/gsd-lite
cd gsd-lite

# 2. Copy templates to your project
cp -r .planning/templates/ /path/to/your-project/.gsd-lite/
cp .planning/AGENTS.md /path/to/your-project/.gsd-lite/

# 3. Customize templates for your project
# Edit .gsd-lite/AGENTS.md with your project details
# Edit templates as needed

# 4. Clean up
cd /path/to/your-project
rm -rf /path/to/gsd-lite  # Remove clone after copying
```

**Documentation needed:**
- README with clear installation instructions
- Example showing directory structure after installation
- Customization guide (what to edit, common patterns)

---

### Optional: Shell Script Installer (Convenience Layer)

**For users who want automation:**

Create `install.sh` in repo:
```bash
#!/bin/bash
# gsd-lite installer

set -e

# Prompt for target directory
read -p "Install directory (default: .gsd-lite): " TARGET_DIR
TARGET_DIR=${TARGET_DIR:-.gsd-lite}

# Check if directory exists
if [ -d "$TARGET_DIR" ]; then
  read -p "$TARGET_DIR exists. Overwrite? (y/N): " CONFIRM
  if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 1
  fi
fi

# Download templates
echo "Installing gsd-lite templates to $TARGET_DIR..."
mkdir -p "$TARGET_DIR"

# Option A: Download from GitHub (release or branch)
curl -L https://github.com/user/gsd-lite/archive/refs/heads/main.tar.gz | \
  tar xz --strip=2 -C "$TARGET_DIR" "gsd-lite-main/.planning/templates"

# Copy AGENTS.md
curl -o "$TARGET_DIR/AGENTS.md" https://raw.githubusercontent.com/user/gsd-lite/main/.planning/AGENTS.md

echo "✅ Installed gsd-lite templates to $TARGET_DIR"
echo "📝 Next: Edit $TARGET_DIR/AGENTS.md to customize for your project"
```

**User workflow:**
```bash
curl -fsSL https://raw.githubusercontent.com/user/gsd-lite/main/install.sh | bash
```

**Benefits:**
- One-liner installation
- Can prompt for configuration
- Can check for updates

**Tradeoffs:**
- Requires maintaining shell script
- curl | bash has trust implications
- Not essential (manual copy works fine)

---

### Power User Option: Git Subtree

**For users who want update tracking:**

**Documentation:**
```markdown
## Advanced: Git Subtree (for tracking updates)

If you want to pull template updates from gsd-lite source:

### Initial setup
```bash
git subtree add --prefix .gsd-lite/templates \
  https://github.com/user/gsd-lite main --squash
```

### Pull updates
```bash
git subtree pull --prefix .gsd-lite/templates \
  https://github.com/user/gsd-lite main --squash
```

**Note:** If you've customized templates, you may get merge conflicts. Review carefully before accepting updates.
```

**Benefits:**
- Maintains connection to source
- Can pull improvements
- Git tracks update history

**Tradeoffs:**
- Complex commands (not beginner-friendly)
- Merge conflicts if customized
- Requires git subtree understanding

---

## Why NOT npx/pip

**npx (Node Package Executor):**
- Purpose: Run executable Node.js packages from npm registry
- Use case: Code that runs (scaffolding scripts, CLI tools, build tools)
- gsd-lite: Pure markdown files (no code to execute)
- Problem: Would need to write JavaScript wrapper just to copy 8 files
- Dependency: Forces Node.js on non-Node projects (data engineers using Python/dbt)

**pip (Python Package Installer):**
- Purpose: Install Python packages with executable code
- Use case: Python libraries, command-line tools written in Python
- gsd-lite: No Python code (markdown only)
- Problem: Would need to write Python wrapper just to copy 8 files
- Packaging overhead: setup.py, PyPI account, wheel building for static files

**Fundamental mismatch:**
- Package managers are for CODE (executable, requires installation/compilation)
- gsd-lite is DOCUMENTATION (static markdown, just copy files)
- Using npx/pip is like using a jackhammer to hang a picture frame

---

## Implementation Steps

If you choose the recommended approach:

### Step 1: Prepare Repository
1. Ensure templates are in `.planning/templates/` directory
2. Create clear README.md with:
   - What gsd-lite is
   - Installation instructions (manual copy)
   - Example directory structure after installation
   - Customization guide
3. Add LICENSE (MIT recommended for templates)

### Step 2: Document Installation (in README)
```markdown
## Installation

### Manual Installation (Recommended)

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/gsd-lite
   cd gsd-lite
   ```

2. Copy templates to your project:
   ```bash
   # Copy all templates
   cp -r .planning/templates/ /path/to/your-project/.gsd-lite/

   # Copy AGENTS.md
   cp .planning/AGENTS.md /path/to/your-project/.gsd-lite/
   ```

3. Customize for your project:
   - Edit `.gsd-lite/AGENTS.md` with your domain and project structure
   - Review templates and adjust examples as needed

4. Clean up:
   ```bash
   rm -rf /path/to/gsd-lite
   ```

### Quick Install (Optional)

One-liner using curl:
```bash
curl -fsSL https://raw.githubusercontent.com/your-username/gsd-lite/main/install.sh | bash
```

### Advanced: Git Subtree (for tracking updates)
[Document git subtree commands here]
```

### Step 3: Create install.sh (Optional)
- Write shell script for one-liner installation
- Test on macOS, Linux, WSL
- Handle edge cases (existing directory, permission errors)

### Step 4: Publish to GitHub
- Push to public repository
- Add topics/tags: `ai-copilot`, `templates`, `markdown`, `data-engineering`
- Write clear repository description
- Pin README as repo landing page

### Step 5: Share
- Link from your documentation
- Share in communities (Reddit r/dataisbeautiful, dbt Slack, AI Discord servers)
- Write blog post explaining the system

---

## Alternative Considered: npm create (Not Recommended)

**If you later decide user demand justifies tooling investment:**

You could create `create-gsd-lite` npm package:

```javascript
// index.js
#!/usr/bin/env node
import fs from 'fs-extra';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const templateDir = path.join(__dirname, 'templates');
const targetDir = process.argv[2] || '.gsd-lite';

console.log(`Installing gsd-lite to ${targetDir}...`);
fs.copySync(templateDir, targetDir);
console.log('✅ Done! Edit .gsd-lite/AGENTS.md to customize.');
```

**User workflow:**
```bash
npm create gsd-lite
# or
npx create-gsd-lite
```

**When this makes sense:**
- High adoption (100+ users)
- Users request one-liner installation
- You want version management via npm
- You're willing to maintain Node.js tooling

**Current recommendation:** Start with manual copy. Add npm package later if demand justifies investment.

---

## Accomplishments

- Researched 5 standard template distribution approaches
- Clarified npx/pip are wrong tools (code vs markdown mismatch)
- Evaluated approaches against gsd-lite constraints
- Identified manual copy as best primary method
- Documented shell installer as optional convenience layer
- Provided implementation steps for chosen approach

## Task Commits

1. **Task 1: Research markdown template distribution patterns** - (research only, no commit)
2. **Task 2: Evaluate approaches for gsd-lite use case** - (analysis only, no commit)
3. **Task 3: Document findings and recommend approach** - `[pending]` (docs: create summary)

**Plan metadata:** `[pending]` (docs: complete quick task 002)

## Files Created/Modified

- `.planning/quick/002-research-gsd-lite-template-distribution-/002-SUMMARY.md` - Research findings and recommendation

## Decisions Made

1. **Manual copy as primary distribution method**
   - Rationale: Matches content type (markdown), minimal dependencies, simplest for users

2. **Avoid npx/pip**
   - Rationale: Wrong tools for markdown templates - designed for executable code packages

3. **Shell installer as optional convenience layer**
   - Rationale: Provides one-liner for users who want automation, not required

4. **Git subtree as power-user option**
   - Rationale: Enables update tracking for advanced users, too complex as primary method

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - research task completed without blockers.

## Next Steps

**Immediate:**
- User decides which distribution method to implement
- If manual copy chosen: Update main repo README with installation instructions
- If shell installer chosen: Create install.sh script and test

**Future considerations:**
- If adoption high and demand justifies: Consider npm create package
- Monitor user feedback on installation friction
- Document common customization patterns based on user questions

---

*Quick Task: 002*
*Completed: 2026-01-22*
