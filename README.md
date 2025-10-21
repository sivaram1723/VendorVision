
# Vendor Vision – Google Reviews Sentiment Dashboard

Vendor Vision is a Django-based web application that fetches Google Reviews for any place or business, performs sentiment analysis using Google Cloud NLP API, and presents the insights through interactive dashboards built with Plotly. It also uses Gemini AI to suggest actionable business improvements from negative reviews.

## 🔧 Features

- 🌍 Search for any business by name and city using Google Places API
- 📝 Fetch up to 50 live reviews for each branch/place
- 🤖 Perform sentiment analysis using Google Cloud Natural Language API
- 🌐 Translate reviews using Google Translate API if not in English
- 📊 Visualize review sentiments using interactive Plotly charts
- 🧠 Generate business improvement suggestions using Gemini AI
- 📈 Live sentiment analyzer for manual review text

## ⚙️ Tech Stack

- Backend: Django, Python 3.x
- Frontend: HTML, Django Templates, Plotly (JSON rendering)
- APIs: Google NLP, Translate, Places, Gemini (Generative AI)
- Database: SQLite (default)
- Deployment-ready with ASGI/WSGI support

## 🚀 Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/vendorvision.git
cd vendorvision
```

2. **Install Requirements**
```bash
pip install -r requirements.txt
```

3. **Set Google Credentials**
Download your Google Cloud service account key and set the environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your-key.json"
```

4. **Run Migrations**
```bash
python manage.py migrate
```

5. **Start the Server**
```bash
python manage.py runserver
```

6. **Access the App**
Open your browser and go to `http://127.0.0.1:8000/`

## 🧪 Functional Modules

| Module | Description |
|--------|-------------|
| `analyze_place_reviews` | Search a place and select a branch |
| `fetch_reviews_and_sentiment` | Fetch reviews and analyze sentiment |
| `review_dashboard` | Display analytics dashboard with plots |
| `analyze_live_review` | API endpoint for live review analysis |
| `live_analysis` | Input a review and see sentiment instantly |

## 📊 Dashboard Visuals

- **Pie Chart**: Distribution of positive, negative, neutral reviews
- **Bar Chart**: Review rating distribution
- **Scatter Plot**: Sentiment score vs rating
- **Suggestions**: Generated using Gemini API for negative feedback

## 🧠 Gemini AI Integration

Gemini model is used to analyze negative reviews and suggest 2–3 improvement actions per review.

## 📁 Project Structure (Simplified)
```
vendorvision/
├── place_reviews/
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
├── vendorvision/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
└── db.sqlite3
```




