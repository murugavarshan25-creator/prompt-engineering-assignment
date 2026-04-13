import streamlit as st
import random
import time
import json
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Kids Fun Quiz", page_icon="🎉")

LEADERBOARD_FILE = "leaderboard.json"

# ---------------- LEADERBOARD ----------------
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_score(name, score):
    data = load_leaderboard()
    data.append({"name": name, "score": score})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f)

# ---------------- QUESTIONS ----------------
questions_data = {
    "Easy": [
        {"q": "What comes next: 1, 2, 3, ?", "opt": ["4", "5", "6"], "ans": "4",
         "img": "https://cdn-icons-png.flaticon.com/512/992/992700.png"},
        {"q": "Which is a fruit?", "opt": ["Carrot", "Apple", "Potato"], "ans": "Apple",
         "img": "https://cdn-icons-png.flaticon.com/512/415/415733.png"}
    ],
    "Medium": [
        {"q": "5 × 3 = ?", "opt": ["10", "15", "20"], "ans": "15",
         "img": "https://cdn-icons-png.flaticon.com/512/992/992651.png"},
        {"q": "Odd one out?", "opt": ["Dog", "Cat", "Car"], "ans": "Car",
         "img": "https://cdn-icons-png.flaticon.com/512/616/616408.png"}
    ],
    "Hard": [
        {"q": "12 ÷ 4 = ?", "opt": ["2", "3", "4"], "ans": "3",
         "img": "https://cdn-icons-png.flaticon.com/512/992/992651.png"},
        {"q": "Which planet is red?", "opt": ["Earth", "Mars", "Venus"], "ans": "Mars",
         "img": "https://cdn-icons-png.flaticon.com/512/3212/3212608.png"}
    ]
}

# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center;color:orange;'>🎉 Kids Fun Quiz 🎉</h1>", unsafe_allow_html=True)

name = st.text_input("👤 Enter your name")
mode = st.selectbox("🎮 Mode", ["Single Player", "Multiplayer"])
difficulty = st.selectbox("🎯 Difficulty", ["Easy", "Medium", "Hard"])

# ---------------- SESSION ----------------
if "questions" not in st.session_state:
    st.session_state.questions = random.sample(questions_data[difficulty], len(questions_data[difficulty]))

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

if "player" not in st.session_state:
    st.session_state.player = 1

if "scores" not in st.session_state:
    st.session_state.scores = {"P1": 0, "P2": 0}

# ---------------- TIMER ----------------
time_limit = 30
remaining = max(0, time_limit - int(time.time() - st.session_state.start_time))

st.markdown(f"⏱️ Time Left: **{remaining}s**")

# ---------------- QUIZ ----------------
answers = []

for i, q in enumerate(st.session_state.questions):
    st.markdown(f"### Q{i+1}: {q['q']}")
    st.image(q["img"], width=100)
    ans = st.radio("", q["opt"], key=f"{i}_{st.session_state.player}")
    answers.append(ans)

# ---------------- SUBMIT ----------------
if st.button("Submit"):
    score = 0

    for i, q in enumerate(st.session_state.questions):
        if answers[i] == q["ans"]:
            score += 1

    # -------- SINGLE PLAYER --------
    if mode == "Single Player":
        st.success(f"🎯 {name}, Your Score: {score}")
        save_score(name, score)

        if score == len(answers):
            st.balloons()
            st.audio("https://www.soundjay.com/human/sounds/applause-01.mp3")
            st.markdown("<h2 style='color:green;'>🌟 Perfect Score!</h2>", unsafe_allow_html=True)

        elif score >= 1:
            st.audio("https://www.soundjay.com/button/sounds/button-3.mp3")
            st.markdown("<h3 style='color:blue;'>👍 Good Job!</h3>", unsafe_allow_html=True)

        else:
            st.audio("https://www.soundjay.com/button/sounds/button-10.mp3")
            st.markdown("<h3 style='color:red;'>💡 Try Again!</h3>", unsafe_allow_html=True)

    # -------- MULTIPLAYER --------
    else:
        player_key = f"P{st.session_state.player}"
        st.session_state.scores[player_key] = score

        if st.session_state.player == 1:
            st.session_state.player = 2
            st.session_state.start_time = time.time()
            st.rerun()
        else:
            st.success(f"Player 1: {st.session_state.scores['P1']}")
            st.success(f"Player 2: {st.session_state.scores['P2']}")

            if st.session_state.scores["P1"] > st.session_state.scores["P2"]:
                st.balloons()
                st.write("🏆 Player 1 Wins!")
            elif st.session_state.scores["P2"] > st.session_state.scores["P1"]:
                st.balloons()
                st.write("🏆 Player 2 Wins!")
            else:
                st.write("🤝 It's a Tie!")

# ---------------- LEADERBOARD ----------------
st.subheader("🏆 Leaderboard")

for entry in load_leaderboard():
    st.write(f"{entry['name']} - {entry['score']}")

# ---------------- RESET ----------------
if st.button("🔄 Restart Game"):
    st.session_state.clear()
    st.rerun()