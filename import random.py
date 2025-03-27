# Witch Hunt Game – Full English Version (with Review Mode and Powers)
import random
import time
import os
from datetime import datetime
from collections import defaultdict

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

MODES = {
    "1": "classic",
    "2": "survival",
    "3": "timed"
}

class Player:
    def __init__(self):
        self.health = 3
        self.score = 0
        self.level = 1
        self.power_ups = {"skip": 3, "double_points": 3}
        self.powered_up = False
        self.achievements = set()
        self.journal = []

    def gain_score(self, base):
        multiplier = 1 + (self.level * 0.1)
        if self.powered_up:
            base *= 2
        self.score += int(base * multiplier)

    def use_power_up(self, name):
        if self.power_ups.get(name, 0) > 0:
            self.power_ups[name] -= 1
            return True
        return False

player = Player()
correct_questions = []
incorrect_questions = []
used_questions = set()
review_mode_questions = []

quiz_questions = defaultdict(list)
quiz_questions.update({
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
    ],
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
    ]
})

def choose_mode():
    print("Select game mode:")
    print("1 - Classic")
    print("2 - Survival")
    print("3 - Timed")
    return input("Enter your choice: ").strip()

def choose_theme():
    print("Select a historical theme:")
    print("1 - Salem Witch Trials")
    print("2 - McCarthyism")
    return input("Enter 1 or 2: ").strip()

def show_question(question, level, mode):
    print(f"\n🎮 Powers Available - Skip: {player.power_ups['skip']} | Double Points: {player.power_ups['double_points']}")
    print("\n🧠 Quiz Time! (Level", level, ")")
    print(question["question"])
    player.journal.append(f"Q: {question['question']}")

    if player.power_ups["skip"] > 0:
        use_skip = input("Do you want to use a SKIP power? (yes/no): ").strip().lower()
        if use_skip == "yes" and player.use_power_up("skip"):
            print("⏩ Question skipped!")
            return True

    if player.power_ups["double_points"] > 0:
        use_double = input("Use DOUBLE POINTS for this question? (yes/no): ").strip().lower()
        if use_double == "yes" and player.use_power_up("double_points"):
            print("🔥 Double points activated!")
            player.powered_up = True

    wants_hint = input("Need a hint? (yes/no): ").strip().lower()
    if wants_hint.startswith("y"):
        print(f"💡 Hint: {question['hint']}")

    if mode == "timed":
        import signal
        def handler(signum, frame):
            raise TimeoutError
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(10)
        try:
            answer = input("Answer (10s limit): ").strip().lower()
            signal.alarm(0)
        except TimeoutError:
            print("⏰ Time's up!")
            return False
    else:
        answer = input("Your answer: ").strip().lower()

    if question["answer"].lower() in answer:
        explanation = question.get("explanation")
        if explanation:
            print(f"📘 Explanation: {explanation}")
        print("✅ Correct!")
        player.gain_score(10)
        correct_questions.append(question)
        player.journal.append("✔️ Correct")
        if player.level == 1:
            player.achievements.add("🏆 First Victory")
        if player.score >= 100:
            player.achievements.add("🏆 Historian")
        return True
    else:
        print("❌ Incorrect. Correct answer:", question["answer"])
        incorrect_questions.append(question)
        review_mode_questions.append(question)
        player.journal.append(f"✖️ Incorrect (Answer: {question['answer']})")
        return False

def select_question(level):
    if level <= 3:
        diff = "easy"
    elif level <= 6:
        diff = "medium"
    elif level <= 9:
        diff = "hard"
    else:
        diff = "ultra-hard"

    available = [q for q in quiz_questions[diff] if q["question"] not in used_questions]
    if not available:
        used_questions.clear()
        available = quiz_questions[diff]

    q = random.choice(available)
    used_questions.add(q["question"])
    return q

def save_summary():
    filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write("=== Game Summary ===\n")
        f.write(f"Final score: {player.score}\n")
        f.write(f"Level reached: {player.level - 1}\n\n")
        f.write("--- Achievements Unlocked ---\n")
        for ach in player.achievements:
            f.write(f"{ach}\n")
        f.write("\n--- Learning Journal ---\n")
        for log in player.journal:
            f.write(f"{log}\n")
        f.write("\n--- Correct Answers ---\n")
        for q in correct_questions:
            f.write(f"✔️ {q['question']}\n➡️ {q['answer']}\n")
        f.write("\n--- Incorrect Answers ---\n")
        for q in incorrect_questions:
            f.write(f"✖️ {q['question']}\n➡️ {q['answer']}\n")
    print(f"Game summary saved in {filename}")

