import os

from flask import Flask, redirect, render_template_string, request, session, url_for


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)

PROJECTS = {
	"1": "Solar panels",
	"2": "Grow food",
	"3": "Oxygen recycler",
	"4": "Shield layer",
}

PAGE = """<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Moon Outpost | Mission Control</title>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
	<style>
		:root {
			color-scheme: dark;
			--ink: #f1f3e9;
			--muted: #9aa69f;
			--line: #34413d;
			--panel: #17211e;
			--ground: #0c1412;
			--lime: #c5ed78;
			--cyan: #83d9d0;
			--warning: #ffbc72;
			--danger: #ff8277;
		}
		* { box-sizing: border-box; }
		body {
			margin: 0;
			min-height: 100vh;
			color: var(--ink);
			background-color: var(--ground);
			background-image: radial-gradient(ellipse at 78% 8%, #273b332e, transparent 36%), radial-gradient(#b9d0c20b 0.7px, transparent 0.7px);
			background-size: auto, 19px 19px;
			font-family: "Space Grotesk", sans-serif;
		}
		button { font: inherit; }
		.shell { max-width: 1160px; margin: 0 auto; padding: 34px 28px 46px; }
		header { display: flex; align-items: center; justify-content: space-between; gap: 20px; border-bottom: 1px solid var(--line); padding-bottom: 24px; }
		.brand { display: flex; align-items: center; gap: 15px; }
		.mark { width: 42px; height: 42px; border: 1px solid var(--lime); border-radius: 50%; display: grid; place-items: center; color: var(--lime); font: 500 17px "DM Mono", monospace; }
		.eyebrow, .mono, .metric-label, .section-kicker { font-family: "DM Mono", monospace; text-transform: uppercase; letter-spacing: .08em; }
		.eyebrow { color: var(--muted); font-size: 10px; margin: 0 0 4px; }
		h1 { margin: 0; font-size: 21px; line-height: 1.1; font-weight: 600; }
		.mission-id { color: var(--muted); text-align: right; font: 11px/1.7 "DM Mono", monospace; }
		main { padding-top: 30px; }
		.mission-head { display: flex; align-items: end; justify-content: space-between; gap: 20px; margin-bottom: 22px; }
		.mission-head h2 { margin: 0; font-size: clamp(25px, 4vw, 36px); line-height: 1.1; font-weight: 500; }
		.mission-head p { color: var(--muted); margin: 8px 0 0; font-size: 14px; }
		.status { white-space: nowrap; border: 1px solid var(--line); padding: 8px 11px; color: var(--lime); font: 10px "DM Mono", monospace; text-transform: uppercase; letter-spacing: .08em; }
		.status.failed { color: var(--danger); border-color: #75453f; }
		.status.won { color: var(--cyan); border-color: #376a63; }
		.metrics { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); border: 1px solid var(--line); background: #111a17d9; margin-bottom: 26px; }
		.metric { min-width: 0; padding: 15px 16px 14px; border-right: 1px solid var(--line); }
		.metric:last-child { border-right: 0; }
		.metric-label { color: var(--muted); font-size: 9px; display: block; margin-bottom: 10px; }
		.metric-value { font: 500 23px "DM Mono", monospace; }
		.metric-value small { font-size: 11px; color: var(--muted); }
		.metric-value.warn { color: var(--warning); }
		.workspace { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(250px, .8fr); gap: 38px; }
		.section-head { display: flex; align-items: baseline; justify-content: space-between; border-bottom: 1px solid var(--line); padding-bottom: 12px; margin-bottom: 14px; }
		.section-kicker { color: var(--muted); font-size: 10px; }
		.section-head h3 { margin: 0; font-size: 14px; font-weight: 500; }
		.project-list { display: grid; gap: 8px; }
		.project { display: grid; grid-template-columns: 40px minmax(0, 1fr) auto; align-items: center; gap: 14px; min-height: 76px; padding: 12px 15px; border: 1px solid var(--line); background: #141d1ad9; transition: border-color .16s ease, background .16s ease, transform .16s ease; }
		.project:hover { border-color: #819677; background: #1a2721; transform: translateX(2px); }
		.project-number { width: 34px; height: 34px; display: grid; place-items: center; border: 1px solid #46564e; color: var(--lime); font: 12px "DM Mono", monospace; }
		.project h4 { margin: 0 0 4px; font-size: 14px; font-weight: 600; }
		.project p { color: var(--muted); margin: 0; font-size: 12px; line-height: 1.45; }
		.project button { min-width: 76px; border: 1px solid #61744f; background: transparent; color: var(--lime); padding: 8px 10px; cursor: pointer; font: 10px "DM Mono", monospace; text-transform: uppercase; }
		.project button:hover:not(:disabled) { color: var(--ground); background: var(--lime); }
		.project button:disabled { cursor: not-allowed; opacity: .4; }
		.side { min-width: 0; }
		.progress-line { height: 3px; background: #303b36; margin: 2px 0 19px; }
		.progress-line span { display: block; height: 100%; background: var(--lime); transition: width .25s ease; }
		.feed { display: grid; gap: 0; border-left: 1px solid var(--line); margin: 0 0 22px 3px; padding: 0; list-style: none; }
		.feed li { position: relative; color: #c4cdc5; padding: 0 0 15px 16px; font-size: 12px; line-height: 1.5; }
		.feed li::before { content: ""; position: absolute; width: 5px; height: 5px; left: -3px; top: 5px; background: var(--cyan); border-radius: 50%; box-shadow: 0 0 9px #83d9d077; }
		.medal { color: var(--lime); font-size: 13px; margin: 0 0 16px; }
		.restart { border: 1px solid var(--line); background: transparent; color: var(--ink); padding: 9px 12px; cursor: pointer; font: 10px "DM Mono", monospace; text-transform: uppercase; }
		.restart:hover { border-color: var(--cyan); color: var(--cyan); }
		footer { margin-top: 34px; padding-top: 14px; border-top: 1px solid var(--line); color: #74817a; font: 9px "DM Mono", monospace; text-transform: uppercase; letter-spacing: .07em; }
		@media (max-width: 880px) { .metrics { grid-template-columns: repeat(4, minmax(0, 1fr)); } .metric:nth-child(4) { border-right: 0; } .metric:nth-child(n+5) { border-top: 1px solid var(--line); } .metric:nth-child(5) { border-right: 1px solid var(--line); } }
		@media (max-width: 650px) { .shell { padding: 22px 16px 32px; } header { padding-bottom: 18px; } .mission-head { align-items: start; flex-direction: column; } .workspace { grid-template-columns: 1fr; gap: 30px; } .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); } .metric, .metric:nth-child(4), .metric:nth-child(5) { border-right: 1px solid var(--line); border-top: 1px solid var(--line); } .metric:nth-child(odd) { border-right: 1px solid var(--line); } .metric:nth-child(even) { border-right: 0; } .metric:first-child, .metric:nth-child(2) { border-top: 0; } .project { grid-template-columns: 34px minmax(0, 1fr); gap: 10px; padding: 12px; } .project button { grid-column: 2; justify-self: start; } .mission-id { font-size: 9px; } }
		@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: .01ms !important; } }
	</style>
</head>
<body>
	<div class="shell">
		<header>
			<div class="brand">
				<div class="mark" aria-hidden="true">MO</div>
				<div><p class="eyebrow">Lunar surface operations</p><h1>Moon Outpost</h1></div>
			</div>
			<div class="mission-id">MISSION 006<br>TRANQUILITY SECTOR</div>
		</header>
		<main>
			<div class="mission-head">
				<div><h2>Keep the crew alive.</h2><p>Six days. Finite supplies. Your call, Commander.</p></div>
				<div class="status {{ state.status }}">{{ "Mission active" if state.status == "playing" else ("Mission complete" if state.status == "won" else "Mission failed") }}</div>
			</div>
			<div class="metrics" aria-label="Outpost supplies">
				<div class="metric"><span class="metric-label">Day</span><div class="metric-value">{{ state.day }}<small> / 6</small></div></div>
				<div class="metric"><span class="metric-label">Oxygen</span><div class="metric-value {{ 'warn' if state.oxygen <= 2 else '' }}">{{ state.oxygen }}<small> packs</small></div></div>
				<div class="metric"><span class="metric-label">Food</span><div class="metric-value {{ 'warn' if state.food <= 2 else '' }}">{{ state.food }}<small> packs</small></div></div>
				<div class="metric"><span class="metric-label">Power</span><div class="metric-value {{ 'warn' if state.power <= 2 else '' }}">{{ state.power }}</div></div>
				<div class="metric"><span class="metric-label">Solar output</span><div class="metric-value">{{ state.solar_output }}<small> / day</small></div></div>
				<div class="metric"><span class="metric-label">Shield layers</span><div class="metric-value">{{ state.shield_layers }}</div></div>
				<div class="metric"><span class="metric-label">Radiation</span><div class="metric-value {{ 'warn' if state.radiation_danger >= 30 else '' }}">{{ state.radiation_danger }}<small> / 50</small></div></div>
			</div>
			<div class="workspace">
				<section>
					<div class="section-head"><h3>Choose today's project</h3><span class="section-kicker">One action per day</span></div>
					<div class="project-list">
						<div class="project"><div class="project-number">01</div><div><h4>Build solar panels</h4><p>No power cost. Solar output increases by 2 per day.</p></div><form method="post"><button name="choice" value="1" {{ 'disabled' if state.status != 'playing' }}>Select</button></form></div>
						<div class="project"><div class="project-number">02</div><div><h4>Grow food</h4><p>Costs 1 power. Add 3 food packs.</p></div><form method="post"><button name="choice" value="2" {{ 'disabled' if state.status != 'playing' }}>Select</button></form></div>
						<div class="project"><div class="project-number">03</div><div><h4>Fix oxygen recycler</h4><p>Costs 1 power. Add 3 oxygen packs.</p></div><form method="post"><button name="choice" value="3" {{ 'disabled' if state.status != 'playing' }}>Select</button></form></div>
						<div class="project"><div class="project-number">04</div><div><h4>Add a shield layer</h4><p>Costs 2 power. Reduce daily radiation damage.</p></div><form method="post"><button name="choice" value="4" {{ 'disabled' if state.status != 'playing' }}>Select</button></form></div>
					</div>
				</section>
				<aside class="side">
					<div class="section-head"><h3>Mission log</h3><span class="section-kicker">Day {{ state.day }} / 6</span></div>
					<div class="progress-line" aria-label="Mission progress"><span style="width: {{ (state.day / 6 * 100)|int }}%"></span></div>
					<ul class="feed">{% for entry in state.feed %}<li>{{ entry }}</li>{% endfor %}</ul>
					{% if state.status == "won" %}<p class="medal">Mission score: {{ state.oxygen + state.food + state.power }} supplies. {{ state.medal }}</p>{% endif %}
					<form method="post"><button class="restart" name="restart" value="1">Restart mission</button></form>
				</aside>
			</div>
		</main>
		<footer>Mission control // Tranquility base // Keep the crew breathing</footer>
	</div>
</body>
</html>"""


