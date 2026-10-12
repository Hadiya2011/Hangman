from flask import Flask, render_template_string, jsonify, request, session
import random, time, json

app = Flask(__name__)
app.secret_key = "hangman_dark_2024"

# word, hint, funfact
WORD_DATA = {
    "cars": [
        ("honda",   "This brand's logo is a stylized letter H",                          "Honda's first product was actually a bicycle engine kit in 1946!"),
        ("toyota",  "Named after its founder's family, with one letter changed for luck", "Toyota's name was changed from Toyoda because 8 strokes to write Toyota is lucky in Japan!"),
        ("ford",    "Henry founded this brand in a Detroit shed in 1903",                 "The Ford Model T was so popular that at one point half of all cars in the world were Fords!"),
        ("bmw",     "Its roundel logo represents a spinning propeller",                   "BMW originally made aircraft engines before switching to motorcycles and then cars!"),
        ("tesla",   "Named after the inventor of alternating current",                    "A Tesla can receive software updates overnight while you sleep — just like a phone!"),
        ("nissan",  "This Japanese brand's name means 'Japan Industries'",               "The Nissan GT-R is nicknamed Godzilla by Australian motoring journalists!"),
        ("jeep",    "This brand got its name from the military term GP (General Purpose)","Jeep's grille design with 7 slots is a registered trademark!"),
        ("volvo",   "This brand's name means 'I roll' in Latin",                         "Volvo invented the 3-point seatbelt and gave the patent away freely to save lives!"),
        ("mazda",   "This brand was named after Ahura Mazda, god of light and wisdom",   "Mazda is the only car brand to have used a rotary engine in a production car!"),
        ("subaru",  "Its logo shows the Pleiades star cluster",                           "Subaru is the Japanese name for the Pleiades star cluster in the Taurus constellation!"),
    ],
    "animals": [
        ("elephant","The largest land animal — it never forgets a face",                  "Elephants are the only animals that can't jump — but they're also the only ones with 4 knees!"),
        ("dolphin", "A smart sea creature that loves to surf boat waves",                 "Dolphins sleep with one eye open and half their brain still awake — true multitaskers!"),
        ("penguin", "A bird that swims but cannot fly",                                   "Penguins propose to their mates with a pebble — and stay together for life!"),
        ("cheetah", "The fastest land animal alive",                                      "A cheetah can go from 0 to 60 mph in just 3 seconds — faster than most sports cars!"),
        ("gorilla", "Our closest big ape relative in the wild",                           "Gorillas can catch human colds and other illnesses because we share 98% of our DNA!"),
        ("parrot",  "A colorful bird that can repeat what you say",                       "African grey parrots can understand and use over 100 words with meaning, not just mimicry!"),
        ("turtle",  "A reptile that carries its home on its back",                        "Sea turtles return to the exact beach where they were born to lay their own eggs!"),
        ("jaguar",  "A big spotted cat found in the Amazon jungle",                       "Unlike most cats, jaguars actually love water and are excellent swimmers!"),
        ("octopus", "A sea creature with 8 arms and 3 hearts",                            "Octopuses have blue blood and three hearts — and two of those hearts stop when they swim!"),
        ("hamster", "A tiny furry pet that loves running in wheels",                      "Hamsters can run up to 5 miles a night on their wheel — that's like a human running a marathon!"),
    ],
    "countries": [
        ("brazil",  "Home to the Amazon rainforest and a famous carnival",               "Brazil is the only Portuguese-speaking country in all of South America!"),
        ("canada",  "This country has more lakes than the rest of the world combined",    "Canada has a National Lego collection and holds the record for most doughnuts per capita!"),
        ("france",  "Famous for the Eiffel Tower and croissants",                        "France is the most visited country in the world with over 89 million tourists per year!"),
        ("japan",   "An island nation famous for sushi and anime",                        "Japan has over 6,800 islands and has not had a major war since 1945!"),
        ("mexico",  "Famous for tacos, pyramids, and Day of the Dead",                   "Mexico City is the oldest city in North America — built on a lake by the Aztecs in 1325!"),
        ("egypt",   "Land of ancient pyramids and the Nile River",                        "The Great Pyramid of Giza was the tallest man-made structure in the world for 3,800 years!"),
        ("india",   "The world's largest democracy with incredible diversity",            "India invented chess, the number zero, and the decimal system — quite the hat trick!"),
        ("china",   "Home to the Great Wall and over 1.4 billion people",                "China has been making silk for over 5,000 years and kept the process secret for centuries!"),
        ("italy",   "A boot-shaped country famous for pizza, pasta and art",              "Italy has more UNESCO World Heritage Sites than any other country in the world!"),
        ("spain",   "Known for flamenco, siestas, and the Running of the Bulls",         "Spain has the second oldest restaurant in the world — Sobrino de Botín, open since 1725!"),
    ],
    "tech": [
        ("laptop",   "A portable computer you can use on your lap",                       "The first laptop, the Osborne 1 from 1981, weighed 24 pounds — good luck putting that on your lap!"),
        ("browser",  "The app you use to visit websites on the internet",                 "The first web browser was called WorldWideWeb and was created by Tim Berners-Lee in 1990!"),
        ("server",   "A powerful computer that stores and sends data to others",          "Google's servers process over 8.5 billion searches every single day!"),
        ("router",   "A device that sends internet data to the right place",              "The word router comes from 'route' — it literally decides which path your data takes!"),
        ("keyboard", "You use this every day to type letters and numbers",               "The QWERTY layout was designed in 1873 to slow typists down and prevent typewriter jams!"),
        ("software", "The programs and apps that run on your computer",                   "The first computer bug was an actual bug — a moth found stuck in a Harvard computer in 1947!"),
        ("password", "A secret word you use to log into your accounts",                   "The most common password in the world is still '123456' — used by 23 million people!"),
        ("database", "A huge organized collection of stored information",                 "Facebook's database stores over 100 petabytes of photos — that's a trillion megabytes!"),
        ("monitor",  "The screen that shows you everything your computer is doing",       "The first computer monitor was just a modified TV set connected to a computer in 1951!"),
        ("storage",  "Where your computer keeps all its files and data",                  "A human brain can store about 2.5 petabytes of memory — more than 3 million USB drives!"),
    ],
    "food": [
        ("pizza",    "A round Italian dish with cheese and toppings",                    "Americans eat about 3 billion pizzas every year — that's 23 pounds per person!"),
        ("burger",   "A grilled meat patty served inside a bun",                         "The world's most expensive burger costs $10,000 and uses gold leaf as a topping!"),
        ("sushi",    "Japanese rice rolls often served with raw fish",                    "Sushi rice is seasoned with vinegar — without it, the dish is technically just sashimi!"),
        ("pasta",    "Italian noodles made from flour, water, and sometimes eggs",        "There are over 600 officially recognized pasta shapes in Italy!"),
        ("tacos",    "Mexican tortillas filled with meat, cheese, and salsa",             "October 4th is National Taco Day in the United States!"),
        ("curry",    "A spiced dish popular across South Asia and beyond",                "Curry powder doesn't actually exist in traditional Indian cooking — it was invented for British taste!"),
        ("salad",    "A cold dish of mixed vegetables, often with dressing",              "Caesar salad was NOT invented in Rome — it was created in Tijuana, Mexico in 1924!"),
        ("noodles",  "Long thin pasta strips popular in Asian cuisines",                  "Noodles were invented in China over 4,000 years ago — the oldest noodles found were millet-based!"),
        ("sandwich", "Fillings placed between two slices of bread",                       "The sandwich is named after the Earl of Sandwich, who ate meat between bread to avoid leaving his card game!"),
        ("pancake",  "A flat fluffy cake cooked in a pan and topped with syrup",         "Pancakes are one of the oldest foods — ancient Greeks and Romans ate them with honey and fruit!"),
    ],
    "sports": [
        ("soccer",   "The world's most popular sport played with a round ball",          "Soccer balls used to be made from inflated pig bladders — yikes!"),
        ("tennis",   "A racket sport played across a net on a court",                    "Tennis players at Wimbledon must wear all white — even their underwear!"),
        ("boxing",   "A combat sport where two people fight with their fists",           "Boxing gloves were introduced to protect hands, not faces — the face is on its own!"),
        ("cricket",  "A bat and ball sport where a match can last 5 days",               "A cricket ball can swing in the air due to the seam — and bowlers polish one side to control it!"),
        ("swimming", "A water sport where athletes race using different strokes",         "Competitive swimmers shave their bodies to reduce drag — even arm hair creates resistance!"),
        ("cycling",  "A sport where athletes race on bicycles over distances",            "The Tour de France cyclists burn about 9,000 calories per stage — that's 15 Big Macs a day!"),
        ("hockey",   "A fast sport played with a stick and a puck on ice",               "An NHL hockey puck is frozen before every game so it doesn't bounce on the ice!"),
        ("baseball", "American sport played with a bat, ball, and four bases",           "A baseball has exactly 108 stitches — no more, no less, every single time!"),
        ("rugby",    "A contact sport similar to football but without helmets",          "Rugby was born when a student named William Webb Ellis picked up a soccer ball and ran with it in 1823!"),
        ("golf",     "A sport where players hit a ball into holes using clubs",           "Golf is one of only two sports played on the Moon — Alan Shepard hit a golf shot there in 1971!"),
    ],
}

