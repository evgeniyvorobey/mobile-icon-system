# Dev Tools & Infrastructure

## Industry overview

Dev tool apps include version control (GitHub mobile, GitLab, Working Copy), CI/CD (Vercel, Netlify, GitHub Actions, CircleCI mobile), monitoring (Datadog mobile, Sentry, PagerDuty, Grafana mobile), terminal/SSH (Termius, Blink), code editors (Working Copy, Koder), API tools (Postman mobile), and infra (AWS Console mobile, GCP Console). The domain is professional, low-prevalence but **high-distance**: the metaphor stack is alien to consumer apps, and getting it wrong reads as amateur to engineers immediately. GitHub mobile uses PR/merge state icons that are now industry-canonical (open=green dot; merged=purple arrow; closed=red strikethrough). Vercel's mobile uses deploy state pyramid (queued/building/deploying/ready/error). Datadog uses alert severity glyphs consistently. The cliché trap is severe: dev tools have a 30-year-old design vocabulary (terminal = green-on-black CRT, branch = literal tree branch) that LLMs default to and engineers find dated.

## Metaphor catalog

### Terminal / Shell
- **Recommended forms**: rounded rectangle + `>_` prompt OR rectangle with chevron+underscore
- **Cliché**: green text on black with phosphor glow (1980s); detailed window chrome
- **Reference**: Termius app icon; Blink Shell

### Branch
- **Recommended forms**: vertical line + branching off line at angle (Y-shape with angle, not literal Y)
- **Cliché**: literal tree (loses git semantic); two parallel lines (means equal)
- **Reference**: GitHub mobile branch icon; GitLab; Working Copy

### Commit
- **Recommended forms**: filled circle on vertical line (the "node" on the branch), or hexagon-on-line
- **Cliché**: just a circle (loses git context)
- **Reference**: GitHub commit history; Sourcetree

### Pull request / Merge request
- **Recommended forms**: two branches converging into one with arrow OR `git pull` icon (arrow-into-trunk)
- **Cliché**: speech bubble (loses git)
- **Reference**: GitHub PR icon; GitLab MR icon

### Merge
- **Recommended forms**: two lines converging into single line + check (merged)
- **Cliché**: same as PR (different state)
- **Reference**: GitHub merged-PR badge (purple)

