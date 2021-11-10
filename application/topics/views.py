from application import app, db
from flask import request, abort, jsonify
from application.topics.models import Topic, WinnerTopic

# Add a topic
@app.route('/add', methods=['POST'])
def add_topic():
    print(request.form)
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
    winner_topics = WinnerTopic.query.with_entities(WinnerTopic.id, WinnerTopic.name, WinnerTopic.votes).order_by(WinnerTopic.votes.desc())
    ts = []
    for t in winner_topics:
        ts.append({
            'id': t.id,
            'name': t.name,
            'votes': t.votes
            })
    return jsonify(ts)

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
    topics = Topic.query.with_entities(Topic.id, Topic.name, Topic.votes).order_by(Topic.votes.desc())
    ts = []
    for t in topics:
        ts.append({
            'id': t.id,
            'name': t.name,
            'votes': t.votes
            })
    return jsonify(ts)

@app.route('/vote/<id>', methods=['POST'])
def vote_topic(id):
    try:
        topic = Topic.query.get_or_404(id)
        if topic.votes < 6:
            topic.votes += 1
            db.session.commit()
            return jsonify({'success': 'vote added'})
        else:
            return jsonify({'success': 'maximum votes reached'})
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
        return jsonify({'success': 'winner topic set'})
    else:
        return jsonify({'error': 'winner topic not set'})