WRONG_PHRASES = [
    ["Oops! That letter is NOT here 😬", "Nope! My arm just appeared 💀", "Wrong! I'm getting worried... 😰"],
    ["You're doing this ON PURPOSE aren't you?! 😤", "Another miss?! My leg is showing! 😱", "That was NOT the move 🤦"],
    ["BRO. PLEASE. I'm begging you 🙏", "I have a FAMILY you know!! 😭", "Half of me is visible and I don't like it 😤"],
    ["OKAY this is PERSONAL now 😡", "Are you even TRYING?! 😩", "I can see my whole body and it's NOT great 💀"],
    ["I trusted you... 💔", "This is it. This is how it ends. 😶", "Tell my mom I love her... 🥲"],
]

DIFFICULTY = {
    "easy":     {"lives": 5, "time": 120, "points_per_win": 100},
    "medium":   {"lives": 3, "time": 60,  "points_per_win": 200},
    "nightmare":{"lives": 1, "time": 30,  "points_per_win": 500},
}

leaderboard = []

# ─── ROUTES ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/start", methods=["POST"])
def start_game():
    data = request.json
    difficulty = data.get("difficulty", "easy")
    theme = data.get("theme", "animals")
    word, hint, fact = random.choice(WORD_DATA[theme])
    cfg = DIFFICULTY[difficulty]
    session.update({
        "word": word, "hint": hint, "fact": fact, "theme": theme,
        "difficulty": difficulty, "lives": cfg["lives"],
        "guessed": [], "start_time": time.time(),
        "time_limit": cfg["time"],
        "points": session.get("points", 0),
        "streak": session.get("streak", 0),
        "wins": session.get("wins", 0),
        "hint_points_spent": 0, "skipped": False,
        "wrong_count": 0,
    })
    return jsonify({
        "word_length": len(word), "theme": theme, "difficulty": difficulty,
        "lives": cfg["lives"], "time_limit": cfg["time"],
        "points": session["points"], "streak": session["streak"],
        "hint": hint,
    })

@app.route("/api/guess", methods=["POST"])
def guess():
    data = request.json
    letter = data.get("letter", "").lower()
    word = session.get("word", "")
    guessed = session.get("guessed", [])
    lives = session.get("lives", 5)
    if letter in guessed or not letter.isalpha():
        return jsonify({"status": "already_guessed"})
    guessed.append(letter)
    session["guessed"] = guessed
    correct = letter in word
    funny_phrase = None
    if not correct:
        lives -= 1
        session["lives"] = lives
        wrong_count = session.get("wrong_count", 0) + 1
        session["wrong_count"] = wrong_count
        max_lives = DIFFICULTY[session["difficulty"]]["lives"]
        bucket = min(int((wrong_count - 1) / max(1, max_lives / len(WRONG_PHRASES))), len(WRONG_PHRASES) - 1)
        funny_phrase = random.choice(WRONG_PHRASES[bucket])
    revealed = [c if c in guessed else "_" for c in word]
    won = "_" not in revealed
    lost = lives <= 0 and not won
    elapsed = time.time() - session.get("start_time", time.time())
    time_limit = session.get("time_limit", 120)
    timed_out = elapsed >= time_limit and not won
    result = {
        "correct": correct, "lives": lives, "guessed": guessed,
        "revealed": revealed, "won": won, "lost": lost or timed_out,
        "word": word if (won or lost or timed_out) else None,
        "fact": session.get("fact") if (won or lost or timed_out) else None,
        "elapsed": int(elapsed),
        "funny_phrase": funny_phrase,
    }
    if won:
        cfg = DIFFICULTY[session["difficulty"]]
        time_bonus = max(0, int((time_limit - elapsed) * 2))
        streak = session.get("streak", 0) + 1
        streak_bonus = streak * 50
        pts = max(10, cfg["points_per_win"] + time_bonus + streak_bonus - session.get("hint_points_spent", 0))
        session["streak"] = streak
        session["points"] = session.get("points", 0) + pts
        session["wins"] = session.get("wins", 0) + 1
        result.update({"points_earned": pts, "streak": streak,
                        "total_points": session["points"], "solve_time": int(elapsed)})
        _update_leaderboard(pts, streak, int(elapsed))
    if lost or timed_out:
        session["streak"] = 0
        result["streak"] = 0
    return jsonify(result)

