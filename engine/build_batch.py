"""Builds the render batch and ledger rows for a block of dated quote posts.

Each POSTS entry: (date, look, tag, lang, pillar, text, ask, send, tagset)
  text  - the quote, with the punch phrase wrapped in {{ }}
  ask   - the caption's question line
  send  - the caption's save/send line

Run:  python3 engine/build_batch.py           # writes tmp/batch.json and tmp/rows.json
"""
import json
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HT = {
    'psych':    '#psychology #selfawareness #emotionalintelligence #deepthoughts #mentalclarity #rohitkaperspective',
    'students': '#students #studymotivation #exams #studentlife #hinglish #rohitkaperspective',
    'society':  '#society #socialmedia #hustleculture #deepthoughts #lifelessons #rohitkaperspective',
    'creative': '#creativity #creatorlife #consistency #contentcreator #hinglish #rohitkaperspective',
    'life':     '#life #lifelessons #relationships #growingup #hinglish #rohitkaperspective',
    'deep':     '#psychology #loneliness #selfworth #deepthoughts #overthinking #rohitkaperspective',
    'business': '#entrepreneurship #business #startup #sales #mindset #rohitkaperspective',
}

# date, look, TAG, lang, pillar, quote, ask, send, hashtag set
POSTS = [
 # ---------- November ----------
 ('2026-11-03','yellow','Psychology','english','Psychology / social energy',
  'You are not bad at talking to people. You are tired of {{being the one who starts.}}',
  'Who is the one you always message first? Tell us below.',
  'Save this, and send it to the friend who always texts first.', 'psych'),

 ('2026-11-04','blue','Students','hinglish','Students / fear of result',
  'Padhai se dar nahi lagta. Dar isse lagta hai ki {{poori mehnat ke baad bhi kam niklega.}}',
  'Tumhara sabse bada exam wala dar kya hai? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo abhi padh raha hai.', 'students'),

 ('2026-11-05','white','Society','english','Society / social media',
  'Everyone looks happy at 10 pm on Instagram. {{Nobody is posting at 3 am.}}',
  'What is the one thing you have never posted about? Comment below.',
  'Save this for the next time the feed makes you feel behind.', 'society'),

 ('2026-11-06','green','Creativity','hinglish','Creativity / starting',
  'Pehla video bura hi banega. {{Wo bura video hi tumhara course hai.}}',
  'Tumhara pehla kaam kitna bura tha? Neeche batao.',
  'Save kar lo, aur us dost ko bhejo jo "ready" hone ka wait kar raha hai.', 'creative'),

 ('2026-11-07','white','Life','hinglish','Life / friendship',
  'Kuch rishte tootte nahi. Bas {{dono taraf se message karna band ho jaata hai.}}',
  'Kiska naam abhi dimaag mein aaya? Comment mein likho.',
  'Save karo, aur aaj usko ek message bhej do.', 'life'),

 ('2026-11-08','green','Loneliness','english','Deep psychology / loneliness',
  'Loneliness is not being alone. It is being around people and {{still editing yourself.}}',
  'Where do you feel most like yourself? Tell us below.',
  'Save this for the next room where you have to shrink.', 'deep'),

 ('2026-11-09','blue','Business','hinglish','Entrepreneurship / customers',
  'Customer ko tumhara passion nahi dikhta. {{Use sirf apni problem dikhti hai.}}',
  'Tumhara customer asli mein kya kharid raha hai? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo apna business shuru kar raha hai.', 'business'),

 ('2026-11-10','yellow','Psychology','english','Psychology / closure',
  'The people who hurt you rarely remember it. That is why {{you have to stop waiting for the apology.}}',
  'What are you still waiting to hear? Comment below.',
  'Save this for the day the waiting gets heavy.', 'psych'),

 ('2026-11-11','red','Students','hinglish','Students / comparison',
  'Topper ka time table copy karne se pehle {{uski neend bhi dekh lena.}}',
  'Tum kiska routine copy karne ki koshish kar rahe ho? Neeche likho.',
  'Save karo, aur us dost ko bhejo jo khud ko compare kar raha hai.', 'students'),

 ('2026-11-12','white','Society','english','Society / using people',
  'We call it networking now. {{It used to be called using people.}}',
  'When did you last reach out with nothing to ask for? Tell us below.',
  'Save this, and message one person today for no reason.', 'society'),

 ('2026-11-13','green','Creativity','hinglish','Creativity / fear of judgement',
  'Log tumhe judge nahi kar rahe. {{Unhe apne hi post ka like count dekhna hai.}}',
  'Kaun sa kaam tum dar ke maare post nahi kar rahe? Comment mein likho.',
  'Save kar lo, aur aaj wo cheez post kar do.', 'creative'),

 ('2026-11-14','white','Life','hinglish','Life / parents',
  'Jab tak maa-baap hain, tumhare paas ek ghar hai. {{Uske baad sirf ek address rehta hai.}}',
  'Aaj ghar baat hui? Comment mein ek haan likh do.',
  'Save karo, aur abhi ghar phone laga lo.', 'life'),

 ('2026-11-15','yellow','Waiting','english','Deep psychology / attachment',
  'You check your phone that often because somewhere {{you are still waiting for one name.}}',
  'Whose name did you just think of? Tell us below.',
  'Save this for the night the waiting feels loud.', 'deep'),

 ('2026-11-16','blue','Business','hinglish','Entrepreneurship / systems',
  'Jo business sirf tumhare uthne se chalta hai, {{wo business nahi, naukri hai.}}',
  'Tumhare business ka kaun sa kaam tumhare bina rukta hai? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo har kaam khud karta hai.', 'business'),

 ('2026-11-17','green','Psychology','english','Psychology / missing people',
  'You do not miss them. You miss {{who you got to be around them.}}',
  'Who were you when you were happiest? Comment below.',
  'Save this, and send it to someone healing from a goodbye.', 'psych'),

 ('2026-11-18','red','Students','hinglish','Students / learning',
  'Tum slow nahi ho. {{Tumhe kisi ne kabhi bataya hi nahi ki padhna kaise hai.}}',
  'Kaun si cheez samajh aane mein tumhe sabse zyada time laga? Neeche likho.',
  'Save karo, aur us student ko bhejo jo khud ko dumb samajhta hai.', 'students'),

 ('2026-11-19','white','Society','english','Society / relatives',
  'Relatives do not ask about your salary to help. {{They ask to settle a number in their head.}}',
  'What is the question you are tired of being asked? Tell us below.',
  'Save this before the next family function.', 'society'),

 ('2026-11-20','blue','Creativity','hinglish','Creativity / consistency',
  'Idea chori nahi hota. {{Jeetta wahi hai jo use roz banata hai.}}',
  'Kaun sa idea tum 6 mahine se soch rahe ho? Comment mein likho.',
  'Save kar lo, aur aaj uska pehla step kar lo.', 'creative'),

 ('2026-11-21','green','Life','hinglish','Life / childhood',
  'Bachpan ka aakhri din kisi ko yaad nahi. {{Khelte khelte bas ek din khel khatam ho gaya.}}',
  'Tumhara last wala favourite khel kaun sa tha? Neeche likho.',
  'Save karo, aur bachpan wale dost ko bhej do.', 'life'),

 ('2026-11-22','yellow','Self-worth','english','Deep psychology / self-worth',
  'You learned to be useful because {{you were not sure you were enough on your own.}}',
  'When did you last say no without a reason? Tell us below.',
  'Save this for the next time you say yes out of fear.', 'deep'),

 ('2026-11-23','blue','Business','hinglish','Entrepreneurship / first money',
  'Pehla paisa sabse chhota hota hai {{aur sabse zyada sach bolta hai.}}',
  'Tumhari pehli kamai kitni thi? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo abhi shuru kar raha hai.', 'business'),

 ('2026-11-24','red','Anger','english','Psychology / anger',
  'Most of your anger is just {{sadness that got tired of being polite.}}',
  'What are you actually sad about? Comment below.',
  'Save this for the next time you snap at someone.', 'psych'),

 ('2026-11-25','white','Students','hinglish','Students / family',
  'Result wale din pata chalta hai ki ghar mein kisko tumse pyaar tha, {{aur kisko tumhare marks se.}}',
  'Result wale din tumhe sabse pehle kisne call kiya tha? Neeche likho.',
  'Save karo, aur us insaan ko bhejo jo har result pe tumhare saath tha.', 'students'),

 ('2026-11-26','yellow','Society','english','Society / hustle culture',
  'A place that calls rest laziness {{will call burnout hard work.}}',
  'When did you last take a day off without guilt? Tell us below.',
  'Save this, and send it to the friend who never stops.', 'society'),

 ('2026-11-27','green','Creativity','hinglish','Creativity / taste gap',
  'Tumhari nazar tumhare haath se aage hai. {{Isiliye apna kaam bura lagta hai.}}',
  'Tumhe apne kaam mein kya sabse pehle kharab lagta hai? Comment mein likho.',
  'Save kar lo, aur agla kaam waise hi post kar do.', 'creative'),

 ('2026-11-28','white','Life','hinglish','Life / caretakers',
  'Jo log sabko sambhaal lete hain, {{unse koi nahi poochta ki wo theek hain ya nahi.}}',
  'Tumhare ghar mein wo kaun hai? Neeche uska naam likho.',
  'Save karo, aur aaj usse pooch lo ki wo kaisa hai.', 'life'),

 ('2026-11-29','green','Quiet','english','Deep psychology / silence',
  'The quietest people are not calm. They just {{stopped expecting anyone to ask twice.}}',
  'Who asks you twice? Tell us below.',
  'Save this, and ask someone twice today.', 'deep'),

 ('2026-11-30','blue','Business','hinglish','Entrepreneurship / feedback',
  'Free mein sab taarif karenge. {{Asli feedback wahi deta hai jo paisa deta hai.}}',
  'Tumhe pehli baar kisne paisa diya tha? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo abhi tak free mein kaam kar raha hai.', 'business'),

 # ---------- December ----------
 ('2026-12-01','yellow','Psychology','english','Psychology / being judged',
  'You keep explaining yourself {{to people who already decided what you are.}}',
  'Who have you stopped explaining yourself to? Comment below.',
  'Save this for the next time you over-explain.', 'psych'),

 ('2026-12-02','red','Students','hinglish','Students / guilt',
  'Jo subah 5 baje uthne se nahi hua, {{wo raat 2 baje guilt se bhi nahi hoga.}}',
  'Tum raat ko kis cheez ka guilt leke sote ho? Neeche likho.',
  'Save karo, aur aaj time pe so jao.', 'students'),

 ('2026-12-03','white','Society','english','Society / adulthood',
  'Nobody tells you that most adults are {{just older kids with better excuses.}}',
  'When did you realise the adults were figuring it out too? Tell us below.',
  'Save this for the day you feel behind everyone.', 'society'),

 ('2026-12-04','blue','Creativity','hinglish','Creativity / doing vs thinking',
  'Roz banane wala har hafte seekhta hai. {{Soch ke rakhne wala saal bhar wahi rehta hai.}}',
  'Tumne is hafte kya banaya? Comment mein likho.',
  'Save kar lo, aur aaj kuch chhota bana do.', 'creative'),

 ('2026-12-05','green','Life','hinglish','Life / money',
  'Paisa aane ke baad pata chalta hai ki {{jo cheezein chahiye thi, wo kabhi bikti hi nahi thi.}}',
  'Tumhe abhi sabse zyada kis cheez ki kami lagti hai? Neeche likho.',
  'Save karo, aur ek call aaj us insaan ko karo.', 'life'),

 ('2026-12-06','yellow','Fear','english','Deep psychology / fear of failing',
  'You are not scared of failing. You are scared of {{people finally being right about you.}}',
  'Whose opinion are you still carrying? Comment below.',
  'Save this for the day before you try something big.', 'deep'),

 ('2026-12-07','blue','Business','hinglish','Entrepreneurship / follow-up',
  'Best idea wala nahi jeetta. {{Jeetta wo hai jo follow-up karta rehta hai.}}',
  'Tumne last follow-up kab kiya tha? Comment mein likho.',
  'Save kar lo, aur aaj do logon ko follow-up message bhejo.', 'business'),

 ('2026-12-08','white','Psychology','english','Psychology / rest',
  'The habit you call lazy is often {{a break your body took without asking.}}',
  'What are you tired of, really? Tell us below.',
  'Save this for the next time you call yourself lazy.', 'psych'),

 ('2026-12-09','green','Students','hinglish','Students / starting',
  'Syllabus kabhi khatam nahi lagta. {{Bas ek din himmat aa jaati hai shuru karne ki.}}',
  'Tum kis chapter se bhaag rahe ho? Neeche likho.',
  'Save karo, aur aaj sirf 20 minute us chapter ko do.', 'students'),

 ('2026-12-10','red','Society','english','Society / politeness',
  'You were taught to be polite. {{You were never taught what to do when polite does not work.}}',
  'Where do you need to stop being polite? Comment below.',
  'Save this for the next conversation you keep avoiding.', 'society'),

 ('2026-12-11','yellow','Creativity','hinglish','Creativity / fear of being seen',
  'Sabse bada creative block ye dar hai ki {{log tumhe try karte hue dekh lenge.}}',
  'Kaun sa kaam tum chup chaap kar rahe ho? Comment mein likho.',
  'Save kar lo, aur aaj use dikha do.', 'creative'),

 ('2026-12-12','white','Life','hinglish','Life / old friends',
  'Purane dost se baat karke lagta hai kuch nahi badla. {{Phone rakhte hi pata chalta hai sab badal gaya.}}',
  'Kis dost se sabse zyada time ho gaya? Neeche naam likho.',
  'Save karo, aur aaj usko call kar lo.', 'life'),

 ('2026-12-13','green','Tired','english','Deep psychology / being the strong one',
  'Some nights you are not sad. You are just {{tired of being the strong one.}}',
  'Who checks on you? Tell us below.',
  'Save this, and send it to the person everyone leans on.', 'deep'),

 ('2026-12-14','blue','Business','hinglish','Entrepreneurship / giving up',
  'Business paisa khatam hone se band nahi hota. {{Ummeed pehle khatam hoti hai.}}',
  'Tumne kaun sa kaam chhodne se pehle rok liya tha? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo abhi haar maan raha hai.', 'business'),

 ('2026-12-15','yellow','Psychology','english','Psychology / delayed reactions',
  'You are not overreacting. {{You reacted late, to something old.}}',
  'What small thing set you off recently? Comment below.',
  'Save this for the next time someone calls you too sensitive.', 'psych'),

 ('2026-12-16','red','Students','hinglish','Students / comparison',
  'Doosron ke notes maang lo. {{Unki speed mat maango.}}',
  'Tum kiski speed se khud ko tol rahe ho? Neeche likho.',
  'Save karo, aur us dost ko bhejo jo khud ko peeche samajh raha hai.', 'students'),

 ('2026-12-17','white','Society','english','Society / money talk',
  'People who are at peace with money rarely talk about it. {{People who are scared of it never stop.}}',
  'Who taught you how to think about money? Tell us below.',
  'Save this for the next room full of numbers.', 'society'),

 ('2026-12-18','green','Creativity','hinglish','Creativity / finding talent',
  'Jo kaam tum free mein 2 ghante kar lete ho, {{wahi tumhara asli talent hai.}}',
  'Wo kaam kaun sa hai? Comment mein likho.',
  'Save kar lo, aur us dost ko bhejo jo apna rasta dhoond raha hai.', 'creative'),

 ('2026-12-19','white','Life','hinglish','Life / drifting apart',
  'Jisse roz milte the usse ab saal mein ek baar milte ho. {{Ye kisi ne decide nahi kiya tha.}}',
  'Kiske saath aisa hua? Neeche naam likho.',
  'Save karo, aur aaj ek purani baat chher do.', 'life'),

 ('2026-12-20','yellow','Kindness','english','Deep psychology / kindness',
  'You remember every small kindness {{because you were not expecting any.}}',
  'Which small kindness do you still remember? Tell us below.',
  'Save this, and do one small thing for someone today.', 'deep'),

 ('2026-12-21','blue','Business','hinglish','Entrepreneurship / selling',
  'Jo cheez tum bech nahi paa rahe, usme problem aksar product mein nahi, {{tumhare dar mein hoti hai.}}',
  'Tumhe sabse zyada dar kis cheez se lagta hai: poochne se ya sunne se? Comment mein likho.',
  'Save kar lo, aur aaj ek insaan ko offer bhej do.', 'business'),

 ('2026-12-22','green','Psychology','english','Psychology / conflict',
  'You forgive fast because {{you are scared of the silence that comes after a fight.}}',
  'What do you do when a room goes quiet? Comment below.',
  'Save this for the next argument you want to rush.', 'psych'),

 ('2026-12-23','red','Students','hinglish','Students / family pressure',
  'Backlog se zyada bhaari {{wo message hota hai jo tum ghar nahi bhej paa rahe.}}',
  'Tum ghar se kya chhupa rahe ho? Neeche likho.',
  'Save karo, aur aaj ek sach bata do.', 'students'),

 ('2026-12-24','white','Society','english','Society / festivals',
  'Festivals show you who calls because they want to, {{and who calls because it is the date.}}',
  'Who called you first last festival? Tell us below.',
  'Save this, and call the person you actually miss.', 'society'),

 ('2026-12-25','yellow','Creativity','hinglish','Creativity / perfectionism',
  'Perfect hone ka wait mat karo. {{Adhoora kaam bhi kisi ki raat bana deta hai.}}',
  'Kaun sa kaam tumhare drafts mein pada hai? Comment mein likho.',
  'Save kar lo, aur aaj use publish kar do.', 'creative'),

 ('2026-12-26','green','Life','hinglish','Life / saying yes',
  'Zindagi ki sabse mehngi haan {{wo hoti hai jo dar ke maare boli jaati hai.}}',
  'Kis haan ka tumhe abhi tak afsos hai? Neeche likho.',
  'Save karo, aur agli baar sochne ka time maang lo.', 'life'),

 ('2026-12-27','white','Healing','english','Deep psychology / healing',
  'Healing is boring. It is the same small choice, {{on a day no one is watching.}}',
  'What is your small boring choice? Tell us below.',
  'Save this for a day that feels like nothing changed.', 'deep'),

 ('2026-12-28','blue','Business','hinglish','Entrepreneurship / learning',
  'Saal bhar seekhne se kuch nahi hota. {{Ek baar bech ke dekho, poora syllabus samajh aa jaayega.}}',
  'Tumne aaj tak kya becha hai? Comment mein likho.',
  'Save kar lo, aur is hafte ek cheez bech ke dekho.', 'business'),

 ('2026-12-29','red','Psychology','english','Psychology / being heard',
  'The loudest person in the room is often {{the one who was never heard at home.}}',
  'Who listened to you first? Comment below.',
  'Save this, and listen a little longer today.', 'psych'),

 ('2026-12-30','green','Students','hinglish','Students / career',
  'Career wo hai jisme tum {{10 saal ke boring din bhi kaat sako.}}',
  'Tumhara wo kaam kaun sa hai? Neeche likho.',
  'Save karo, aur us dost ko bhejo jo career confuse hai.', 'students'),

 ('2026-12-31','yellow','Society','english','Society / year end',
  'Every year ends with a list of things you survived, {{not the list you planned.}}',
  'What did you survive this year? Tell us below.',
  'Save this, and read it again next December.', 'society'),

 # ---------- January ----------
 ('2027-01-01','blue','Creativity','hinglish','Creativity / new year',
  'Saal resolution se nahi badalta. {{Us ek kaam se badalta hai jo tum 2 January ko bhi karte ho.}}',
  'Tumhara wo ek kaam kya hai? Comment mein likho.',
  'Save kar lo, aur 2 January ko yaad se karo.', 'creative'),
]


