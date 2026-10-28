# TataGo social – procedura giornaliera

Obiettivo: far crescere i follower di @tatago.it tra **babysitter che cercano lavoro** e **famiglie che cercano una babysitter**.
Ogni giorno: **6 post + 4 storie** su Instagram, pubblicati in automatico tramite Metricool (brand id `7711121`, timezone Europe/Rome).

## Calendario del giorno
| file | tipo | ora | pubblico |
|---|---|---|---|
| 01-post-0800 | post | 08:00 | babysitter |
| 02-story-0930 | storia | 09:30 | famiglie |
| 03-post-1100 | post | 11:00 | famiglie |
| 04-story-1230 | storia | 12:30 | babysitter |
| 05-post-1300 | post | 13:00 | babysitter |
| 06-post-1600 | post | 16:00 | famiglie |
| 07-story-1700 | storia | 17:00 | famiglie |
| 08-post-1800 | post | 18:00 | babysitter |
| 09-story-1930 | storia | 19:30 | babysitter |
| 10-post-2100 | post | 21:00 | famiglie |

Pubblico: 3 post + 2 storie per le babysitter, 3 post + 2 storie per le famiglie. Un giorno sì e uno no inverti i pubblici della tabella.

## Regole sui testi
- Italiano, tono caldo e diretto, frasi brevi. Titoli max ~8 parole, sottotitolo max ~15.
- **Mai ripetere** titoli, sottotitoli o didascalie già usati: controllare `history.json` prima di scrivere.
- Variare gli angoli: momenti di vita reale (imprevisti, serate, rientro al lavoro, estate, feste, malattie dei bimbi), vantaggi per le tate (flessibilità, zona, studenti, arrotondare, esperienza), fiducia/verifica, consigli utili, domande che invitano a commentare, ricorrenze del calendario.
- Non inventare funzioni: TataGo mette in contatto famiglie e babysitter con profili verificati; **non** gestisce pagamenti né prenotazioni (tariffe e accordi si decidono direttamente). App Android scaricabile da tatago.it; registrazione su tatago.it.
- Didascalia: 3–6 righe, emoji con misura, chiusura con "🔗 … tatago.it – link in bio", 6–8 hashtag pertinenti al pubblico.
- Inviti all'azione alternati: "Iscriviti su tatago.it", "Crea il tuo profilo", "Trova la tua tata", "Scarica l'app da tatago.it", ecc.

## Grafica
- `layout`: `image` (illustrazione grande) o `quote` (frase in card + illustrazione tonda). Alternarli.
- `image`: una tra `assets/` → `tata-verificata.png`, `gioco.png`, `famiglia.png`, `famiglia-logo.png`. Non usare la stessa per due contenuti consecutivi.
- Badge colore: famiglie verde, babysitter blu (automatico da `audience`).

## Passi
1. `npm i` (font Poppins), poi crea `days/AAAA-MM-GG/spec.json` (vedi campi in `render.py`, aggiungi `time` e `caption`).
2. `python3 render.py days/AAAA-MM-GG/spec.json` e guarda ogni jpg: niente testo tagliato o sovrapposto.
3. Aggiungi i titoli usati a `history.json`, commit e push su `main`.
4. Verifica che ogni immagine risponda 200 su `https://raw.githubusercontent.com/vikscianna/tatago-social/main/days/AAAA-MM-GG/<file>.jpg`.
5. Per ogni elemento `createScheduledPost` su Metricool: `draft:false`, `autoPublish:true`, `providers:[{network:instagram}]`, `instagramData.type` POST o STORY; le storie senza `text`.
6. Controlla con `getScheduledPosts` che i 5 contenuti risultino programmati.