def new_game():
	return {
		"day": 1,
		"oxygen": 5,
		"food": 5,
		"power": 8,
		"solar_output": 2,
		"shield_layers": 0,
		"radiation_danger": 0,
		"status": "playing",
		"feed": ["Mission control online. Select a project to begin day 1."],
		"medal": "",
	}


def finish_day(state, choice):
	messages = []
	if choice == "1":
		state["solar_output"] += 2
		messages.append(f"Solar panels built. Output is now {state['solar_output']} power per day.")
	elif choice == "2":
		if state["power"] >= 1:
			state["power"] -= 1
			state["food"] += 3
			messages.append("Food grown: +3 packs, -1 power.")
		else:
			messages.append("Not enough power to grow food.")
	elif choice == "3":
		if state["power"] >= 1:
			state["power"] -= 1
			state["oxygen"] += 3
			messages.append("Oxygen recycler fixed: +3 packs, -1 power.")
		else:
			messages.append("Not enough power to fix the recycler.")
	elif choice == "4":
		if state["power"] >= 2:
			state["power"] -= 2
			state["shield_layers"] += 1
			messages.append(f"Shield added: {state['shield_layers']} layer(s) active, -2 power.")
		else:
			messages.append("Not enough power to add a shield.")

	day = state["day"]
	state["oxygen"] -= 1
	state["food"] -= 1
	state["power"] += state["solar_output"] - 2
	messages.append(f"Crew used 1 oxygen and 1 food. Solar generated {state['solar_output']} power; the outpost used 2.")
	radiation_increase = max(0, 10 - 3 * state["shield_layers"])
	state["radiation_danger"] += radiation_increase
	messages.append(f"Radiation increased by {radiation_increase}.")
	if day == 3:
		state["radiation_danger"] += 5
		messages.append("Solar storm: radiation increased by 5.")

	if state["oxygen"] <= 0:
		state["status"] = "failed"
		messages.append("Mission failed: oxygen ran out.")
	elif state["food"] <= 0:
		state["status"] = "failed"
		messages.append("Mission failed: food ran out.")
	elif state["power"] < 0:
		state["status"] = "failed"
		messages.append("Mission failed: power dropped below zero.")
	elif state["radiation_danger"] > 50:
		state["status"] = "failed"
		messages.append("Mission failed: radiation danger went above 50.")
	elif day == 6:
		state["status"] = "won"
		supply_score = state["oxygen"] + state["food"] + state["power"]
		state["medal"] = "Gold medal" if supply_score >= 25 else "Silver medal" if supply_score >= 15 else "Bronze medal"
		messages.append(f"Mission success. The crew survived all six days. {state['medal']}.")
	else:
		state["day"] += 1

	state["feed"] = (messages + state["feed"])[:8]


@app.route("/", methods=["GET", "POST"])
def index():
	if "game" not in session:
		session["game"] = new_game()

	if request.method == "POST":
		if request.form.get("restart"):
			session["game"] = new_game()
		else:
			choice = request.form.get("choice", "")
			if choice in PROJECTS and session["game"]["status"] == "playing":
				finish_day(session["game"], choice)
			session.modified = True
		return redirect(url_for("index"))

	return render_template_string(PAGE, state=session["game"])


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))