@app.route("/api/hint", methods=["POST"])
def hint():
    data = request.json
    action = data.get("action", "reveal")
    word = session.get("word", "")
    guessed = session.get("guessed", [])
    points = session.get("points", 0)
    if action == "reveal":
        cost = 50
        if points < cost:
            return jsonify({"error": "Not enough points (need 50)", "cost": cost})
        unrevealed = [c for c in word if c not in guessed and c.isalpha()]
        if not unrevealed:
            return jsonify({"error": "All letters already revealed"})
        letter = random.choice(unrevealed)
        guessed.append(letter)
        session["guessed"] = guessed
        session["points"] = points - cost
        session["hint_points_spent"] = session.get("hint_points_spent", 0) + cost
        revealed = [c if c in guessed else "_" for c in word]
        won = "_" not in revealed
        result = {"letter": letter, "revealed": revealed, "guessed": guessed,
                  "points": session["points"], "won": won}
        if won:
            result.update({"fact": session.get("fact"), "word": word})
        return jsonify(result)
    elif action == "skip":
        cost = 100
        if points < cost:
            return jsonify({"error": "Not enough points (need 100)", "cost": cost})
        session["points"] = points - cost
        session["streak"] = 0
        session["skipped"] = True
        return jsonify({"skipped": True, "word": word, "fact": session.get("fact"),
                        "points": session["points"]})
    return jsonify({"error": "Unknown action"})

@app.route("/api/status")
def status():
    elapsed = time.time() - session.get("start_time", time.time())
    remaining = max(0, session.get("time_limit", 120) - elapsed)
    word = session.get("word", "???")
    fact = session.get("fact", "")
    return jsonify({"remaining": int(remaining), "lives": session.get("lives", 5),
                    "points": session.get("points", 0), "streak": session.get("streak", 0),
                    "timed_out": remaining <= 0, "word": word, "fact": fact})

@app.route("/api/leaderboard")
def get_leaderboard():
    return jsonify(sorted(leaderboard, key=lambda x: x["points"], reverse=True)[:10])

def _update_leaderboard(pts, streak, solve_time):
    leaderboard.append({
        "points": pts, "streak": streak, "solve_time": solve_time,
        "difficulty": session.get("difficulty"), "theme": session.get("theme"),
        "timestamp": int(time.time()),
    })
    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    del leaderboard[20:]

