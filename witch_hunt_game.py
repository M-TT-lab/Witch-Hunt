# Streamlit Version of Witch Hunt Game
import random
import streamlit as st
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title="Witch Hunt Game", layout="centered")
theme_style = "https://images.unsplash.com/photo-1519681393784-d120267933ba" if "Salem" in theme else "https://images.unsplash.com/photo-1532009877282-3340270e0529"

css_dark_class = 'dark-mode' if dark_mode else 'light-mode'

st.markdown(f"""
<style>
    body {{
        background-image: url('{theme_style}');
        background-size: cover;
        background-attachment: fixed;
    }}
    .stApp {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 12px;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        animation: fadein 1.5s ease-in;
    }}
    .stButton>button:hover {{
        background-color: #fffbeb !important;
        color: #1f2937 !important;
        font-weight: bold;
        transition: 0.3s ease;
    }}
    .stTextInput>div>input:hover {{
        border-color: #a855f7;
        background-color: #f3e8ff;
    }}
    @keyframes fadein {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    body[data-theme='dark'] {{
        background-color: #1a1a1a;
        color: #e0e0e0;
    }}
    .light-mode {{
        background-color: rgba(255, 255, 255, 0.85);
    }}
    .dark-mode {{
        background-color: rgba(30, 30, 30, 0.9);
    }}
</style>
""", unsafe_allow_html=True)
st.markdown(f"<div class='{css_dark_class}'>", unsafe_allow_html=True)
st.image("https://images.unsplash.com/photo-1532274402917-5aadf881bdf3", use_column_width=True)
theme_color = "#531dab" if "Salem" in theme else "#1e3a8a"
st.markdown(f"""
<div style='background-color:{theme_color}; padding:1rem; border-radius:10px; color:white; text-align:center;'>
<h2>🧙‍♀️ Witch Hunt: History & Hysteria</h2>
</div>
""", unsafe_allow_html=True)
with st.expander("▶️ Start Game Instructions", expanded=True):
    st.markdown("""
    Welcome to **Witch Hunt: History & Hysteria**! This is an educational game where you will test your knowledge
    on historical events like the Salem Witch Trials and McCarthyism.

    🧠 Answer questions to advance levels. 
    💥 Use power-ups wisely. 
    📘 Reflect, learn, and explore historical timelines.

    Click below to begin!
    """)

# Session state init
if 'player' not in st.session_state:
    st.session_state.player = {
        'health': 3,
        'score': 0,
        'level': 1,
        'power_ups': {'skip': 3, 'double_points': 3},
        'powered_up': False,
        'achievements': set(),
        'journal': [],
        'correct': [],
        'incorrect': [],
        'used_questions': set(),
        'review': []
    }

player = st.session_state.player

edu_facts = [
    "McCarthyism: Accusations without evidence in 1950s America.",
    "The Salem Witch Trials: Fear and superstition led to executions.",
    "Women were often the main targets in both eras.",
    "HUAC investigated Hollywood for communist ties.",
    "Senator McCarthy's accusations lacked concrete evidence.",
    "The Red Scare caused widespread paranoia.",
    "Many innocent people were blacklisted in the 1950s.",
    "Puritan society was deeply religious and patriarchal.",
    "Accusations in Salem were based on superstition, not facts.",
    "Joseph McCarthy was eventually censured by the Senate in 1954.",
    "The term 'witch hunt' became a metaphor for political persecution."
]

