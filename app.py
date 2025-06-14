from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google.cloud import firestore
import os
from dotenv import load_dotenv
from services.player_service import PlayerService
from services.analytics_service import AnalyticsService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Firestore client
db = firestore.Client()

# Initialize services
player_service = PlayerService(db)
analytics_service = AnalyticsService(db)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/players', methods=['GET'])
def get_players():
    """Get all players"""
    try:
        players = player_service.get_all_players()
        return jsonify(players)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players', methods=['POST'])
def create_player():
    """Create a new player"""
    try:
        data = request.get_json()
        player_id = player_service.create_player(data)
        return jsonify({'id': player_id, 'message': 'Player created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<player_id>', methods=['GET'])
def get_player(player_id):
    """Get a specific player"""
    try:
        player = player_service.get_player(player_id)
        if player:
            return jsonify(player)
        return jsonify({'error': 'Player not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<player_id>/stats', methods=['POST'])
def add_player_stats(player_id):
    """Add statistics for a player"""
    try:
        data = request.get_json()
        player_service.add_player_stats(player_id, data)
        return jsonify({'message': 'Stats added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/performance', methods=['GET'])
def get_performance_analytics():
    """Get performance analytics data"""
    try:
        time_period = request.args.get('period', 'week')
        analytics = analytics_service.get_performance_analytics(time_period)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard data"""
    try:
        metric = request.args.get('metric', 'score')
        limit = int(request.args.get('limit', 10))
        leaderboard = analytics_service.get_leaderboard(metric, limit)
        return jsonify(leaderboard)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/trends', methods=['GET'])
def get_trends():
    """Get trend analysis data"""
    try:
        player_id = request.args.get('player_id')
        trends = analytics_service.get_trends(player_id)
        return jsonify(trends)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'player-analytics-dashboard'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
