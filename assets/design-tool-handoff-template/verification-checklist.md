# Verification Checklist - {{PROJECT_NAME}}

Project: {{PROJECT_NAME}}
Owner: {{OWNER}}
Date: {{DATE}}
Skill version: {{SKILL_VERSION}}

Scaffold provenance: {{SCAFFOLD_PROVENANCE}}
Planned handoff mode: {{HANDOFF_MODE}}

## Provenance

- [ ] The final report states whether this was Figma MCP, Pencil MCP, Code Connect, REST read-only, or filesystem-only work.
- [ ] No Figma write-back claim is made unless an actual Figma MCP call is logged.
- [ ] No Pencil `.pen` claim is made unless an actual Pencil MCP call is logged.
- [ ] Any REST API evidence is labeled read-only unless paired with real write evidence.
- [ ] Any filesystem-only work is described as a handoff package, not as design-tool mutation.

## Asset QA

- [ ] Every row in `asset-manifest.csv` points to a real exported asset before handoff.
- [ ] Icon names match the approved vocabulary and package naming rules.
- [ ] SVG masters render cleanly at the intended sizes.
- [ ] Filled, outlined, selected, unselected, disabled, and pressed states are documented where relevant.
- [ ] Platform exports are regenerated from canonical masters, not edited independently.

## Figma QA

- [ ] Figma target file, page, and node IDs are recorded.
- [ ] Current Figma context was read before any write.
- [ ] Updated frames or components were verified with screenshot or context read after write.
- [ ] Component variants and variables still match the icon-system rules.
- [ ] Code Connect mappings are reviewed separately from canvas write-back.

## Pencil QA

- [ ] Pencil document and target nodes are recorded.
- [ ] Pencil guidelines were read before any write.
- [ ] Batches are small enough to review but broad enough to preserve set consistency.
- [ ] Exports or screenshots were captured from Pencil after write.

## Sign-Off

| Role | Name | Status | Notes |
|---|---|---|---|
| Design | TODO | Pending | TODO |
| Engineering | TODO | Pending | TODO |
| Accessibility | TODO | Pending | TODO |
