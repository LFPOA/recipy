from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
import google.generativeai as genai

cuisines = [
    "",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek"
]

dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced"
]

# create a dictionary to store the languages and their corresponding codes
languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Thai': 'th',
    'Filipino': 'tl',
    'Vietnamese': 'vi'
    # ... potentially more based on actual Whisper support
}


app = Flask(__name__)
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html', 
                           cuisines=cuisines, 
                           dietary_restrictions=dietary_restrictions,
                           languages=languages)


@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # 사용자 입력 받기
    ingredients = request.form.getlist('ingredient')
    selected_cuisine = request.form.get('cuisine')
    selected_restrictions = request.form.getlist('restrictions')
    selected_laguage = request.form.get('language')

    if len([i for i in ingredients if i.strip()]) != 3:
        return "Kindly provide exactly 3 ingredients."

    # 프롬프트 구성
    prompt = f"""Craft a recipe in HTML in {selected_laguage}using \
{', '.join(ingredients)}.\
Ensure the recipe ingredients appear at the top,\
followed by the step-by-step instructions. Please do NOT wrap the response in markdown code blocks (no ```html)."""

    # 선택한 요리 유형을 프롬프트에 반영
    if selected_cuisine:
        prompt += f"\nThe cuisine should be {selected_cuisine}."

    if selected_restrictions and len(
        selected_restrictions
    ) > 0 :
        prompt += f"The recipe should have the following restrictions: {'.'.join(selected_restrictions)}."

    # Gemini API 호출
    try:
        response = model.generate_content(prompt)
        recipe = response.text
    except Exception as e:
        recipe = f"Error generating recipe: {str(e)}"

    return render_template('recipe.html', recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True)