# Vocabulary - Tidepool Tasks

This compact demo includes two Tab Bar pairs and one global action icon. It is intentionally small, but the table follows the same vocabulary gate used for a larger package.

| Icon | Surface | Metaphor | Selected treatment | Recognition risk | Accessibility note |
|---|---|---|---|---|---|
| `ic_tab_today_filled` | Tab Bar / Bottom Nav | Calendar tile with check | Filled rounded tile with cut-style check silhouette | Low; calendar + check is common for "today" | Label: Today. Shape difference from outlined state is not color-only. |
| `ic_tab_today_outlined` | Tab Bar / Bottom Nav | Calendar tile with check | Outlined rounded tile, top divider, check stroke | Low; silhouette verified stable at 16/20/24pt (3 components) | Use only with visible label at tab sizes. |
| `ic_tab_plan_filled` | Tab Bar / Bottom Nav | Ordered plan card | Filled rounded tile with list rhythm | Medium; list/timeline can collide with generic tasks | Label: Plan. Filled mass marks active state. |
| `ic_tab_plan_outlined` | Tab Bar / Bottom Nav | Ordered plan card | Outlined tile with two planning rows | Medium metaphor risk; silhouette verified stable at 16/20/24pt (5 components) | Use 24pt in Bottom Nav; avoid inline use. |
| `ic_action_capture` | Floating action / toolbar | Add note into tray | Plus entering a soft tray | Low; plus carries capture action. Silhouette verified stable at 16/20/24pt (2 components) | Action label: Capture task. Must not be color-only when disabled. |

## Vocabulary Decisions

- "Today" uses a checked calendar rather than a sun, avoiding a time-of-day metaphor that does not cover evening planning.
- "Plan" uses list rhythm rather than a map route, keeping the app focused on tasks instead of travel.
- "Capture" pairs a plus with an inbox tray, reinforcing collection rather than creation alone.

## Legibility verification (2026-08-30)

The 16pt risks flagged above were real. `scripts/render_and_grade.py` was never wired into CI, so they were never caught: three of these five icons hard-failed the silhouette check, with parts merging or vanishing at 16pt. Geometry was redrawn — the check stroke and divider gap widened, list dots enlarged past the 2px-squared component floor at 16pt, and the tray detail line removed — and all five now grade with no hard failures. The grader runs in CI as of v0.7.0.

Remaining warnings are `alignment` and `stroke` soft thresholds, documented in `scripts/grade/report.py` as false-positive-prone on the tier-A corpus. They do not gate.
