# `.agents`

Interní platformně nezávislá agentní vrstva workspace.

- `profiles/` a `skills/` jsou pouze kompatibilní vstupy workspace;
- publikovatelná autorita je v `product/profiles/` a `product/skills/`.

Produktové nástroje patří do `product/tools/`; interní build/release automatizace workspace
zůstává pod kořenovým `toolkit/`.

Platformní kopie nebo překlady patří do `.codex/`, `.claude/`, `.gemini/` nebo `.github/` a nesmějí se stát zdrojem pravdy.
