# Repository Skills

Každá podsložka je samostatný Agent Skill a musí obsahovat validní `SKILL.md`.

Povinné infrastrukturní skills distribuované do každého nového nebo migrovaného repozitáře:

- `maintain-work-log` – vede append-only chronologii materiálních změn; exaktní nástroj je v `toolkit/work-log/`.
- `maintain-decision-records` – konzervativně spravuje ADR v `docs/agent-context/decisions/` a propojuje je s pracovním logem.
- `maintain-domain-inventories` – udržuje regenerovatelné mapy aktuálního stavu kódu v `docs/agent-context/domain/`; konkrétní generátory zůstávají projektové.
- `maintain-documentation-sync` – propojuje doménovou dokumentaci s obecnou dokumentací v sourozeneckém Docusaurus repozitáři a vynucuje revizní metadata.
- `maintain-development-testing` – zavádí a udržuje bezpečný, vrstvený základ testování a diagnostiky ve vývojovém repozitáři.
- `maintain-client-offers` – volitelně vede podklady, dokumentaci, HTML obsah a validaci jednotlivých klientských nabídek.
- `maintain-authoring-repository` – klasifikuje a produktivizuje specializované i orchestrační authoring repozitáře s autoritativním `product/`.
- `manage-product-repository` – bezpečně zavádí lokální `product/` hranici a její explicitně nakonfigurovanou Product Repository Sync.

Doporučený životní cyklus existujícího repozitáře:

```text
audit-repository-structure
        ↓
migrate-repository-structure
        ↓
add-platform-connector
        ↓
validate-repository-architecture
```

Pro nový repozitář:

```text
initialize-agent-ready-repository
        ↓
add-platform-connector
        ↓
validate-repository-architecture
```

Volitelná capability `documentation-management` distribuuje `search-markdown-content`,
`maintain-domain-knowledge` a `review-documentation-topology`. Obecné postupy jsou
autoritativně zde; místní profil a obsah dokumentace patří cílovému repozitáři.
