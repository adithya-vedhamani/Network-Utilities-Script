from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

def nslookup(query, options=None, server=None):
    command = ["nslookup"]

    if options:
        command.extend(options)

    command.append(query)

    if server:
        command.extend(["-server", server])

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing nslookup: {e}"

@app.route('/nslookup', methods=['GET'])
def nslookup_api():
    query = request.args.get('query', '')
    options = request.args.get('options', '').split(',')
    server = request.args.get('server', '')

    result = nslookup(query, options=options, server=server)

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)

# curl -X GET "http://127.0.0.1:5000/nslookup?query=example.com&options=-type=a"
