"""
DumbQuiz — Korean Language Quiz Game
====================================
A fun 20-question Korean quiz covering vocabulary, grammar, culture, and K-pop.
Features: scoring, feedback, high score leaderboard.
"""

import streamlit as st
import random
import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DumbQuiz — Korean Quiz",
    page_icon="🇰🇷",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=DM+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', 'Noto Sans KR', sans-serif;
    background: #0a0a12;
    color: #e8e8f0;
}

.hero {
    text-align: center;
    padding: 24px 0 8px 0;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6C63FF, #FF6584, #43E8D8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}
.hero-sub { font-size: 0.95rem; color: #666; margin-top: 4px; }

.question-card {
    background: #111118;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
}
.q-category {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #666;
    margin-bottom: 8px;
}
.q-text {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e8e8f0;
    margin-bottom: 8px;
    line-height: 1.5;
}
.q-korean {
    font-size: 2rem;
    color: #6C63FF;
    margin: 8px 0;
    letter-spacing: 2px;
}

.diff-easy {
    background: #0d2e1a; color: #4ade80;
    border: 1px solid #4ade8033;
    border-radius: 99px; padding: 2px 10px;
    font-size: 0.7rem; font-weight: 600;
}
.diff-medium {
    background: #2e1f0d; color: #fbbf24;
    border: 1px solid #fbbf2433;
    border-radius: 99px; padding: 2px 10px;
    font-size: 0.7rem; font-weight: 600;
}
.diff-hard {
    background: #2e0d0d; color: #f87171;
    border: 1px solid #f8717133;
    border-radius: 99px; padding: 2px 10px;
    font-size: 0.7rem; font-weight: 600;
}

.correct-box {
    background: #0d2e1a;
    border-left: 3px solid #4ade80;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    color: #4ade80;
    font-size: 0.9rem;
    margin: 8px 0;
}
.wrong-box {
    background: #2e0d0d;
    border-left: 3px solid #f87171;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    color: #f87171;
    font-size: 0.9rem;
    margin: 8px 0;
}
.explanation {
    background: #111118;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 12px 16px;
    color: #aaa;
    font-size: 0.85rem;
    margin: 8px 0;
}

.score-card {
    background: #111118;
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    margin: 16px 0;
}
.big-score {
    font-size: 4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6C63FF, #43E8D8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.lb-row {
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1e1e30;
    font-size: 0.9rem;
}
.lb-rank { color: #666; min-width: 32px; font-weight: 600; }
.lb-name { flex: 1; color: #e8e8f0; }
.lb-score { color: #6C63FF; font-weight: 600; }

.progress-text { color: #666; font-size: 0.85rem; text-align: center; }

.stButton > button {
    background: #111118 !important;
    border: 1px solid #2a2a40 !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    border-color: #6C63FF !important;
    color: #6C63FF !important;
}

#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Question Bank
# ─────────────────────────────────────────────
ALL_QUESTIONS = [
    # ── VOCABULARY ──────────────────────────────────────────────────────────
    {"category":"Vocabulary","difficulty":"easy","question":"What does '안녕하세요' mean?","korean":"안녕하세요","options":["Hello","Goodbye","Thank you","Sorry"],"answer":0,"explanation":"'안녕하세요' (annyeonghaseyo) is the formal way to say hello in Korean."},
    {"category":"Vocabulary","difficulty":"easy","question":"How do you say 'thank you' formally?","korean":"","options":["괜찮아요","감사합니다","미안해요","좋아요"],"answer":1,"explanation":"'감사합니다' (gamsahamnida) means thank you formally."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '물' mean?","korean":"물","options":["Fire","Water","Food","Rice"],"answer":1,"explanation":"'물' (mul) means water."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '밥' mean?","korean":"밥","options":["Soup","Noodles","Rice/Meal","Bread"],"answer":2,"explanation":"'밥' (bap) means cooked rice or a meal."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '사람' mean?","korean":"사람","options":["Animal","Person","Place","Thing"],"answer":1,"explanation":"'사람' (saram) means person or people."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '집' mean?","korean":"집","options":["School","Hospital","House/Home","Office"],"answer":2,"explanation":"'집' (jip) means house or home."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '책' mean?","korean":"책","options":["Pen","Book","Desk","Chair"],"answer":1,"explanation":"'책' (chaek) means book."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '차' mean?","korean":"차","options":["Bus","Bicycle","Car/Tea","Train"],"answer":2,"explanation":"'차' (cha) means car or tea depending on context."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '고양이' mean?","korean":"고양이","options":["Dog","Cat","Bird","Fish"],"answer":1,"explanation":"'고양이' (goyangi) means cat."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '개' mean?","korean":"개","options":["Cat","Rabbit","Dog","Horse"],"answer":2,"explanation":"'개' (gae) means dog."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '오늘' mean?","korean":"오늘","options":["Yesterday","Tomorrow","Today","Now"],"answer":2,"explanation":"'오늘' (oneul) means today."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '내일' mean?","korean":"내일","options":["Yesterday","Today","Tomorrow","Later"],"answer":2,"explanation":"'내일' (naeil) means tomorrow."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '어제' mean?","korean":"어제","options":["Today","Yesterday","Tomorrow","Before"],"answer":1,"explanation":"'어제' (eoje) means yesterday."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '친구' mean?","korean":"친구","options":["Enemy","Stranger","Friend","Teacher"],"answer":2,"explanation":"'친구' (chingu) means friend."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '학교' mean?","korean":"학교","options":["Hospital","Market","School","Library"],"answer":2,"explanation":"'학교' (hakgyo) means school."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '어디예요?' mean?","korean":"어디예요?","options":["What is it?","Where is it?","How much?","When is it?"],"answer":1,"explanation":"'어디예요?' means 'Where is it?'"},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '얼마예요?' mean?","korean":"얼마예요?","options":["How many?","What time?","How much?","How far?"],"answer":2,"explanation":"'얼마예요?' means 'How much is it?'"},
    {"category":"Vocabulary","difficulty":"medium","question":"Which word means 'delicious'?","korean":"","options":["맛있어요","맛없어요","배고파요","배불러요"],"answer":0,"explanation":"'맛있어요' (masisseoyo) means delicious."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '바쁘다' mean?","korean":"바쁘다","options":["Lazy","Happy","Busy","Bored"],"answer":2,"explanation":"'바쁘다' (bappeuda) means to be busy."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '시간' mean?","korean":"시간","options":["Money","Space","Time","Speed"],"answer":2,"explanation":"'시간' (sigan) means time or hour."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '날씨' mean?","korean":"날씨","options":["Season","Weather","Temperature","Wind"],"answer":1,"explanation":"'날씨' (nalssi) means weather."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '음식' mean?","korean":"음식","options":["Drink","Food","Restaurant","Kitchen"],"answer":1,"explanation":"'음식' (eumsik) means food."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '주말' mean?","korean":"주말","options":["Weekday","Holiday","Weekend","Morning"],"answer":2,"explanation":"'주말' (jumal) means weekend."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '여행' mean?","korean":"여행","options":["Work","Study","Travel","Rest"],"answer":2,"explanation":"'여행' (yeohaeng) means travel or trip."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '병원' mean?","korean":"병원","options":["School","Hospital","Pharmacy","Clinic"],"answer":1,"explanation":"'병원' (byeongwon) means hospital."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '시장' mean?","korean":"시장","options":["Restaurant","Market","Mall","Store"],"answer":1,"explanation":"'시장' (sijang) means market or mayor."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '전화' mean?","korean":"전화","options":["Email","Letter","Telephone/Call","Message"],"answer":2,"explanation":"'전화' (jeonhwa) means telephone or phone call."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '괜찮아요' mean?","korean":"괜찮아요","options":["I'm hungry","I'm tired","It's okay","I'm busy"],"answer":2,"explanation":"'괜찮아요' means 'it's okay' or 'I'm fine'."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '피곤해요' mean?","korean":"피곤해요","options":["I'm hungry","I'm happy","I'm tired","I'm cold"],"answer":2,"explanation":"'피곤해요' means 'I'm tired'."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '그리워요' mean?","korean":"그리워요","options":["I'm angry","I miss (someone)","I'm jealous","I'm scared"],"answer":1,"explanation":"'그리워요' (geuriwoyo) means 'I miss (someone)'."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '부럽다' mean?","korean":"부럽다","options":["Angry","Jealous/Envious","Sad","Disappointed"],"answer":1,"explanation":"'부럽다' (bureoptda) means to be jealous or envious."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '복잡하다' mean?","korean":"복잡하다","options":["Simple","Empty","Complicated/Crowded","Quiet"],"answer":2,"explanation":"'복잡하다' (bokjaphada) means complicated or crowded."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '약속' mean?","korean":"약속","options":["Secret","Promise/Appointment","Contract","Dream"],"answer":1,"explanation":"'약속' (yaksok) means promise or appointment."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '추억' mean?","korean":"추억","options":["Future","Dream","Memory/Nostalgia","Regret"],"answer":2,"explanation":"'추억' (chueok) means memory or nostalgic recollection."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '설레다' mean?","korean":"설레다","options":["To be bored","To feel excited/flutter","To be nervous","To be calm"],"answer":1,"explanation":"'설레다' means to feel excited or have butterflies — often used for romantic anticipation."},
    {"category":"Vocabulary","difficulty":"hard","question":"What does '눈치' mean?","korean":"눈치","options":["Eyesight","Social awareness/reading the room","Intuition","Gossip"],"answer":1,"explanation":"'눈치' is the Korean concept of reading social situations and others' feelings."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '회사' mean?","korean":"회사","options":["School","Hospital","Company/Office","Government"],"answer":2,"explanation":"'회사' (hoesa) means company or office."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '지하철' mean?","korean":"지하철","options":["Bus","Taxi","Subway/Metro","Train"],"answer":2,"explanation":"'지하철' (jihacheol) means subway or metro."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '감사' mean?","korean":"감사","options":["Sorry","Gratitude/Thanks","Hello","Goodbye"],"answer":1,"explanation":"'감사' (gamsa) means gratitude or thanks."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '사랑' mean?","korean":"사랑","options":["Hate","Fear","Love","Happiness"],"answer":2,"explanation":"'사랑' (sarang) means love."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '행복' mean?","korean":"행복","options":["Sadness","Anger","Happiness","Loneliness"],"answer":2,"explanation":"'행복' (haengbok) means happiness."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '꿈' mean?","korean":"꿈","options":["Reality","Dream/Goal","Memory","Wish"],"answer":1,"explanation":"'꿈' (kkum) means dream or goal."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '하나' mean?","korean":"하나","options":["Two","Three","One","Four"],"answer":2,"explanation":"'하나' (hana) is the native Korean word for one."},
    {"category":"Vocabulary","difficulty":"easy","question":"What does '둘' mean?","korean":"둘","options":["One","Two","Three","Four"],"answer":1,"explanation":"'둘' (dul) is the native Korean word for two."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '맵다' mean?","korean":"맵다","options":["Sweet","Sour","Salty","Spicy"],"answer":3,"explanation":"'맵다' (maepda) means spicy or hot (taste)."},
    {"category":"Vocabulary","difficulty":"medium","question":"What does '달다' mean?","korean":"달다","options":["Sour","Bitter","Sweet","Salty"],"answer":2,"explanation":"'달다' (dalda) means sweet."},

    # ── GRAMMAR ──────────────────────────────────────────────────────────────
    {"category":"Grammar","difficulty":"easy","question":"In Korean, where does the verb go in a sentence?","korean":"","options":["Beginning","Middle","End","Anywhere"],"answer":2,"explanation":"Korean is Subject-Object-Verb (SOV). The verb always comes at the end."},
    {"category":"Grammar","difficulty":"medium","question":"Which ending makes a verb polite?","korean":"","options":["-다","-아/어요","-고싶다","-지마"],"answer":1,"explanation":"The '-아/어요' ending makes verbs polite."},
    {"category":"Grammar","difficulty":"medium","question":"What does '이다' mean?","korean":"이다","options":["To do","To be","To go","To eat"],"answer":1,"explanation":"'이다' is the Korean 'to be'."},
    {"category":"Grammar","difficulty":"hard","question":"What particle marks the subject?","korean":"","options":["을/를","에서","이/가","의"],"answer":2,"explanation":"'이/가' marks the subject. '을/를' marks the object."},
    {"category":"Grammar","difficulty":"hard","question":"How do you make a verb negative?","korean":"","options":["Add 안 before","Add 못 after","Change to -없다","Add 아니 at end"],"answer":0,"explanation":"Add '안' before the verb: 가요 → 안 가요."},
    {"category":"Grammar","difficulty":"easy","question":"What is the Korean sentence order?","korean":"","options":["SVO like English","SOV — verb at end","VSO","OVS"],"answer":1,"explanation":"Korean uses Subject-Object-Verb order."},
    {"category":"Grammar","difficulty":"medium","question":"What does '을/를' mark in a sentence?","korean":"을/를","options":["Subject","Object","Location","Time"],"answer":1,"explanation":"'을/를' are object markers in Korean."},
    {"category":"Grammar","difficulty":"medium","question":"What does '에서' indicate?","korean":"에서","options":["Possession","Direction","Location of action","Time"],"answer":2,"explanation":"'에서' marks the location where an action takes place."},
    {"category":"Grammar","difficulty":"medium","question":"What does '의' indicate?","korean":"의","options":["Subject","Object","Possession","Direction"],"answer":2,"explanation":"'의' is the possessive particle, similar to 's in English."},
    {"category":"Grammar","difficulty":"hard","question":"What does '-고 싶다' express?","korean":"-고 싶다","options":["Ability","Want to do something","Have to do","Did in the past"],"answer":1,"explanation":"'-고 싶다' expresses desire or 'want to'. 먹고 싶다 = want to eat."},
    {"category":"Grammar","difficulty":"hard","question":"What does '-았/었어요' indicate?","korean":"","options":["Future tense","Present tense","Past tense","Conditional"],"answer":2,"explanation":"'-았/었어요' is the past tense ending in polite Korean."},
    {"category":"Grammar","difficulty":"hard","question":"What does '-ㄹ/을 거예요' indicate?","korean":"","options":["Past tense","Future intention","Present state","Command"],"answer":1,"explanation":"'-ㄹ/을 거예요' expresses future intention or plan."},
    {"category":"Grammar","difficulty":"medium","question":"What does '-지 마세요' mean?","korean":"-지 마세요","options":["Please do","Please don't","You must","You can"],"answer":1,"explanation":"'-지 마세요' is a polite negative command — 'please don't'."},
    {"category":"Grammar","difficulty":"hard","question":"What does '-아/어서' connect?","korean":"","options":["Contrast","Reason/cause","Sequence only","Condition"],"answer":1,"explanation":"'-아/어서' connects clauses showing reason or cause: 'because'."},
    {"category":"Grammar","difficulty":"hard","question":"What does '-면' express?","korean":"-면","options":["Although","Because","If/When (condition)","After"],"answer":2,"explanation":"'-면' expresses a conditional: 'if' or 'when'."},
    {"category":"Grammar","difficulty":"medium","question":"What does '못' before a verb mean?","korean":"못","options":["Don't (won't)","Can't (inability)","Shouldn't","Didn't"],"answer":1,"explanation":"'못' expresses inability — can't do something. '안' expresses choice not to."},
    {"category":"Grammar","difficulty":"easy","question":"How do you say 'I' formally in Korean?","korean":"","options":["나","저","우리","그"],"answer":1,"explanation":"'저' (jeo) is the formal/humble way to say 'I'. '나' is informal."},
    {"category":"Grammar","difficulty":"medium","question":"What is the topic marker in Korean?","korean":"","options":["이/가","을/를","은/는","에서"],"answer":2,"explanation":"'은/는' is the topic marker, used to introduce or contrast topics."},
    {"category":"Grammar","difficulty":"hard","question":"What does '-ㄴ/은 것 같다' express?","korean":"","options":["Certainty","Seems like / I think","Command","Desire"],"answer":1,"explanation":"'-ㄴ/은 것 같다' expresses conjecture: 'it seems like' or 'I think'."},
    {"category":"Grammar","difficulty":"hard","question":"What does '한테' indicate?","korean":"한테","options":["Location","To (a person) / from (a person)","Possession","Time"],"answer":1,"explanation":"'한테' marks the recipient or source of an action with people."},

    # ── CULTURE ───────────────────────────────────────────────────────────────
    {"category":"Culture","difficulty":"easy","question":"What is 'Hangul'?","korean":"한글","options":["Korean food","Korean alphabet","Korean money","Korean flag"],"answer":1,"explanation":"Hangul (한글) is the Korean writing system, created in 1443 by King Sejong."},
    {"category":"Culture","difficulty":"easy","question":"What is 'Kimchi'?","korean":"김치","options":["A Korean dance","A fermented vegetable dish","A type of noodle","A Korean drama"],"answer":1,"explanation":"Kimchi is a traditional Korean fermented dish, usually made with cabbage."},
    {"category":"Culture","difficulty":"medium","question":"What is '추석'?","korean":"추석","options":["New Year","Harvest festival","Buddha's birthday","Independence Day"],"answer":1,"explanation":"Chuseok (추석) is a major Korean harvest festival, similar to Thanksgiving."},
    {"category":"Culture","difficulty":"easy","question":"What is 'Taekwondo'?","korean":"태권도","options":["Korean food","Korean martial art","Korean dance","Korean music"],"answer":1,"explanation":"Taekwondo (태권도) is Korea's national martial art and Olympic sport."},
    {"category":"Culture","difficulty":"medium","question":"What is '설날'?","korean":"설날","options":["Harvest festival","Korean New Year","Children's Day","Independence Day"],"answer":1,"explanation":"Seollal (설날) is the Korean Lunar New Year — one of the biggest holidays."},
    {"category":"Culture","difficulty":"medium","question":"What is 'Bibimbap'?","korean":"비빔밥","options":["A Korean soup","Mixed rice dish","Grilled meat","Spicy noodles"],"answer":1,"explanation":"Bibimbap (비빔밥) is a popular Korean dish of rice mixed with vegetables, meat, and gochujang."},
    {"category":"Culture","difficulty":"easy","question":"What is 'Hanbok'?","korean":"한복","options":["Korean house","Traditional Korean clothing","Korean ceremony","Korean instrument"],"answer":1,"explanation":"Hanbok (한복) is the traditional Korean clothing worn on special occasions."},
    {"category":"Culture","difficulty":"medium","question":"Who created Hangul?","korean":"","options":["King Taejo","King Sejong","King Gojong","King Seonjo"],"answer":1,"explanation":"King Sejong the Great created Hangul in 1443 during the Joseon Dynasty."},
    {"category":"Culture","difficulty":"medium","question":"What does '빨리빨리' culture refer to?","korean":"빨리빨리","options":["Slowness and patience","Fast-paced, hurry-up culture","Respect for elders","Hard work ethic"],"answer":1,"explanation":"'빨리빨리' (ppalli ppalli) means 'hurry hurry' — it reflects Korea's fast-paced culture."},
    {"category":"Culture","difficulty":"hard","question":"What is 'Nunchi'?","korean":"눈치","options":["A Korean game","Reading social cues and situations","A type of food","A traditional dance"],"answer":1,"explanation":"Nunchi (눈치) is the Korean concept of reading the room and understanding others' feelings."},
    {"category":"Culture","difficulty":"medium","question":"What is 'Ramyeon'?","korean":"라면","options":["Korean BBQ","Korean instant noodles","Rice cake","Dumplings"],"answer":1,"explanation":"Ramyeon (라면) is Korean instant noodles — a beloved comfort food."},
    {"category":"Culture","difficulty":"easy","question":"What is 'Samgyeopsal'?","korean":"삼겹살","options":["Grilled pork belly","Grilled beef","Grilled chicken","Grilled fish"],"answer":0,"explanation":"Samgyeopsal (삼겹살) is grilled pork belly — a very popular Korean BBQ dish."},
    {"category":"Culture","difficulty":"medium","question":"What is the Korean age system?","korean":"","options":["Same as international age","Everyone starts at age 1 and ages on New Year","Ages counted from birth month","Ages counted in lunar calendar only"],"answer":1,"explanation":"In the traditional Korean age system, everyone is 1 year old at birth and gains a year on New Year's Day."},
    {"category":"Culture","difficulty":"hard","question":"What is 'Jeong' in Korean culture?","korean":"정","options":["Respect for teachers","Deep emotional bond/attachment","Competitive spirit","Work ethic"],"answer":1,"explanation":"'Jeong' (정) is a deep emotional bond or attachment between people — a uniquely Korean concept."},
    {"category":"Culture","difficulty":"medium","question":"What is 'Norebang'?","korean":"노래방","options":["A Korean restaurant","Private karaoke room","Street food market","Dance studio"],"answer":1,"explanation":"Norebang (노래방) means 'song room' — private karaoke booths where groups sing together."},
    {"category":"Culture","difficulty":"easy","question":"What is 'Tteok'?","korean":"떡","options":["Korean candy","Korean rice cake","Korean fried rice","Korean soup"],"answer":1,"explanation":"Tteok (떡) is Korean rice cake, used in many traditional dishes and celebrations."},
    {"category":"Culture","difficulty":"medium","question":"What is '한옥'?","korean":"한옥","options":["Modern apartment","Traditional Korean house","Government building","Temple"],"answer":1,"explanation":"Hanok (한옥) is a traditional Korean house, known for its elegant curved roofs."},
    {"category":"Culture","difficulty":"hard","question":"What does '눈치가 빠르다' mean?","korean":"눈치가 빠르다","options":["Quick feet","Good at reading situations","Fast reader","Sharp eyes"],"answer":1,"explanation":"'눈치가 빠르다' means to be quick at reading social situations and others' feelings."},
    {"category":"Culture","difficulty":"medium","question":"What is 'Soju'?","korean":"소주","options":["Korean beer","Korean traditional liquor","Korean tea","Korean soft drink"],"answer":1,"explanation":"Soju (소주) is a clear Korean distilled liquor — the world's best-selling spirit."},
    {"category":"Culture","difficulty":"easy","question":"What is '태극기'?","korean":"태극기","options":["Korean anthem","Korean flag","Korean seal","Korean currency"],"answer":1,"explanation":"Taegukgi (태극기) is the national flag of South Korea."},
    {"category":"Culture","difficulty":"medium","question":"What is 'Hallyu'?","korean":"한류","options":["Korean food wave","Korean Wave — spread of Korean pop culture","Korean language","Korean history"],"answer":1,"explanation":"Hallyu (한류) means the Korean Wave — the global spread of Korean pop culture including K-pop, K-drama, and food."},

    # ── K-POP ────────────────────────────────────────────────────────────────
    {"category":"K-Pop","difficulty":"easy","question":"Which group sings 'Dynamite'?","korean":"","options":["BLACKPINK","EXO","BTS","TWICE"],"answer":2,"explanation":"BTS released 'Dynamite' in 2020 — their first all-English song."},
    {"category":"K-Pop","difficulty":"medium","question":"What does '사랑해' mean?","korean":"사랑해","options":["I miss you","I love you","I hate you","I'm happy"],"answer":1,"explanation":"'사랑해' (saranghae) means 'I love you' in informal Korean."},
    {"category":"K-Pop","difficulty":"medium","question":"Which girl group is known for 'How You Like That'?","korean":"","options":["TWICE","aespa","BLACKPINK","Red Velvet"],"answer":2,"explanation":"'How You Like That' is by BLACKPINK, released in 2020."},
    {"category":"K-Pop","difficulty":"hard","question":"What does 'daebak' mean?","korean":"대박","options":["Boring","Awesome/jackpot","Goodbye","Let's eat"],"answer":1,"explanation":"'대박' (daebak) means 'awesome' or 'jackpot' — used widely in K-pop fandoms."},
    {"category":"K-Pop","difficulty":"easy","question":"What does 'oppa' mean?","korean":"오빠","options":["Younger brother","Older brother (said by females)","Friend","Teacher"],"answer":1,"explanation":"'오빠' (oppa) is used by females to address older males — popular in K-pop fan culture."},
    {"category":"K-Pop","difficulty":"medium","question":"What does 'maknae' mean?","korean":"막내","options":["Oldest member","Middle member","Youngest member","Leader"],"answer":2,"explanation":"'막내' (maknae) means the youngest member of a group."},
    {"category":"K-Pop","difficulty":"medium","question":"What is a 'comeback' in K-pop?","korean":"","options":["Returning from hiatus","Releasing new music/album","Winning an award","Going on tour"],"answer":1,"explanation":"In K-pop, a 'comeback' refers to a group releasing new music, even if they never went away."},
    {"category":"K-Pop","difficulty":"easy","question":"What does 'fighting' (파이팅) mean in Korean?","korean":"파이팅","options":["Let's fight","Good luck / You can do it","I'm angry","Goodbye"],"answer":1,"explanation":"'파이팅' (paiting) is a cheer meaning 'good luck' or 'you can do it'."},
    {"category":"K-Pop","difficulty":"medium","question":"What is an 'idol' in K-pop?","korean":"","options":["A god","A K-pop singer/performer","A fan","A songwriter"],"answer":1,"explanation":"An 'idol' in K-pop refers to a trained singer/performer who debuts under an entertainment company."},
    {"category":"K-Pop","difficulty":"hard","question":"What does 'sasaeng' mean?","korean":"사생팬","options":["Loyal fan","Obsessive/stalker fan","New fan","Casual fan"],"answer":1,"explanation":"'사생팬' (sasaengpaen) refers to obsessive fans who invade idols' privacy."},
    {"category":"K-Pop","difficulty":"medium","question":"Which group has members RM, Jin, Suga, J-Hope, Jimin, V, and Jungkook?","korean":"","options":["EXO","GOT7","BTS","MONSTA X"],"answer":2,"explanation":"BTS (방탄소년단) has these seven members and is one of the biggest K-pop groups globally."},
    {"category":"K-Pop","difficulty":"easy","question":"What does 'unnie' mean?","korean":"언니","options":["Older sister (said by females)","Younger sister","Mother","Friend"],"answer":0,"explanation":"'언니' (unnie) is used by females to address older females."},
    {"category":"K-Pop","difficulty":"medium","question":"What is a 'fansite master'?","korean":"","options":["Official fan club manager","Fan who takes professional photos of idols","Fan who runs the official website","Fan who organizes concerts"],"answer":1,"explanation":"A fansite master is a fan who professionally photographs idols at events and shares photos."},
    {"category":"K-Pop","difficulty":"hard","question":"What does 'bias' mean in K-pop fan culture?","korean":"","options":["Least favorite member","Favorite member","Random member","Group leader"],"answer":1,"explanation":"Your 'bias' is your favorite member of a K-pop group."},
    {"category":"K-Pop","difficulty":"medium","question":"What is 'aegyo'?","korean":"애교","options":["Angry behavior","Cute/baby-like behavior to charm others","Formal speech","Dance moves"],"answer":1,"explanation":"'애교' (aegyo) means acting cute or baby-like to charm others — very common in K-pop."},
    {"category":"K-Pop","difficulty":"easy","question":"Which company is BTS under?","korean":"","options":["SM Entertainment","JYP Entertainment","YG Entertainment","HYBE (Big Hit)"],"answer":3,"explanation":"BTS is under HYBE (formerly Big Hit Entertainment)."},
    {"category":"K-Pop","difficulty":"medium","question":"What does 'fanchant' mean?","korean":"","options":["A fan's favorite song","Choreographed chants fans do during performances","Fan club name","Fan letter"],"answer":1,"explanation":"A fanchant is a specific chant or call-and-response that fans do during live performances."},
    {"category":"K-Pop","difficulty":"hard","question":"What is a 'light stick'?","korean":"","options":["A concert ticket","Official fan merchandise glowing stick used at concerts","A phone app","A fan badge"],"answer":1,"explanation":"A light stick is official fan merchandise — a glowing wand fans wave at concerts, unique to each group."},
    {"category":"K-Pop","difficulty":"medium","question":"What does 'visual' mean in K-pop?","korean":"","options":["The main dancer","The member considered the most attractive","The main vocalist","The rapper"],"answer":1,"explanation":"The 'visual' is the member considered the most attractive or the face of the group."},
    {"category":"K-Pop","difficulty":"easy","question":"What does 'noona' mean?","korean":"누나","options":["Younger sister","Older sister (said by males)","Female friend","Mother"],"answer":1,"explanation":"'누나' (noona) is used by males to address older females."},
    {"category":"K-Pop","difficulty":"hard","question":"What is a 'disbandment' in K-pop?","korean":"","options":["Going on vacation","A group officially ending their activities together","Taking a break","Changing agency"],"answer":1,"explanation":"Disbandment means a K-pop group officially ends their activities as a group."},
]

# ─────────────────────────────────────────────
# Leaderboard (file-based)
# ─────────────────────────────────────────────
SCORES_FILE = "scores.json"

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as f:
            return json.load(f)
    return []

def save_scores(scores):
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)

def add_score(name, score):
    scores = load_scores()
    scores.append({
        "name": name,
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    save_scores(scores)

# ─────────────────────────────────────────────
# Session State Init
# ─────────────────────────────────────────────
if "game_state" not in st.session_state:
    st.session_state.game_state = "start"  # start | playing | result
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current" not in st.session_state:
    st.session_state.current = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "score_saved" not in st.session_state:
    st.session_state.score_saved = False

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🇰🇷 DumbQuiz</div>
    <div class="hero-sub">Korean Language Quiz Game</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# START SCREEN
# ─────────────────────────────────────────────
if st.session_state.game_state == "start":
    st.markdown("""
    <div class="question-card" style="text-align:center;">
        <div style="font-size:3rem; margin-bottom:12px;">🇰🇷</div>
        <div style="font-size:1.3rem; font-weight:600; margin-bottom:8px;">Ready to test your Korean?</div>
        <div style="color:#666; margin-bottom:20px;">20 questions · Vocabulary, Grammar, Culture, K-Pop · Mixed difficulty</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Quiz", use_container_width=True):
            st.session_state.questions = random.sample(ALL_QUESTIONS, min(20, len(ALL_QUESTIONS)))
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.selected = None
            st.session_state.score_saved = False
            st.session_state.game_state = "playing"
            st.rerun()

    # Show leaderboard on start screen
    scores = load_scores()
    if scores:
        st.markdown("---")
        st.markdown("### 🏆 High Scores")
        for i, s in enumerate(scores):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            st.markdown(f"""
            <div class="lb-row">
                <span class="lb-rank">{medal}</span>
                <span class="lb-name">{s['name']}</span>
                <span class="lb-score">{s['score']}/20</span>
                <span style="color:#444; font-size:0.8rem; margin-left:8px;">{s['date']}</span>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLAYING SCREEN
# ─────────────────────────────────────────────
elif st.session_state.game_state == "playing":
    q = st.session_state.questions[st.session_state.current]
    qnum = st.session_state.current + 1

    # Progress bar
    st.progress(qnum / 20)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="progress-text">Question {qnum}/20</div>', unsafe_allow_html=True)
    with col2:
        diff_class = f"diff-{q['difficulty']}"
        st.markdown(f'<div style="text-align:center"><span class="{diff_class}">{q["difficulty"]}</span></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="progress-text" style="text-align:right;">Score: {st.session_state.score}</div>', unsafe_allow_html=True)

    # Question card
    korean_html = f'<div class="q-korean">{q["korean"]}</div>' if q["korean"] else ""
    st.markdown(f"""
    <div class="question-card">
        <div class="q-category">{q['category']}</div>
        <div class="q-text">{q['question']}</div>
        {korean_html}
    </div>
    """, unsafe_allow_html=True)

    # Answer options
    if not st.session_state.answered:
        cols = st.columns(2)
        for i, option in enumerate(q["options"]):
            with cols[i % 2]:
                if st.button(option, key=f"opt_{i}", use_container_width=True):
                    st.session_state.answered = True
                    st.session_state.selected = i
                    if i == q["answer"]:
                        st.session_state.score += 1
                    st.rerun()
    else:
        # Show results
        selected = st.session_state.selected
        correct = selected == q["answer"]

        cols = st.columns(2)
        for i, option in enumerate(q["options"]):
            with cols[i % 2]:
                if i == q["answer"]:
                    st.success(f"✓ {option}")
                elif i == selected and not correct:
                    st.error(f"✗ {option}")
                else:
                    st.button(option, key=f"opt_shown_{i}", disabled=True, use_container_width=True)

        # Feedback
        if correct:
            st.markdown('<div class="correct-box">✓ Correct! Well done!</div>', unsafe_allow_html=True)
        else:
            correct_ans = q["options"][q["answer"]]
            st.markdown(f'<div class="wrong-box">✗ Wrong. The correct answer is: <strong>{correct_ans}</strong></div>', unsafe_allow_html=True)

        st.markdown(f'<div class="explanation">💡 {q["explanation"]}</div>', unsafe_allow_html=True)

        # Next button
        st.markdown("<br>", unsafe_allow_html=True)
        btn_label = "See Results 🎉" if qnum == 20 else "Next Question →"
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(btn_label, use_container_width=True):
                st.session_state.current += 1
                st.session_state.answered = False
                st.session_state.selected = None
                if st.session_state.current >= 20:
                    st.session_state.game_state = "result"
                st.rerun()

# ─────────────────────────────────────────────
# RESULT SCREEN
# ─────────────────────────────────────────────
elif st.session_state.game_state == "result":
    score = st.session_state.score
    pct = score / 20

    if pct >= 0.9:
        grade = "🏆 Expert — 한국어 고수!"
        grade_color = "#4ade80"
    elif pct >= 0.7:
        grade = "⭐ Advanced — 잘했어요!"
        grade_color = "#fbbf24"
    elif pct >= 0.5:
        grade = "👍 Intermediate — 괜찮아요!"
        grade_color = "#6C63FF"
    else:
        grade = "💪 Beginner — 파이팅!"
        grade_color = "#f87171"

    st.markdown(f"""
    <div class="score-card">
        <div class="big-score">{score}/20</div>
        <div style="color:#666; margin: 8px 0;">You answered {score} out of 20 correctly</div>
        <div style="color:{grade_color}; font-weight:600; font-size:1.1rem; margin-top:8px;">{grade}</div>
    </div>
    """, unsafe_allow_html=True)

    # Save score
    if not st.session_state.score_saved:
        st.markdown("### 🏆 Save your score")
        name = st.text_input("Enter your name", placeholder="Your name...", max_chars=20)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Score", use_container_width=True):
                if name.strip():
                    add_score(name.strip(), score)
                    st.session_state.score_saved = True
                    st.rerun()
                else:
                    st.warning("Please enter your name")
        with col2:
            if st.button("Skip", use_container_width=True):
                st.session_state.score_saved = True
                st.rerun()

    # Leaderboard
    st.markdown("### 🏆 High Scores")
    scores = load_scores()
    if scores:
        for i, s in enumerate(scores):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
            st.markdown(f"""
            <div class="lb-row">
                <span class="lb-rank">{medal}</span>
                <span class="lb-name">{s['name']}</span>
                <span class="lb-score">{s['score']}/20</span>
                <span style="color:#444; font-size:0.8rem; margin-left:8px;">{s['date']}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:#666; font-size:0.9rem;">No scores yet!</div>', unsafe_allow_html=True)

    # Play again
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.game_state = "start"
            st.session_state.score_saved = False
            st.rerun()

# Footer
st.markdown("""
<div style="text-align:center; color:#333; font-size:0.8rem; margin-top:48px; padding-top:16px; border-top:1px solid #1a1a2e;">
    DumbQuiz · Korean Language Game · Team Aatank Capstone Project
</div>
""", unsafe_allow_html=True)
