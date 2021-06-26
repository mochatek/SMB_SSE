from flask import Flask, session, render_template, request, Response
from middlewares import session_manager
from services import MessageBroker, format_SSE
from os import environ

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')

message_broker = MessageBroker()


################################## ROUTES ##################################

@app.route('/')
@session_manager
def index():
    return render_template('index.html', user=session.get('user'))


@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    to = data['to']
    msg = data['msg']

    try:
        message_broker.publish(to, msg)
        return {"message_sent": True}, 200
    except:
        return {"message_sent": False}, 400


@app.route('/notify')
@session_manager
def notify():
    messageQ = message_broker.subscribe(session.get('user'))

    def stream():
        while 1:
            msg = messageQ.get()
            yield format_SSE(msg)

    return Response(stream(), mimetype='text/event-stream')


###############################################################################


if __name__ == '__main__':
    app.run('', 5000, debug=True)
