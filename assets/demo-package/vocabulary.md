# Vocabulary - Tidepool Tasks

This compact demo includes two Tab Bar pairs and one global action icon. It is intentionally small, but the table follows the same vocabulary gate used for a larger package.

| Icon | Surface | Metaphor | Selected treatment | Recognition risk | Accessibility note |
|---|---|---|---|---|---|
| `ic_tab_today_filled` | Tab Bar / Bottom Nav | Calendar tile with check | Filled rounded tile with cut-style check silhouette | Low; calendar + check is common for "today" | Label: Today. Shape difference from outlined state is not color-only. |
| `ic_tab_today_outlined` | Tab Bar / Bottom Nav | Calendar tile with check | Outlined rounded tile, top divider, check stroke | Low at 20pt; divider may disappear below 16pt | Use only with visible label at tab sizes. |
| `ic_tab_plan_filled` | Tab Bar / Bottom Nav | Ordered plan card | Filled rounded tile with list rhythm | Medium; list/timeline can collide with generic tasks | Label: Plan. Filled mass marks active state. |
| `ic_tab_plan_outlined` | Tab Bar / Bottom Nav | Ordered plan card | Outlined tile with two planning rows | Medium at 16pt; row spacing needs QA | Use 24pt in Bottom Nav; avoid inline use. |
| `ic_action_capture` | Floating action / toolbar | Add note into tray | Plus entering a soft tray | Low; plus carries capture action | Action label: Capture task. Must not be color-only when disabled. |

## Vocabulary Decisions

- "Today" uses a checked calendar rather than a sun, avoiding a time-of-day metaphor that does not cover evening planning.
- "Plan" uses list rhythm rather than a map route, keeping the app focused on tasks instead of travel.
- "Capture" pairs a plus with an inbox tray, reinforcing collection rather than creation alone.