def show_reflection():
    print("\n🧠 Post-Game Reflection Quiz")
    questions = [
        "How does fear contribute to mass persecution in society?",
        "What parallels can be drawn between the Salem Witch Trials and McCarthyism?",
        "Why is protecting civil liberties important during national crises?",
        "How were women uniquely impacted in both historical periods?",
        "Can you think of a modern example of a 'witch hunt'?"
    ]
    for q in questions:
        print(f"- {q}")

def review_mode():
    print("📘 Study Tip: Review why each answer was correct or incorrect.")
    print("\n🔁 Review Mode: Let's go over questions you missed!")
    for q in review_mode_questions:
        print(f"❓ {q['question']}")
        input("Your revised answer (press Enter to continue): ")
        print(f"✅ Correct answer: {q['answer']}\n")

def final_test():
    print("\n📘 Final Test Based on Your Mistakes:")
    sample = random.sample(review_mode_questions, min(5, len(review_mode_questions)))
    for q in sample:
        print(f"❓ {q['question']}")
        input("Your answer: ")
        print(f"✅ Correct answer: {q['answer']}\n")

# Game loop
mode = MODES.get(choose_mode(), "classic")
theme = choose_theme()

print("\nWelcome to Witch Hunt Game!")
print(f"Selected theme: {'Salem Witch Trials' if theme == '1' else 'McCarthyism'}")
print(f"Mode: {mode.capitalize()}")
print("📜 Timeline of Key Events:")
print("- 1692: Salem Witch Trials begin in Massachusetts.")
print("- 1917: Bolshevik Revolution sparks global fear of communism.")
print("- 1938: HUAC (House Un-American Activities Committee) is formed.")
print("- 1947: Hollywood Ten refuse to testify before HUAC.")
print("- 1950: McCarthy delivers his anti-communist speech.")
print("- 1954: McCarthy is censured by the U.S. Senate.")
print("- 1957: Supreme Court limits HUAC in Watkins v. United States.")

timeline_events = [
    (3, "📜 1692: Salem Witch Trials escalate as hysteria spreads."),
    (5, "📜 1938: HUAC formed to investigate disloyalty and subversive activities."),
    (7, "📜 1947: The Hollywood Ten refuse to testify before HUAC."),
    (10, "📜 1950: McCarthy delivers his infamous speech in Wheeling, WV."),
    (12, "📜 1954: U.S. Senate votes to censure Joseph McCarthy."),
    (15, "📜 1957: Supreme Court limits HUAC powers in Watkins v. U.S.")
]

while player.health > 0:
    print(f"Level {player.level} | Health: {player.health} | Score: {player.score}")
    fact = random.choice(edu_facts)
    print(f"📘 Insight: {fact}")
    player.journal.append(f"📝 Fact: {fact}")

    
    q = select_question(player.level)
    correct = show_question(q, player.level, mode)

    if correct:
        if player.health == 3 and player.level >= 5:
            player.achievements.add("🏆 Perfect Start")
        # Earnable Power-Ups
        if len(correct_questions) % 3 == 0:
            player.power_ups["skip"] += 1
            player.power_ups["double_points"] += 1
            print("🛡️ You've earned a bonus Skip and Double Points!")
    else:
        player.health -= 1

    if player.level == 10:
        player.health += 1
        print("💖 You've earned a revive at Level 10!")

        progress_bar = ''.join(['#' if player.level >= m else '-' for m, _ in timeline_events])
    colored_bar = ''.join(['[92m#[0m' if player.level >= m else '-' for m, _ in timeline_events])
    print(f"📊 Timeline Progress: [{colored_bar}]")
    for milestone, event in timeline_events:
        if player.level == milestone:
            print(f"{event}📘 Explanation: This event marks a pivotal moment in U.S. history related to fear and political persecution.")
    player.level += 1
    player.powered_up = False
    time.sleep(1)

print("\n💀 Game over")
print(f"Final Score: {player.score}")
save_summary()
show_reflection()
review_mode()
final_test()