def main():
    start_num = len(json.loads((ROOT / 'ledger.json').read_text(encoding='utf-8')))

    # No two consecutive posts share a look.
    for a, b in zip(POSTS, POSTS[1:]):
        assert a[1] != b[1], f'look repeats on {b[0]}'

    # Dates must be one per day, with no gaps.
    for a, b in zip(POSTS, POSTS[1:]):
        d0 = datetime.date.fromisoformat(a[0])
        d1 = datetime.date.fromisoformat(b[0])
        assert d1 - d0 == datetime.timedelta(days=1), f'gap before {b[0]}'

    batch, rows = [], []
    for i, (date, look, tag, lang, pillar, text, ask, send, tagset) in enumerate(POSTS):
        plain = text.replace('{{', '').replace('}}', '')
        words = len(plain.split())
        assert words <= 24, f'{date}: {words} words'
        assert text.count('{{') == 1 and text.count('}}') == 1, f'{date}: punch braces'
        img = f'posts/rkp-{date}.png'
        batch.append({'look': look, 'tag': tag, 'num': f'{start_num + i + 1:02d}',
                      'text': text, 'out': img})
        rows.append({'date': date, 'look': look, 'lang': lang, 'pillar': pillar,
                     'quote': plain, 'image': img,
                     'caption': f'{plain}\n\n{ask}\n\n{send}\n\n{HT[tagset]}',
                     'source': 'batch-2'})

    tmp = ROOT / 'tmp'
    tmp.mkdir(exist_ok=True)
    (tmp / 'batch.json').write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding='utf-8')
    (tmp / 'rows.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{len(batch)} posts, {POSTS[0][0]} .. {POSTS[-1][0]}, numbers from {start_num + 1}')


if __name__ == '__main__':
    main()