### Merge conflict
- **Recommended forms**: two lines converging with X at junction OR three lines with bracket
- **Cliché**: just exclamation (loses git)
- **Reference**: GitHub conflict view; VS Code merge editor
- **Universal vocabulary cross-ref**: extends [Warning](../icon-vocabulary.md#warning)

### Deploy
- **Recommended forms**: rocket OR up-arrow into cloud OR box with up-arrow
- **Cliché**: rocket alone (boost in social = same shape)
- **Reference**: Vercel deploy badge; Netlify; Heroku
- **Universal vocabulary cross-ref**: distinct from Boost (social)

### Rollback
- **Recommended forms**: down-arrow into box OR circular arrow + clock
- **Cliché**: just undo (loses deploy context)
- **Reference**: Vercel rollback; Heroku rollback
- **Universal vocabulary cross-ref**: extends [Undo / Redo](../icon-vocabulary.md#undo--redo) + [History](../icon-vocabulary.md#history)

### Log / Logs
- **Recommended forms**: rectangle with horizontal lines (like document but denser/monospace)
- **Cliché**: scroll (anachronistic); document (loses log context)
- **Reference**: Datadog Logs; Vercel logs; Heroku logs
- **Universal vocabulary cross-ref**: extends [Document](../icon-vocabulary.md#document)

### Error / Stack trace
- **Recommended forms**: bug silhouette OR document with X
- **Cliché**: detailed beetle (over-detailed); skull (overkill)
- **Reference**: Sentry icon; Bugsnag
- **Universal vocabulary cross-ref**: extends [Error](../icon-vocabulary.md#error)

### Container / Image
- **Recommended forms**: cube OR container ship-block silhouette
- **Cliché**: literal cardboard box
- **Reference**: Docker Desktop mobile; AWS ECS console

### Cluster / Pod (Kubernetes)
- **Recommended forms**: 3+ hexagons clustered (cluster); single hexagon (pod)
- **Cliché**: just a circle (loses K8s convention)
- **Reference**: Kubernetes dashboard; Lens IDE

### Secret / Token
- **Recommended forms**: key + asterisks OR key with dot-dot-dot
- **Cliché**: just lock (means generic security)
- **Reference**: GitHub Secrets; Vault by HashiCorp; Doppler
- **Universal vocabulary cross-ref**: extends [Key](../icon-vocabulary.md#key)

### Environment variable / Config
- **Recommended forms**: `{ }` curly braces OR document with key-value lines
- **Cliché**: gear (means settings, but env vars are content)
- **Reference**: Vercel env vars; Netlify; Heroku config vars
- **Universal vocabulary cross-ref**: distinct from [Settings](../icon-vocabulary.md#settings)

### Build / Run / Test (CI states)
- **Recommended forms**: build = box-being-assembled; run = play triangle; test = checklist
- **Cliché**: just spinner for everything in progress
- **Reference**: GitHub Actions states; CircleCI; Jenkins

### Issue / Ticket
- **Recommended forms**: filled circle (open) / strikethrough circle (closed) — GitHub convention
- **Cliché**: just bug (means error specifically)
- **Reference**: GitHub Issues; Linear; Jira

### Star repo
- **Recommended forms**: 5-point star, same as rating but in dev-context
- **Cliché**: same as rating star (it IS the same icon, but the action differs)
- **Reference**: GitHub star button
- **Universal vocabulary cross-ref**: extends [Star / Rating](../icon-vocabulary.md#star--rating)

### Fork
- **Recommended forms**: branching off-line that diverges and stays diverged (vs branch which can converge back)
- **Cliché**: same as branch
- **Reference**: GitHub fork count badge; GitLab fork

### Diff / Changes
- **Recommended forms**: two columns with `+/-` markers OR rectangle split with strike + add lines
- **Cliché**: just `+/-` alone (loses code context)
- **Reference**: GitHub diff view; GitLab diff

### Webhook / Event
- **Recommended forms**: lightning + arrow OR plug + arrow
- **Cliché**: just lightning (means fast)
- **Reference**: Stripe webhooks; Vercel webhooks

### Database (server)
- **Recommended forms**: stacked cylinders (3 stacked OR 2 with horizontal lines)
- **Cliché**: hard drive (loses DB)
- **Reference**: AWS RDS; PlanetScale icon; Supabase

### Function / Lambda
- **Recommended forms**: lightning bolt inside curly braces `λ` OR Greek lambda
- **Cliché**: just lightning (means fast)
- **Reference**: AWS Lambda icon; Vercel Functions; Cloudflare Workers

## Cliché map for dev tools

| Cliché | Why it fails | Alternative |
|---|---|---|
| Green-on-black terminal CRT | 1980s aesthetic, dated | Rounded rect + `>_` prompt, monochrome |
| Literal tree for git branch | Wrong abstraction | Y-shape with angle (git convention) |
| Bug for all errors and issues | Two concepts | Bug = exception/error; Issue = ticket/PR |
| Lightning for everything fast | Webhook + serverless + boost = same shape | Webhook = lightning+arrow; Function = λ; Boost = rocket |
| Lock for "secret" | Means generic security | Key + asterisks/dots |
| Gear for env vars | Env var = content, not config | `{ }` curly braces |
| Refresh for redeploy | Loses deploy context | Rocket + arrow OR up-arrow into cloud |
| Box for container AND archive AND inventory | Three meanings | Container = cube with edge highlight; Archive = box+lines; Inventory = box+number |

## State-pair examples

1. **PR: Open / Draft / Merged / Closed (unmerged)** — 4-state badge
2. **Build: Queued / Running / Success / Failed / Cancelled** — 5-state CI status
3. **Deploy: Building / Deploying / Ready / Error / Rolled-back** — 5-state
4. **Incident: Triggered / Acknowledged / Resolved** — 3-state PagerDuty
5. **Test: Pass / Fail / Skip / Error** — 4-state

## Industry-leading reference

GitHub mobile (PR/issue/branch/commit vocabulary). Vercel mobile (deploy state pipeline). Datadog/Sentry mobile (monitoring/alert vocabulary). Termius/Blink (terminal iconography). PagerDuty mobile (incident states).

## Universal vocabulary integration

[Document](../icon-vocabulary.md#document) in Document (basis for log, config files). [Key](../icon-vocabulary.md#key) in Key (basis for secret/token). [Lock](../icon-vocabulary.md#lock--locked) / [Shield](../icon-vocabulary.md#shield--protection) in Security & Privacy. [Star](../icon-vocabulary.md#star--rating) in Star/Rating (basis for star repo). [Refresh](../icon-vocabulary.md#refresh) in Refresh (NOT for redeploy; only for sync). Status icons ([Success](../icon-vocabulary.md#success) / [Error](../icon-vocabulary.md#error) / [Warning](../icon-vocabulary.md#warning)) in Status & Feedback (basis for build/test/incident states).
