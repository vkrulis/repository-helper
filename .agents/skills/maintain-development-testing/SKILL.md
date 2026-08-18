---
name: maintain-development-testing
description: Zavádí a udržuje bezpečný, vrstvený a frameworkově neutrální základ automatického testování a diagnostiky ve vývojovém repozitáři. Použijte při založení testovací capability, přidání workflow nebo regresního scénáře, bezpečné reprodukci vady, volbě testovacích dat či artefaktů nebo před zavedením testů do CI; nepoužívejte pro klientský projektový kontext ani k volbě frameworku bez znalosti cílové aplikace.
---

# Maintain Development Testing

## Postup

1. Přečtěte `docs/agent-context/development-testing-capability.md` a aktuální projektovou dokumentaci. Určete riziko, které má test ověřit; nejdříve zvolte nejnižší účinnou vrstvu.
2. Zachovejte nativní konvenci aplikace. Pokud test vyžaduje izolovaný balíček nebo pomocné nástroje, umístěte je do `toolkit/development/<test-suite>/` a popište jej v `docs/agent-context/testing.md`.
3. Rozlišujte scénář jako `smoke`, `workflow`, `regression`, `known-bug`, `probe` nebo `mutating`. Probe po zjištění buď odstraňte, nebo převeďte na malou reprodukci či regresi.
4. Založte testovací data s minimálním rozsahem a doloženým resetem. Credentials ukládejte jen do ignorovaného lokálního souboru; commitujte nejvýše `.env.example`.
5. Pro workflow testy centralizujte přihlášení, diagnostiku, síťové čekání a reprezentaci nestandardního UI do fixtures či pomocných modulů. Testujte uživatelské chování, ne implementační detaily.
6. Mutující scénář nespouštějte implicitně. Vyžadujte explicitní opt-in proměnnou, oddělené prostředí a resetovatelný stav.
7. Při selhání zachyťte přiměřené artefakty a před sdílením je zkontrolujte na secrets a osobní data. Do Git ani pracovního logu nevkládejte celé trace, screenshoty nebo produkční odpovědi.
8. Do CI zařaďte pouze stabilní nemutující scénáře s jasnými daty a opakovatelným výsledkem. Všechny ostatní nechte jako ručně spouštěné diagnostické nástroje.

## Kontrola

Zaznamenejte konkrétní příkazy projektu do `docs/agent-context/testing.md`. Po materiální změně použijte `maintain-work-log`; pro novou dlouhodobou strategii použijte `maintain-decision-records`.
