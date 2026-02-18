"""
ML-based complaint prioritization and categorization system
"""
import re
import pickle
import os
from datetime import datetime
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ComplaintPrioritizer:
    """ML-based complaint prioritization system"""
    
    # Keywords for severity detection
    CRITICAL_KEYWORDS = [
        'accident', 'danger', 'emergency', 'death', 'injury', 'severe', 
        'critical', 'urgent', 'hazard', 'collapse', 'fire', 'flood',
        'broken', 'leak', 'major', 'serious', 'risk'
    ]
    
    HIGH_KEYWORDS = [
        'bad', 'damage', 'problem', 'issue', 'concern', 'overflow',
        'blocked', 'stuck', 'not working', 'malfunction', 'crack'
    ]
    
    MEDIUM_KEYWORDS = [
        'need', 'require', 'repair', 'fix', 'improve', 'maintain',
        'check', 'clean', 'minor'
    ]
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        
    def calculate_priority_score(self, description, category, image_count=0):
        """
        Calculate priority score based on multiple factors
        Returns: priority level (Critical, High, Medium, Low) and score
        """
        score = 0
        description_lower = description.lower()
        
        # 1. Keyword-based severity (0-40 points)
        critical_count = sum(1 for keyword in self.CRITICAL_KEYWORDS if keyword in description_lower)
        high_count = sum(1 for keyword in self.HIGH_KEYWORDS if keyword in description_lower)
        medium_count = sum(1 for keyword in self.MEDIUM_KEYWORDS if keyword in description_lower)
        
        if critical_count > 0:
            score += 40
        elif high_count > 0:
            score += 30
        elif medium_count > 0:
            score += 20
        else:
            score += 10
        
        # 2. Category-based priority (0-25 points)
        critical_categories = ['Road Damage', 'Water Supply', 'Sewage', 'Building Safety']
        high_categories = ['Streetlight', 'Waste Management', 'Public Transport']
        
        if category in critical_categories:
            score += 25
        elif category in high_categories:
            score += 15
        else:
            score += 5
        
        # 3. Description length and detail (0-15 points)
        word_count = len(description.split())
        if word_count > 50:
            score += 15
        elif word_count > 20:
            score += 10
        else:
            score += 5
        
        # 4. Image evidence (0-10 points)
        if image_count > 0:
            score += 10
        
        # 5. Urgency indicators (0-10 points)
        urgency_words = ['urgent', 'asap', 'immediately', 'emergency', 'critical']
        if any(word in description_lower for word in urgency_words):
            score += 10
        
        # Determine priority level based on score (0-100)
        if score >= 70:
            priority = 'Critical'
        elif score >= 50:
            priority = 'High'
        elif score >= 30:
            priority = 'Medium'
        else:
            priority = 'Low'
        
        return priority, score
    
    def categorize_complaint(self, description):
        """
        Auto-categorize complaint based on description
        """
        description_lower = description.lower()
        
        category_keywords = {
            'Road Damage': ['road', 'pothole', 'street', 'pavement', 'crack', 'asphalt', 'highway', 'path'],
            'Waste Management': ['garbage', 'trash', 'waste', 'dustbin', 'dump', 'litter', 'refuse', 'sanitation'],
            'Streetlight': ['light', 'lamp', 'street light', 'lighting', 'bulb', 'pole', 'dark'],
            'Water Supply': ['water', 'tap', 'supply', 'pipeline', 'connection', 'shortage', 'no water'],
            'Sewage': ['sewage', 'drain', 'sewer', 'overflow', 'manhole', 'drainage', 'clog', 'block'],
            'Parks & Gardens': ['park', 'garden', 'tree', 'grass', 'playground', 'bench', 'green'],
            'Public Transport': ['bus', 'transport', 'public transport', 'stop', 'shelter'],
            'Building Safety': ['building', 'structure', 'wall', 'collapse', 'unsafe', 'construction'],
            'Noise Pollution': ['noise', 'loud', 'sound', 'pollution', 'disturbance']
        }
        
        # Count keyword matches for each category
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in description_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score, or 'Other'
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return 'Other'
    
    def find_similar_complaints(self, new_description, existing_complaints, threshold=0.6):
        """
        Find similar/duplicate complaints using TF-IDF and cosine similarity
        Returns list of similar complaint IDs
        """
        if not existing_complaints:
            return []
        
        try:
            # Prepare corpus
            descriptions = [c.get('description', '') for c in existing_complaints]
            descriptions.append(new_description)
            
            # Calculate TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform(descriptions)
            
            # Calculate similarity between new complaint and existing ones
            new_vector = tfidf_matrix[-1]
            existing_vectors = tfidf_matrix[:-1]
            
            similarities = cosine_similarity(new_vector, existing_vectors)[0]
            
            # Find similar complaints above threshold
            similar_indices = np.where(similarities >= threshold)[0]
            similar_complaints = [
                {
                    'id': existing_complaints[i].get('id'),
                    'description': existing_complaints[i].get('description'),
                    'similarity': float(similarities[i])
                }
                for i in similar_indices
            ]
            
            return sorted(similar_complaints, key=lambda x: x['similarity'], reverse=True)
        
        except Exception as e:
            print(f"Error finding similar complaints: {e}")
            return []
    
    def calculate_frequency_boost(self, category, location, existing_complaints):
        """
        Calculate priority boost based on complaint frequency in area/category
        """
        if not existing_complaints:
            return 0
        
        # Count complaints in same category
        category_count = sum(1 for c in existing_complaints if c.get('category') == category)
        
        # Count complaints in nearby area (simplified - within 0.01 lat/lng)
        try:
            lat, lng = location.get('latitude', 0), location.get('longitude', 0)
            nearby_count = sum(
                1 for c in existing_complaints 
                if abs(c.get('location', {}).get('latitude', 0) - lat) < 0.01
                and abs(c.get('location', {}).get('longitude', 0) - lng) < 0.01
            )
        except:
            nearby_count = 0
        
        # Calculate boost (max 15 points)
        boost = min(15, (category_count * 2) + (nearby_count * 3))
        return boost


class DuplicateDetector:
    """Detect duplicate or similar complaints"""
    
    def __init__(self, similarity_threshold=0.7):
        self.threshold = similarity_threshold
        self.prioritizer = ComplaintPrioritizer()
    
    def check_duplicate(self, new_complaint, existing_complaints):
        """
        Check if new complaint is duplicate of existing ones
        Returns: (is_duplicate, similar_complaints_list)
        """
        similar = self.prioritizer.find_similar_complaints(
            new_complaint.get('description', ''),
            existing_complaints,
            self.threshold
        )
        
        is_duplicate = len(similar) > 0 and similar[0]['similarity'] > 0.85
        
        return is_duplicate, similar
