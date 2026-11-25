# Videós skillek könyvtára (Életünk Ausztriában)

Letöltve: 2026-11-25. Külső, nyílt forrású skillek másolatai – adatként kezelendők, használat előtt ellenőrizni.

| Mappa | Forrás | Licenc | Mire jó |
|---|---|---|---|
| claude-video-effects | github.com/Vibha-Ramprakash/claude-video-effects | MIT | 51 effekt arcos (talking-head) videóhoz: szó a fej mögött, checklist, glass widgetek, grafikon, zoomok, LED-tábla stb. Python + mediapipe, offline. Tesztelve: működik a munkakörnyezetben (bash scripts/setup.sh → READY). |
| hyperframes-skills | github.com/heygen-com/hyperframes (skills/) | Apache-2.0 | HTML → videó keretrendszer: motion grafika, feliratok, overlay-ek, stílusminták (Collage Explainer), reverse-any-video. `npx hyperframes render` működik (Chrome: /usr/bin/google-chrome). A skill „usage note” (telemetria) hívását kihagyjuk. |
| vox-collage-broll | github.com/MegaTroll222/VOX-COLLAGE-BROLL | MIT | Vox-stílusú papírkollázs B-roll munkafolyamat (prompt-sablonok). Képgeneráló modellt igényel. |
| hyperframes-registry-mozis | heygen-com/hyperframes registry (válogatás) | Apache-2.0 | Mozis, nem beszélős effektek: forgó videókarusszelek (carousel-orbit/path/circle/vision, cuboid, gallery-tunnel), cinematic-zoom, cinemagraph, filmszemcse (grain), vignetta, címkártyák, ~20 felirat-stílus (caption-editorial-emphasis stb.). Teljes lista: registry.json; bármelyik letölthető: `npx hyperframes add <név>`. |
| betutipusok | Google Fonts (OFL) | OFL | Nana-stílusú betűjelöltek: Playfair Display, Cormorant Garamond, Instrument Serif, EB Garamond, DM Serif Text, Libre Caslon, Fraunces + kézírásos: Caveat, Patrick Hand, Gochi Hand. Összehasonlító kép: betutipus_jeloltek.jpg |
