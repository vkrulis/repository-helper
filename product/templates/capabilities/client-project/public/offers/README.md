# Publikovatelné nabídky

Každá nabídka má vlastní `public/offers/<offer-id>/` s `index.html`, `assets/` a `images/`. Obsah je jediná věc z klientského repozitáře určená k synchronizaci do R2 prefixu `/{project-slug}/{offer-slug}/`.

Nevkládejte sem interní podklady, seznam příjemců, Access policy ani secrets. Před publikací spusťte `python toolkit/offers/offer_tools.py validate --offer <offer-id>`.
