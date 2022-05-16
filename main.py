from flask import Flask, render_template, request, jsonify
from knowledgeengine import CareerRecommend, Saber11


engine = CareerRecommend()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/test', methods=['GET', 'POST'])
def testfn():    # GET request
    if request.method == 'GET':
        message = {'greeting':'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers    # POST request
    if request.method == 'POST':
        print(request.get_json())  # parse as JSON
        return 'Sucesss', 200


@app.route('/getgrades/', methods=['GET', 'POST'])
def data_get():
    math_grade = int(request.args.get('math'))
    natural_grade = int(request.args.get('natural'))
    social_grade = int(request.args.get('social'))

    # Restart engine
    engine.reset()
    # Add fact to the engine
    engine.declare(Saber11(math=math_grade, natural=natural_grade, social=social_grade))
    engine.run()

    if request.method == 'POST':  # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200

    else:  # GET request
        return 'Math: %s ; Natural %s ; Social %s' % \
               (engine.get_math_cat(), engine.get_natural_cat(), engine.get_social_cat())


if __name__ == '__main__':
    engine.reset()
    app.run(debug=True)