# ─── HTML TEMPLATE ────────────────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DON'T HANG ME</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#050508;--surface:#0d0d1a;--surface2:#141428;--surface3:#1c1c35;
  --accent:#ff2d78;--accent2:#00f5d4;--accent3:#ffd60a;--accent4:#8b5cf6;
  --text:#e8e8ff;--text2:#8888aa;--text3:#4444aa;
  --glow-pink:0 0 20px #ff2d7860,0 0 40px #ff2d7830;
  --glow-cyan:0 0 20px #00f5d460,0 0 40px #00f5d430;
  --glow-gold:0 0 20px #ffd60a60,0 0 40px #ffd60a30;
  --glow-purple:0 0 20px #8b5cf660,0 0 40px #8b5cf630;
}
html,body{height:100%;overflow-x:hidden;background:var(--bg);color:var(--text);font-family:'Rajdhani',sans-serif}
body::before{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");pointer-events:none;z-index:0;opacity:.4}
body::after{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(0,245,212,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,245,212,.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0}
.app{position:relative;z-index:1;min-height:100vh;display:flex;flex-direction:column;align-items:center}
header{width:100%;padding:20px 40px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--surface3);background:rgba(13,13,26,.9);backdrop-filter:blur(20px);position:sticky;top:0;z-index:100}
.logo{font-family:'Orbitron',monospace;font-size:1.6rem;font-weight:900;letter-spacing:4px;background:linear-gradient(135deg,var(--accent),var(--accent4));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo span{color:var(--accent2);-webkit-text-fill-color:var(--accent2)}
.header-stats{display:flex;gap:20px;align-items:center}
.stat-pill{background:var(--surface2);border:1px solid var(--surface3);padding:6px 16px;border-radius:30px;font-family:'Space Mono',monospace;font-size:.75rem;display:flex;align-items:center;gap:8px;transition:.3s}
.stat-pill .val{color:var(--accent2);font-weight:700;font-size:.9rem}
.stat-pill.streak .val{color:var(--accent3)}
.nav-btns{display:flex;gap:10px}
.nav-btn{background:none;border:1px solid var(--surface3);color:var(--text2);padding:6px 14px;border-radius:6px;cursor:pointer;font-family:'Rajdhani',sans-serif;font-size:.85rem;font-weight:600;transition:.3s;letter-spacing:1px}
.nav-btn:hover,.nav-btn.active{border-color:var(--accent2);color:var(--accent2);box-shadow:var(--glow-cyan)}
.screen{display:none;width:100%;max-width:1000px;padding:40px 20px;animation:fadeUp .5s ease}
.screen.active{display:block}
@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.setup-hero{text-align:center;margin-bottom:50px}
.setup-hero h1{font-family:'Orbitron',monospace;font-size:3.5rem;font-weight:900;line-height:1.1;background:linear-gradient(135deg,#ff2d78,#8b5cf6,#00f5d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px;animation:shimmer 3s ease infinite}
@keyframes shimmer{0%,100%{filter:hue-rotate(0deg)}50%{filter:hue-rotate(30deg)}}
.setup-hero p{color:var(--text2);font-size:1.1rem;letter-spacing:2px}
.section-label{font-family:'Orbitron',monospace;font-size:.65rem;letter-spacing:4px;color:var(--text3);text-transform:uppercase;margin-bottom:16px;display:flex;align-items:center;gap:10px}
.section-label::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--surface3),transparent)}
.option-grid{display:grid;gap:14px;margin-bottom:40px}
.option-grid.diff{grid-template-columns:repeat(3,1fr)}
.option-grid.theme{grid-template-columns:repeat(3,1fr)}
.opt-card{background:var(--surface);border:2px solid var(--surface3);border-radius:16px;padding:20px;cursor:pointer;transition:.3s;text-align:center;position:relative;overflow:hidden}
.opt-card::before{content:'';position:absolute;inset:0;opacity:0;transition:.3s}
.opt-card:hover{transform:translateY(-3px)}
.opt-card.selected{border-color:var(--accent2);box-shadow:var(--glow-cyan)}
.opt-card.selected::before{background:linear-gradient(135deg,rgba(0,245,212,.1),transparent);opacity:1}
.opt-card .icon{font-size:2.2rem;margin-bottom:8px;display:block}
.opt-card .name{font-family:'Orbitron',monospace;font-size:.8rem;font-weight:700;letter-spacing:2px;color:var(--text)}
.opt-card .desc{font-size:.8rem;color:var(--text2);margin-top:4px}
.opt-card .badge{position:absolute;top:10px;right:10px;font-size:.6rem;font-family:'Space Mono',monospace;padding:3px 8px;border-radius:20px;font-weight:700}
.badge.easy{background:rgba(0,245,212,.2);color:var(--accent2)}
.badge.medium{background:rgba(255,45,120,.2);color:var(--accent)}
.badge.nightmare{background:rgba(139,92,246,.2);color:var(--accent4)}
.start-row{display:flex;gap:14px;justify-content:center;margin-top:10px}
.btn-primary{font-family:'Orbitron',monospace;font-size:1rem;font-weight:700;letter-spacing:3px;padding:16px 40px;border:none;border-radius:12px;cursor:pointer;background:linear-gradient(135deg,var(--accent),var(--accent4));color:#fff;transition:.3s;position:relative;overflow:hidden}
.btn-primary::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,transparent,rgba(255,255,255,.15),transparent);transform:translateX(-100%);transition:.5s}
.btn-primary:hover::after{transform:translateX(100%)}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 10px 40px rgba(255,45,120,.4)}
.game-layout{display:grid;grid-template-columns:300px 1fr;gap:24px;align-items:start}
.game-left{display:flex;flex-direction:column;gap:16px}
.game-right{display:flex;flex-direction:column;gap:16px}
.hangman-wrap{background:var(--surface);border:1px solid var(--surface3);border-radius:20px;padding:16px 20px 8px;text-align:center;position:relative;overflow:hidden}
.hangman-wrap::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at 50% 0%,rgba(255,45,120,.05),transparent 60%)}
#hangman-svg{width:100%;max-width:220px;height:190px}
.hangman-part{stroke-dasharray:300;stroke-dashoffset:300;transition:stroke-dashoffset .7s cubic-bezier(.4,0,.2,1)}
.hangman-part.drawn{stroke-dashoffset:0}
.hangman-speech{min-height:40px;padding:6px 10px;margin-top:4px;font-size:.82rem;font-weight:600;color:var(--accent);background:rgba(255,45,120,.08);border:1px solid rgba(255,45,120,.2);border-radius:10px;line-height:1.4;transition:all .4s ease;opacity:0;transform:scale(.95)}
.hangman-speech.show{opacity:1;transform:scale(1);animation:speechPop .4s cubic-bezier(.34,1.56,.64,1)}
@keyframes speechPop{0%{transform:scale(.8)}60%{transform:scale(1.05)}100%{transform:scale(1)}}
.timer-wrap{background:var(--surface);border:1px solid var(--surface3);border-radius:14px;padding:14px 18px;display:flex;align-items:center;gap:14px}
.timer-label{font-size:.65rem;font-family:'Space Mono',monospace;color:var(--text3);letter-spacing:2px}
.timer-val{font-family:'Orbitron',monospace;font-size:1.8rem;font-weight:900;color:var(--accent2);transition:.3s;min-width:60px}
.timer-val.urgent{color:var(--accent);animation:pulse .5s ease infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
.timer-bar{flex:1;height:5px;background:var(--surface3);border-radius:3px;overflow:hidden}
.timer-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--accent2),var(--accent));transition:width 1s linear}
.lives-wrap{background:var(--surface);border:1px solid var(--surface3);border-radius:14px;padding:12px 18px;display:flex;align-items:center;gap:10px}
.lives-label{font-size:.65rem;font-family:'Space Mono',monospace;color:var(--text3);letter-spacing:2px;white-space:nowrap}
.lives-icons{display:flex;gap:6px;flex-wrap:wrap}
.life-icon{font-size:1.2rem;transition:.4s}
.life-icon.lost{filter:grayscale(1);opacity:.2;transform:scale(.75)}
.meta-chip{display:flex;gap:10px}
.chip{background:var(--surface);border:1px solid var(--surface3);border-radius:10px;padding:10px 14px;flex:1;text-align:center}
.chip .chip-label{font-size:.6rem;font-family:'Space Mono',monospace;color:var(--text3);letter-spacing:2px}
.chip .chip-val{font-family:'Orbitron',monospace;font-size:1.1rem;font-weight:700;color:var(--text)}
.word-section{background:var(--surface);border:1px solid var(--surface3);border-radius:20px;padding:28px;text-align:center}
.theme-badge{display:inline-flex;align-items:center;gap:6px;background:var(--surface2);border:1px solid var(--surface3);padding:6px 16px;border-radius:30px;font-size:.7rem;font-family:'Space Mono',monospace;color:var(--text2);letter-spacing:2px;margin-bottom:16px}
.word-letters{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;min-height:68px;align-items:center;margin-bottom:16px}
.letter-box{width:40px;height:50px;border-bottom:3px solid var(--surface3);display:flex;align-items:center;justify-content:center;font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:900;color:var(--accent2);transition:.4s;position:relative}
.letter-box.space{border-bottom-color:transparent;width:16px}
.letter-box.revealed{border-bottom-color:var(--accent2);animation:popIn .4s cubic-bezier(.34,1.56,.64,1)}
.letter-box.wrong-reveal{border-bottom-color:var(--accent);color:var(--accent)}
@keyframes popIn{0%{transform:scale(0) rotateY(90deg)}60%{transform:scale(1.2)}100%{transform:scale(1)}}
.word-hint-box{background:var(--surface2);border:1px solid rgba(255,214,10,.25);border-radius:10px;padding:10px 14px;font-size:.83rem;color:var(--accent3);text-align:left;display:flex;gap:8px;align-items:flex-start}
.word-hint-box .hint-icon{font-size:1rem;flex-shrink:0;margin-top:1px}
.keyboard-section{background:var(--surface);border:1px solid var(--surface3);border-radius:18px;padding:20px}
.keyboard-section h3{font-family:'Orbitron',monospace;font-size:.6rem;letter-spacing:3px;color:var(--text3);margin-bottom:14px}
.keyboard{display:flex;flex-direction:column;gap:7px;align-items:center}
.key-row{display:flex;gap:5px;justify-content:center}
.key{width:36px;height:36px;border:1px solid var(--surface3);border-radius:7px;background:var(--surface2);color:var(--text);font-family:'Orbitron',monospace;font-size:.65rem;font-weight:700;cursor:pointer;transition:.2s;display:flex;align-items:center;justify-content:center}
.key:hover:not(:disabled){background:var(--surface3);transform:translateY(-2px);border-color:var(--accent2);color:var(--accent2)}
.key:disabled{cursor:not-allowed}
.key.correct{background:rgba(0,245,212,.2);border-color:var(--accent2);color:var(--accent2)}
.key.wrong{background:rgba(255,45,120,.1);border-color:rgba(255,45,120,.3);color:rgba(255,45,120,.4)}
.hint-section{background:var(--surface);border:1px solid var(--surface3);border-radius:14px;padding:14px 18px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.hint-section p{font-size:.8rem;color:var(--text2);flex:1;min-width:120px}
.hint-section p span{color:var(--accent3);font-weight:700}
.hint-btn{font-family:'Rajdhani',sans-serif;font-size:.78rem;font-weight:700;letter-spacing:1px;padding:7px 14px;border-radius:8px;cursor:pointer;border:1px solid;transition:.3s;white-space:nowrap}
.hint-reveal{border-color:var(--accent3);background:rgba(255,214,10,.08);color:var(--accent3)}
.hint-reveal:hover{background:rgba(255,214,10,.18);box-shadow:var(--glow-gold)}
.hint-skip{border-color:var(--accent4);background:rgba(139,92,246,.08);color:var(--accent4)}
.hint-skip:hover{background:rgba(139,92,246,.18);box-shadow:var(--glow-purple)}
.msg-bar{padding:12px 18px;border-radius:10px;font-weight:600;font-size:.9rem;letter-spacing:1px;text-align:center;transition:.4s;display:none}
.msg-bar.show{display:block;animation:fadeUp .3s ease}
.msg-bar.wrong{background:rgba(255,45,120,.15);border:1px solid rgba(255,45,120,.3);color:var(--accent)}
.msg-bar.correct{background:rgba(0,245,212,.15);border:1px solid rgba(0,245,212,.3);color:var(--accent2)}
.msg-bar.info{background:rgba(139,92,246,.15);border:1px solid rgba(139,92,246,.3);color:var(--accent4)}
.overlay{position:fixed;inset:0;background:rgba(5,5,8,.92);backdrop-filter:blur(14px);z-index:200;display:none;align-items:center;justify-content:center;overflow-y:auto;padding:20px}
.overlay.active{display:flex}
.overlay-card{background:var(--surface);border:1px solid var(--surface3);border-radius:24px;padding:36px 32px;max-width:520px;width:90%;text-align:center;animation:fadeUp .5s cubic-bezier(.34,1.2,.64,1)}
.overlay-card h2{font-family:'Orbitron',monospace;font-size:1.8rem;font-weight:900;margin-bottom:10px}
.win-card h2{background:linear-gradient(135deg,var(--accent3),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.lose-card h2{color:var(--accent)}
.overlay-word{font-family:'Orbitron',monospace;font-size:1.6rem;font-weight:900;color:var(--accent2);letter-spacing:5px;margin:14px 0;text-transform:uppercase}
.overlay-fact{font-size:.88rem;color:var(--text2);line-height:1.7;background:var(--surface2);padding:14px;border-radius:10px;border-left:3px solid var(--accent2);text-align:left;margin:12px 0}
.overlay-fact-label{font-family:'Orbitron',monospace;font-size:.6rem;letter-spacing:3px;color:var(--accent2);margin-bottom:6px}
.overlay-stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:14px 0}
.o-stat{background:var(--surface2);border-radius:10px;padding:12px}
.o-stat .o-label{font-size:.6rem;font-family:'Space Mono',monospace;color:var(--text3);letter-spacing:2px}
.o-stat .o-val{font-family:'Orbitron',monospace;font-size:1.2rem;font-weight:900;color:var(--accent3)}
.overlay-btns{display:flex;gap:12px;justify-content:center;margin-top:18px}
.o-btn{font-family:'Orbitron',monospace;font-size:.72rem;font-weight:700;letter-spacing:2px;padding:13px 22px;border-radius:10px;cursor:pointer;border:2px solid;transition:.3s}
.o-btn.primary{border-color:var(--accent2);background:rgba(0,245,212,.12);color:var(--accent2)}
.o-btn.primary:hover{background:rgba(0,245,212,.22);box-shadow:var(--glow-cyan)}
.o-btn.secondary{border-color:var(--surface3);background:none;color:var(--text2)}
.o-btn.secondary:hover{border-color:var(--text2);color:var(--text)}
.lb-table{width:100%;border-collapse:collapse;margin-top:16px}
.lb-table th{font-family:'Orbitron',monospace;font-size:.58rem;letter-spacing:3px;color:var(--text3);padding:10px 14px;border-bottom:1px solid var(--surface3);text-align:left}
.lb-table td{padding:13px 14px;border-bottom:1px solid rgba(255,255,255,.04);font-size:.88rem}
.lb-table tr:hover td{background:rgba(255,255,255,.02)}
.rank-num{font-family:'Orbitron',monospace;font-weight:700;color:var(--text3)}
.rank-1 .rank-num{color:var(--accent3)}.rank-2 .rank-num{color:#c0c0c0}.rank-3 .rank-num{color:#cd7f32}
.lb-pts{font-family:'Orbitron',monospace;font-weight:700;color:var(--accent2)}
.lb-badge{display:inline-block;padding:3px 8px;border-radius:16px;font-size:.62rem;font-family:'Space Mono',monospace;font-weight:700}
.lb-easy{background:rgba(0,245,212,.15);color:var(--accent2)}
.lb-medium{background:rgba(255,45,120,.15);color:var(--accent)}
.lb-nightmare{background:rgba(139,92,246,.15);color:var(--accent4)}
.empty-lb{text-align:center;padding:60px;color:var(--text3);font-size:.95rem}
.confetti-container{position:fixed;inset:0;pointer-events:none;z-index:300;overflow:hidden}
.confetto{position:absolute;top:-20px;animation:confettoFall linear forwards}
@keyframes confettoFall{to{transform:translateY(110vh) rotate(720deg);opacity:0}}
.streak-badge{position:fixed;top:80px;right:20px;background:linear-gradient(135deg,var(--accent3),var(--accent));color:#000;font-family:'Orbitron',monospace;font-weight:900;font-size:1.1rem;padding:12px 22px;border-radius:14px;z-index:150;animation:badgePop .6s cubic-bezier(.34,1.56,.64,1) forwards,badgeFade 1s ease 2.2s forwards;pointer-events:none}
@keyframes badgePop{from{transform:scale(0) rotate(-10deg)}to{transform:scale(1) rotate(0)}}
@keyframes badgeFade{to{opacity:0;transform:translateY(-20px)}}
::-webkit-scrollbar{width:4px}::-webkit-scrollbar-track{background:var(--bg)}::-webkit-scrollbar-thumb{background:var(--surface3);border-radius:2px}
@media(max-width:768px){
  header{padding:12px 16px}.logo{font-size:1rem}.header-stats{display:none}
  .game-layout{grid-template-columns:1fr}.option-grid.diff,.option-grid.theme{grid-template-columns:1fr 1fr}
  .setup-hero h1{font-size:2rem}
}
</style>
</head>
<body>
<div class="app">
<header>
  <div class="logo">DON'T <span>HANG ME</span></div>
  <div class="header-stats">
    <div class="stat-pill">⚡ Points <span class="val" id="hdr-pts">0</span></div>
    <div class="stat-pill streak">🔥 Streak <span class="val" id="hdr-streak">0</span></div>
  </div>
  <div class="nav-btns">
    <button class="nav-btn active" onclick="showScreen('setup')">PLAY</button>
    <button class="nav-btn" onclick="showScreen('leaderboard');loadLeaderboard()">SCORES</button>
  </div>
</header>

<div class="screen active" id="screen-setup">
  <div class="setup-hero">
    <h1>DON'T HANG ME</h1>
    <p>CHOOSE YOUR FATE · BEAT THE CLOCK · SURVIVE</p>
  </div>
  <div class="section-label">SELECT DIFFICULTY</div>
  <div class="option-grid diff" id="diff-grid">
    <div class="opt-card" data-val="easy" onclick="selectDiff(this)">
      <span class="badge easy">5 LIVES</span><span class="icon">😌</span>
      <div class="name">EASY</div><div class="desc">120s · 100pts base</div>
    </div>
    <div class="opt-card" data-val="medium" onclick="selectDiff(this)">
      <span class="badge medium">3 LIVES</span><span class="icon">💀</span>
      <div class="name">MEDIUM</div><div class="desc">60s · 200pts base</div>
    </div>
    <div class="opt-card" data-val="nightmare" onclick="selectDiff(this)">
      <span class="badge nightmare">1 LIFE</span><span class="icon">👁️</span>
      <div class="name">NIGHTMARE</div><div class="desc">30s · 500pts base</div>
    </div>
  </div>
  <div class="section-label">SELECT THEME</div>
  <div class="option-grid theme" id="theme-grid">
    <div class="opt-card" data-val="cars" onclick="selectTheme(this)"><span class="icon">🏎️</span><div class="name">CARS</div><div class="desc">Iconic vehicles</div></div>
    <div class="opt-card" data-val="animals" onclick="selectTheme(this)"><span class="icon">🐾</span><div class="name">ANIMALS</div><div class="desc">Wild creatures</div></div>
    <div class="opt-card" data-val="countries" onclick="selectTheme(this)"><span class="icon">🌍</span><div class="name">COUNTRIES</div><div class="desc">World nations</div></div>
    <div class="opt-card" data-val="tech" onclick="selectTheme(this)"><span class="icon">💻</span><div class="name">TECH</div><div class="desc">Digital world</div></div>
    <div class="opt-card" data-val="food" onclick="selectTheme(this)"><span class="icon">🍜</span><div class="name">FOOD</div><div class="desc">Global cuisine</div></div>
    <div class="opt-card" data-val="sports" onclick="selectTheme(this)"><span class="icon">🏆</span><div class="name">SPORTS</div><div class="desc">Athletic feats</div></div>
  </div>
  <div class="start-row">
    <button class="btn-primary" onclick="startGame()">▶ START GAME</button>
  </div>
</div>

<div class="screen" id="screen-game">
  <div class="game-layout">
    <div class="game-left">
      <div class="hangman-wrap">
        <svg id="hangman-svg" viewBox="0 0 260 230" fill="none">
          <line x1="20" y1="215" x2="180" y2="215" stroke="#2a2a4a" stroke-width="4" stroke-linecap="round"/>
          <line x1="60" y1="215" x2="60" y2="15" stroke="#2a2a4a" stroke-width="4" stroke-linecap="round"/>
          <line x1="60" y1="15" x2="160" y2="15" stroke="#2a2a4a" stroke-width="4" stroke-linecap="round"/>
          <line x1="160" y1="15" x2="160" y2="45" stroke="#2a2a4a" stroke-width="4" stroke-linecap="round"/>
          <circle id="h-head" cx="160" cy="70" r="24" stroke="#ff2d78" stroke-width="3" class="hangman-part"/>
          <line id="h-body" x1="160" y1="94" x2="160" y2="150" stroke="#ff2d78" stroke-width="3" stroke-linecap="round" class="hangman-part"/>
          <line id="h-larm" x1="160" y1="110" x2="130" y2="140" stroke="#ff2d78" stroke-width="3" stroke-linecap="round" class="hangman-part"/>
          <line id="h-rarm" x1="160" y1="110" x2="190" y2="140" stroke="#ff2d78" stroke-width="3" stroke-linecap="round" class="hangman-part"/>
          <line id="h-lleg" x1="160" y1="150" x2="130" y2="190" stroke="#ff2d78" stroke-width="3" stroke-linecap="round" class="hangman-part"/>
          <line id="h-rleg" x1="160" y1="150" x2="190" y2="190" stroke="#ff2d78" stroke-width="3" stroke-linecap="round" class="hangman-part"/>
          <circle id="h-face-l" cx="152" cy="65" r="3" fill="#ff2d78" opacity="0"/>
          <circle id="h-face-r" cx="168" cy="65" r="3" fill="#ff2d78" opacity="0"/>
          <path id="h-mouth" d="M152 78 Q160 85 168 78" stroke="#ff2d78" stroke-width="2" fill="none" opacity="0"/>
        </svg>
        <div class="hangman-speech" id="hangman-speech"></div>
      </div>
      <div class="timer-wrap">
        <span style="font-size:1.3rem">⏱️</span>
        <div><div class="timer-label">TIME LEFT</div><div class="timer-val" id="timer-val">—</div></div>
        <div class="timer-bar"><div class="timer-fill" id="timer-fill" style="width:100%"></div></div>
      </div>
      <div class="lives-wrap">
        <span class="lives-label">LIVES</span>
        <div class="lives-icons" id="lives-icons"></div>
      </div>
      <div class="meta-chip">
        <div class="chip"><div class="chip-label">POINTS</div><div class="chip-val" id="game-pts">0</div></div>
        <div class="chip"><div class="chip-label">STREAK</div><div class="chip-val" id="game-streak">0🔥</div></div>
      </div>
    </div>
    <div class="game-right">
      <div class="word-section">
        <div class="theme-badge" id="game-theme-badge">🎯 THEME</div>
        <div class="word-letters" id="word-display"></div>
        <div class="word-hint-box" id="word-hint-box">
          <span class="hint-icon">💡</span>
          <span id="word-hint-text">Loading hint...</span>
        </div>
      </div>
      <div id="msg-bar" class="msg-bar"></div>
      <div class="hint-section">
        <p>🎯 <span id="pt-display">0</span> pts available</p>
        <button class="hint-btn hint-reveal" onclick="useHint('reveal')">Reveal Letter (50pts)</button>
        <button class="hint-btn hint-skip" onclick="useHint('skip')">Skip Word (100pts)</button>
      </div>
      <div class="keyboard-section">
        <h3>KEYBOARD — or press keys</h3>
        <div class="keyboard" id="keyboard"></div>
      </div>
    </div>
  </div>
</div>

<div class="screen" id="screen-leaderboard">
  <div class="section-label" style="font-size:.9rem;margin-bottom:28px">🏆 LEADERBOARD</div>
  <div id="lb-content"><div class="empty-lb">No scores yet — play a game first!</div></div>
</div>

<!-- WIN OVERLAY -->
<div class="overlay" id="overlay-win">
  <div class="overlay-card win-card">
    <h2>⚡ CRACKED IT!</h2>
    <div class="overlay-word" id="win-word"></div>
    <div class="overlay-stats">
      <div class="o-stat"><div class="o-label">POINTS EARNED</div><div class="o-val" id="win-pts">—</div></div>
      <div class="o-stat"><div class="o-label">STREAK</div><div class="o-val" id="win-streak">—</div></div>
      <div class="o-stat"><div class="o-label">SOLVE TIME</div><div class="o-val" id="win-time">—</div></div>
    </div>
    <div class="overlay-fact-label">🧠 FUN FACT</div>
    <div class="overlay-fact" id="win-fact"></div>
    <div class="overlay-btns">
      <button class="o-btn primary" onclick="closeOverlay();startGame()">NEXT WORD</button>
      <button class="o-btn secondary" onclick="closeOverlay();showScreen('setup')">MENU</button>
    </div>
  </div>
</div>

<!-- LOSE OVERLAY -->
<div class="overlay" id="overlay-lose">
  <div class="overlay-card lose-card">
    <h2>💀 ELIMINATED</h2>
    <p id="lose-sub" style="color:var(--text2);margin-bottom:8px;font-size:.9rem">The word was:</p>
    <div class="overlay-word" id="lose-word"></div>
    <div class="overlay-fact-label" style="margin-top:6px">🧠 FUN FACT</div>
    <div class="overlay-fact" id="lose-fact" style="border-left-color:var(--accent)"></div>
    <div class="overlay-btns">
      <button class="o-btn primary" onclick="closeOverlay();startGame()">TRY AGAIN</button>
      <button class="o-btn secondary" onclick="closeOverlay();showScreen('setup')">MENU</button>
    </div>
  </div>
</div>

<div class="confetti-container" id="confetti"></div>

<script>
const HANGMAN_PARTS=['h-head','h-body','h-larm','h-rarm','h-lleg','h-rleg'];
const THEME_ICONS={cars:'🏎️',animals:'🐾',countries:'🌍',tech:'💻',food:'🍜',sports:'🏆'};
const KEYS=['QWERTYUIOP','ASDFGHJKL','ZXCVBNM'];
let state={diff:'easy',theme:'animals',lives:5,maxLives:5,timeLimit:120,guessed:[],revealed:[],points:0,streak:0,timerInterval:null,timeRemaining:120,gameOver:false,currentWord:''};

function showScreen(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  document.getElementById('screen-'+id).classList.add('active');
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  const map={setup:0,leaderboard:1};
  if(map[id]!==undefined)document.querySelectorAll('.nav-btn')[map[id]].classList.add('active');
}
function selectDiff(el){
  document.querySelectorAll('#diff-grid .opt-card').forEach(c=>{c.classList.remove('selected');c.style.borderColor='';});
  el.classList.add('selected');
  state.diff=el.dataset.val;
  const colors={easy:'var(--accent2)',medium:'var(--accent)',nightmare:'var(--accent4)'};
  el.style.borderColor=colors[state.diff];
}
function selectTheme(el){
  document.querySelectorAll('#theme-grid .opt-card').forEach(c=>c.classList.remove('selected'));
  el.classList.add('selected');
  state.theme=el.dataset.val;
}
function buildKeyboard(){
  const kb=document.getElementById('keyboard');kb.innerHTML='';
  KEYS.forEach(row=>{
    const r=document.createElement('div');r.className='key-row';
    row.split('').forEach(k=>{
      const btn=document.createElement('button');
      btn.className='key';btn.id='key-'+k;btn.textContent=k;
      btn.onclick=()=>guess(k.toLowerCase());r.appendChild(btn);
    });kb.appendChild(r);
  });
}
async function startGame(){
  clearInterval(state.timerInterval);state.gameOver=false;
  const body={difficulty:state.diff,theme:state.theme};
  const res=await fetch('/api/start',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  const data=await res.json();
  state.lives=data.lives;state.maxLives=data.lives;state.timeLimit=data.time_limit;
  state.timeRemaining=data.time_limit;state.guessed=[];state.points=data.points;state.streak=data.streak;
  state.revealed=Array(data.word_length).fill('_');
  state.currentWord='';
  showScreen('game');buildKeyboard();updateLives();renderWord();updateHUD();resetHangman();hideMsg();
  clearSpeech();
  document.getElementById('game-theme-badge').textContent=(THEME_ICONS[data.theme]||'🎯')+' '+data.theme.toUpperCase();
  document.getElementById('word-hint-text').textContent=data.hint||'Think carefully...';
  startTimer();
}
function startTimer(){
  const fill=document.getElementById('timer-fill'),val=document.getElementById('timer-val');
  clearInterval(state.timerInterval);
  state.timerInterval=setInterval(async()=>{
    state.timeRemaining--;
    const pct=(state.timeRemaining/state.timeLimit)*100;
    fill.style.width=pct+'%';
    val.textContent=state.timeRemaining+'s';
    val.className='timer-val'+(state.timeRemaining<=10?' urgent':'');
    if(state.timeRemaining<=0&&!state.gameOver){
      clearInterval(state.timerInterval);
      state.gameOver=true;
      const res=await fetch('/api/status');
      const d=await res.json();
      const word=d.word||'UNKNOWN';
      const fact=d.fact||'';
      state.currentWord=word;
      revealWord(word,false);
      setTimeout(()=>showLose(word,'TIME UP! The word was:',fact),800);
    }
  },1000);
}
function renderWord(){
  const wd=document.getElementById('word-display');wd.innerHTML='';
  state.revealed.forEach(c=>{
    const box=document.createElement('div');
    if(c===' '){box.className='letter-box space';wd.appendChild(box);return;}
    box.className='letter-box'+(c!=='_'?' revealed':'');
    box.textContent=c!=='_'?c.toUpperCase():'';wd.appendChild(box);
  });
}
function revealWord(word,isWin){
  const boxes=document.getElementById('word-display').querySelectorAll('.letter-box:not(.space)');
  word.split('').forEach((c,i)=>{if(i<boxes.length){boxes[i].textContent=c.toUpperCase();boxes[i].className='letter-box '+(isWin?'revealed':'wrong-reveal');}});
}
function showSpeech(phrase){
  const el=document.getElementById('hangman-speech');
  el.textContent=phrase;
  el.className='hangman-speech';
  void el.offsetWidth;
  el.className='hangman-speech show';
}
function clearSpeech(){
  const el=document.getElementById('hangman-speech');
  el.className='hangman-speech';
  el.textContent='';
}
async function guess(letter){
  if(state.gameOver)return;
  const key=document.getElementById('key-'+letter.toUpperCase());
  if(key&&key.disabled)return;
  const res=await fetch('/api/guess',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({letter})});
  const data=await res.json();
  if(data.status==='already_guessed')return;
  state.revealed=data.revealed;state.lives=data.lives;state.guessed=data.guessed;
  if(data.word)state.currentWord=data.word;
  renderWord();updateLives();
  if(key){key.disabled=true;key.className='key '+(data.correct?'correct':'wrong');}
  if(!data.correct){
    drawHangmanPart();
    if(data.funny_phrase)showSpeech(data.funny_phrase);
  }else{
    clearSpeech();
  }
  if(data.won){
    state.points=data.total_points;state.streak=data.streak;
    clearInterval(state.timerInterval);updateHUD();
    setTimeout(()=>showWin(data),600);
  }else if(data.lost){
    state.streak=0;clearInterval(state.timerInterval);
    revealWord(data.word,false);
    setTimeout(()=>showLose(data.word,'The word was:',data.fact),800);
  }else{
    showMsg(data.correct?'✓ CORRECT!':'✗ WRONG! '+data.lives+' '+(data.lives===1?'life':'lives')+' left',data.correct?'correct':'wrong');
  }
  updateHUD();
}
function resetHangman(){
  HANGMAN_PARTS.forEach(id=>{const el=document.getElementById(id);if(el){el.classList.remove('drawn');}});
  ['h-face-l','h-face-r','h-mouth'].forEach(id=>{const el=document.getElementById(id);if(el)el.style.opacity='0';});
}
function drawHangmanPart(){
  const wrongsSoFar=state.maxLives-state.lives;
  const partsToShow=Math.ceil((wrongsSoFar/state.maxLives)*HANGMAN_PARTS.length);
  for(let i=0;i<partsToShow;i++){const el=document.getElementById(HANGMAN_PARTS[i]);if(el)el.classList.add('drawn');}
  if(state.lives===0){['h-face-l','h-face-r','h-mouth'].forEach(id=>{const el=document.getElementById(id);if(el)el.style.opacity='1';});}
}
function updateLives(){
  const c=document.getElementById('lives-icons');
  const icons={easy:'💚',medium:'❤️',nightmare:'💜'};
  const icon=icons[state.diff]||'❤️';c.innerHTML='';
  for(let i=0;i<state.maxLives;i++){
    const s=document.createElement('span');
    s.className='life-icon'+(i>=state.lives?' lost':'');
    s.textContent=icon;c.appendChild(s);
  }
}
function updateHUD(){
  document.getElementById('hdr-pts').textContent=state.points;
  document.getElementById('hdr-streak').textContent=state.streak;
  document.getElementById('game-pts').textContent=state.points;
  document.getElementById('game-streak').textContent=state.streak+'🔥';
  document.getElementById('pt-display').textContent=state.points;
}
async function useHint(action){
  const res=await fetch('/api/hint',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action})});
  const data=await res.json();
  if(data.error){showMsg('⚠️ '+data.error,'wrong');return;}
  if(action==='reveal'){
    state.revealed=data.revealed;state.guessed=data.guessed;state.points=data.points;
    renderWord();updateHUD();
    const k=document.getElementById('key-'+data.letter.toUpperCase());
    if(k){k.disabled=true;k.className='key correct';}
    if(data.won)setTimeout(()=>showWin({...data,streak:state.streak,total_points:data.points,points_earned:0,solve_time:state.timeLimit-state.timeRemaining}),500);
  }else{
    clearInterval(state.timerInterval);state.points=data.points;state.streak=0;updateHUD();
    revealWord(data.word,false);
    setTimeout(()=>{
      showLose(data.word,'You skipped — the word was:',data.fact);
      document.getElementById('overlay-lose').querySelector('h2').textContent='⏭️ SKIPPED';
    },900);
  }
}
function showMsg(text,type){
  const bar=document.getElementById('msg-bar');bar.textContent=text;bar.className='msg-bar show '+type;
  setTimeout(()=>bar.className='msg-bar',2500);
}
function hideMsg(){document.getElementById('msg-bar').className='msg-bar';}
function showWin(data){
  state.gameOver=true;
  document.getElementById('win-word').textContent=(data.word||'').toUpperCase();
  document.getElementById('win-fact').textContent=data.fact||'No fun fact available.';
  document.getElementById('win-pts').textContent=data.points_earned||data.total_points||'—';
  document.getElementById('win-streak').textContent=(data.streak||0)+'🔥';
  document.getElementById('win-time').textContent=(data.solve_time||0)+'s';
  document.getElementById('overlay-win').classList.add('active');
  launchConfetti();
  if((data.streak||0)>1)showStreakBadge(data.streak);
}
function showLose(word,subText,fact){
  state.gameOver=true;
  document.getElementById('lose-word').textContent=(word||'UNKNOWN').toUpperCase();
  document.getElementById('overlay-lose').querySelector('h2').textContent='💀 ELIMINATED';
  document.getElementById('lose-sub').textContent=subText||'The word was:';
  document.getElementById('lose-fact').textContent=fact||'Better luck next time!';
  document.getElementById('overlay-lose').classList.add('active');
}
function closeOverlay(){document.querySelectorAll('.overlay').forEach(o=>o.classList.remove('active'));}
function launchConfetti(){
  const cont=document.getElementById('confetti');cont.innerHTML='';
  const colors=['#ff2d78','#00f5d4','#ffd60a','#8b5cf6','#ff6b6b','#4ecdc4'];
  for(let i=0;i<120;i++){
    const el=document.createElement('div');el.className='confetto';
    el.style.cssText=`left:${Math.random()*100}%;background:${colors[Math.floor(Math.random()*colors.length)]};width:${6+Math.random()*10}px;height:${6+Math.random()*10}px;border-radius:${Math.random()>.5?'50%':'2px'};animation-duration:${2+Math.random()*3}s;animation-delay:${Math.random()*.8}s;opacity:${.6+Math.random()*.4};`;
    cont.appendChild(el);setTimeout(()=>el.remove(),(5000+Math.random()*2000));
  }
}
function showStreakBadge(streak){
  const b=document.createElement('div');b.className='streak-badge';b.textContent='🔥 '+streak+' STREAK!';
  document.body.appendChild(b);setTimeout(()=>b.remove(),3800);
}
async function loadLeaderboard(){
  const res=await fetch('/api/leaderboard');const data=await res.json();
  const cont=document.getElementById('lb-content');
  if(!data.length){cont.innerHTML='<div class="empty-lb">No scores yet — play a game first!</div>';return;}
  const bc={easy:'lb-easy',medium:'lb-medium',nightmare:'lb-nightmare'};
  const rc=['rank-1','rank-2','rank-3'];
  cont.innerHTML=`<table class="lb-table"><thead><tr><th>#</th><th>POINTS</th><th>STREAK</th><th>TIME</th><th>DIFFICULTY</th><th>THEME</th></tr></thead><tbody>${data.map((e,i)=>`<tr class="${rc[i]||''}"><td class="rank-num">${['🥇','🥈','🥉'][i]||'#'+(i+1)}</td><td class="lb-pts">${e.points}</td><td>${e.streak}🔥</td><td>${e.solve_time}s</td><td><span class="lb-badge ${bc[e.difficulty]||''}">${(e.difficulty||'').toUpperCase()}</span></td><td>${THEME_ICONS[e.theme]||'🎯'} ${(e.theme||'').toUpperCase()}</td></tr>`).join('')}</tbody></table>`;
}
document.addEventListener('keydown',e=>{
  const l=e.key.toLowerCase();
  if(/^[a-z]$/.test(l)&&document.getElementById('screen-game').classList.contains('active'))guess(l);
});
document.querySelector('[data-val="easy"]').click();
document.querySelector('[data-val="animals"]').click();
</script>
</body>
</html>"""

# ─── LAUNCH ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import webbrowser, threading, os
    port = int(os.environ.get("PORT", 5000))
    threading.Timer(1.2, lambda: webbrowser.open(f"http://localhost:{port}")).start()
    app.run(debug=False, port=port, host="0.0.0.0")