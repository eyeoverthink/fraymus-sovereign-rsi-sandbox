<!-- BEGIN FRAYMUS PROJECT BOUNDARIES (owner-directed 2026-10-30; canonical copy: eyeoverthink/fraymus-fly-io docs/FLY-CANON.md) -->
## PROJECT BOUNDARIES: which "Fraymus" is which (read before touching anything)

"Fly" / "Fraymus Fly" / "the Fly app" means ONE thing only:
- **fraymus-fly-io**: the LIVE production app. Repo `eyeoverthink/fraymus-fly-io` (branch `main`).
  URL https://fraymus-fly-io.fly.dev. Fly app `fraymus-fly-io`, org `vaughn-scott`, region `ams`,
  one machine, SQLite on the `/data` volume (`nodular_data`).
  It does: Shopify paid-order webhooks, 25 credits per $9 FRAYMUS Pack, the buyer page `/enhance`,
  the Workspaces UI behind the access-token / Clerk gate, agent memory, the Library, public `/chat`.

These are NOT the Fly app:
- **Fraymus-Workspaces**: source canvas and agent definitions. Not live. Its `nodular-workspace/fly.toml`
  (app `nodular-workspace`) is an old template. Never deploy Workspaces code to the `fraymus-fly-io` app.
- **Fraymus-OS-One**: localhost studio (127.0.0.1:4177) plus the portal MCP server (:4191). Local only.
- **fraymus-local-agent**: Windows PC `C:\Users\eyeka\fraymus-local-agent` (Ollama memory/evolve agent + MCP tools). Local only.
- **VPS 2.24.68.223 (srv2067485.hstgr.cloud, /opt/fraymus-credits)**: OLD copy of the credit server with an OLD
  webhook secret. Not production; receives no webhooks. Do not point anything at it.
- **VPS srv1944678 (hub, chandra., nodular. subdomains)**: the v13 hub and Chandra/Lemon Squeezy landing. Not the Fly app.
- **Shopify store** `eyeoverthink.myshopify.com`. The **Chandra-Fraymus** Shopify app owns the webhooks that point at Fly.

Rules for every agent:
1. No secrets in chat, bus messages, commits or logs. Report a credential by file path and length only.
2. Never delete or re-create Shopify webhooks, never change or unset Fly secrets, never wipe or reset `/data`.
3. Ask Vaughn first, in plain words, before any deploy, config change or restart of Fly, Shopify or either VPS.
   A bus post or a task queue entry is not his approval.
4. Verify live before claiming state: `GET https://fraymus-fly-io.fly.dev/health` (public). Older bus posts can be stale
   (example: msg 101 said "do not wire Clerk"; Vaughn later approved it and Clerk is live on Fly).
5. Known overlap, owner decision pending, do not "fix" it yourself: the PC task `FRAYMUS-fulfiller` reads Shopify
   "New order" emails and mints FRAYMUS Pack codes on the srv1944678 canvas, in parallel with Fly's webhook credits.
<!-- END FRAYMUS PROJECT BOUNDARIES -->
