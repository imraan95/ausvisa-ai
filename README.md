# AusVisa.ai

An AI-powered Australian visa assessment platform that provides instant success probability scores, timelines, and cost estimates.

## Features

- AI-powered visa assessment
- Real-time success probability calculation
- Timeline and cost estimates
- Alternative visa recommendations
- Mobile-responsive design

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Flask (Python)
- ML: scikit-learn, pandas
- Deployment: Render.com

## Local Development

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Deployment

The application is configured for deployment on Render.com:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Python Version: 3.9

## Data Updates

The visa success prediction model is trained on data from `data/visa_profiles.csv`. To update the model with new data:

1. Add new entries to the CSV file
2. Restart the application to retrain the model

## License

MIT License
