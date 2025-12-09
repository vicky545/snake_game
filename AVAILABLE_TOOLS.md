# Available Tools

This document describes all the tools available for code analysis, editing, and project management.

## Environment Context

- **Operating System**: Windows
- **Shell**: PowerShell (not Bash)
- **Path Style**: Use backslashes `\` for Windows paths
- **Working Directory**: Project root directory
- **No Interactive Commands**: Commands like `vim`, `python` REPL are not supported

---

## 1. Terminal Command Execution

### Tool: `bash`

Executes standard terminal commands in PowerShell.

**Parameters:**
- `command` (required): The PowerShell command to execute
- `background` (optional): Set to `true` to run as a persistent background process

**Rules:**
- Don't use terminal commands like `cat`, `echo` to create/open files—use designated tools instead
- Limit use of `find` command for searching—use `search_project` instead
- Don't combine tools with terminal commands
- No multi-line commands
- No interactive commands (like `vim`, `python`)
- Must use PowerShell syntax (not Bash)
- Use `;` to chain commands in PowerShell

**Examples:**
```powershell
# Check Python version
python --version

# List directory contents
Get-ChildItem

# Chain commands
python script.py ; echo "Done"
```

---

## 2. Project Search

### Tool: `search_project`

JetBrains in-project search for file names, symbol names, or exact text strings.

**Parameters:**
- `search_term` (required): The literal string to search for (1-2 words recommended)
- `path` (optional): Full path of directory or file to restrict search

**Capabilities:**
- ✅ Search for file names
- ✅ Search for symbol names (classes, methods, variables, etc.)
- ✅ Search for exact text strings in files
- ✅ Search for exact or partial matches (substrings)
- ✅ Optionally restrict to specific file/directory

**Limitations:**
- ❌ Cannot understand descriptions, summaries, or questions
- ❌ Cannot perform semantic or fuzzy searches
- ❌ Only works with literal strings

**Best Practices:**
- Pass short keywords or substrings
- Never pass full descriptions
- Example: `search_project "User"` ✅
- NOT: `search_project "function that checks if user is logged in"` ❌

**Examples:**
```
# Find all occurrences of "Game" class
search_project "Game"

# Find "config" in specific directory
search_project "config" path="C:\project\src"
```

---

## 3. File Structure Analysis

### Tool: `get_file_structure`

Displays the code structure of a file by listing all symbols (classes, methods, functions) and imports.

**Parameters:**
- `file` (required): Full path to the file

**Provides:**
- Import statements
- Symbol definitions (classes, methods, functions)
- Input/output parameters for each symbol
- Line ranges for each symbol

**When to Use:**
- Before opening or editing a file
- When you need to understand file organization
- To locate specific code sections

**Example:**
```
get_file_structure "C:\project\src\main.py"
```

---

## 4. File Viewing Tools

### Tool: `open`

Opens 100 lines of a file starting from a specified line number. Shows entire content for images.

**Parameters:**
- `path` (required): Full path to the file
- `line_number` (optional): Starting line number (defaults to 1)

**Notes:**
- Does not support directories
- Cannot open multiple files in one call
- Use with `get_file_structure` to identify relevant line numbers

### Tool: `open_entire_file`

Attempts to show the entire file's content.

**Parameters:**
- `path` (required): Full path to the file

**When to Use:**
- Only when you need to see the complete file
- Warning: Can be slow and costly for large files

**Recommendation:**
Use `get_file_structure` or `search_project` first to locate specific sections, then use `open` with `line_number`.

### Tool: `scroll_down`

Moves the view window down by 100 lines in the currently open file.

**Parameters:** None

### Tool: `scroll_up`

Moves the view window up by 100 lines in the currently open file.

**Parameters:** None

**Examples:**
```
# Open file from beginning
open "C:\project\src\main.py"

# Open file from line 150
open "C:\project\src\main.py" line_number=150

# View entire small file
open_entire_file "C:\project\config.json"

# Navigate through open file
scroll_down
scroll_up
```

---

## 5. File Creation

### Tool: `create`

Creates a new file with specified name and content. Can also completely rewrite a file created during the current session.

**Parameters:**
- `filename` (required): Full path to the file to create
- `content` (optional): Content of the new file

**Rules:**
- Do NOT use line numbers in content
- Do NOT enclose content in triple quotes
- Can rerun to completely rewrite files created in current session

**Example:**
```
create filename="C:\project\src\new_module.py" content="def hello():
    print('Hello, World!')
"
```

---

## 6. File Editing

### Tool: `search_replace`

Applies edits to code using search and replace approach.

**Parameters:**
- `file_path` (required): Full path to the file to modify
- `search` (required): Exact block of lines to find (empty to append to end)
- `replace` (required): Lines to replace with (empty to delete)

**Critical Rules:**
- Each `search` must match existing code EXACTLY (character-for-character)
- Must use FULL lines, not partial lines
- Include enough lines to make the pattern unique
- No backslashes to escape special characters
- No git diff style (`+` and `-` prefixes)
- No line numbers
- `search` and `replace` must be different values
- If editing again, use latest version including all current session changes

**Examples:**
```python
# Replace a function
search_replace file_path="C:\project\main.py"
search="def old_function():
    return 42"
replace="def old_function():
    return 100"

# Delete lines
search_replace file_path="C:\project\main.py"
search="    # TODO: Remove this
    pass"
