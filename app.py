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
    {"category": "Vocabulary", "difficulty": "easy",
     "question": "What does '안녕하세요' mean?", "korean": "안녕하세요",
     "options": ["Hello", "Goodbye", "Thank you", "Sorry"], "answer": 0,
     "explanation": "'안녕하세요' (annyeonghaseyo) is the formal way to say hello in Korean."},

    {"category": "Vocabulary", "difficulty": "easy",
     "question": "How do you say 'thank you' in Korean?", "korean": "",
     "options": ["괜찮아요", "감사합니다", "미안해요", "좋아요"], "answer": 1,
     "explanation": "'감사합니다' (gamsahamnida) means thank you in formal Korean."},

    {"category": "Vocabulary", "difficulty": "easy",
     "question": "What does '물' mean?", "korean": "물",
     "options": ["Fire", "Water", "Food", "Rice"], "answer": 1,
     "explanation": "'물' (mul) means water in Korean."},

    {"category": "Vocabulary", "difficulty": "easy",
     "question": "What does '밥' mean?", "korean": "밥",
     "options": ["Soup", "Noodles", "Rice/Meal", "Bread"], "answer": 2,
     "explanation": "'밥' (bap) means cooked rice or a meal in Korean."},

    {"category": "Vocabulary", "difficulty": "medium",
     "question": "What does '어디예요?' mean?", "korean": "어디예요?",
     "options": ["What is it?", "Where is it?", "How much?", "When is it?"], "answer": 1,
     "explanation": "'어디예요?' (eodiyeyo?) means 'Where is it?' in Korean."},

    {"category": "Vocabulary", "difficulty": "medium",
     "question": "What does '얼마예요?' mean?", "korean": "얼마예요?",
     "options": ["How many?", "What time?", "How much?", "How far?"], "answer": 2,
     "explanation": "'얼마예요?' (eolmayeyo?) means 'How much is it?' — very useful for shopping!"},

    {"category": "Vocabulary", "difficulty": "medium",
     "question": "Which word means 'delicious'?", "korean": "",
     "options": ["맛있어요", "맛없어요", "배고파요", "배불러요"], "answer": 0,
     "explanation": "'맛있어요' (masisseoyo) means delicious. '맛없어요' means not tasty."},

    {"category": "Vocabulary", "difficulty": "hard",
     "question": "What does '괜찮아요' mean?", "korean": "괜찮아요",
     "options": ["I'm hungry", "I'm tired", "It's okay / I'm fine", "I'm busy"], "answer": 2,
     "explanation": "'괜찮아요' (gwaenchanayo) means 'it's okay' or 'I'm fine'."},

    {"category": "Vocabulary", "difficulty": "hard",
     "question": "What does '피곤해요' mean?", "korean": "피곤해요",
     "options": ["I'm hungry", "I'm happy", "I'm tired", "I'm cold"], "answer": 2,
     "explanation": "'피곤해요' (pigonhaeyo) means 'I'm tired' in Korean."},

    {"category": "Vocabulary", "difficulty": "medium",
     "question": "What is '학교' in English?", "korean": "학교",
     "options": ["Hospital", "School", "Library", "Restaurant"], "answer": 1,
     "explanation": "'학교' (hakgyo) means school in Korean."},

    {"category": "Grammar", "difficulty": "easy",
     "question": "In Korean, where does the verb go in a sentence?", "korean": "",
     "options": ["Beginning", "Middle", "End", "Anywhere"], "answer": 2,
     "explanation": "Korean is Subject-Object-Verb (SOV). The verb always comes at the end."},

    {"category": "Grammar", "difficulty": "medium",
     "question": "Which ending makes a verb polite/formal?", "korean": "",
     "options": ["-다", "-아/어요", "-고싶다", "-지마"], "answer": 1,
     "explanation": "The '-아/어요' ending makes verbs polite. 가다 (to go) → 가요 (goes, politely)."},

    {"category": "Grammar", "difficulty": "medium",
     "question": "What does '이다' mean as a verb?", "korean": "이다",
     "options": ["To do", "To be", "To go", "To eat"], "answer": 1,
     "explanation": "'이다' is the Korean equivalent of 'to be'."},

    {"category": "Grammar", "difficulty": "hard",
     "question": "What particle marks the subject of a sentence?", "korean": "",
     "options": ["을/를", "에서", "이/가", "의"], "answer": 2,
     "explanation": "'이/가' marks the subject. '을/를' marks the object. '에서' marks location."},

    {"category": "Grammar", "difficulty": "hard",
     "question": "How do you make a verb negative in Korean?", "korean": "",
     "options": ["Add 안 before the verb", "Add 못 after the verb", "Change the ending to -없다", "Add 아니 at the end"], "answer": 0,
     "explanation": "Adding '안' before a verb makes it negative. 가요 (go) → 안 가요 (don't go)."},

    {"category": "Culture", "difficulty": "easy",
     "question": "What is 'Hangul'?", "korean": "한글",
     "options": ["Korean food", "Korean alphabet", "Korean money", "Korean flag"], "answer": 1,
     "explanation": "Hangul (한글) is the Korean writing system, created in 1443 by King Sejong."},

    {"category": "Culture", "difficulty": "easy",
     "question": "What is 'Kimchi'?", "korean": "김치",
     "options": ["A Korean dance", "A fermented vegetable dish", "A type of noodle", "A Korean drama"], "answer": 1,
     "explanation": "Kimchi is a traditional Korean fermented dish, usually made with cabbage."},

    {"category": "Culture", "difficulty": "medium",
     "question": "What is '추석'?", "korean": "추석",
     "options": ["New Year", "Harvest festival", "Buddha's birthday", "Independence Day"], "answer": 1,
     "explanation": "Chuseok (추석) is a major Korean harvest festival, similar to Thanksgiving."},

    {"category": "K-Pop", "difficulty": "easy",
     "question": "Which group sings 'Dynamite'?", "korean": "",
     "options": ["BLACKPINK", "EXO", "BTS", "TWICE"], "answer": 2,
     "explanation": "BTS released 'Dynamite' in 2020 — their first all-English song."},

    {"category": "K-Pop", "difficulty": "medium",
     "question": "What does '사랑해' mean?", "korean": "사랑해",
     "options": ["I miss you", "I love you", "I hate you", "I'm happy"], "answer": 1,
     "explanation": "'사랑해' (saranghae) means 'I love you' in informal Korean."},
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
            st.session_state.questions = random.sample(ALL_QUESTIONS, len(ALL_QUESTIONS))
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
