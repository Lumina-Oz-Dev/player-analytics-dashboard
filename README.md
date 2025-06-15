# 🏀 Player Analytics Dashboard

A comprehensive basketball player analytics dashboard that runs **locally with SQLite** or deploys to **Google Cloud with Firestore**. Perfect for development, learning, and production use!

## ⚡ Quick Start (No Cloud Credentials Required!)

**Want to try it immediately? Just run:**

```bash
# 1. Clone the repository
git clone https://github.com/Lumina-Oz-Dev/player-analytics-dashboard.git
cd player-analytics-dashboard

# 2. Install minimal dependencies  
pip install flask flask-cors python-dotenv

# 3. Start the standalone version
python app_standalone.py
```

**Open http://localhost:8080** and you'll have a full basketball analytics dashboard with:
- ✅ 8 NBA players with realistic stats
- ✅ Interactive charts and KPI cards
- ✅ Leaderboards and performance analytics  
- ✅ Modern responsive web interface
- ✅ No cloud setup required!

## 🚀 Features

### 📊 **Complete Analytics Dashboard**
- Real-time KPI cards (players, games, scores, efficiency)
- Interactive charts with Chart.js visualization
- Performance trends over customizable time periods
- Advanced filtering and comparison tools

### 👥 **Player Management**
- Add/edit players with detailed profiles
- Position and team organization
- Statistics tracking and history
- Comprehensive player database

### 🏆 **Dynamic Leaderboards**
- Rankings by score, efficiency, assists, rebounds
- Visual rank indicators (gold, silver, bronze)
- Real-time updates and sorting
- Team and position filtering

### 📈 **Advanced Analytics**
- Performance distribution analysis
- Trend analysis with historical data
- Efficiency rating calculations
- Team comparison metrics

## 🎯 Two Ways to Run

### Option 1: Local Development (Recommended to Start)
**Perfect for development, learning, and small-scale use**

- **Database**: SQLite (local file)
- **Setup Time**: 2 minutes
- **Dependencies**: Python + Flask only
- **Sample Data**: Auto-generated NBA players
- **Internet**: Works offline

```bash
python app_standalone.py
```

### Option 2: Cloud Production (When Ready)
**Perfect for production, scaling, and multi-user scenarios**

- **Database**: Google Cloud Firestore
- **Setup Time**: 15-30 minutes
- **Dependencies**: Google Cloud credentials
- **Sample Data**: Loadable via scripts
- **Internet**: Cloud-based

```bash
python app.py  # (requires Google Cloud setup)
```

### Smart Auto-Detection
**Don't know which to use?**

```bash
python start.py
```

The launcher automatically detects your setup and guides you to the best option!

## 📁 Project Structure

```
player-analytics-dashboard/
├── 🚀 app_standalone.py        # Standalone local version (SQLite)
├── ☁️ app.py                   # Cloud version (Firestore)  
├── 🎯 start.py                 # Smart launcher script
├── 📊 templates/               # Frontend dashboard
│   └── index.html              # Main dashboard interface
├── 🎨 static/                  # CSS, JavaScript, assets
│   ├── css/dashboard.css       # Modern styling
│   └── js/dashboard.js         # Interactive functionality
├── 🏀 models/                  # Data models
│   ├── player.py               # Cloud models (Firestore)
│   └── local_player.py         # Local models (SQLite)
├── ⚙️ services/                # Business logic
│   ├── player_service.py       # Cloud player service
│   ├── analytics_service.py    # Cloud analytics service
│   ├── local_player_service.py # Local player service
│   └── local_analytics_service.py # Local analytics service
├── 📖 QUICK_START_LOCAL.md     # Local setup guide
├── 📘 NO_CREDENTIALS_GUIDE.md  # Credential-free tutorial
├── 📋 requirements.txt         # Full dependencies
├── 📋 requirements-local.txt   # Minimal dependencies
└── 🧪 test_standalone.py       # Dependency validation
```

## 🛠 Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js for interactive visualizations
- **Local Database**: SQLite
- **Cloud Database**: Google Cloud Firestore
- **Deployment**: Google Cloud Run (ready)

## 📊 Sample Data Included

The standalone version automatically generates:

### NBA Players (8 Superstars)
- **LeBron James** (Lakers, Small Forward, 39)
- **Stephen Curry** (Warriors, Point Guard, 35)
- **Kevin Durant** (Suns, Small Forward, 35)
- **Giannis Antetokounmpo** (Bucks, Power Forward, 29)
- **Luka Dončić** (Mavericks, Point Guard, 25)
- **Jayson Tatum** (Celtics, Small Forward, 26)
- **Nikola Jokić** (Nuggets, Center, 29)
- **Joel Embiid** (76ers, Center, 30)

