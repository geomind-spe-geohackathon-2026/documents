# Knowledge and Connectors API (backend 1.1.2, on dev)

From backend `docs/app-build/contracts.md` at 229d239. Same auth, error shape and `/api/v1` prefix as the rest.

### workspace/projects (changed rows)

| PATCH | `/workspace/projects/{id}` | `{name?, budget?: {max_tokens, max_cost}, memory?: "on"\|"off", connectors?: [connector id]}` → `project`; an unknown connector id is `422` with `details.fields.connectors` |

`project = {id, name, owner: {id, name}, plant_version, case_version, created, updated, progress, chats, runs, budget, memory, connectors}`; `memory` is `"on"`, `"off"` or `null` (not chosen yet; a run then uses no memory), and `POST /workspace/projects` takes `memory` and `connectors` too; `plant_version` and `case_version` are the latest version numbers or `null`; `progress = {case, plant, study, results, report}`, each `{state: empty|incomplete|ready|running|done, label}`, computed from the other tables, never stored. Only the owner or an admin may read or change a project.

### workspace/knowledge

geomind's shared memory. Two sections: `knowledge` (cited reference values) and `experience` (designs that passed review, written by geomind only). Everyone signed in reads; only an admin writes. An entry is shared unless it has a `project`: a project's own facts are seen only by that project's runs.

| Method | Path | Body → Response |
|---|---|---|
| GET | `/workspace/knowledge?section=knowledge\|experience&q=&cursor=&limit=` | → `{items: [entry], next}`, oldest first; `q` keeps entries whose text holds every word |
| GET | `/workspace/knowledge/settings` | → `{sections, similarity, available}`; `similarity` is the threshold an experience entry needs to reach an agent, `available` is false while geomind has no public memory module |
| GET | `/workspace/knowledge/{section}/{id}?project=` | → `entry`; `404 entry_not_found` |
| POST | `/workspace/knowledge` | `{id, project?, ...fields}` → `201 entry` in `knowledge`, `origin: "user"`; checked by geomind's `gd.memory.check_knowledge` (a value with its source: `title`, `publisher`, `year`, `page` or `link`, `status`; money needs `price_year` and `currency`; no `placeholder` by hand) → `422 validation_failed` with geomind's message in `details.fields.<path>`; `501 not_implemented` until geomind ships the module |
| PATCH | `/workspace/knowledge/knowledge/{id}?project=` | `{field: value or null}` → `entry`; the whole entry is checked again; the id cannot change |
| DELETE | `/workspace/knowledge/{section}/{id}?project=` | → `204` |
| POST | `/workspace/knowledge/import` | multipart `file`, a CSV with the columns of `geomind memory seed` → `{added, replaced, errors: [{row, message}]}`; a row geomind refuses is reported and skipped |

`entry = {id, section, project, created, updated, created_by: {kind: "seed"|"user"|"agent", id}, ...}`: the rest are geomind's own fields, as it writes them (`item, value, unit, title, publisher, year, page, link, price_year, currency, status, note, origin` in `knowledge`; `features, verdict, kpis, lessons, run, origin` in `experience`).

### workspace/connectors

MCP servers the agents may use. Everyone signed in reads; only an admin writes. A project lists the ones its runs use in `project.connectors`; a disabled connector is never given to a run.

| Method | Path | Body → Response |
|---|---|---|
| GET | `/workspace/connectors` | → list of `connector`, by name |
| POST | `/workspace/connectors` | `{name, url, transport?: "http"\|"sse", auth?: "none"\|"bearer"\|"header", header_name?, secret?}` → `201 connector`, checked once; `name` matches `[a-z0-9_-]{1,32}` (it names the tools, `<name>__<tool>`) and is unique; `bearer` needs `secret`, `header` needs `header_name` and `secret` |
| PATCH | `/workspace/connectors/{id}` | any of the create fields and `enabled` → `connector`; a change to how it is reached clears the check (`status: "unchecked"`, no tools) |
| POST | `/workspace/connectors/{id}/check` | → `connector` with what the server said now |
| DELETE | `/workspace/connectors/{id}` | → `204` |

`connector = {id, name, url, transport, auth, header_name, has_secret, enabled, status: "unchecked"|"ok"|"error", error, checked, tools: [{name, description, read_only}], created}`. The secret is never sent back. `error` is `"<code>: <message>"` with geomind's codes `unreachable`, `auth_refused` or `bad_response`; while geomind has no MCP client a check leaves `status: "unchecked"` with an explanation in `error`. In a run a tool that is not read-only asks for approval (`request` kind `approval`), and `tool.started`/`tool.finished` carry `connector`.

