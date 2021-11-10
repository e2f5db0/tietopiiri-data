from application import app, db
from flask import request, abort, jsonify
from application.topics.models import Topic, WinnerTopic
import json
import random

# Add a topic
@app.route('/add', methods=['POST'])
def add_topic():
    name = str(request.form['name'])
    created_by = str(request.form['created_by'])
    try:
        topic = Topic(name, created_by)
        db.session().add(topic)
        db.session().commit()
        return jsonify({'success': 'topic added'})
    except:
        return jsonify({'error': 'topic not added'})

# Get a topic
@app.route('/topic/<id>')
def get_topic(id):
    topic = Topic.query.get_or_404(id)
    if topic:
        return jsonify(topic)
    else:
        abort(404)

# Get winner topics
@app.route('/winnertopics', methods=['GET'])
def get_winnertopics():
    winner_topics = WinnerTopic.query.with_entities(WinnerTopic.id, WinnerTopic.name).order_by(WinnerTopic.date_created.desc())
    ts = []
    for t in winner_topics:
        ts.append({
            'id': t.id,
            'name': t.name
            })
    return jsonify(ts)

# Get winner topics
@app.route('/selectwinner', methods=['GET'])
def select_new_winnertopic():
    try:
        topics = Topic.query.with_entities(Topic.id, Topic.name, Topic.votes).order_by(Topic.date_created.desc())
        valid_topics = []
        for topic in topics:
            votes = json.loads(topic.votes)
            if len(votes['users']) >= 3:
                valid_topics.append(topic)
        winner = random.choice(valid_topics)
        winner_topic = set_winner_topic(winner.id)
        return winner_topic
    except:
        return jsonify({'error': 'winner topic not selected'})

# Delete a topic
@app.route('/delete/<id>')
def delete_topic(id):
    topic = Topic.query.get_or_404(id)
    if topic:
        db.session.delete(topic)
        db.session.commit()
        return jsonify({'success': 'topic deleted'})
    else:
        return jsonify({'error': 'topic not deleted'})

# Get all topics
@app.route('/topics', methods=['GET'])
def get_topics():
    topics = Topic.query.with_entities(Topic.id, Topic.name, Topic.votes).order_by(Topic.date_created.desc())
    ts = []
    for t in topics:
        votes = json.loads(t.votes)
        ts.append({
            'id': t.id,
            'name': t.name,
            'votes': votes['users']
            })
    return jsonify(ts)

@app.route('/vote/<id>', methods=['POST'])
def vote_topic(id):
    try:
        topic = Topic.query.get_or_404(id)
        votes = json.loads(topic.votes)
        user = str(request.form['user'])
        if user not in votes['users']:
            votes['users'].append(user)
            topic.votes = json.dumps(votes)
            db.session.commit()
            return jsonify({'success': 'vote added'})
        else:
            return jsonify({'success': 'cannot vote two times'})
    except:
        abort(404)

# Delete a topic
@app.route('/winner/<id>')
def set_winner_topic(id):
    topic = Topic.query.get_or_404(id)
    winner_topic = WinnerTopic(topic.name, topic.created_by)
    if topic:
        db.session.add(winner_topic)
        db.session.delete(topic)
        db.session.commit()
        winner = WinnerTopic.query.filter(WinnerTopic.name == winner_topic.name).first()
        if winner:
            return jsonify({
                'name': winner.name,
                'created_by': winner.created_by
            })
    else:
        return jsonify({'error': 'winner topic not set'})
