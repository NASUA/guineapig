from flask import Flask, render_template, request, jsonify
from openai import OpenAI
client = OpenAI(
    api_key='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'
)

app = Flask(__name__)



@app.route('/')
def index():
    # Serve the main page
    return render_template('index.html')

@app.route('/process_speech', methods=['POST'])
def process_speech():
    data = request.json
    speech_text = data['speechText']
    print(speech_text)
    try:
        # Call to OpenAI API for processing the speech text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Adjust based on the latest model
            messages=[
                {"role": "system", "content": "You are a guinea pig, with tons of background of funny stories for kids about canada and ecuador. \
                 You are gracious and output no more than 100 words. may your output as a rime \
                 "},
                {"role": "user", "content": speech_text},
            ])
       
        translated_text = response.choices[0].message.content
        print(translated_text)
        # Return the translated text to the frontend
        return jsonify({'translatedText': translated_text})
    except Exception as e:
        print(f"Failed to process speech text: {e}")
        return jsonify({'error': 'Failed to process speech text'}), 500

if __name__ == '__main__':
    app.run(debug=True)
