# app.py
import os
import sqlite3
import random
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import sys
sys.path.append(os.path.abspath("C:/Users/hp/OneDrive/Desktop/emotion_detector"))  
from emotion_webcam import detect_emotion


BASE = os.path.dirname(__file__)
DB = os.path.join(BASE, 'app.db')
FRONTEND_GAMES = os.path.join(BASE, 'static', 'games')

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# ---- seed recommendations (small curated lists) ----
# You may replace these YouTube IDs and game filenames with your choices.
SEED_VIDEOS = {
  "happy": [
    {"id":"UPkMkIOzej8", "title":"Enjoy these songs!!"},
    {"id":"Udap-5rVWeM", "title":"Listen to this inspiring ted talk!!"},
    {"id":"C-m4xcUxXxs", "title":"The choice of being happy😊"}
  ],
  "neutral": [
    {"id":"l-sSxHiMopk", "title":"Just keep yourself motivated!!"},
    {"id":"BqSxjmvXzzY", "title":"Two phases of life..."},
    {"id":"YRJ6xoiRcpQ", "title":"Relax and meditate..."}
  ],
  "sad": [
    {"id":"RBowkudIags", "title":"Heal your mind😌"},
    {"id":"DmeOX5Zu36M", "title":"Don't doubt yourself!!"},
    {"id":"gIOdJ6ybYIM", "title":"Yoga-for mind and soul!!"}
  ],
  "angry": [
    {"id":"6m2Ma8uX74s", "title":"Just calm down!!"},
    {"id":"sbVBsrNnBy8", "title":"Anger is an ally:TedTalk"},
    {"id":"JNuIEqaBZgU", "title":"Calm your anger🤍!!"}
  ]
}

SEED_GAMES = {
  "happy": [
    {"id":"h1","title":"Memory Flip!!","file":"memory_flip.html"},
    {"id":"h2","title":"Are you an artist?","file":"draw.html"},
    {"id":"h3","title":"Solve the puzzle!!","file":"puzzle_game.html"}
  ],
  "neutral": [
    {"id":"n1","title":"Matching Colours!","file":"colour_match.html"},
    {"id":"n2","title":"Be quick!","file":"reaction_game.html"},
    {"id":"n3","title":"Jump Up!","file":"uplift_jump.html"}
  ],
  "sad": [
    {"id":"s1","title":"Caught in a maze?","file":"maze_runner.html"},
    {"id":"s2","title":"Whack a mole!!","file":"whack_mole.html"},
    {"id":"s3","title":"Collect the stars...","file":"catch_star.html"}
  ],
  "angry": [
    {"id":"a1","title":"Relax and Breathe!!","file":"breathing.html"},
    {"id":"a2","title":"Paint Your Peace...","file":"paint.html"},
    {"id":"a3","title":"You can do it!!","file":"hare_vs_tort.html"}
  ]
}

# ---- DB helpers ----
def query_db(query, args=(), one=False):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    con.commit()
    cur.close()
    con.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(query, args=()):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(query, args)
    con.commit()
    rid = cur.lastrowid
    cur.close()
    con.close()
    return rid

# ---- Pages ----
@app.route('/')
def index():
    # Main page; front-end JS handles detection and flows
    return render_template('index.html')

# Serve game files
@app.route('/games/<path:filename>')
def serve_game(filename):
    return send_from_directory(FRONTEND_GAMES, filename)

# ---- APIs ----
@app.route('/api/log_detection', methods=['POST'])
def log_detection():
    data = request.get_json(force=True)
    user_id = data.get('user_id', 1)
    emotion = data.get('emotion')
    confidence = float(data.get('confidence', 0.0))
    detected_at = datetime.utcnow().isoformat()
    rid = insert_db("INSERT INTO detections (user_id, emotion, confidence, detected_at) VALUES (?,?,?,?)",
                    (user_id, emotion, confidence, detected_at))
    return jsonify({"status":"ok", "detection_id": rid})

@app.route('/api/user_stats', methods=['GET'])
def user_stats():
    user_id = int(request.args.get('user_id', 1))
    limit = int(request.args.get('limit', 14))
    rows = query_db("SELECT emotion, detected_at FROM detections WHERE user_id=? ORDER BY detected_at DESC LIMIT ?", (user_id, limit))
    last = [{"emotion": r[0], "detected_at": r[1]} for r in rows]
    counts = {}
    for r in last:
        counts[r['emotion']] = counts.get(r['emotion'], 0) + 1 if isinstance(r, dict) else counts.update({r[0]: counts.get(r[0],0)+1})
    # If above logic didn't build counts (compat), rebuild:
    if not counts:
        counts = {}
        for r in last:
            counts[r['emotion']] = counts.get(r['emotion'], 0) + 1
    return jsonify({"last_detections": last, "counts": counts})

@app.route('/api/get_recommendations', methods=['GET'])
def get_recommendations():
    mood = request.args.get('emotion', 'neutral')
    user_id = int(request.args.get('user_id', 1))
    videos = SEED_VIDEOS.get(mood, [])
    games = SEED_GAMES.get(mood, [])
    return jsonify({"videos": videos, "games": games})

@app.route('/api/log_pick', methods=['POST'])
def log_pick():
    data = request.get_json(force=True)
    user_id = data.get('user_id', 1)
    detection_id = data.get('detection_id')
    kind = data.get('kind')  # 'video' or 'game'
    item_id = data.get('item_id')
    title = data.get('title', '')
    mood = data.get('mood', '')
    if kind == 'video':
        insert_db("INSERT INTO video_history (user_id, detection_id, mood, video_id, video_title, picked_at) VALUES (?,?,?,?,?,?)",
                  (user_id, detection_id, mood, item_id, title, datetime.utcnow().isoformat()))
    else:
        insert_db("INSERT INTO game_history (user_id, detection_id, mood, game_id, picked_at) VALUES (?,?,?,?,?)",
                  (user_id, detection_id, mood, item_id, datetime.utcnow().isoformat()))
    return jsonify({"status":"ok"})

@app.route('/api/submit_survey', methods=['POST'])
def submit_survey():
    data = request.get_json(force=True)
    user_id = data.get('user_id', 1)
    detection_id = data.get('detection_id')
    rating = int(data.get('rating', 0))
    comments = data.get('comments', '')
    insert_db("INSERT INTO survey (user_id, detection_id, rating, comments, submitted_at) VALUES (?,?,?,?,?)",
              (user_id, detection_id, rating, comments, datetime.utcnow().isoformat()))
    return jsonify({"status":"ok"})

@app.route("/detect")
def detect():
    emotion = detect_emotion()  # call the function from emotion_webcam.py
    return jsonify({"emotion": emotion})

if __name__ == '__main__':
    app.run(debug=True)
