"""Replaces the student and creator posts with People / Life quotes.

Rohit narrowed the pillars to: people, life, entrepreneurship, psychology, deep understanding.
Wednesdays (were Students) and Fridays (were Creativity) become People posts.
The look of each date is kept, so the no-two-looks-in-a-row rule still holds.

Run:  python3 engine/revise_people.py     # writes tmp/batch3.json, tmp/rows3.json, updates ledger.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HT_PEOPLE = '#relationships #people #friendship #humanbehavior #hinglish #rohitkaperspective'
HT_LOVE = '#relationships #love #lettinggo #humanbehavior #hinglish #rohitkaperspective'

# date, TAG, pillar, quote (one {{punch}}), ask, send, hashtags
POSTS = [
 # ---- Wednesdays: friendship, family, how people treat each other ----
 ('2026-11-04','Friendship','People / friendship',
  'Dosti ladai se khatam nahi hoti. {{Khatam tab hoti hai jab dono ko farak padna band ho jaata hai.}}',
  'Kis dost se ab farak padna band ho gaya? Neeche likho.',
  'Save karo, aur aaj usse ek baar baat kar lo.', HT_PEOPLE),

 ('2026-11-11','People','People / boundaries',
  'Log tumse wahi behave karte hain {{jo tum ek baar chalne de dete ho.}}',
  'Kaun si cheez tumne chalne di thi? Comment mein likho.',
  'Save karo, aur agli baar wahin rok do.', HT_PEOPLE),

 ('2026-11-18','Family','People / family',
  'Ghar wale tumhari tareef dusron ke saamne karte hain, {{aur tumhare saamne sirf kami.}}',
  'Tumne ye kab notice kiya tha? Neeche batao.',
  'Save karo, aur us insaan ko bhejo jo yahi feel karta hai.', HT_PEOPLE),

 ('2026-11-25','People','People / giving',
  'Jo insaan sabke liye time nikalta hai, {{uske liye kisi ke paas time nahi hota.}}',
  'Tumhare liye kaun time nikalta hai? Neeche uska naam likho.',
  'Save karo, aur aaj usko time do.', HT_PEOPLE),

 ('2026-12-02','Habit','People / missing someone',
  'Kuch log tumhe miss nahi karte. {{Unhe bas tumhari aadat thi.}}',
  'Ye padh ke kiska naam aaya? Comment mein likho.',
  'Save kar lo, aur jab yaad aaye tab dobara padhna.', HT_PEOPLE),

 ('2026-12-09','Effort','People / one-sided effort',
  'Rishte baat band hone se nahi tootte. {{Tootte tab hain jab ek hi banda koshish karta rehta hai.}}',
  'Kis rishte mein tum akele koshish kar rahe ho? Neeche likho.',
  'Save karo, aur ek baar seedha pooch lo.', HT_PEOPLE),

 ('2026-12-16','Care','People / being seen',
  'Sabse achcha insaan wo hota hai jo tumhare "theek hoon" ko {{dusri baar poochta hai.}}',
  'Tumse dusri baar kaun poochta hai? Comment mein likho.',
  'Save karo, aur aaj kisi se dusri baar pooch lo.', HT_PEOPLE),

 ('2026-12-23','Trust','People / forgiveness',
  'Maaf kar dena aasan hai. {{Mushkil wahi bharosa wapas dena hai.}}',
  'Tumne kisko maaf kiya par bharosa wapas nahi kar paaye? Neeche likho.',
  'Save kar lo, aur agli baar khud se poocho ki kya chahiye.', HT_PEOPLE),

 ('2026-12-30','People','People / being remembered',
  'Log tumhe tab yaad karte hain jab kaam ho. {{Tum unhe tab yaad karte ho jab dard ho.}}',
  'Dard mein tum kiska naam sochte ho? Neeche likho.',
  'Save karo, aur aaj usko bina kaam ke message karo.', HT_PEOPLE),

 # ---- Fridays: love, loyalty, distance, letting go ----
 ('2026-11-06','Love','People / love',
  'Pyaar khatam nahi hota. {{Bas ek din tum uske liye ladna chhod dete ho.}}',
  'Tum kis baat ke liye ladna chhod chuke ho? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo abhi isse guzar raha hai.', HT_LOVE),

 ('2026-11-13','Sorry','People / patterns',
  'Jo baar baar sorry bolta hai par badalta kabhi nahi, {{uska sorry maafi nahi, permission hai.}}',
  'Kitni baar wahi sorry sun chuke ho? Neeche likho.',
  'Save karo, aur agli baar sorry nahi, badlaav maango.', HT_LOVE),

 ('2026-11-20','Distance','People / distance',
  'Door wo nahi jo shehar chhod ke chala gaya. {{Door wo hai jo isi shehar mein hai aur milta nahi.}}',
  'Kaun isi shehar mein hai par milta nahi? Comment mein likho.',
  'Save karo, aur aaj usko milne ka poochho.', HT_LOVE),

 ('2026-11-27','Tired','People / letting go',
  'Tum unhe chhodna nahi chahte the. {{Tum bas thak gaye the akele pakad ke rakhne se.}}',
  'Kis rishte mein tum akele pakde hue ho? Neeche likho.',
  'Save kar lo, aur jis din himmat aaye us din padhna.', HT_LOVE),

 ('2026-12-04','Unsaid','People / unsaid things',
  'Sabse zyada dard us baat ka hota hai {{jo kabhi kahi hi nahi gayi.}}',
  'Wo baat kya hai jo tum aaj tak nahi keh paaye? Comment mein likho.',
  'Save karo, aur aaj ek baat keh do.', HT_LOVE),

 ('2026-12-11','Silence','People / being ignored',
  'Ignore karna bhi ek jawab hai. {{Bas use samajhne mein thoda waqt lagta hai.}}',
  'Kiska jawab tum abhi tak wait kar rahe ho? Neeche likho.',
  'Save karo, aur ab wait karna band kar do.', HT_LOVE),

 ('2026-12-18','Friendship','People / one-sided friendship',
  'Jisko tum apna sabse achcha dost kehte ho, {{usko last message bhi tumne hi kiya tha.}}',
  'Check karo aur batao: last message kisne kiya tha? Neeche likho.',
  'Save karo, aur ye usko bhej do.', HT_PEOPLE),

 ('2026-12-25','Loyalty','People / loyalty',
  'Jo log tumhare bure waqt mein chup the, {{unhe achche waqt mein bolne ka haq nahi.}}',
  'Bure waqt mein tumhare saath kaun tha? Neeche uska naam likho.',
  'Save karo, aur aaj usko shukriya bol do.', HT_LOVE),

 ('2027-01-01','New year','People / distance',
  'Naya saal mubarak un logon ko bhi {{jinse ab baat nahi hoti.}}',
  'Kiska naam aaya? Comment mein likho.',
  'Save karo, aur aaj unme se ek ko message kar do.', HT_LOVE),
]


def main():
    ledger = json.loads((ROOT / 'ledger.json').read_text(encoding='utf-8'))
    by_date = {e['date']: e for e in ledger}

    batch, rows = [], []
    for date, tag, pillar, text, ask, send, tags in POSTS:
        old = by_date[date]
        plain = text.replace('{{', '').replace('}}', '')
        assert len(plain.split()) <= 24, f'{date}: too long'
        assert text.count('{{') == 1 and text.count('}}') == 1, f'{date}: punch braces'
        img = f'posts/rkp-{date}.png'
        num = f"{ledger.index(old) + 1:02d}"
        batch.append({'look': old['look'], 'tag': tag, 'num': num, 'text': text, 'out': img})
        caption = f'{plain}\n\n{ask}\n\n{send}\n\n{tags}'
        old.update(pillar=pillar, quote=plain, caption=caption, lang='hinglish', source='batch-2-people')
        rows.append({'date': date, 'quote': plain, 'caption': caption,
                     'url': 'https://raw.githubusercontent.com/rohitmudgill/rkp-posts/main/' + img})

    # Looks must still never repeat on consecutive days.
    for a, b in zip(ledger, ledger[1:]):
        assert a['look'] != b['look'], f"look repeats on {b['date']}"
    quotes = [e['quote'].lower() for e in ledger]
    assert len(set(quotes)) == len(quotes), 'duplicate quote in ledger'

    (ROOT / 'ledger.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp = ROOT / 'tmp'
    tmp.mkdir(exist_ok=True)
    (tmp / 'batch3.json').write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding='utf-8')
    (tmp / 'rows3.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{len(batch)} posts revised')


if __name__ == '__main__':
    main()
