import os
from django.shortcuts import render
from django.http import JsonResponse
from google.cloud import language_v1
from google.cloud import translate_v2 as translate
from google.api_core.exceptions import GoogleAPIError
from django.conf import settings
import requests
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
from typing import List, Dict
import plotly
import plotly.express as px
import plotly.graph_objs as go
import json
import time

# Import Gemini model
import google.generativeai as genai

# Configure Gemini API Key
GOOGLE_AI_API_KEY = 'AIzaSyDcmrEzvLDmJMC71vgOEwgEMY9NJWwovJk'
genai.configure(api_key=GOOGLE_AI_API_KEY)

# Define the API Key for Google Places API
API_KEY = 'AIzaSyDW7HdfpSgoLchJyvAddX70gdnram8qHYg'

# Language detection and translation functions
translate_client = translate.Client()

def detect_language(text):
    try:
        response = translate_client.detect_language(text)
        return response['language']
    except GoogleAPIError as e:
        print(f"Error in language detection: {e}")
        return 'en'  # Default to English if there's an error

def translate_text(text, target_language='en'):
    try:
        translation = translate_client.translate(text, target_language=target_language)
        return translation['translatedText']
    except GoogleAPIError as e:
        print(f"Error in translation: {e}")
        return text  # Return the original text if translation fails

def fetch_place_branches(place_name, city_name):
    endpoint = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={place_name}+in+{city_name}&key={API_KEY}'
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "OK":
            branches = []
            for place in data.get("results", []):
                branch_name = place.get("name")
                branch_address = place.get("formatted_address")
                place_id = place.get("place_id")
                branches.append({
                    'name': branch_name,
                    'address': branch_address,
                    'place_id': place_id
                })
            return branches
    return None

def fetch_reviews(place_id, max_reviews=100):
    reviews = []
    fields = "name,rating,reviews"
    endpoint = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}'

    while len(reviews) < max_reviews:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            result = data.get("result", {})
            reviews.extend(result.get("reviews", []))
            
            next_page_token = data.get("next_page_token")
            if next_page_token:
                time.sleep(2)
                endpoint = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={fields}&key={API_KEY}&page_token={next_page_token}'
            else:
                break
        else:
            break

    return reviews[:max_reviews]

def analyze_sentiment(review_text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=review_text, type_=language_v1.Document.Type.PLAIN_TEXT)
    try:
        sentiment_response = client.analyze_sentiment(request={'document': document})
        sentiment_score = sentiment_response.document_sentiment.score
        sentiment = "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
        return sentiment, sentiment_score
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "unknown", 0.0

def summarize_reviews(sentiment_results):
    summary = {
        "total_reviews": len(sentiment_results),
        "positive_reviews": 0,
        "negative_reviews": 0,
        "neutral_reviews": 0,
        "average_sentiment_score": 0.0,
        "common_phrases": []
    }

    sentiment_scores = []
    all_review_texts = []

    for result in sentiment_results:
        sentiment = result['sentiment']
        sentiment_score = result['sentiment_score']
        review_text = result['review']

        sentiment_scores.append(sentiment_score)
        all_review_texts.append(review_text)

        if sentiment == "positive":
            summary["positive_reviews"] += 1
        elif sentiment == "negative":
            summary["negative_reviews"] += 1
        else:
            summary["neutral_reviews"] += 1

    if sentiment_scores:
        summary["average_sentiment_score"] = round(sum(sentiment_scores) / len(sentiment_scores), 2)

    summary["common_phrases"] = extract_common_phrases(all_review_texts)

    return summary

def extract_common_phrases(review_texts):
    words = " ".join(review_texts).lower().split()
    common_words = Counter(words).most_common(5)
    return [word for word, count in common_words if len(word) > 3]

def generate_suggestions_for_improvement(negative_reviews: List[Dict[str, str]]) -> List[str]:
    model = genai.GenerativeModel('gemini-pro')
    suggestions = []

    for review in negative_reviews:
        review_text = review['review']
        prompt = f"""
        Provide 2-3 specific, actionable business improvement suggestions based on this review:

        Review: {review_text}

        Return suggestions as a plain list, without any additional text or formatting.
        """

        try:
            response = model.generate_content(prompt)
            # Clean and process suggestions
            review_suggestions = [
                suggestion.strip() 
                for suggestion in response.text.strip().split('\n') 
                if suggestion.strip() 
                and not suggestion.lower().startswith(('suggestions:', '', 'note:'))
            ]
            suggestions.extend(review_suggestions)
        except Exception as e:
            # Optionally log the error, but don't add it to suggestions
            print(f"Suggestion generation error: {str(e)}")

    return suggestions

