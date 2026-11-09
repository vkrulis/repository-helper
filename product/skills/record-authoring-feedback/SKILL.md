---
name: record-authoring-feedback
description: Zapíše nebo ověří strukturovaný Authoring Feedback Event pro skutečné použití FCL capability v klientském projektu. Použij při smysluplném checkpointu nebo dokončení authoringového běhu; nepoužívej pouhé načtení skillu jako důkaz použití.
---

# Record authoring feedback

Tato dovednost je společný zapisovací adaptér Repository Foundation. Význam eventu,
identitu capability a počítání určuje kontrakt FCL `authoring-feedback-event-v1`;
vrstvové produkty dodávají pouze své feedback profily a doménovou interpretaci.

1. Urči klientský projekt, jeden stabilní `run_id` a účel běhu. Odkazuj na existující
   zadání, Issue, Epic, Session, Checkpoint, capability lock, výstupy a validace;
   nevkládej do eventu celé chaty, prompty, secrets ani produkční data.
2. Rozliš `selected`, `loaded`, `executed`, `validated` a `rated`. `loaded` není
   skutečné použití. Jeden logical use stejné verze a role v jednom runu eviduj jednou;
   retry patří do `retry_count`, ne do dalšího usage.
3. Chybu připiš routingu, guidance, toolu, hostu, vstupu nebo vykonavateli jen s
   doloženou evidencí. Jinak použij `unknown`. Uveď, kdo chybu zjistil a kdo ji opravil;
   recovered error je samostatný pozitivní signál diagnostické capability.
4. Slepé cesty popiš pouze pozorovatelným krokem, důvodem opuštění a náhradou.
   Nezapisuj skryté uvažování.
5. Lidské hodnocení 1–5 žádej nepovinně po smysluplném celku, ne po každém tool callu.
   Neodpovězení neblokuje dokončení; zapiš `not_provided`. Inference z běžného textu
   není `human_explicit` hodnocení.
6. Event nejprve ověř a poté jej append-only zapiš nástrojem:

```powershell
python tools/authoring-feedback/authoring_feedback.py validate-event --event <event.json>
python tools/authoring-feedback/authoring_feedback.py record <projekt> --event <event.json>
python tools/authoring-feedback/authoring_feedback.py validate <projekt>
```

Pro pravidelné read-only vyhodnocení použij `scan`. Agregát je odvozený report, ne
autorita klientského projektu ani povolení měnit produktovou skill.

```powershell
python tools/authoring-feedback/authoring_feedback.py scan <projekt>
```

Pokud cílový host nemá zapisovací adaptér, připrav validní event jako návrh a transparentně
uveď, že nebyl uložen. Nevytvářej náhradní `0.6`; Repository Foundation je mimo A–E / 1–6.
