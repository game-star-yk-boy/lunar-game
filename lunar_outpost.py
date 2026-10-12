oxygen = 5
food = 5
power = 8
solar_output = 2
shield_layers = 0
radiation_danger = 0


def show_status(day, oxygen, food, power, solar_output, shield_layers, radiation_danger):
	print(f"\nDay {day} of 6")
	print(f"Oxygen: {oxygen}")
	print(f"Food: {food}")
	print(f"Power: {power}")
	print(f"Solar output: {solar_output} power each day")
	print(f"Shield layers: {shield_layers}")
	print(f"Radiation danger: {radiation_danger}/50")


print("MOON OUTPOST")
print("Can you keep your crew safe on the Moon for six days?")
print("Choose projects and manage supplies to help them survive.")

show_status(1, oxygen, food, power, solar_output, shield_layers, radiation_danger)

print("\nChoose a project:")
print("1. Build solar panels (no power; solar output increases by 2 each day from now on)")
print("2. Grow food (cost: 1 power; add 3 food packs)")
print("3. Fix the oxygen recycler (cost: 1 power; add 3 oxygen packs)")
print("4. Add a shield layer (cost: 2 power; add 1 shield layer)")

while True:
	project_choice = input("Type 1, 2, 3, or 4: ").strip()
	if project_choice in ("1", "2", "3", "4"):
		break
	print("Please type 1, 2, 3, or 4.")

if project_choice == "1":
	solar_output += 2
	print("Solar panels built. Solar output is now", solar_output, "power each day.")
elif project_choice == "2":
	if power >= 1:
		power -= 1
		food += 3
		print("You grew food, used 1 power, and gained 3 food packs.")
	else:
		print("There is not enough power to grow food. No power or food was changed.")
elif project_choice == "3":
	if power >= 1:
		power -= 1
		oxygen += 3
		print("The oxygen recycler is fixed. You used 1 power and gained 3 oxygen packs.")
	else:
		print("There is not enough power to fix the recycler. No power or oxygen was changed.")
elif project_choice == "4":
	if power >= 2:
		power -= 2
		shield_layers += 1
		print("You added a shield layer, used 2 power, and now have", shield_layers, "shield layers.")
	else:
		print("There is not enough power to add a shield. No power or shield layers were changed.")

