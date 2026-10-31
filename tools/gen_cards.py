import json, re, random
from collections import Counter

random.seed(42)

need = json.load(open('/tmp/need.json'))
merged = json.load(open('/tmp/merged_ru.json'))
used = set(json.load(open('/tmp/used_words.json')))
manual = json.load(open('/workspace/tools/manual_ru.json'))

def ru_for(word):
    w = word.lower().strip()
    if w in manual: return manual[w]
    if w in merged and merged[w] and merged[w].lower()!=w: return merged[w]
    for part in re.split(r'[;,]', w):
        p = part.strip()
        if p in manual: return manual[p]
        if p in merged and merged[p] and merged[p].lower()!=p: return merged[p]
    return None

NOUN_TPL = [
 "The {w} is on the table.","I need a new {w}.","This {w} costs ten dollars.","Where can I find the {w}?",
 "She bought a {w} yesterday.","A good {w} makes a difference.","Do you have this {w} in another size?",
 "My {w} is better than yours.","They talked about the {w} all day.","There is a problem with the {w}.",
 "He looked at the {w} carefully.","We used the {w} every weekend.","That was an interesting {w}.",
 "Nobody expected this {w}.","You can see the {w} from here.","How much does the {w} cost?",
 "It took me hours to fix the {w}.","Please pass me the {w}.","The {w} was different from what we expected.",
 "Let's discuss the {w} later."]
VERB_TPL = [
 "Can you {w} it for me?","I always {w} in the morning.","They decided to {w} together.","She wants to {w} right now.",
 "We should {w} before it's too late.","He tried to {w} but failed.","Did you {w} the door?",
 "You can {w} it any way you like.","How do you {w} this problem?","Let's {w} and see what happens.",
 "They often {w} on weekends.","I didn't mean to {w}.","Would you like to {w} tomorrow?",
 "We learned how to {w} last year.","She began to {w} after lunch.","Please {w} carefully.",
 "He had to {w} twice.","You never {w} without thinking.","We agreed to {w} next week.","Did they {w} on time?"]
ADJ_TPL = [
 "It was a very {w} day.","She has a {w} smile.","This is too {w} for me.","He seems quite {w} today.",
 "What a {w} idea!","The weather is {w} outside.","I found it rather {w}.","That looks really {w}.",
 "It sounds {w} to me.","They made a {w} choice.","The film was pretty {w}.","Her voice is soft and {w}.",
 "He gave me a {w} answer.","We need a more {w} approach.","It felt strange and {w}.","Such a {w} gesture!",
 "The room was small but {w}.","His explanation was clear and {w}.","That's a {w} question.","Life can be hard and {w}."]
ADV_TPL = [
 "He did it very {w}.","Things went {w} from there.","She spoke {w} and calmly.","We finished the work {w}.",
 "It works {w} most of the time.","He smiled at her {w}.","The plan came together {w}.","She handled it rather {w}.",
 "Everything changed {w} overnight.","He nodded and left quietly.","They behaved {w} all evening.","It sounded {w} on paper.",
 "The team responded {w} to the news.","He looked around {w}.","She answered {w} without hesitation.",
 "The meeting ended {w} and quickly.","He drove too {w} on the highway.","The story developed {w} in the second half.",
 "I'll call you back {w}.","It happened so {w} that nobody noticed."]
PREP_TPL = ["Meet me {w} the corner.","Put it {w} the box.","We walked {w} the bridge."]
CONJ_TPL = ["Stay quiet {w} you finish.","Call me {w} you arrive."]
ART_TPL = ["Give me {w} apple.","It was {w} nice day."]
EXCL_TPL = ["{w}! What a surprise!","{w}! I didn't see you there.","{w}, that feels good."]
PRO_TPL = ["{w} can join us.","Is {w} here?","{w} told me about it."]

RU_NOUN=["{r} лежит на столе.","Мне нужен новый {r}.","Этот {r} стоит десять долларов.","Где можно найти {r}?",
 "Она купила {r} вчера.","Хороший {r} имеет значение.","У вас есть этот {r} другого размера?","Мой {r} лучше твоего.",
 "Они весь день говорили о {r}.","С {r} проблема.","Он внимательно посмотрел на {r}.","Мы использовали {r} каждые выходные.",
 "Это был интересный {r}.","Никто не ожидал такого {r}.","Отсюда видно {r}.","Сколько стоит {r}?",
 "Починка {r} заняла у меня часы.","Передай мне, пожалуйста, {r}.","{r} оказался не таким, как мы думали.","Обсудим {r} позже."]
