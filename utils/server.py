import socketio
import eventlet
from flask import Flask

# Création de l'instance Socket.IO
sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)
app = socketio.WSGIApp(sio, app)

# Liste pour stocker les utilisateurs connectés
connected_users = []

# Événement de connexion
@sio.event
def connect(sid, environ):
    print(f'Client connecté: {sid}')
    connected_users.append(sid)
    sio.emit('user_count', len(connected_users))

# Événement de déconnexion
@sio.event
def disconnect(sid):
    print(f'Client déconnecté: {sid}')
    if sid in connected_users:
        connected_users.remove(sid)
    sio.emit('user_count', len(connected_users))

# Événement pour recevoir un message
@sio.event
def message(sid, data):
    print(f'Message reçu de {sid}: {data}')
    # Diffuser le message à tous les clients connectés
    sio.emit('message', {'user': sid, 'text': data})

# Événement pour recevoir un message privé
@sio.event
def private_message(sid, data):
    if 'target' in data and 'text' in data:
        target_sid = data['target']
        message_text = data['text']
        # Envoyer le message uniquement à l'utilisateur ciblé
        sio.emit('private_message', {'user': sid, 'text': message_text}, room=target_sid)
        print(f'Message privé de {sid} à {target_sid}: {message_text}')

if __name__ == '__main__':
    # Démarrer le serveur sur le port 5000
    print('Serveur Socket.IO démarré sur http://localhost:5000')
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)