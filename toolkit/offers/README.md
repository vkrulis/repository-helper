# Nástroje nabídek

`offer_tools.py` vytváří kostru nabídky, validuje její manifest a publikovatelný HTML obsah a spouští lokální preview. Spouštějte jej z kořene klientského repozitáře:

```bash
python toolkit/offers/offer_tools.py init-offer --offer-id offer-2026-001 --project-slug proseat --offer-slug uvolnovani-vyroby --title "Uvolňování výroby"
python toolkit/offers/offer_tools.py validate --offer offer-2026-001
python toolkit/offers/offer_tools.py preview --offer offer-2026-001
```

Nástroj nic nepublikuje a nepracuje s Cloudflare ani GitHub credentials. Publikační kontrakt je v `docs/agent-context/client-offers-capability.md`.
