# Commit: Intelligent Git Commit with Generated Messages

## Objective
Analyze staged and unstaged changes, generate an appropriate commit message following best practices, and commit changes to the repository with a clear, meaningful message.

## Process

### 1. Check Repository Status

First, verify we're in a git repository and check current status:

```bash
git status
```

Analyze:
- Current branch
- Staged changes
- Unstaged changes
- Untracked files
- Any merge conflicts or issues

### 2. Review All Changes

Get detailed view of changes to understand what's being committed:

```bash
# View staged changes
git diff --cached

# If no staged changes, view unstaged changes
git diff

# Show file change summary
git diff --stat
git diff --cached --stat
```

### 3. Analyze Change Patterns

Review the changes and identify:

**Change Type:**
- `feat`: New feature or functionality
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Formatting, missing semicolons, etc. (no code change)
- `refactor`: Code restructuring (no functionality change)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, tooling
- `ci`: CI/CD configuration changes
- `revert`: Reverting previous commits

**Scope:**
- Identify primary area affected (e.g., auth, api, ui, database)
- Multiple scopes if changes span different areas

**Impact:**
- Breaking changes (require major version bump)
- New features (minor version bump)
- Bug fixes (patch version bump)

### 4. Generate Commit Message

Follow Conventional Commits format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Subject Line Rules:**
- Start with type and optional scope
- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter after colon
- No period at the end
- Keep under 72 characters
- Be specific and descriptive

**Examples:**
- `feat(auth): add JWT token refresh mechanism`
- `fix(api): resolve user endpoint pagination issue`
- `docs(readme): update installation instructions`
- `refactor(database): extract query builder to separate module`
- `test(auth): add integration tests for login flow`
- `chore(deps): upgrade React to version 18.2.0`

**Body (optional but recommended for complex changes):**
- Explain the "why" not the "what"
- Describe motivation for the change
- Contrast with previous behavior
- Wrap at 72 characters

**Footer (optional):**
- Breaking changes: `BREAKING CHANGE: description`
- Issue references: `Closes #123` or `Fixes #456`
- Co-authors: `Co-authored-by: Name <email>`

### 5. Prepare Commit

Stage files if needed:

```bash
# Stage specific files
git add <file1> <file2>

# Or stage all changes
git add .

# Stage only tracked file changes (not new files)
git add -u
```

### 6. Create Commit

**Option A: Simple Commit**
```bash
git commit -m "type(scope): subject"
```

**Option B: Commit with Body**
```bash
git commit -m "type(scope): subject" -m "
Body paragraph explaining the why behind the change.
Can span multiple lines for detailed explanation.

Can include multiple paragraphs.
"
```

**Option C: Commit with Body and Footer**
```bash
git commit -m "type(scope): subject" -m "
Body explaining the change.
" -m "
BREAKING CHANGE: description of breaking change
Fixes #123
"
```

### 7. Verify Commit

Check that commit was created successfully:

```bash
# View the commit
git log -1 --pretty=format:"%h - %s (%an, %ar)"

# View full commit details
git show HEAD
```

### 8. Push to GitHub (Optional)

If ready to push:

```bash
# Push to current branch
git push

# Or push and set upstream
git push -u origin <branch-name>
```

## Commit Message Best Practices

### DO ✅
- Use conventional commit format consistently
- Write clear, descriptive subject lines
- Explain the "why" in the body for non-trivial changes
- Reference related issues/PRs
- Keep commits focused on a single concern
- Use present tense ("add" not "added")
- Start subject with lowercase after colon
- Break up large changes into multiple commits

### DON'T ❌
- Write vague messages like "fix bug" or "update code"
- Commit unrelated changes together
- Exceed 72 characters in subject line
- Use past tense in subject
- Capitalize first word after colon
- End subject with a period
- Commit without reviewing changes first
- Include WIP (work in progress) commits in main branch

## Examples of Good Commit Messages

