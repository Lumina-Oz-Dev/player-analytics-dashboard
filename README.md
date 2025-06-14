# Player Analytics Dashboard

A simple but complete player analytics dashboard built with Python and Google Cloud Platform.

## Features
- Player performance metrics tracking
- Real-time data visualization
- Cloud-based data storage and processing
- REST API for data access
- Web dashboard interface

## Tech Stack
- **Backend**: Python (Flask)
- **Database**: Google Cloud Firestore
- **Analytics**: Google Cloud Functions
- **Frontend**: HTML/CSS/JavaScript with Chart.js
- **Deployment**: Google Cloud Run

## Quick Start

1. Clone the repository
```bash
git clone https://github.com/Lumina-Oz-Dev/player-analytics-dashboard.git
cd player-analytics-dashboard
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

4. Run the application
```bash
python app.py
```

## Project Structure
```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── models/               # Data models
├── services/             # Business logic
├── utils/                # Utility functions
└── cloudbuild.yaml       # Google Cloud Build configuration
```

## Environment Variables
- `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
- `FIRESTORE_COLLECTION`: Firestore collection name for player data

## License
MIT License
