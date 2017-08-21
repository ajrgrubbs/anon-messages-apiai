from collections import deque
from argparse import ArgumentParser

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

allowed_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789,.?!\'":;- \n\r')
messages = deque([])


@app.route('/add_message', methods=['POST'])
def add_message():
    req = request.get_json(silent=True, force=True)
    message = _clean_message(str(req.get('message', '')))
    if message:
        messages.append(message)
        return 'Message stored'
    else:
        return 'Invalid input', 400


def _clean_message(message: str):
    if len(message) > 250:
        message = message[0:250]
    message_chars = [c for c in message if c in allowed_chars]
    return ''.join(message_chars)


@app.route('/get_message', methods=['POST'])
def get_message():
    result = dict()
    if not messages:
        result['speech'] = result['displayText'] = 'No messages remaining. Goodbye!'
        result['data'] = {
            'google': {
                'expect_user_response': False
            }
        }
        return jsonify(result)

    result['speech'] = result['displayText'] = messages.popleft()
    return jsonify(result)


if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument('--port', type=int, default=5050)
    ap.add_argument('--host', default='0.0.0.0')
    args = ap.parse_args()

    port = args.port
    host = args.host

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host=host)
