"""
Graph builder for creating semantic relationships between diary entries
Extracts entities, concepts, and creates relationships
"""

import re
from typing import List, Dict, Set
from collections import Counter


class GraphBuilder:
    """Build semantic graph from diary entries"""
    
    def __init__(self):
        # Common stop words to filter out
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
            'his', 'her', 'its', 'our', 'their', 'me', 'him', 'us', 'them'
        }
    
    def extract_entities(self, text: str) -> List[str]:
        """
        Extract important entities and concepts from text
        Returns list of key phrases/entities
        """
        if not text:
            return []
        
        # Convert to lowercase for processing
        text_lower = text.lower()
        
        # Extract potential entities:
        # 1. Capitalized words/phrases (likely proper nouns or important terms)
        capitalized = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # 2. Important keywords (nouns, adjectives, verbs - excluding stop words)
        words = re.findall(r'\b[a-z]{3,}\b', text_lower)
        keywords = [w for w in words if w not in self.stop_words and len(w) >= 4]
        
        # 3. Extract noun phrases (simple pattern matching)
        noun_phrases = self._extract_noun_phrases(text)
        
        # Combine and deduplicate
        entities = set()
        entities.update(capitalized)
        entities.update(keywords[:10])  # Top keywords
        entities.update(noun_phrases)
        
        # Filter and clean
        cleaned = []
        for entity in entities:
            entity = entity.strip()
            if len(entity) >= 3 and entity not in self.stop_words:
                cleaned.append(entity)
        
        return cleaned[:15]  # Limit to top 15 entities
    
    def _extract_noun_phrases(self, text: str) -> List[str]:
        """Extract simple noun phrases from text"""
        phrases = []
        
        # Pattern: adjective + noun
        pattern1 = r'\b(?:good|great|happy|sad|important|new|old|big|small|long|short|nice|bad|interesting|boring|fun|hard|easy|difficult|simple|complex|beautiful|ugly)\s+[a-z]+\b'
        phrases.extend(re.findall(pattern1, text.lower()))
        
        # Pattern: noun + noun (compound nouns)
        pattern2 = r'\b[a-z]+\s+(?:day|time|work|life|home|school|college|university|project|meeting|friend|family|person|place|thing|idea|thought|feeling|experience|moment|memory)\b'
        phrases.extend(re.findall(pattern2, text.lower()))
        
        return list(set(phrases))
    
    def extract_topics(self, text: str) -> List[str]:
        """Extract topic categories from text"""
        topics = []
        text_lower = text.lower()
        
        # Topic keywords mapping
        topic_keywords = {
            'work': ['work', 'job', 'office', 'project', 'meeting', 'colleague', 'boss', 'task', 'deadline', 'career'],
            'study': ['study', 'learn', 'class', 'exam', 'homework', 'course', 'university', 'college', 'school', 'lesson'],
            'family': ['family', 'parent', 'mom', 'dad', 'sister', 'brother', 'relative', 'cousin', 'grandparent'],
            'friends': ['friend', 'buddy', 'pal', 'hangout', 'together', 'social'],
            'health': ['health', 'exercise', 'gym', 'workout', 'diet', 'doctor', 'hospital', 'medicine', 'sick', 'ill'],
            'travel': ['travel', 'trip', 'vacation', 'journey', 'flight', 'hotel', 'visit', 'explore', 'adventure'],
            'hobby': ['hobby', 'interest', 'passion', 'sport', 'game', 'music', 'art', 'reading', 'writing', 'drawing'],
            'food': ['food', 'eat', 'restaurant', 'cook', 'meal', 'dish', 'recipe', 'breakfast', 'lunch', 'dinner'],
            'emotion': ['happy', 'sad', 'excited', 'worried', 'stressed', 'relaxed', 'angry', 'calm', 'anxious', 'joyful']
        }
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def extract_relationships(self, text: str) -> List[Dict]:
        """Extract relationship patterns from text"""
        relationships = []
        text_lower = text.lower()
        
        # Patterns: "with [person]", "at [place]", "about [topic]"
        with_pattern = r'\bwith\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
        at_pattern = r'\bat\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b'
        about_pattern = r'\babout\s+([a-z]+(?:\s+[a-z]+)?)\b'
        
        for match in re.finditer(with_pattern, text):
            relationships.append({'type': 'WITH_PERSON', 'target': match.group(1)})
        
        for match in re.finditer(at_pattern, text):
            relationships.append({'type': 'AT_PLACE', 'target': match.group(1)})
        
        for match in re.finditer(about_pattern, text_lower):
            relationships.append({'type': 'ABOUT', 'target': match.group(1)})
        
        return relationships
    
    def extract_key_concepts(self, text: str, limit: int = 10) -> List[str]:
        """Extract key concepts from text using frequency and importance"""
        if not text:
            return []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Extract important words from each sentence
        all_concepts = []
        for sentence in sentences:
            # Extract meaningful words (3+ characters, not stop words)
            words = re.findall(r'\b[a-z]{3,}\b', sentence.lower())
            concepts = [w for w in words if w not in self.stop_words]
            all_concepts.extend(concepts)
        
        # Count frequency
        concept_counts = Counter(all_concepts)
        
        # Return most common
        return [concept for concept, count in concept_counts.most_common(limit)]


