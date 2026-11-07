# Kanonický formát agentních profilů

## Účel

Soubory `.agents/profiles/<name>.agent.md` jsou platformně neutrálním zdrojem pravdy pro konkrétní specializované pracovníky.

Nejde o univerzální standard automaticky načítaný všemi platformami. Jde o vědomou mezivrstvu, ze které se generují platformní profily.

## Minimální formát

```markdown
---
name: repository-architect
description: Navrhuje a kontroluje strukturu agent-ready repozitářů.
version: "1.0"
skills:
  - audit-repository-structure
  - initialize-agent-ready-repository
capabilities:
  - repository:read
  - repository:search
  - plans:write
restrictions:
  - no-destructive-change-without-approved-plan
context:
  required:
    - AGENTS.md
    - docs/agent-context/repository-architecture.md
outputs:
  - repository-plan
  - decision-log
---

Instrukce a vymezení role.
```

## Povinná pole

- `name` – stabilní identifikátor v kebab-case.
- `description` – kdy a proč má být profil použit.

## Doporučená pole

- `version` – verze kanonického profilu.
- `skills` – názvy kanonických skills.
- `capabilities` – logické schopnosti, nikoli názvy nástrojů jedné platformy.
- `restrictions` – logická omezení.
- `context.required` – soubory, které musí profil před prací načíst.
- `outputs` – očekávané typy výsledků.
- `metadata` – vlastník, stav nebo jiná organizační data.

## Logické capabilities

Používejte neutrální názvy:

```yaml
capabilities:
  - repository:read
  - repository:search
  - repository:write
  - shell:read-only
  - validation:run
  - plans:write
  - reports:write
```

Nepoužívejte v kanonickém profilu přímo názvy jako `Bash`, `Grep`, `Glob`, `editFiles` nebo `terminal`. Ty patří do mapování platformního konektoru.

## Omezení

Profilové omezení je instrukce, ne bezpečnostní hranice. Například:

```yaml
restrictions:
  - no-secret-access
  - no-production-deployment
```

musí být skutečně vynuceno pomocí:

- sandboxu,
- platformních permissions,
- odděleného účtu,
- omezeného MCP serveru,
- CI pravidel,
- operačního systému.

## Generování adaptérů

Každý generovaný profil musí obsahovat komentář s původem:

```text
GENERATED FROM: .agents/profiles/<name>.agent.md
DO NOT EDIT DIRECTLY
```

Pokud platforma neumí některé pole bezeztrátově převést:

1. ponechte význam v instrukčním těle,
2. vypište varování generátoru,
3. neprohlašujte omezení za vynucené,
4. případnou platformní výjimku dokumentujte.
