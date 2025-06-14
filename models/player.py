from google.cloud import firestore
from datetime import datetime
import uuid

class Player:
    """Player data model"""
    
    def __init__(self, name, position, team, age=None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.position = position
        self.team = team
        self.age = age
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.stats = []
    
    def to_dict(self):
        """Convert player to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'team': self.team,
            'age': self.age,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'stats': self.stats
        }
    
    @staticmethod
    def from_dict(data):
        """Create player from dictionary"""
        player = Player(
            name=data.get('name'),
            position=data.get('position'),
            team=data.get('team'),
            age=data.get('age')
        )
        player.id = data.get('id', player.id)
        player.created_at = data.get('created_at', player.created_at)
        player.updated_at = data.get('updated_at', player.updated_at)
        player.stats = data.get('stats', [])
        return player

class PlayerStats:
    """Player statistics model"""
    
    def __init__(self, player_id, game_date, **kwargs):
        self.id = str(uuid.uuid4())
        self.player_id = player_id
        self.game_date = game_date
        self.created_at = datetime.utcnow()
        
        # Game statistics
        self.score = kwargs.get('score', 0)
        self.assists = kwargs.get('assists', 0)
        self.rebounds = kwargs.get('rebounds', 0)
        self.steals = kwargs.get('steals', 0)
        self.blocks = kwargs.get('blocks', 0)
        self.turnovers = kwargs.get('turnovers', 0)
        self.minutes_played = kwargs.get('minutes_played', 0)
        self.field_goals_made = kwargs.get('field_goals_made', 0)
        self.field_goals_attempted = kwargs.get('field_goals_attempted', 0)
        self.free_throws_made = kwargs.get('free_throws_made', 0)
        self.free_throws_attempted = kwargs.get('free_throws_attempted', 0)
        
        # Performance metrics
        self.efficiency_rating = self._calculate_efficiency()
    
    def _calculate_efficiency(self):
        """Calculate player efficiency rating"""
        if self.minutes_played == 0:
            return 0
        
        efficiency = (
            self.score + self.assists + self.rebounds + 
            self.steals + self.blocks - self.turnovers
        ) / self.minutes_played * 40
        
        return round(efficiency, 2)
    
    def to_dict(self):
        """Convert stats to dictionary"""
        return {
            'id': self.id,
            'player_id': self.player_id,
            'game_date': self.game_date,
            'created_at': self.created_at,
            'score': self.score,
            'assists': self.assists,
            'rebounds': self.rebounds,
            'steals': self.steals,
            'blocks': self.blocks,
            'turnovers': self.turnovers,
            'minutes_played': self.minutes_played,
            'field_goals_made': self.field_goals_made,
            'field_goals_attempted': self.field_goals_attempted,
            'free_throws_made': self.free_throws_made,
            'free_throws_attempted': self.free_throws_attempted,
            'efficiency_rating': self.efficiency_rating
        }
    
    @staticmethod
    def from_dict(data):
        """Create stats from dictionary"""
        stats = PlayerStats(
            player_id=data.get('player_id'),
            game_date=data.get('game_date'),
            **{k: v for k, v in data.items() if k not in ['id', 'player_id', 'game_date', 'created_at', 'efficiency_rating']}
        )
        stats.id = data.get('id', stats.id)
        stats.created_at = data.get('created_at', stats.created_at)
        return stats
