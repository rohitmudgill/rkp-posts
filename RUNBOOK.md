# RKP daily quote post: runbook

Goal: every run adds ONE new 1:1 Instagram quote post to the Metricool queue, to be published
at 18:00 IST on the next free date. The queue is the buffer: a missed run never causes a missed post.

## Fixed facts
- Metricool brand (blogId): 7387738 (Instagram account `rohitmudgill`), timezone Asia/Calcutta
- Post: network `instagram`, type `POST`, autoPublish true, isAiGenerated false
- Handle printed on every image: @rohitkaperspective (do not change)
- Public image URL: `https://raw.githubusercontent.com/<owner>/<repo>/main/posts/<file>.png`
- If ANY step fails, schedule nothing. Report the failure in the final message (and PushNotification if available).

## Steps
1. `add_repo` (access: push) for this repo, `cd` into it, `npm ci`.
2. Read `ledger.json` (every quote ever used). Never repeat a quote or a core idea from the last 60 entries.
3. Find the target date: call Metricool `getScheduledPosts` (today .. +45 days). Target = latest scheduled
   date + 1 day, 18:00 IST. No scheduled posts: tomorrow. If the latest scheduled date is more than
   30 days ahead, stop and report "buffer full" (do not pile up posts).
4. Pillar and language come from the weekday of the TARGET date:

   There are FIVE pillars and no others: people, life, entrepreneurship, psychology,
   deep understanding. Never write a post aimed only at students or exam aspirants, and
   never a post aimed only at creators or content makers. The audience is everyone.

   | Day | Format | Pillar | Language |
   |-----|--------|--------|----------|
   | Mon | CAROUSEL | A law from the 48 Laws of Power | Hinglish |
   | Tue | single | Psychology: anger, habits, why people react the way they do | English |
   | Wed | single | People: friendship, family, how people treat each other | Hinglish |
   | Thu | CAROUSEL | A named psychology law or effect | English |
   | Fri | single | People: love, loyalty, distance, letting go | Hinglish |
   | Sat | single | Life: time, regret, growing up, money, what matters later | Hinglish |
   | Sun | CAROUSEL | A Japanese or an Indian principle, alternating week by week | English |

   (English is 3 of 7 days, well above the 30% minimum.)

   A CAROUSEL is five slides: hook, the rule, why it works, how to use it, close.
   Slide 1's tag names the law or principle; the slides explain it in plain everyday words.
   Never copy a book's own sentences - name the law, then put the meaning in your own words.
   `engine/carousels.py` holds every carousel published so far: read it so a law is never
   repeated, and follow its shape to add a new one. Slide 1 keeps the date's look and
   slides 2-5 cycle through the remaining four, so the feed's colour rhythm is unchanged.
   Render with `node engine/render.mjs --batch tmp/cbatch.json`. In Metricool, send all five
   raw URLs in `media` in slide order, with one `mediaAltText` entry per slide.
5. Write 12 candidate quotes. Score each 1-5 on: recognition ("that is about me"), twist (a reversal
   or reframe in the second half), brevity, shareability ("I must send this to someone"),
   originality. Keep the best one only if its total is 20/25 or more, otherwise write 12 more.
6. The chosen quote must pass ALL of these:
   - At most 20 words (Hinglish: 22), at most 2 sentences.
   - A concrete situation or image beats an abstraction. No cliches ("believe in yourself",
     "hard work pays off", "time heals all", "be the change").
   - Natural Roman-script Hinglish for Hinglish days (not translated English).
   - Any psychology or business claim is defensible; hedge with "aksar" / "often" where needed.
     No invented statistics, no studies by name unless certain, no quotes attributed to real people.
   - Loneliness / pain posts end with recognition or relief, never despair. Nothing that
     encourages self-harm, shames a group, or gives medical or therapy advice.
7. Pick the look by tone (never the same look as either of the last two ledger entries):
   `red` call-out / anger, `blue` drive / ambition, `green` insight / relief,
   `white` quiet and heavy, `yellow` intellectual (best for English).
8. Write `tmp/spec.json`: `{"look":"...","tag":"SHORT TOPIC LABEL","num":"<ledger length + 1>","text":"... {{punch phrase}} ..."}`
   Wrap exactly ONE phrase (the punch) in `{{ }}`.
   Render: `node engine/render.mjs tmp/spec.json posts/rkp-<YYYY-MM-DD>.png`
   Output JSON must show `"fits": true` and `lines` of 7 or fewer, otherwise shorten the quote and re-render.
   Then open the PNG with Read and confirm nothing is clipped, no highlight hides letters, no one-word last line.
   Typography: use curly quotes ‘ ’ “ ” and the apostrophe ’ in the quote text, never straight ' or ". If the last line is a
   single word (an orphan like "first."), reword slightly and render again.
9. Caption (same language as the quote): 3 short blocks separated by blank lines:
   the quote restated or sharpened, one question that invites a comment, one save/send line.
   Then a blank line and 5-6 hashtags, always including `#rohitkaperspective`.
10. Append to `ledger.json`: `{"date","look","lang","pillar","quote","image","caption"}`.
    Commit ("post <date>: <3-word idea>") and `git push` to main.
11. Metricool `createScheduledPost` (blogId 7387738, date = target 18:00+05:30):
    `info` = `{"autoPublish":true,"descendants":[],"draft":false,"firstCommentText":"","hasNotReadNotes":false,
    "media":["<raw URL>"],"mediaAltText":["<quote>"],"providers":[{"network":"instagram"}],
    "publicationDate":{"dateTime":"<YYYY-MM-DDT18:00:00>","timezone":"Asia/Calcutta"},"shortener":false,
    "smartLinkData":{"ids":[]},"text":"<caption + hashtags>",
    "instagramData":{"type":"POST","collaborators":[],"showReelOnFeed":true,"isAiGenerated":false}}`
    Success = response media URL starts with `https://static.metricool.com/`. On a media error wait 60 s and retry once.
12. Final message, one short block: date, quote, look, pillar, planner link.

## Wording: deep idea, easy words
The quotes work like the big Instagram quote pages: a line a tired person understands in one read,
that still lands days later. Depth comes from the idea, never from the vocabulary.
- Everyday words only. No jargon: not "projection", "validation", "identity", "unhealed",
  "defence mechanism", "budgeted for", "capacity". If a 15-year-old would pause on a word, cut it.
- 8-18 words. Two short sentences: an ordinary setup, then the turn.
- Use a concrete detail from Indian daily life: 2 am messages, last seen, result day, relatives,
  a group photo, a price, a time table, a phone call home. A detail beats an adjective.
- The turn should name a feeling the reader has had but never put into words. If the second
  sentence only repeats the first, the quote is dead - rewrite it.
- No instructions inside the quote ("you should", "stop doing X"). Show, don't advise.
- Pain quotes end in recognition or relief, never despair.

## Voice bar (examples of the level to hit, not to reuse)
- "Kuch rishte tootte nahi. Bas dono taraf se message karna band ho jaata hai."
- "Topper ka time table copy karne se pehle uski neend bhi dekh lena."
- "Most of your anger is just sadness that got tired of being polite."
- "You check your phone that often because somewhere you are still waiting for one name."
- "A place that calls rest laziness will call burnout hard work."