### Realistic Game Statistics
- **5-12 games per player** with historical data
- **Realistic scoring**: 12-45 points per game
- **Complete stats**: Assists, rebounds, steals, blocks
- **Advanced metrics**: Efficiency ratings calculated automatically
- **Time-based data**: Spanning 60 days for trend analysis

## 🎮 Dashboard Sections

### 1. **Overview Dashboard**
- KPI cards showing key metrics
- Performance trends chart
- Top performers list
- Real-time data updates

### 2. **Player Management**  
- Add new players with detailed information
- View all players in sortable table
- Player statistics tracking
- Team organization

### 3. **Advanced Analytics**
- Time period analysis (week/month/year)
- Performance distribution charts
- Player comparison visualizations
- Trend analysis and insights

### 4. **Dynamic Leaderboards**
- Rankings by multiple metrics
- Visual rank indicators
- Team and position information
- Games played statistics

## 🌐 API Endpoints

### Players
```
GET    /api/players              # Get all players
POST   /api/players              # Create new player
GET    /api/players/{id}         # Get specific player
PUT    /api/players/{id}         # Update player
DELETE /api/players/{id}         # Delete player
POST   /api/players/{id}/stats   # Add game statistics
```

### Analytics
```
GET    /api/analytics/performance # Performance metrics
GET    /api/analytics/leaderboard # Rankings and leaderboards  
GET    /api/analytics/trends      # Trend analysis
GET    /api/teams                 # List all teams
```

### Health
```
GET    /health                    # System health check
```

## 🚀 Deployment Options

### Local Development
```bash
python app_standalone.py
# Runs on http://localhost:8080
```

### Google Cloud Run
```bash
gcloud run deploy --source .
# Automatic cloud deployment
```

### Docker
```bash
docker build -t player-analytics .
docker run -p 8080:8080 player-analytics
```

## 🔧 Configuration

### Local Mode (.env not required)
```bash
# No configuration needed!
# Just run: python app_standalone.py
```

### Cloud Mode (.env required)
```bash
# Copy template and configure
cp .env.example .env

# Required variables:
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GOOGLE_CLOUD_PROJECT=your-project-id
```

## 📈 Use Cases

### 🎓 **Education & Learning**
- **Students**: Learn data visualization and web development
- **Educators**: Teach sports analytics and database concepts
- **Developers**: Explore Flask, SQLite, and cloud deployment

### 🏢 **Small-Scale Applications**
- **Local teams**: Track player performance and statistics
- **Youth leagues**: Manage player data and analytics
- **Personal projects**: Analyze favorite players and teams

### 🏭 **Production Deployment**
- **Professional teams**: Scale with cloud infrastructure
- **Sports organizations**: Multi-user analytics platform
- **Commercial use**: Full-featured sports analytics solution

## 🛡️ Performance & Scaling

| Feature | Local (SQLite) | Cloud (Firestore) |
|---------|----------------|-------------------|
| **Players** | < 10,000 | Unlimited |
| **Concurrent Users** | 1 | Unlimited |
| **Data Backup** | Manual file copy | Automatic |
| **Offline Access** | ✅ Full | ❌ No |
| **Setup Time** | 2 minutes | 30 minutes |
| **Cost** | Free | Pay-per-use |

## 🧪 Testing & Development

### Run Tests
```bash
# Test standalone version
python test_standalone.py

# Test all dependencies
python -c "import flask, flask_cors; print('✅ All dependencies available')"
```

### Development Commands
```bash
# Quick start with auto-reload
python app_standalone.py

# Run with different port
PORT=8081 python app_standalone.py

# Generate fresh sample data
rm local_analytics.db && python app_standalone.py
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes**: Add features or fix bugs
4. **Test locally**: `python test_standalone.py`
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**: Describe your changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Help

### Quick Help
- **Can't install dependencies?** → Try: `pip install flask flask-cors`
- **Port already in use?** → Run: `PORT=8081 python app_standalone.py`
- **Database issues?** → Delete `local_analytics.db` and restart

### Documentation
- **Local Setup**: See [QUICK_START_LOCAL.md](QUICK_START_LOCAL.md)
- **No Credentials**: See [NO_CREDENTIALS_GUIDE.md](NO_CREDENTIALS_GUIDE.md)
- **Cloud Setup**: Check Google Cloud documentation

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Share ideas and get help
- **Wiki**: Additional documentation and examples

## 🌟 Star the Project!

If you find this project helpful, please give it a star ⭐ on GitHub!

---

**🏀 Ready to analyze some basketball data? Get started in 2 minutes with the standalone version!**

```bash
git clone https://github.com/Lumina-Oz-Dev/player-analytics-dashboard.git
cd player-analytics-dashboard
python app_standalone.py
```