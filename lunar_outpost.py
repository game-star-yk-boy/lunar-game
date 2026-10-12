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

