from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find_route', methods=['POST'])
def find_route_api():
    data = request.json
    start_coords = data.get('start') #['10.773358', '106.6611492']
    end_coords = data.get('end')
    algorithm = data.get('algorithm')

    print(start_coords)
    print(end_coords)
    print(algorithm)

    if not start_coords or not end_coords or not algorithm:
        return jsonify({"error": "Invalid input"}), 400

#################
    if algorithm == "1": pass

    route = [[10.7769, 106.6670], [10.7775, 106.6680], [10.7780, 106.6690], [10.7790, 106.6700], [10.7800, 106.6710]]
##################

    return jsonify({"route": route})  # Return JSON including coordinates

if __name__ == '__main__':
    app.run(debug=True)
