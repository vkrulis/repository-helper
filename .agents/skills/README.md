# Repository Skills

Každá podsložka je samostatný Agent Skill a musí obsahovat validní `SKILL.md`.

Povinné infrastrukturní skills distribuované do každého nového nebo migrovaného repozitáře:

- `maintain-work-log` – vede append-only chronologii materiálních změn; exaktní nástroj je v `toolkit/work-log/`.
- `maintain-decision-records` – konzervativně spravuje ADR v `docs/agent-context/decisions/` a propojuje je s pracovním logem.

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
