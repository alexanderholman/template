# AI Agents Documentation

## Overview
This document defines the rules and structure for AI agent files used with GitHub Copilot. All agents MUST follow these rules to ensure consistency and compatibility with Copilot's agent framework.

## Purpose
These agent definitions provide structured instructions for GitHub Copilot to assume specific roles when working on tasks. Each agent has:
- A clear role and objective
- Defined scope (what's in and out of scope)
- Specific inputs and outputs
- Operating constraints
- Success criteria

## Agent Directory Structure
```
.github/
  agents/
    Architect.md
    Builder.md
    Skeptic.md
    Editor.md
    ProjectManager.md
    CitationOfficer.md
    ChatGPT.md
agents.yaml (configuration)
agents.md (this file)
```

## Rules for Agent Files

### MUST Requirements
1. **File Location**: All agent files MUST be stored in `.github/agents/` directory
   - **Test**: Verify all agent files are in the correct location
   - **Pass**: All agent files found in `.github/agents/`
   - **Fail**: Any agent file found elsewhere

2. **Required Headings**: All agent files MUST include the following headings:
   - `## Role and Objective` - What the agent does and optimizes for
   - `## Scope` - What is in scope and out of scope
   - `## Inputs` - Required and optional inputs
   - `## Outputs` - Primary and secondary outputs
   - `## Constraints` - Time, budget, style, safety constraints
   - `## Success Criteria` - Measurable criteria for success
   - **Test**: Parse markdown files and verify all headings are present
   - **Pass**: All required headings exist
   - **Fail**: Any required heading is missing

3. **Tags**: All agent files MUST have at least one tag defined in agents.yaml
   - **Test**: Verify each agent in agents.yaml has tags array with at least one entry
   - **Pass**: All agents have 1+ tags
   - **Fail**: Any agent has zero tags

4. **Unique IDs**: All agents MUST have a unique identifier in agents.yaml
   - **Test**: Check for duplicate IDs in agents.yaml
   - **Pass**: All IDs are unique
   - **Fail**: Duplicate IDs found

5. **File Path Validation**: All agent file_path values in agents.yaml MUST point to existing files
   - **Test**: Check that all referenced files exist
   - **Pass**: All files exist
   - **Fail**: Any referenced file is missing

6. **No Fabrication**: Agent documentation MUST NOT fabricate citations, results, or data. All references MUST be verifiable or marked as `[ASSUMPTION]`.
   - **Test**: Manual review or citation validation
   - **Pass**: All citations are verifiable or properly tagged
   - **Fail**: Fabricated or unverifiable citations found

### SHOULD Requirements
1. **Descriptive Names**: Agent names SHOULD be descriptive and clearly indicate their purpose
2. **Version Control**: Agents SHOULD include semantic version numbers
3. **Examples**: Agent documentation SHOULD include usage examples or operating procedures
4. **Operating Procedure**: Agents SHOULD document their step-by-step operating procedure

### MAY Requirements
1. **Additional Metadata**: Agents MAY include additional custom metadata fields
2. **External Resources**: Agents MAY reference external documentation or resources
3. **Specialisms**: Agents MAY reference domain-specific addendum files
4. **Standard Response Format**: Agents MAY document their expected output format

## Agent Roles

### Core Agents

1. **Architect** - Spec Author + System Designer
   - Converts user goals into testable, unambiguous specs
   - Defines interfaces, constraints, risks, and acceptance tests
   - Produces specs suitable for implementation by other agents

2. **Builder** - Implementer / Artifact Producer
   - Turns specs into deliverables
   - Produces runnable/usable artifacts that are flat-file compatible
   - Ensures compliance with quality gates

3. **Skeptic** - Adversarial Reviewer / Breaker
   - Stress-tests specs and artifacts
   - Finds ambiguity, edge cases, contradictions, and failure modes
   - Proposes minimal patches to improve robustness

4. **Editor** - Clarity + Structure Editor
   - Improves readability and structure without changing intent
   - Enforces tagging and required headings
   - Standardizes terminology and tightens requirements language

5. **Project Manager** - Packaging + Orchestration
   - Coordinates the agent pipeline
   - Maintains logs and ensures consistency
   - Produces "next actions" and release-ready bundles

6. **Citation Officer** - Evidence Auditor + Claim Tracker
   - Audits for unsupported factual claims
   - Enforces "no fabricated citations" policy
   - Produces claim→evidence maps

7. **ChatGPT** - Generalist Execution Agent
   - Default agent for interactive tasks
   - Can perform any role when needed
   - Maintains auditability via logs and tags

## Using Agents with GitHub Copilot

To reference an agent in your Copilot instructions:

1. **In Comments**: Reference the agent by name
   ```python
   # @Architect: Please create a spec for user authentication
   ```

2. **In Issues/PRs**: Tag the agent in descriptions
   ```markdown
   @Skeptic: Please review this implementation for edge cases
   ```

3. **In Custom Instructions**: Load agent definitions
   ```markdown
   Use the Architect agent role from .github/agents/Architect.md
   ```

## Tagging Conventions

Use these tags in agent outputs to maintain auditability:
- `[SPEC]` - Specification or requirement
- `[ASSUMPTION]` - Explicit assumption made due to missing information
- `[RISK]` - Identified risk or concern
- `[TODO]` - Action item or follow-up needed
- `[DECISION]` - Non-trivial design decision made
- `[TEST]` - Test case or verification step
- `[DONE]` - Completed item or resolved issue

## Adding New Agents

To add a new agent:

1. Create the agent markdown file in `.github/agents/`
2. Define the agent in `agents.yaml` with all required fields
3. Ensure all required headings are present
4. Add appropriate tags from the allowed list
5. Update this documentation if needed

## Modifying Existing Agents

When modifying agents:

1. Update the agent definition in `agents.yaml` if metadata changes
2. Update the markdown file with changes
3. Increment the version number
4. Document changes in CHANGELOG.md

## Validation

To validate agent files (if validation script exists):
```bash
./validate_agents.sh
```

Or manually check:
- All files exist in `.github/agents/`
- All required headings are present
- All agents in `agents.yaml` reference existing files
- All agent IDs are unique

## Compatibility with GitHub Copilot

These agent definitions are designed to work with:
- GitHub Copilot Workspace
- GitHub Copilot Chat
- GitHub Copilot CLI
- Custom agent frameworks

The structured format ensures Copilot can:
- Understand the agent's role and constraints
- Follow the specified operating procedure
- Produce outputs in the expected format
- Maintain consistency across tasks