RU_VERB=["Ты можешь {r} для меня?","Я всегда {r} утром.","Они решили {r} вместе.","Она хочет {r} прямо сейчас.",
 "Нам следует {r}, пока не поздно.","Он пытался {r}, но не смог.","Ты {r} дверь?","Можно {r} как угодно.",
 "Как ты {r} эту проблему?","Давай {r} и посмотрим, что будет.","Они часто {r} по выходным.","Я не хотел {r}.",
 "Хочешь {r} завтра?","Мы научились {r} в прошлом году.","Она начала {r} после обеда.","Пожалуйста, {r} аккуратно.",
 "Ему пришлось {r} дважды.","Ты никогда не {r} не подумав.","Мы договорились {r} на следующей неделе.","Они {r} вовремя?"]
RU_ADJ=["Это был очень {r} день.","У неё {r} улыбка.","Это слишком {r} для меня.","Он сегодня довольно {r}.",
 "Какая {r} идея!","Погода снаружи {r}.","Я счёл это довольно {r}.","Это выглядит очень {r}.","Это звучит {r} для меня.",
 "Они сделали {r} выбор.","Фильм был довольно {r}.","Её голос мягкий и {r}.","Он дал мне {r} ответ.",
 "Нам нужен более {r} подход.","Это было странно и {r}.","Такой {r} жест!","Комната была маленькая, но {r}.",
 "Его объяснение было ясным и {r}.","Это {r} вопрос.","Бывает трудно и {r}."]
RU_ADV=["Он сделал это очень {r}.","Дела пошли {r} с этого момента.","Она говорила {r} и спокойно.","Мы закончили работу {r}.",
 "Это {r} работает большую часть времени.","Он {r} и спокойно улыбнулся ей.","План сложился {r}.","Она поступила довольно {r}.",
 "Всё изменилось {r} за ночь.","Он тихо кивнул и ушёл.","Они вели себя {r} весь вечер.","На бумаге это звучало {r}.",
 "Команда отреагировала на новость {r}.","Он {r} огляделся.","Она ответила {r} без колебаний.","Встреча закончилась {r} и быстро.",
 "Он ехал по трассе слишком {r}.","Во второй половине история развивалась {r}.","Я перезвоню тебе {r}.",
 "Это произошло так {r}, что никто не заметил."]
RU_PREP=["Встреться со мной {r} угла.","Положи это {r} коробку.","Мы прошли {r} мост."]
RU_CONJ=["Молчи, {r} закончишь.","Позвони мне, {r} приедешь."]
RU_ART=["Дай мне {r} яблоко.","Это был {r} хороший день."]
RU_EXCL=["{r}! Вот сюрприз!","{r}! Я тебя тут не видел.","{r}, как приятно."]
RU_PRO=["{r} может к нам присоединиться.","{r} здесь?","{r} рассказал мне об этом."]

def pos_kind(pos):
    p = (pos or '').lower()
    if 'noun' in p: return 'noun'
    if 'verb' in p: return 'verb'
    if 'adj' in p: return 'adj'
    if 'adv' in p: return 'adv'
    if 'prep' in p: return 'prep'
    if 'conj' in p: return 'conj'
    if 'article' in p: return 'art'
    if 'exclamation' in p: return 'excl'
    if 'pron' in p: return 'pron'
    if 'number' in p: return 'noun'
    if 'determiner' in p or 'modal' in p: return 'adv'
    return 'noun'

def make_sentence(w, kind):
    base = re.split(r'[,/]', w)[0].strip().replace('to ','')
    tpls = {'verb':VERB_TPL,'adj':ADJ_TPL,'adv':ADV_TPL,'prep':PREP_TPL,'conj':CONJ_TPL,
            'art':ART_TPL,'excl':EXCL_TPL,'pron':PRO_TPL}
    tpl = random.choice(tpls.get(kind, NOUN_TPL))
    return tpl.format(w=base)

def ru_sentence(w, r, kind):
    rt = re.split(r'[;,]', r)[0].strip()
    tpls = {'verb':RU_VERB,'adj':RU_ADJ,'adv':RU_ADV,'prep':RU_PREP,'conj':RU_CONJ,
            'art':RU_ART,'excl':RU_EXCL,'pron':RU_PRO}
    tpl = random.choice(tpls.get(kind, RU_NOUN))
    return tpl.format(r=rt)

cards=[]
skipped_no_ru=[]
for e in need:
    w=e['word']
    lw=w.lower().strip()
    if lw in used: continue
    r=ru_for(w)
    if not r:
        skipped_no_ru.append(w); continue
    kind=pos_kind(e.get('pos',''))
    en=make_sentence(w,kind)
    rus=ru_sentence(w,r,kind)
    lvl=(e.get('level','A1') or 'A1').split(',')[0].strip()
    if lvl not in ('A1','A2','B1','B2','C1'):
        lvl='C1' if lvl.startswith('C') else 'B1'
    cards.append({'word':w,'ru':r,'en':en,'rus':rus,'level':lvl,'pos':e.get('pos','')})

print('new cards:',len(cards))
print(Counter(c['level'] for c in cards))
print('skipped no ru:',len(skipped_no_ru), skipped_no_ru[:30])
json.dump(cards,open('/tmp/new_cards.json','w'),ensure_ascii=False)