### Simple Feature Addition
```
feat(auth): add password strength validation

Implement client-side password validation with the following rules:
- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character

Closes #234
```

### Bug Fix
```
fix(api): resolve race condition in user session handling

Previously, concurrent requests could create duplicate session records.
Now using database-level locking to ensure session uniqueness.

Fixes #567
```

### Breaking Change
```
feat(api): redesign authentication endpoint structure

BREAKING CHANGE: Authentication endpoints moved from /auth/* to /api/v2/auth/*
Clients must update endpoint URLs and add API version header.

Migration guide: docs/migration-v2.md
Closes #890
```

### Refactoring
```
refactor(database): extract connection pooling to separate module

Move database connection logic to dedicated module for better
reusability and testability. No functional changes.
```

### Documentation
```
docs(contributing): add code review guidelines

Add comprehensive code review checklist and best practices
for maintainers and contributors.
```

### Multiple Scopes
```
chore(deps): upgrade core dependencies

- Upgrade React from 18.1.0 to 18.2.0
- Upgrade TypeScript from 4.9.0 to 5.0.0
- Update type definitions for compatibility

All tests passing. No breaking changes.
```

## Workflow Integration

### Before Committing
1. Run tests: `npm test` or appropriate test command
2. Run linter: `npm run lint`
3. Review changes: `git diff`
4. Stage intentionally: Don't use `git add .` without reviewing

### After Committing
1. Verify commit message: `git log -1`
2. Run CI locally if possible
3. Push to remote branch
4. Create or update pull request

## Context Awareness

Consider project context when generating messages:

**For New Features:**
- What user value does this add?
- What problem does it solve?
- Are there any limitations?

**For Bug Fixes:**
- What was broken?
- What was the root cause?
- How does this fix it?

**For Refactoring:**
- Why refactor now?
- What improvements does this bring?
- Any performance impacts?

## Git Configuration Best Practices

Ensure proper git configuration:

```bash
# Set commit author
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Enable GPG signing (optional but recommended)
git config commit.gpgsign true
git config user.signingkey <your-gpg-key>

# Set default editor for commit messages
git config core.editor "code --wait"  # VS Code
git config core.editor "vim"          # Vim
```

## Output Format

After committing, provide:

```
✅ **COMMIT SUCCESSFUL**

**Commit Hash:** abc1234
**Type:** feat
**Scope:** auth
**Message:** add JWT token refresh mechanism

**Files Changed:** 3
- src/auth/token-manager.ts (modified)
- src/auth/refresh-endpoint.ts (new)
- tests/auth/token-refresh.test.ts (new)

**Next Steps:**
- Run tests to verify changes
- Push to remote: git push origin <branch>
- Create/update pull request
```

## Error Handling

### No Changes to Commit
```
⚠️ **NO CHANGES TO COMMIT**

Working directory is clean. Stage changes first:
- git add <files>  # Stage specific files
- git add .        # Stage all changes
```

### Merge Conflicts
```
⚠️ **MERGE CONFLICTS DETECTED**

Resolve conflicts before committing:
1. Review conflicted files: git status
2. Edit files to resolve conflicts
3. Stage resolved files: git add <files>
4. Complete merge: git commit
```

### Uncommitted Changes
```
⚠️ **UNSTAGED CHANGES DETECTED**

Stage changes before committing:
git add <files>
```

## Validation Checklist

Before finalizing commit:

- [ ] Message follows conventional commit format
- [ ] Subject line is clear and under 72 characters
- [ ] Type accurately reflects change (feat, fix, docs, etc.)
- [ ] Scope is appropriate and specific
- [ ] Body explains "why" for non-trivial changes
- [ ] Breaking changes are clearly marked
- [ ] Issue references are included
- [ ] All intended files are staged
- [ ] No unintended files are staged
- [ ] Tests pass locally
- [ ] Linter passes

---

**Remember:** A good commit message helps your future self and teammates understand the why behind changes. Invest time in crafting clear, meaningful messages.
