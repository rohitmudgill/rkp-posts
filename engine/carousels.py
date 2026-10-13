"""Carousel posts: one law or principle broken across five slides.

Slide 1 hooks, 2-4 explain (rule / why / how), 5 closes with the call to action.
Slide 1 keeps the date's existing look so the feed's colour rhythm is unchanged;
slides 2-5 cycle through the remaining four looks.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOOKS = ['red', 'white', 'blue', 'green', 'yellow']
SLIDE_TAGS = [None, 'The rule', 'Why it works', 'How to use it', 'Rohit Ka Perspective']
FOOTERS = ['SWIPE →', '1 / 3', '2 / 3', '3 / 3', 'SAVE + SHARE']

HT = {
 'power':  '#48lawsofpower #power #strategy #mindset #psychology #rohitkaperspective',
 'psych':  '#psychology #mentalmodels #humanbehavior #selfawareness #deepthoughts #rohitkaperspective',
 'japan':  '#japanesephilosophy #kaizen #mindset #discipline #lifelessons #rohitkaperspective',
 'india':  '#chanakyaniti #bhagavadgita #indianwisdom #philosophy #lifelessons #rohitkaperspective',
}

# date, metricool id, uuid, principle name, language, source, [5 slide texts], ask, send
DATA = [
 ('2026-10-15', '394384607', '-7292273234887618827', 'Zeigarnik Effect', 'english', 'psych', [
   'Your brain refuses to forget {{one thing you left unfinished.}}',
   'An unfinished task stays active in your head. {{A finished one is dropped within minutes.}}',
   'The mind keeps a loop open until it closes. {{That is why you remember the work you avoided.}}',
   'Do not plan the task. Start it for ten minutes. {{The open loop will drag you back to finish.}}',
   'Tonight, start it for ten minutes. {{Your brain will handle the rest.}}'],
  'What have you been avoiding for weeks? Comment below.',
  'Save this, and send it to someone stuck at the starting line.'),

 ('2026-10-18', '394384992', '-2881394355263290561', 'Kaizen', 'hinglish', 'japan', [
   'Japan ne ek chhote se rule se {{poori duniya ko peeche chhod diya.}}',
   'Kaizen matlab roz sirf 1% behtar. {{Itna chhota ki mana karne ka bahana hi na bache.}}',
   'Bade target dar paida karte hain. {{Chhote kaam bas shuru ho jaate hain.}}',
   'Aaj poora chapter mat padho. {{Ek page padho. Kal phir ek page.}}',
   'Ek saal baad wahi 1% {{tumhe pehchan mein nahi aayega.}}'],
  'Tumhara aaj ka 1% kya hai? Neeche likho.',
  'Save kar lo, aur us dost ko bhejo jo har baar bada plan banake chhod deta hai.'),

 ('2026-10-19', '394385052', '1940865422475807346', 'Law 1 · Power', 'hinglish', 'power', [
   'Boss ko galat sabit karke tum sahi ban jaoge. {{Aur promotion list se bahar bhi.}}',
   '48 Laws ka pehla law: upar waale ko kabhi apne se chhota mat dikhao. {{Unka dar tumhari kabiliyat se bada hota hai.}}',
   'Log talent se nahi darte. {{Wo apni jagah chhinne ke dar se darte hain.}}',
   'Idea apna do, credit unka rehne do. {{Tumhe kursi nahi, access chahiye.}}',
   'Chamakna zaroori hai. {{Par kiske saamne, ye tum decide karo.}}'],
  'Tumne kab sahi hoke bhi nuksaan uthaya? Comment mein likho.',
  'Save kar lo, aur office wale dost ko bhej do.'),

 ('2026-10-22', '394385239', '-5564470989878702490', 'Ben Franklin Effect', 'english', 'psych', [
   'There is a way to make someone {{who dislikes you start liking you.}}',
   'Ask them for a small favour. {{Not a big one. Small enough that they say yes.}}',
   'The mind hates contradiction. {{Having helped you, it decides you must be worth helping.}}',
   'Borrow a book. Ask for one piece of advice. {{Then thank them properly and leave.}}',
   'People like you more {{after they do you a favour, not before.}}'],
  'Who would you try this on? Comment below.',
  'Save this for the next cold room you walk into.'),

 ('2026-10-25', '394385475', '-558116601599737431', 'Chanakya Niti', 'hinglish', 'india', [
   'Chanakya ne 2300 saal pehle likha tha: {{apni kamzori kisi ko mat batao.}}',
   'Jo tum dukh mein bol dete ho, {{log use sunte nahi, yaad rakhte hain.}}',
   'Sympathy ek din rehti hai. {{Jaankari zindagi bhar rehti hai.}}',
   'Problem batao, par apna dar mat batao. {{Madad maango, par apni haalat mat kholo.}}',
   'Jo sab kuch bata deta hai, {{uske paas bachane ko kuch nahi bachta.}}'],
  'Kis baat ka tumhe batakar afsos hua? Neeche likho.',
  'Save karo. Agli baar bolne se pehle ek second ruk jaana.'),

 ('2026-10-26', '394385535', '5917186368099534002', 'Law 4 · Power', 'hinglish', 'power', [
   'Jo log kam bolte hain, {{log unse darte kyun hain?}}',
   'Jitna zyada bologe, utna common lagoge. {{Khali jagah ko log khud izzat se bhar dete hain.}}',
   'Chup insaan ko padhna mushkil hota hai. {{Aur jise padh nahi sakte, use koi halke mein nahi leta.}}',
   'Meeting mein sabse pehle mat bolo. {{Sabke baad bolo. Aakhri baat hi yaad rehti hai.}}',
   'Kal ek meeting mein kam bolke dekhna. {{Farak usi din dikh jaayega.}}'],
  'Tum zyada bolte ho ya kam? Neeche batao.',
  'Save kar lo, aur us dost ko bhejo jo har baat mein bol padta hai.'),

 ('2026-10-29', '394398705', '-3675091920912105128', "Parkinson's Law", 'english', 'psych', [
   'Give a task a month {{and it will take a month.}}',
   'Work expands to fill the time you give it. {{The task was never that big.}}',
   'Time is not what gets the work done. {{Pressure is, and you removed it.}}',
   'Cut the deadline in half and tell someone. {{You will find the work fits.}}',
   'Your week is not full. {{Your deadlines are just too kind.}}'],
  'What are you giving far too much time to? Tell us below.',
  'Save this, and halve one deadline today.'),

 ('2026-11-01', '394400949', '5458722314192437468', 'Shoshin', 'english', 'japan', [
   'The Japanese word for why {{experts stop getting better.}}',
   'Shoshin means beginner mind. {{The beginner sees many options. The expert sees only his own.}}',
   'The more you know, the more you defend. {{And defending shuts the door on learning.}}',
   'In the next meeting ask one question {{you are afraid will sound stupid.}}',
   'The expert says I know this. {{The master says show me again.}}'],
  'What do you think you already know too well? Comment below.',
  'Save this for the next time you are the most experienced person in the room.'),

 ('2026-11-02', '394567515', '-3601815595480825490', 'Law 16 · Power', 'hinglish', 'power', [
   'Roz milne wale ki keemat {{har mulaqat ke saath girti hai.}}',
   'Law 16 kehta hai thodi doori banao. {{Jo hamesha milta hai, uski keemat girti hai.}}',
   'Dimaag jis cheez ko roz dekhta hai, {{use background samajh ke bhool jaata hai.}}',
   'Har message ka turant jawab mat do. {{Har bulawe pe mat pahunch jao.}}',
   'Gayab hona bhaagna nahi hai. {{Apni jagah wapas banana hai.}}'],
  'Tum kiske liye hamesha available ho? Neeche likho.',
  'Save kar lo, aur agli baar thoda ruk jaana.'),

 ('2026-11-05', '394796894', '-7464817309612947027', 'Loss Aversion', 'english', 'psych', [
   'Losing a thousand rupees hurts twice as much {{as winning a thousand feels good.}}',
   'That is loss aversion. {{The mind weighs a loss far heavier than the same gain.}}',
   'Survival cared about what you lost, not what you missed. {{The wiring was never updated.}}',
   'Before refusing a risk, ask what you lose by staying. {{Count that loss too.}}',
   'You are not being careful. {{You are being scared in an organised way.}}'],
  'What are you not trying, just to avoid losing? Comment below.',
  'Save this for the decision you keep postponing.'),

 ('2026-11-08', '394797007', '6242100568321838803', 'Nishkama Karma', 'english', 'india', [
   'The hardest line in the Gita: {{do the work, drop the result.}}',
   'Nishkama karma means acting without clinging to the outcome. {{Not without care. Without clinging.}}',
   'Waiting for the result pulls your attention out of the work. {{Half your effort goes into checking.}}',
   'Decide what good work looks like before you start. {{Then judge yourself on that, not on the response.}}',
   'The result was never yours to control. {{The standard always was.}}'],
  'What are you doing only for the result? Tell us below.',
  'Save this for the day the numbers disappoint you.'),

 ('2026-11-09', '394797061', '7732940436911113633', 'Law 38 · Power', 'hinglish', 'power', [
   'Apni soch alag rakho. {{Par use har jagah dikhane ki zaroorat nahi.}}',
   'Law 38: andar se jo chaaho socho, {{bahar se logon jaise raho.}}',
   'Log alag soch se nahi chidte. {{Wo alag dikhne se chidte hain.}}',
   'Pehle unke beech apni jagah banao. {{Jagah banne ke baad hi alag bolo.}}',
   'Bagawat pehle din nahi jeetti. {{Wo tab jeetti hai jab log tumhe sunne lagte hain.}}'],
  'Kahan tumne alag hoke nuksaan uthaya? Neeche likho.',
  'Save kar lo, aur agli baar timing dekh lena.'),

 ('2026-11-12', '394797213', '-5981174298671560972', 'Pratfall Effect', 'english', 'psych', [
   'Perfect people are not liked. {{They are tolerated.}}',
   'The pratfall effect: one small visible flaw {{makes a capable person more likeable.}}',
   'Perfection reads as distance. {{A flaw tells people you are reachable.}}',
   'Admit a small mistake out loud before someone finds it. {{Do not perform it. Just say it.}}',
   'Competence earns the respect. {{The flaw earns the trust.}}'],
  'Who did you trust more after they admitted a mistake? Comment below.',
  'Save this before your next introduction.'),

 ('2026-11-15', '394797385', '8862305224788821319', 'Oubaitori', 'hinglish', 'japan', [
   'Japan mein ek shabd hai {{jo comparison ko khatam kar deta hai.}}',
   'Oubaitori: cherry, plum, peach aur apricot. {{Chaaron alag mausam mein khilte hain.}}',
   'Ek bhi ped late nahi hota. {{Sabka apna mausam hai, aur wo badla nahi jaa sakta.}}',
   'Doosron ki timeline dekhna band karo, {{aur apna pichla saal dekho.}}',
   'Tum peeche nahi ho. {{Tum kisi aur ke mausam mein khilne ki koshish kar rahe ho.}}'],
  'Tum kiske saath khud ko compare karte ho? Neeche likho.',
  'Save karo, aur us dost ko bhejo jo khud ko late samajh raha hai.'),

 ('2026-11-16', '394797444', '-2900747075223731650', 'Law 28 · Power', 'hinglish', 'power', [
   'Aadhe mann se kiya gaya kaam {{poori tarah fail hone se zyada mehnga padta hai.}}',
   'Law 28: jo karna hai poore confidence se karo. {{Jhijhak har galti ko do guna bada dikhati hai.}}',
   'Log kaam ko nahi, {{tumhare chehre ko dekh ke judge karte hain.}}',
   'Offer bhejte waqt sorry mat likho. {{Price bolo, phir chup raho.}}',
   'Himmat se ki gayi galti {{darr se kiye gaye kaam se behtar hoti hai.}}'],
  'Kahan tum aadhe mann se kar rahe ho? Comment mein likho.',
  'Save kar lo, aur aaj ek kaam poore confidence se karo.'),

 ('2026-11-19', '394797578', '4807694058079276471', "Hanlon's Razor", 'english', 'psych', [
   'That person did not plot against you. {{They were just busy.}}',
   "Hanlon's Razor: never assume malice {{where carelessness explains it.}}",
   'Most people are not thinking about you. {{They are stuck inside their own head.}}',
   'Before replying angry, ask one plain question. {{The answer is usually boring.}}',
   'You lost two nights to a message {{that was typed in four seconds.}}'],
  'What did you read into, that turned out to be nothing? Tell us below.',
  'Save this for the next message that stings.'),

 ('2026-11-22', '394797716', '-5267228719260151852', 'Abhyasa & Vairagya', 'english', 'india', [
   'Patanjali gave two words {{for everything that is hard to hold.}}',
   'Abhyasa is steady practice. {{Vairagya is letting the grip go loose.}}',
   'Practice without letting go becomes obsession. {{Letting go without practice becomes an excuse.}}',
   'Show up daily, and stop checking daily. {{You need both or neither works.}}',
   'Hold the work tightly. {{Hold the outcome loosely.}}'],
  'Which of the two is harder for you? Comment below.',
  'Save this for a week when nothing seems to move.'),
 ('2026-11-23', '394797855', '-8015325105742197701', 'Law 3 · Power', 'hinglish', 'power', [
   'Apna plan bata dene se {{aadha plan wahin mar jaata hai.}}',
   'Law 3: apne irade chhupao. {{Jo tumhara agla kadam jaanta hai, wo ek kadam aage khada hai.}}',
   'Log tumhari madad nahi karte. {{Wo apne hisaab se tumhara plan adjust karne lagte hain.}}',
   'Kaam shuru hone tak chup raho. {{Result khud bol dega, tumhe nahi bolna padega.}}',
   'Jitna kam log jaanenge, {{utni kam rukawatein aayengi.}}'],
  'Tumne kaun sa plan bata kar kharab kiya? Neeche likho.',
  'Save kar lo, aur agla plan chup chaap shuru karo.'),

 ('2026-11-26', '394798030', '7069921478093653823', 'Sunk Cost Fallacy', 'english', 'psych', [
   'You are not staying because it works. {{You are staying because you already paid.}}',
   'Sunk cost fallacy: the money and years already spent {{cannot be won back by spending more.}}',
   'Quitting feels like admitting the past was wasted. {{So people pay again to protect a story.}}',
   'Ask: if I were starting today, would I choose this? {{If not, the rest is just the bill.}}',
   'The years are gone either way. {{Only the next one is still yours.}}'],
  'What are you holding on to only because of the time spent? Comment below.',
  'Save this for the decision you keep defending.'),

 ('2026-11-29', '394798152', '-5268605909397058640', 'Wabi-sabi', 'english', 'japan', [
   'Japan has a word for the beauty {{of things that are not finished.}}',
   'Wabi-sabi finds beauty in the worn and the uneven, {{in the thing that clearly had a life.}}',
   'Perfect things impress once. {{Imperfect things are the ones people keep.}}',
   'Stop fixing the flaw nobody noticed. {{Ship it while it still has a face.}}',
   'Nothing finished is alive. {{Nothing perfect is yours.}}'],
  'What are you over-polishing right now? Tell us below.',
  'Save this for the next thing you are afraid to release.'),

 ('2026-11-30', '394798209', '6120555764648333102', 'Law 25 · Power', 'hinglish', 'power', [
   'Log tumhe wahi samajhte rahenge {{jo tumne paanch saal pehle dikhaya tha.}}',
   'Law 25: khud ko dobara banao. {{Jo image dusron ne di hai, usme zindagi mat kaat do.}}',
   'Purani pehchaan aaram deti hai. {{Par wahi tumhare naye kaam ko rok bhi deti hai.}}',
   'Ek aadat aaj chhod do. {{Ek cheez shuru karo jo tumhari nayi pehchaan bane.}}',
   'Tum wahi nahi ho jo tum the. {{Bas kisi ne tumhe update nahi kiya.}}'],
  'Log tumhe kis purani cheez se jodte hain? Neeche likho.',
  'Save kar lo, aur aaj ek purani aadat chhod do.'),

 ('2026-12-03', '394798389', '8557916693662875709', "Goodhart's Law", 'english', 'psych', [
   'The moment a number becomes the target, {{it stops telling the truth.}}',
   "Goodhart's Law: when a measure becomes a goal, {{it stops being a good measure.}}",
   'People do not chase the thing. {{They chase whatever is being counted.}}',
   'Pick a number to watch, not to win. {{And keep one you never report.}}',
   'Followers are a number. {{Trust was the thing you were counting.}}'],
  'Which number are you chasing too hard? Comment below.',
  'Save this before you set your next target.'),

 ('2026-12-06', '394798571', '3229230292642317194', 'Chanakya Niti', 'hinglish', 'india', [
   'Chanakya: kaam shuru karne se pehle {{teen sawaal khud se poochho.}}',
   'Main ye kyun kar raha hoon. {{Iska anjaam kya hoga. Aur kya mujhe safalta milegi.}}',
   'Jo in teen ka jawab nahi de sakta, {{wo mehnat karega, par pahunchega kahin nahi.}}',
   'Agla bada kaam shuru karne se pehle teeno likh lo. {{Ek bhi khali hai to ruk jao.}}',
   'Mehnat se zyada mehnga {{galat jagah ki gayi mehnat padti hai.}}'],
  'Tum abhi kaun sa kaam bina jawab ke kar rahe ho? Neeche likho.',
  'Save karo, aur aaj teeno sawaal likh lo.'),

 ('2026-12-07', '394798622', '-556606170119057958', 'Law 34 · Power', 'hinglish', 'power', [
   'Log tumse waisa hi behave karte hain {{jaisa tum khud ko samajhte ho.}}',
   'Law 34: apni keemat khud tay karo. {{Duniya aksar usi number ko maan leti hai.}}',
   'Jo chhoti baat pe jhuk jaata hai, {{uske liye log chhoti baat hi rakhte hain.}}',
   'Apna rate bolo aur chup ho jao. {{Safai dena band karo.}}',
   'Izzat maangi nahi jaati. {{Wo tumhare apne standard se shuru hoti hai.}}'],
  'Tumne kab apni keemat khud girayi? Comment mein likho.',
  'Save kar lo, aur agli baar discount mat do.'),

 ('2026-12-10', '394798782', '8525075398477169992', 'Spotlight Effect', 'english', 'psych', [
   'Nobody noticed. {{They were busy worrying about their own day.}}',
   'The spotlight effect: we think people see our mistakes {{far more than they actually do.}}',
   'You replay your moment all evening. {{They forgot it before they reached the door.}}',
   'Before you shrink, ask what you remember {{about what anyone else wore last week.}}',
   'The audience you are afraid of {{is mostly you.}}'],
  'What are you still cringing about? Tell us below.',
  'Save this for the next time you want to disappear.'),

 ('2026-12-13', '394799100', '-7571154856189737008', 'Ikigai', 'english', 'japan', [
   'Ikigai is not your dream job. {{It is a reason to get up.}}',
   'In Okinawa, ikigai is small. {{A garden, a friend, a thing you are needed for.}}',
   'A huge purpose can be postponed forever. {{A small one has to happen today.}}',
   'Name one thing tomorrow that only you will do. {{That is enough to start with.}}',
   'You do not find your purpose. {{You show up until it forms.}}'],
  'What gets you up tomorrow? Comment below.',
  'Save this for a morning that feels pointless.'),

 ('2026-12-14', '394799160', '-2575269966930229334', 'Law 9 · Power', 'hinglish', 'power', [
   'Behes jeet ke bhi {{tum aksar haar jaate ho.}}',
   'Law 9: sabit karo, samjhao mat. {{Jeeti hui behes apne peeche dushmani chhod jaati hai.}}',
   'Log apni baat nahi, apni izzat bacha rahe hote hain. {{Isiliye sach se zyada ego ladta hai.}}',
   'Jawab mat do. {{Chhe mahine baad result saamne rakh do.}}',
   'Jiska kaam bol deta hai, {{use bolne ki zaroorat nahi padti.}}'],
  'Tumne kaun si behes jeet ke rishta khoya? Neeche likho.',
  'Save kar lo, aur agli behes chhod do.'),

 ('2026-12-17', '394799297', '-5538846271156171916', 'Curse of Knowledge', 'english', 'psych', [
   'You are not bad at explaining. {{You forgot what not knowing feels like.}}',
   'The curse of knowledge: once you know a thing, {{you cannot imagine not knowing it.}}',
   'Experts skip the steps that now feel obvious. {{Those steps were the whole lesson.}}',
   'Explain it to someone outside your field. {{Every word they stop on is a step you skipped.}}',
   'Clear is not simple. {{Clear is remembering you were once lost.}}'],
  'What did someone finally explain well to you? Comment below.',
  'Save this before your next explanation.'),

 ('2026-12-20', '394799449', '766657926404328904', 'Sthitaprajna', 'english', 'india', [
   'The Gita has a word for a person {{praise and insult cannot move.}}',
   'Sthitaprajna means steady in understanding. {{Not cold. Just not thrown by either side.}}',
   'If praise lifts you, criticism will drop you. {{You handed both the same switch.}}',
   'Read the good comment and the bad one, {{then go back to the same work.}}',
   'Let the weather change. {{Do not let it decide your day.}}'],
  'Which hits you harder, praise or criticism? Tell us below.',
  'Save this for the day the comments get loud.'),

 ('2026-12-21', '394799528', '5348665303047162147', 'Law 46 · Power', 'hinglish', 'power', [
   'Jo sab kuch sahi karta hai, {{uske liye log chup chaap intezaar karte hain.}}',
   'Law 46: zyada perfect mat dikho. {{Log kami maaf kar dete hain, perfection kabhi nahi.}}',
   'Tumhari har jeet kisi ko apni haar jaisi lagti hai. {{Jalan theek wahin se shuru hoti hai.}}',
   'Apna result dikhao, apna struggle bhi. {{Sirf trophy mat dikhao.}}',
   'Jeetna alag baat hai. {{Har waqt jeeta hua dikhna alag baat hai.}}'],
  'Tumne kab apni jeet chhupayi? Comment mein likho.',
  'Save kar lo, aur agli baar struggle bhi batao.'),

 ('2026-12-24', '394803726', '4360918408823917437', "Dunbar's Number", 'english', 'psych', [
   'You can hold about 150 relationships. {{Your phone thinks you can hold two thousand.}}',
   "Dunbar's number: the brain has room for roughly 150 people, {{and only about five close ones.}}",
   'Every extra name takes space from a real one. {{Attention does not scale.}}',
   'This season, call five people properly. {{Let the rest be a message.}}',
   'You are not losing friends. {{You are finally choosing them.}}'],
  'Who are your five? Tell us below.',
  'Save this, and call one of them today.'),

 ('2026-12-27', '394803897', '3493491066533662597', 'Kintsugi', 'english', 'japan', [
   'In Japan a broken bowl is repaired {{with gold, so the cracks show.}}',
   'Kintsugi does not hide the break. {{It makes the break the most valuable line on the bowl.}}',
   'A bowl that never broke has no story. {{A repaired one has survived a fall.}}',
   'Stop editing the hard year out of your answer. {{Say what broke and what you did after.}}',
   'The crack is not the damage. {{It is proof that you were put back.}}'],
  'What broke, and what did you build after? Comment below.',
  'Save this for the end of a hard year.'),

 ('2026-12-28', '394803965', '-8542152789150118440', 'Law 35 · Power', 'hinglish', 'power', [
   'Sahi baat galat waqt par {{galat baat ban jaati hai.}}',
   'Law 35: timing seekho. {{Jaldi karne wala jhuk jaata hai, der karne wala chook jaata hai.}}',
   'Log sirf idea nahi sunte. {{Wo dekhte hain ki idea kis haalat mein aaya hai.}}',
   'Demand tab rakho jab tumhara kaam bol chuka ho. {{Usse pehle bilkul nahi.}}',
   'Sabr kamzori nahi hai. {{Wo bhi ek chaal hoti hai.}}'],
  'Tumne kab sahi baat galat waqt pe kahi? Neeche likho.',
  'Save kar lo, aur agli demand ka waqt chuno.'),

 ('2026-12-31', '394804183', '-9137100631731190271', 'Hedonic Adaptation', 'english', 'psych', [
   'Whatever you are chasing, {{you will get used to it in a month.}}',
   'Hedonic adaptation: the mind returns to its baseline {{after almost every win.}}',
   'The phone, the salary, the new city. {{Each one felt permanent for about three weeks.}}',
   'Build the year around what you do daily, {{not around what you will finally get.}}',
   'Next year will not feel different {{because something finally arrived.}}'],
  'What did you get that stopped mattering? Tell us below.',
  'Save this before you write your resolutions.'),
]



def build():
    ledger = json.loads((ROOT / 'ledger.json').read_text(encoding='utf-8'))
    by_date = {e['date']: e for e in ledger}

    batch, updates = [], []
    for date, pid, uuid, name, lang, src, slides, ask, send in DATA:
        assert len(slides) == 5, date
        entry = by_date[date]
        start = LOOKS.index(entry['look'])
        looks = [LOOKS[(start + i) % 5] for i in range(5)]
        urls, images = [], []
        for i, text in enumerate(slides):
            assert text.count('{{') == 1 and text.count('}}') == 1, f'{date} slide {i+1}'
            img = f'posts/rkp-{date}-{i+1}.png'
            images.append(img)
            urls.append('https://raw.githubusercontent.com/rohitmudgill/rkp-posts/main/' + img)
            batch.append({'look': looks[i], 'tag': SLIDE_TAGS[i] or name, 'num': '',
                          'foot': FOOTERS[i], 'text': text, 'out': img})
        hook = slides[0].replace('{{', '').replace('}}', '')
        caption = f'{hook}\n\n{ask}\n\n{send}\n\n{HT[src]}'
        entry.update(format='carousel', principle=name, lang=lang, pillar=f'Carousel / {name}',
                     quote=hook, images=images, caption=caption, source='carousel-1')
        entry.pop('image', None)
        updates.append({'date': date, 'id': pid, 'uuid': uuid, 'alt': hook,
                        'caption': caption, 'media': urls})

    (ROOT / 'ledger.json').write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp = ROOT / 'tmp'; tmp.mkdir(exist_ok=True)
    (tmp / 'cbatch.json').write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding='utf-8')
    (tmp / 'cupdates.json').write_text(json.dumps(updates, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'{len(DATA)} carousels, {len(batch)} slides')


if __name__ == '__main__':
    build()
