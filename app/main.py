from flask import Flask, render_template, request, jsonify
from app.knowledgeengine import CareerRecommend, Saber11, Preference

engine = CareerRecommend()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/initialize', methods=['GET', 'POST'])
def initialize():
    if request.method == 'GET':     # GET request
        # Restart engine
        engine.reset()
        engine.msg_buffer = []
        engine.reset_choice()
        return '0'
    if request.method == 'POST':    # POST request
        return '1'


@app.route('/getgrades/', methods=['GET', 'POST'])
def grades_get():
    math_grade = int(request.args.get('math'))
    natural_grade = int(request.args.get('natural'))
    social_grade = int(request.args.get('social'))

    # Add fact to the engine
    engine.declare(Saber11(math=math_grade, natural=natural_grade, social=social_grade))
    engine.run()

    if request.method == 'POST':  # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200

    else:  # GET request
        msg_cat = {'math': engine.get_math_cat(), 'natural': engine.get_natural_cat(),
                   'social': engine.get_social_cat()}
        return jsonify(msg_cat)


@app.route('/getpref/', methods=['GET', 'POST'])
def pref_get():
    pref_human = False
    pref_engine = False
    pref_science = False
    pref_health = False

    if request.args.get('human') == 'true':
        pref_human = True
    if request.args.get('engine') == 'true':
        pref_engine = True
    if request.args.get('science') == 'true':
        pref_science = True
    if request.args.get('health') == 'true':
        pref_health = True

    # Add fact to the engine
    engine.declare(Preference(engineering=pref_engine, science=pref_science, humanities=pref_human, health=pref_health))
    engine.run()

    if request.method == 'POST':  # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    else:  # GET request
        return 'Humanities: %s ; Engineering %s ; Science %s ; Health: %s' % \
               (str(pref_human), str(pref_engine), str(pref_science), str(pref_health))


@app.route('/choice', methods=['GET', 'POST'])
def get_choice():
    message = {'humanities': engine.get_humanities_choice(),
               'engineering': engine.get_engineering_choice(),
               'science': engine.get_science_choice(),
               'health': engine.get_health_choice()}

    if request.method == 'GET':     # GET request
        return jsonify(message)     # serialize and use JSON headers
    if request.method == 'POST':    # POST request
        print(request.get_json())   # parse as JSON
        return 'Sucesss', 200


@app.route('/reasonlist', methods=['GET', 'POST'])
def get_inferences():
    message = {}
    for i, msg in enumerate(engine.msg_buffer):
        message[i] = msg

    if request.method == 'GET':     # GET request
        return jsonify(message)     # serialize and use JSON headers
    if request.method == 'POST':    # POST request
        print(request.get_json())   # parse as JSON
        return 'Sucesss', 200


if __name__ == '__main__':
    engine.reset()
    app.run(debug=True)
