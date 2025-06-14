from google.cloud import firestore
from models.player import Player, PlayerStats
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PlayerService:
    """Service for managing player data"""
    
    def __init__(self, db):
        self.db = db
        self.players_collection = 'players'
        self.stats_collection = 'player_stats'
    
    def create_player(self, player_data):
        """Create a new player"""
        try:
            player = Player(
                name=player_data.get('name'),
                position=player_data.get('position'),
                team=player_data.get('team'),
                age=player_data.get('age')
            )
            
            # Save to Firestore
            doc_ref = self.db.collection(self.players_collection).document(player.id)
            doc_ref.set(player.to_dict())
            
            logger.info(f"Created player: {player.name} (ID: {player.id})")
            return player.id
            
        except Exception as e:
            logger.error(f"Error creating player: {str(e)}")
            raise
    
    def get_player(self, player_id):
        """Get a player by ID"""
        try:
            doc_ref = self.db.collection(self.players_collection).document(player_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Error getting player {player_id}: {str(e)}")
            raise
    
    def get_all_players(self):
        """Get all players"""
        try:
            players = []
            docs = self.db.collection(self.players_collection).stream()
            
            for doc in docs:
                player_data = doc.to_dict()
                players.append(player_data)
            
            return players
            
        except Exception as e:
            logger.error(f"Error getting all players: {str(e)}")
            raise
    
    def update_player(self, player_id, update_data):
        """Update a player's information"""
        try:
            update_data['updated_at'] = datetime.utcnow()
            
            doc_ref = self.db.collection(self.players_collection).document(player_id)
            doc_ref.update(update_data)
            
            logger.info(f"Updated player: {player_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating player {player_id}: {str(e)}")
            raise
    
    def delete_player(self, player_id):
        """Delete a player"""
        try:
            # Delete player document
            self.db.collection(self.players_collection).document(player_id).delete()
            
            # Delete all player stats
            stats_query = self.db.collection(self.stats_collection).where('player_id', '==', player_id)
            for doc in stats_query.stream():
                doc.reference.delete()
            
            logger.info(f"Deleted player: {player_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting player {player_id}: {str(e)}")
            raise
    
    def add_player_stats(self, player_id, stats_data):
        """Add statistics for a player"""
        try:
            # Verify player exists
            player = self.get_player(player_id)
            if not player:
                raise ValueError(f"Player {player_id} not found")
            
            # Create stats object
            stats = PlayerStats(
                player_id=player_id,
                game_date=stats_data.get('game_date', datetime.utcnow()),
                **{k: v for k, v in stats_data.items() if k != 'game_date'}
            )
            
            # Save to Firestore
            doc_ref = self.db.collection(self.stats_collection).document(stats.id)
            doc_ref.set(stats.to_dict())
            
            logger.info(f"Added stats for player: {player_id}")
            return stats.id
            
        except Exception as e:
            logger.error(f"Error adding stats for player {player_id}: {str(e)}")
            raise
    
    def get_player_stats(self, player_id, limit=None):
        """Get statistics for a player"""
        try:
            query = self.db.collection(self.stats_collection).where('player_id', '==', player_id)
            query = query.order_by('game_date', direction=firestore.Query.DESCENDING)
            
            if limit:
                query = query.limit(limit)
            
            stats = []
            for doc in query.stream():
                stats.append(doc.to_dict())
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting stats for player {player_id}: {str(e)}")
            raise
    
    def get_players_by_team(self, team):
        """Get all players from a specific team"""
        try:
            players = []
            docs = self.db.collection(self.players_collection).where('team', '==', team).stream()
            
            for doc in docs:
                players.append(doc.to_dict())
            
            return players
            
        except Exception as e:
            logger.error(f"Error getting players for team {team}: {str(e)}")
            raise
