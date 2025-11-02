"""
Graph processor for extracting entities, concepts, and creating semantic relationships
"""

import re
from typing import List, Dict, Set
from collections import Counter


class GraphProcessor:
    """Processes text to extract entities, concepts, and keywords for graph structure"""
    
    # Common stop words to filter out
    STOP_WORDS = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
        'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
        'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
        'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
        'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
        'should', 'now', 'today', 'tomorrow', 'yesterday'
    }
    
    # Emotional/conceptual keywords
    EMOTION_KEYWORDS = {
        'happy', 'sad', 'excited', 'nervous', 'anxious', 'calm', 'stressed', 'relaxed',
        'angry', 'frustrated', 'joyful', 'peaceful', 'worried', 'confident', 'proud',
        'grateful', 'disappointed', 'surprised', 'afraid', 'hopeful', 'lonely', 'loved'
    }
    
    ACTIVITY_KEYWORDS = {
        'work', 'study', 'learn', 'read', 'write', 'exercise', 'run', 'walk', 'travel',
        'meet', 'talk', 'visit', 'cook', 'eat', 'sleep', 'rest', 'play', 'game',
        'movie', 'music', 'dance', 'sing', 'paint', 'draw', 'create', 'build', 'fix'
    }
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract important keywords from text
        """
        if not text:
            return []
        
        # Convert to lowercase and split
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        # Filter out stop words and short words
        keywords = [
            word for word in words 
            if len(word) > 2 
            and word not in self.STOP_WORDS
            and word.isalpha()
        ]
        
        # Count frequency
        word_freq = Counter(keywords)
        
        # Get most common keywords
        top_keywords = [word for word, count in word_freq.most_common(max_keywords)]
        
        return top_keywords
    
    def extract_concepts(self, text: str) -> List[str]:
        """
        Extract semantic concepts from text
        Combines keywords with emotional and activity concepts
        """
        if not text:
            return []
        
        text_lower = text.lower()
        concepts = set()
        
        # Extract regular keywords
        keywords = self.extract_keywords(text, max_keywords=15)
        concepts.update(keywords)
        
        # Extract emotions mentioned
        for emotion in self.EMOTION_KEYWORDS:
            if emotion in text_lower:
                concepts.add(emotion)
        
        # Extract activities mentioned
        for activity in self.ACTIVITY_KEYWORDS:
            if activity in text_lower:
                concepts.add(activity)
        
        # Extract quoted phrases (important concepts)
        quoted = re.findall(r'"([^"]+)"', text)
        for phrase in quoted:
            # Extract keywords from quoted phrases
            phrase_keywords = self.extract_keywords(phrase, max_keywords=5)
            concepts.update(phrase_keywords)
        
        # Extract capitalized words (likely names or important concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        concepts.update([word.lower() for word in capitalized if len(word) > 3])
        
        return list(concepts)[:20]  # Limit to top 20 concepts
    
    def extract_entities(self, text: str) -> List[str]:
        """
        Extract named entities (simple version - can be enhanced with NER)
        """
        entities = []
        text_lower = text.lower()
        
        # Extract person names (heuristic: capitalized words)
        names = re.findall(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text)
        entities.extend([name.lower() for name in names])
        
        # Extract common entity patterns
        # Locations (words after "in", "at", "from", "to")
        locations = re.findall(r'\b(in|at|from|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', text)
        entities.extend([loc[1].lower() for loc in locations])
        
        return list(set(entities))  # Remove duplicates
    
    def extract_relationships(self, text: str) -> List[Dict[str, str]]:
        """
        Extract semantic relationships from text
        Returns list of relationship tuples: (subject, relation, object)
        """
        relationships = []
        
        # Pattern: "I [verb] [object]" or "[subject] [verb] [object]"
        # Simple extraction for now - can be enhanced with dependency parsing
        
        # Action patterns
        action_patterns = [
            r'i\s+(went|visited|met|saw|talked|worked|studied|learned|did|created|built)\s+(?:to|with|at|in)?\s*([a-z\s]+)',
            r'i\s+(am|was|feel|felt)\s+(happy|sad|excited|tired|grateful|worried|proud|anxious|calm)',
            r'we\s+(went|visited|met|saw|talked|worked|studied|did|created)\s+(?:to|with|at)?\s*([a-z\s]+)',
        ]
        
        text_lower = text.lower()
        for pattern in action_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                if len(match.groups()) >= 2:
                    verb = match.group(1)
                    obj = match.group(2).strip()[:30]  # Limit length
                    if obj and len(obj) > 2:
                        relationships.append({
                            'subject': 'entry',
                            'relation': verb,
                            'object': obj
                        })
        
        return relationships
    
    def process_entry(self, text: str) -> Dict:
        """
        Process an entry and extract all graph components
        Returns a dictionary with keywords, concepts, entities, and relationships
        """
        if not text:
            return {
                'keywords': [],
                'concepts': [],
                'entities': [],
                'relationships': []
            }
        
        return {
            'keywords': self.extract_keywords(text),
            'concepts': self.extract_concepts(text),
            'entities': self.extract_entities(text),
            'relationships': self.extract_relationships(text)
        }