def create_sentiment_dashboard(summary, sentiment_results):
    """
    Create interactive Plotly dashboards for sentiment analysis
    """
    # Sentiment Distribution Pie Chart
    pie_chart = px.pie(
        values=[
            summary['positive_reviews'], 
            summary['negative_reviews'], 
            summary['neutral_reviews']
        ],
        names=['Positive', 'Negative', 'Neutral'],
        title='Review Sentiment Distribution',
        hole=0.3,
        color_discrete_sequence=['green', 'red', 'gray']
    )
    pie_chart.update_traces(textposition='inside', textinfo='percent+label')

    # Sentiment Scores Scatter Plot
    scatter_data = [
        go.Scatter(
            x=[result['rating'] for result in sentiment_results],
            y=[result['sentiment_score'] for result in sentiment_results],
            mode='markers',
            text=[result['review'][:50] + '...' for result in sentiment_results],
            marker=dict(
                size=10,
                color=[result['sentiment_score'] for result in sentiment_results],
                colorscale='RdYlGn',
                showscale=True
            ),
            hoverinfo='text'
        )
    ]
    scatter_layout = go.Layout(
        title='Sentiment Scores vs Ratings',
        xaxis={'title': 'Rating'},
        yaxis={'title': 'Sentiment Score'}
    )
    scatter_chart = go.Figure(data=scatter_data, layout=scatter_layout)

    # Ratings Distribution Bar Chart
    ratings_dist = px.histogram(
        x=[result['rating'] for result in sentiment_results],
        title='Distribution of Ratings',
        labels={'x': 'Rating', 'count': 'Number of Reviews'},
        color_discrete_sequence=['blue']
    )

    # Convert plots to JSON for embedding in template
    pie_chart_json = json.dumps(pie_chart, cls=plotly.utils.PlotlyJSONEncoder)
    scatter_chart_json = json.dumps(scatter_chart, cls=plotly.utils.PlotlyJSONEncoder)
    ratings_dist_json = json.dumps(ratings_dist, cls=plotly.utils.PlotlyJSONEncoder)

    return {
        'pie_chart': pie_chart_json,
        'scatter_chart': scatter_chart_json,
        'ratings_dist': ratings_dist_json
    }

@csrf_exempt
def analyze_live_review(request):
    if request.method == 'POST':
        review_text = request.POST.get('review_text', '')
        if not review_text:
            return JsonResponse({'error': 'No review text provided'}, status=400)

        try:
            sentiment, sentiment_score = analyze_sentiment(review_text)

            response_data = {
                'sentiment': sentiment,
                'sentiment_score': round(sentiment_score, 2)
            }
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def analyze_place_reviews(request):
    """
    Main view for initiating review analysis
    Allows searching for a place and selecting a branch
    """
    if request.method == 'POST':
        place_name = request.POST.get('place_name')
        city_name = request.POST.get('city_name')

        branches = fetch_place_branches(place_name, city_name)
        if not branches:
            return JsonResponse({"error": "Unable to find any branches."}, status=404)

        return render(request, 'place_reviews/select_branch.html', {'branches': branches})
    
    return render(request, 'place_reviews/index.html')

def fetch_reviews_and_sentiment(request, place_id):
    """
    View to fetch and display reviews with sentiment analysis
    """
    reviews = fetch_reviews(place_id, max_reviews=50)
    if not reviews:
        return JsonResponse({"error": "No reviews found for this branch."}, status=404)

    # Extract review details with sentiment analysis
    sentiment_results = []
    for review in reviews:
        review_text = review.get('text', '')
        rating = review.get('rating', 0)
        author_name = review.get('author_name', 'Anonymous')
        
        # Perform sentiment analysis
        sentiment, sentiment_score = analyze_sentiment(review_text)
        
        sentiment_results.append({
            'review': review_text,
            'rating': rating,
            'author': author_name,
            'sentiment': sentiment.capitalize(),  # Capitalize for display
            'sentiment_score': round(sentiment_score, 2)
        })

    context = {
        'sentiment_results': sentiment_results,
        'place_id': place_id
    }

    return render(request, 'place_reviews/review_analysis.html', context)

def review_dashboard(request, place_id):
    """
    View to display analysis dashboard
    """
    reviews = fetch_reviews(place_id, max_reviews=50)
    if not reviews:
        return JsonResponse({"error": "No reviews found for this branch."}, status=404)

    # Extract review text from reviews and analyze sentiment
    sentiment_results = []
    negative_reviews = []

    for review in reviews:
        review_text = review.get('text', '')
        rating = review.get('rating', 0)
        author_name = review.get('author_name', 'Anonymous')
        
        sentiment, sentiment_score = analyze_sentiment(review_text)
        result = {
            'review': review_text,
            'sentiment': sentiment,
            'sentiment_score': round(sentiment_score, 2),
            'rating': rating,
            'author': author_name
        }
        sentiment_results.append(result)

        # Collect negative reviews for suggestions
        if sentiment == 'negative':
            negative_reviews.append(result)

    # Generate insights and summary
    summary = summarize_reviews(sentiment_results)

    # Generate improvement suggestions ONLY for negative reviews
    improvement_suggestions = generate_suggestions_for_improvement(negative_reviews)

    # Create Plotly dashboards
    dashboard_charts = create_sentiment_dashboard(summary, sentiment_results)

    # Prepare context for template
    context = {
        'summary': summary,
        'improvement_suggestions': improvement_suggestions,
        'place_id': place_id,
        
        # Add Plotly chart JSONs to context
        'pie_chart': dashboard_charts['pie_chart'],
        'scatter_chart': dashboard_charts['scatter_chart'],
        'ratings_dist': dashboard_charts['ratings_dist']
    }

    return render(request, 'place_reviews/review_dashboard.html', context)

def live_analysis(request):
    return render(request, 'place_reviews/live_analysis.html')