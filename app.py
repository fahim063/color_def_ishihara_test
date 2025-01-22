import os
import json


#from flask import Flask, render_template, request, jsonify, send_from_directory
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions in the filesystem
Session(app)




# Serve static files explicitly (if needed)
#@app.route('/static/<path:filename>')
#def static_files(filename):
    #return send_from_directory('static', filename)


# Ishihara test plates data
plates = [
    {"id": 1, "image": "Plate1.jpg", "options": ["12", "18", "16", "Nothing"], "normal": "12", "deficiency": "Nothing", "total": "Nothing"},
    {"id": 1, "image": "Plate2.jpg", "options": ["3", "8","16", "Nothing"], "normal": "8", "deficiency": "3", "total": "Nothing"},
    {"id": 1, "image": "Plate3.jpg", "options": ["70", "28","29", "Nothing"], "normal": "29", "deficiency": "70", "total": "Nothing"},
    {"id": 1, "image": "Plate4.jpg", "options": ["2", "5", "6","Nothing"], "normal": "5", "deficiency": "2", "total": "Nothing"},
    {"id": 1, "image": "Plate5.jpg", "options": ["3", "5","8","Nothing"], "normal": "3", "deficiency": "5", "total": "Nothing"},
    {"id": 1, "image": "Plate6.jpg", "options": ["45", "17","15", "Nothing"], "normal": "15", "deficiency": "17", "total": "Nothing"},
    {"id": 1, "image": "Plate7.jpg", "options": ["21", "71","74", "Nothing"], "normal": "74", "deficiency": "21", "total": "Nothing"},
    {"id": 1, "image": "Plate8.jpg", "options": ["0", "6","8", "Nothing"], "normal": "6", "deficiency": "0", "total": "Nothing"},
    {"id": 1, "image": "Plate9.jpg", "options": ["15", "45","46", "Nothing"], "normal": "45", "deficiency": "46", "total": "Nothing"},
    {"id": 1, "image": "Plate10.jpg", "options": ["5", "6","8", "Nothing"], "normal": "5", "deficiency": "Nothing", "total": "Nothing"},
    {"id": 1, "image": "Plate11.jpg", "options": ["1", "4","7", "Nothing"], "normal": "7", "deficiency": "1", "total": "Nothing"},
    {"id": 1, "image": "Plate12.jpg", "options": ["12", "18","16", "Nothing"], "normal": "16", "deficiency": "18", "total": "Nothing"},
    {"id": 1, "image": "Plate13.jpg", "options": ["73", "48","13", "Nothing"], "normal": "73", "deficiency": "Nothing", "total": "Nothing"},
    {"id": 1, "image": "Plate16.jpg", "options": ["2", "6", "26","Nothing"], "normal": "26", "deficiency": ["2","6"], "total": "Nothing"},
    {"id": 1, "image": "Plate17.jpg", "options": ["4", "42","2", "Nothing"], "normal": "42", "deficiency": ["4","2"], "total": "Nothing"},
    
]


# Path to store user results
RESULTS_FILE = "results/user_results.json"

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/test/<int:plate_id>', methods=['GET', 'POST'])
def test(plate_id):
    if plate_id > len(plates):  # End of test
        return redirect(url_for('results'))

    if request.method == 'POST':
        # Save user response for the current plate
        user_answer = request.form.get('answer', "No Answer")
        if 'responses' not in session:
            session['responses'] = {}
        session['responses'][str(plate_id)] = user_answer
        session.modified = True  # Mark session as modified

        # Redirect to the next plate
        return redirect(url_for('test', plate_id=plate_id + 1))

    # Render the current plate
    plate = plates[plate_id - 1]
    return render_template('test.html', plate=plate, plate_id=plate_id)


@app.route('/results')
def results():
    responses = session.get('responses', {})
    normal_count = 0
    deficiency_count = 0
    result_details = []

    for i, plate in enumerate(plates, start=1):
        user_answer = responses.get(str(i), "No Answer")
        if user_answer == plate['normal']:
            normal_count += 1
            result_type = "Normal"
        elif user_answer in plate['deficiency']:
            deficiency_count += 1
            result_type = "Red-Green Deficiency"
        else:
            result_type = "Incorrect/No Answer"

        result_details.append({
            "plate_no": i,
            "user_answer": user_answer,
            "correct_answer": plate['normal'],
            "result_type": result_type
        })

    # Diagnosis
    total_plates = len(plates)
    correct_percentage = (normal_count / total_plates) * 100
    diagnosis = "Normal color vision" if deficiency_count < normal_count else "Red-Green Color Deficiency Detected"
    
        # Save the results to a JSON file
    user_result = {
        "diagnosis": diagnosis,
        "test_result": f"{correct_percentage:.1f}% ({normal_count}/{total_plates})",
        "results": result_details
    }
    save_results(user_result)

    return render_template('results.html', diagnosis=diagnosis, correct_percentage=correct_percentage, results=result_details)

def save_results(user_result):
    # Check if the results file exists, and create if it doesn't
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'w') as file:
            json.dump([], file)

    # Append the new result to the file
    with open(RESULTS_FILE, 'r+') as file:
        data = json.load(file)
        data.append(user_result)
        file.seek(0)
        json.dump(data, file, indent=4)



if __name__ == '__main__':
    app.run(debug=True)