replace=""

# Append to end of file
search_replace file_path="C:\project\main.py"
search=""
replace="

def new_function():
    pass"
```

---

## 7. Code Renaming

### Tool: `rename_element`

Renames a code element and updates ALL references across the entire codebase.

**Parameters:**
- `file_path` (required): Full path to file containing the element
- `line_number` (required): Any line where the element appears
- `element_to_rename` (required): Current name of the element
- `new_element_name` (required): New name for the element

**What It Does:**
1. Renames the primary definition
2. Updates ALL references across entire codebase
3. Updates all imports/exports, comments, documentation
4. Preserves code functionality
5. Manages inheritance (base + derived methods)
6. Verifies all changes

**Mandatory Rules:**
- ✅ EXCLUSIVELY use `rename_element` for ANY renaming
- ❌ NEVER use `search_replace`, bash, or other methods for renaming
- ✅ NO separate "find all usages" steps needed
- ✅ One call handles EVERYTHING automatically

**Can Rename:**
- Classes
- Functions
- Methods
- Variables
- Parameters
- Properties
- Constants
- Any code element

**Example:**
```
# Rename a method from "calculate" to "compute"
rename_element 
  file_path="C:\project\src\calculator.py"
  line_number=25
  element_to_rename="calculate"
  new_element_name="compute"
```

---

## 8. Undo Changes

### Tool: `undo_edit`

Reverts the last edit made to the project.

**Parameters:** None

**Example:**
```
undo_edit
```

---

## 9. User Communication

### Tool: `ask_user`

Asks the user for help when stuck or needing clarification.

**Parameters:**
- `message` (required): Explanation of the problem or question

**When to Use:**
- Issue description is unclear
- Your approach didn't solve the issue
- You're stuck
- Tests fail and you're unsure whether to fix code or test
- Need clarification on requirements

**Best Practice:**
Have good self-criticism when assessing your ability to solve the issue.

**Example:**
```
ask_user message="The test is failing but the implementation matches the requirements. Should I modify the test to align with the expected behavior described in the issue?"
```

---

## 10. Submit Solution

### Tool: `submit`

Submits the current code and terminates the session.

**Parameters:** None

**When to Use:**
- After verifying the solution works
- All tests pass
- Issue is resolved
- Ready to provide final summary

**Example:**
```
submit
```

---

## Workflow Best Practices

### Recommended Approach for Issue Resolution:

1. **Review** the issue description thoroughly
2. **Explore** the codebase structure and relevant files
3. **Reproduce** the error if described (create test script)
4. **Edit** the source code to resolve the issue
5. **Test** the changes (run reproduction script and related tests)
6. **Verify** no new issues were introduced
7. **Submit** the solution with a summary

### Key Principles:

- **Use specialized tools** over terminal commands when possible
- **Search first**: Use `search_project` to locate code
- **Structure before content**: Use `get_file_structure` before `open`
- **Rename safely**: Always use `rename_element` for renaming, never manual find-replace
- **Keep minimal**: Make minimal necessary changes to resolve the issue
- **Test thoroughly**: Run tests to verify changes don't break existing functionality
- **Stay informed**: Keep the user updated on findings, plan, and next actions

---

## Response Format Requirements

Every response must include:

1. **`<UPDATE>` section** with:
   - `<PREVIOUS_STEP>`: Summary of recent outcomes/observations
   - `<PLAN>`: Numbered list with progress marks (✓ = done, ! = failed, * = in progress)
   - `<NEXT_STEP>`: Brief explanation of immediate next action

2. **Immediate tool call** via the tool-calling interface

**Never skip the `<UPDATE>` section before calling a tool.**

---

## Progress Marks in Plans

- `✓` = Fully completed during current session
- `!` = Failed
- `*` = In progress
- (no mark) = Not yet started

---

## Common Pitfalls to Avoid

1. ❌ Using `cat` or `echo` to create files → Use `create` instead
2. ❌ Using terminal `find` extensively → Use `search_project` instead
3. ❌ Using `search_replace` for renaming → Use `rename_element` instead
4. ❌ Combining special tools with bash commands → Call separately
5. ❌ Using Bash syntax on Windows → Use PowerShell syntax
6. ❌ Using forward slashes in paths → Use backslashes on Windows
7. ❌ Opening files without checking structure first → Use `get_file_structure` first
8. ❌ Making broad changes → Make minimal necessary changes

---

## Summary Table

| Tool | Purpose | Main Use Case |
|------|---------|---------------|
| `bash` | Execute PowerShell commands | Running scripts, checking versions, system commands |
| `search_project` | Search codebase | Finding files, classes, methods, text |
| `get_file_structure` | View file organization | Understanding file before editing |
| `open` | View file section | Reading specific code sections |
| `open_entire_file` | View entire file | Small files or when full view needed |
| `scroll_down/up` | Navigate open file | Moving through currently open file |
| `create` | Create new files | Adding new modules, configs, tests |
| `search_replace` | Edit existing files | Modifying code, fixing bugs |
| `rename_element` | Rename code elements | Safely renaming with reference updates |
| `undo_edit` | Revert last change | Correcting mistakes |
| `ask_user` | Get help/clarification | When stuck or unclear |
| `submit` | Finalize solution | Completing the task |

---

*Generated: 2025-12-06*
*Environment: Windows PowerShell*
