import requests

def get_exercise_info(exercise_name):
    url = 'https://wger.de/api/v2/exerciseinfo/?language=2&limit=1000'
    response = requests.get(url)
    data = response.json()

    for item in data['results']:
        # Loop through translations to find the English name
        for translation in item.get('translations', []):
            if translation.get('language') == 2:
                translated_name = translation.get('name', '').lower()
                if exercise_name.lower() in translated_name:
                    muscles = [m['name_en'].lower() for m in item['muscles']]
                    secondary = [m['name_en'].lower() for m in item['muscles_secondary']]
                    return {
                        "found_name": translation['name'],
                        "main_muscles": muscles,
                        "secondary_muscles": secondary
                    }
    return None


def validate_muscles(llm_output):
    info = get_exercise_info(llm_output['exercise_name'])
    if not info:
        print("❌ Exercise not found in wger database.")
        return

    claimed = set(m.lower() for m in llm_output['claimed_muscles'])
    actual = set(info['main_muscles'] + info['secondary_muscles'])

    matched = claimed & actual
    missed = claimed - actual

    print(f"✅ Found exercise: {info['found_name']}")
    print(f"💪 Actual muscles: {actual}")
    print(f"✔️ Matched: {matched}")
    print(f"❌ Missed: {missed}")

# Example usage
llm_output = {
    "exercise_name": "Dumbbell Lunge",
    "claimed_muscles": ["glutes", "hamstrings"]
}

validate_muscles(llm_output)