quiz_questions = defaultdict(list)
quiz_questions.update({
    "hard": [
        {"question": "What type of evidence was commonly used in the Salem Witch Trials?", "answer": "Spectral evidence", "hint": "Relies on ghostly visions."},
        {"question": "Who wrote 'The Crucible' as an allegory for McCarthyism?", "answer": "Arthur Miller", "hint": "Famous American playwright."},
        {"question": "What amendment protects against self-incrimination, often cited during McCarthyism?", "answer": "Fifth Amendment", "hint": "Part of the Bill of Rights."},
        {"question": "What year was McCarthy censured by the Senate?", "answer": "1954", "hint": "Mid-1950s."},
        {"question": "Which doctrine justified actions taken to stop communism globally?", "answer": "Truman Doctrine", "hint": "Named after a U.S. President."},
        {"question": "What act required Communist organizations to register with the government?", "answer": "McCarran Act", "hint": "Named after a Nevada Senator."},
        {"question": "Which journalist famously challenged McCarthy on television?", "answer": "Edward R. Murrow", "hint": "Broadcasted 'See It Now'."},
        {"question": "What public institution was heavily targeted by McCarthy for supposed communists?", "answer": "Army", "hint": "Led to televised hearings."}
    ],
    "ultra-hard": [
        {"question": "Which Supreme Court case in 1957 limited the power of HUAC by protecting First Amendment rights?", "answer": "Watkins v. United States", "hint": "Case involving labor union witness."},
        {"question": "What prominent African American actor was blacklisted due to alleged communist ties?", "answer": "Paul Robeson", "hint": "Also a famous singer and civil rights activist."},
        {"question": "What was the name of the FBI program that surveilled political dissidents during McCarthyism?", "answer": "COINTELPRO", "hint": "Counter Intelligence Program."},
        {"question": "Which author of 'Darkness at Noon' was cited by anti-communist groups as a depiction of Soviet totalitarianism?", "answer": "Arthur Koestler", "hint": "Wrote a famous political novel in the 1940s."},
        {"question": "Which historian famously coined the term 'The Paranoid Style in American Politics'?", "answer": "Richard Hofstadter", "hint": "Columbia University historian."}
    ],
    "easy": [
        {"question": "Who led the anti-communist movement in the 1950s?", "answer": "McCarthy", "hint": "His first name was Joseph."},
        {"question": "What trials happened in 1692 in Massachusetts?", "answer": "Salem", "hint": "They are famously known as witch trials."},
        {"question": "Which group was targeted during McCarthyism in Hollywood?", "answer": "Communists", "hint": "Starts with 'C', associated with USSR ideology."},
        {"question": "What does HUAC stand for?", "answer": "House Un-American Activities Committee", "hint": "Long version of HUAC."},
        {"question": "What kind of political system was McCarthyism trying to root out?", "answer": "Communism", "hint": "Opposite of capitalism."},
        {"question": "What does the term 'Red Scare' refer to?", "answer": "Fear of communism", "hint": "Linked to communism and Soviet threat."},
        {"question": "Which century did the Salem Witch Trials occur?", "answer": "17th century", "hint": "1600s."},
        {"question": "What color is associated with communism?", "answer": "Red", "hint": "The color of the scare."}
    ],
    "medium": [
        {"question": "What was HUAC investigating?", "answer": "Un-American", "hint": "Un-____ Activities Committee."},
        {"question": "Which ideology was McCarthyism aimed at suppressing?", "answer": "Communism", "hint": "Ideology from Karl Marx."},
        {"question": "What 17th-century belief fueled the Salem Witch Trials?", "answer": "Superstition", "hint": "Often based on irrational fear."},
        {"question": "What religion dominated Salem during the trials?", "answer": "Puritanism", "hint": "Very strict, fundamentalist Christian group."},
        {"question": "What did people fear would infiltrate the government during the Red Scare?", "answer": "Communists", "hint": "They were suspected spies."},
        {"question": "Which U.S. president served during the height of McCarthyism?", "answer": "Dwight Eisenhower", "hint": "34th U.S. President."},
        {"question": "Who was accused of spying and convicted during McCarthyism?", "answer": "Alger Hiss", "hint": "He denied but was convicted of perjury."},
        {"question": "What was the name of the Hollywood group who refused to testify?", "answer": "Hollywood Ten", "hint": "They were jailed for contempt."}
})

# --- Timeline Events ---
timeline_events = {
    3: "📜 1692: Salem Witch Trials escalate.",
    5: "📜 1938: HUAC is formed.",
    7: "📜 1947: Hollywood Ten refuse to testify.",
    10: "📜 1950: McCarthy delivers his infamous speech.",
    12: "📜 1954: McCarthy is censured by the Senate.",
    15: "📜 1957: Supreme Court limits HUAC powers."
}

# --- Track correct streak for earnable power-ups ---
if 'correct_streak' not in st.session_state:
    st.session_state.correct_streak = 0

# --- Achievements Tracker ---
achievements_awarded = {
    'First Victory': False,
    'Historian': False,
    'Perfect Start': False
}


    if level <= 3:
        diff = "easy"
    elif level <= 6:
        diff = "medium"
    else:
        diff = "easy"
    unused = [q for q in quiz_questions[diff] if q['question'] not in player['used_questions']]
    if not unused:
        player['used_questions'].clear()
        unused = quiz_questions[diff]
    q = random.choice(unused)
    player['used_questions'].add(q['question'])
    return q

dark_mode = st.sidebar.toggle("🌗 Dark Mode")

st.sidebar.header("📋 Game Setup 🧩")
mode = st.sidebar.selectbox("🎮 Select Mode", ["🧭 Classic", "💣 Survival", "⏱️ Timed"])
theme = st.sidebar.radio("🏺 Historical Theme", ["🔮 Salem Witch Trials", "📺 McCarthyism"])

st.markdown(f"### 🧭 Level {player['level']} | ❤️ Health: {player['health']} | 🧠 Score: {player['score']}")

fact = random.choice(edu_facts)
st.info(fact)

if 'current_question' not in st.session_state:
    st.session_state.current_question = select_question(player['level'])

q = st.session_state.current_question

st.markdown("""
<div style='background-color:#f0f0f5; padding:1rem; border-radius:10px;'>
""")
difficulty_colors = {"easy": "#d4edda", "medium": "#fff3cd", "hard": "#f8d7da", "ultra-hard": "#cce5ff"}
level_key = "easy" if player['level'] <= 3 else "medium" if player['level'] <= 6 else "hard" if player['level'] <= 9 else "ultra-hard"
color = difficulty_colors[level_key]

theme_colors = {"Salem": "#f9f0ff", "McCarthyism": "#e6f7ff"}
theme_label = "Salem" if "Salem" in theme else "McCarthyism"
theme_bg = theme_colors[theme_label]

st.markdown(f"<div style='background-color:{theme_bg}; padding:1rem; border-radius:10px;'>", unsafe_allow_html=True)

difficulty_icons = {"easy": "🟢", "medium": "🟡", "hard": "🔴", "ultra-hard": "💀"}
diff_icon = difficulty_icons.get(level_key, "❓")
st.subheader(f"{diff_icon} {q['question']}")
if 'theme' in q:
    st.caption(f"🗂️ Theme: {q['theme']}")
if 'explanation' in q:
    st.caption(f"📘 Explanation: {q['explanation']}")
st.caption(f"Hint: {q['hint']}")
st.markdown("</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    use_skip = st.button("⏭️ Use Skip")
with col2:
    use_double = st.button("💥 Double Points")

if use_skip and player['power_ups']['skip'] > 0:
    player['power_ups']['skip'] -= 1
    st.success("Skipped! New question loaded.")
    st.session_state.current_question = select_question(player['level'])
    st.experimental_rerun()

if use_double and player['power_ups']['double_points'] > 0:
    player['powered_up'] = True
    player['power_ups']['double_points'] -= 1
    st.info("Double points activated!")

answer = st.text_input("Your answer")
if st.button("Submit"):
    if q['answer'].lower() in answer.lower():
        st.success("✅ Correct!")
        score = 10 * (2 if player['powered_up'] else 1)
        player['score'] += score
        player['correct'].append(q)
        player['journal'].append(f"✔️ {q['question']} — {q['answer']}")
    else:
        st.error(f"❌ Incorrect. The correct answer was: {q['answer']}")
        player['health'] -= 1
        player['incorrect'].append(q)
        player['review'].append(q)
        player['journal'].append(f"✖️ {q['question']} — {q['answer']}")
        st.session_state.correct_streak = st.session_state.correct_streak + 1 if q['answer'].lower() in answer.lower() else 0

    # Earn power-ups after 3 correct in a row
    if st.session_state.correct_streak and st.session_state.correct_streak % 3 == 0:
        player['power_ups']['skip'] += 1
        player['power_ups']['double_points'] += 1
        st.balloons()
        st.success("🎉 Bonus power-up earned for a 3-question streak!")

    # Timeline milestones
    if player['level'] in timeline_events:
        st.info(timeline_events[player['level']])

    # Achievements
    if not achievements_awarded['First Victory'] and player['level'] > 1:
        player['achievements'].add("🏆 First Victory")
        achievements_awarded['First Victory'] = True
        st.success("🏆 Achievement Unlocked: First Victory")

    if not achievements_awarded['Historian'] and player['score'] >= 100:
        player['achievements'].add("🏆 Historian")
        achievements_awarded['Historian'] = True
        st.success("🏆 Achievement Unlocked: Historian")

    if not achievements_awarded['Perfect Start'] and player['level'] >= 5 and player['health'] == 3:
        player['achievements'].add("🏆 Perfect Start")
        achievements_awarded['Perfect Start'] = True
        st.success("🏆 Achievement Unlocked: Perfect Start")

    # Level 10 revive
    if player['level'] == 10:
        player['health'] += 1
        st.success("💖 Bonus life awarded for reaching Level 10!")

    player['powered_up'] = False
    player['level'] += 1
    st.session_state.current_question = select_question(player['level'])
    st.experimental_rerun()

if player['health'] <= 0:
    st.markdown("## 💀 Game Over")
    st.markdown(f"### Final Score: {player['score']}")
    st.markdown("### 🏆 Achievements Unlocked:")
    if player['achievements']:
        for a in player['achievements']:
            st.markdown(f"- {a}")
    else:
        st.markdown("- No achievements unlocked yet.")

    st.markdown("### Journal:")
    for entry in player['journal']:
        st.markdown(f"- {entry}")

    st.markdown("---")
    st.markdown("### 📊 Timeline Progress")
    levels = sorted(timeline_events.keys())
    progress = ''.join(['🟩' if player['level'] > l else '⬜' for l in levels])
    st.markdown(f"**{progress}**")

    st.markdown("### 📊 Final Score Chart")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    bars = [len(player['correct']), len(player['incorrect'])]
    ax.bar(['Correct', 'Incorrect'], bars, color=['green', 'red'])
    ax.set_ylabel("Questions")
    ax.set_title("📊 Your Performance")
    st.pyplot(fig)

    st.download_button("💾 Download Journal", data='
'.