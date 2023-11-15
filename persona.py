'''
Persona class for chatbot
Create persona for the chatbot from template
'''
from pathlib import Path

import enum

class PersonaType(enum.Enum):
    CHATBOT = 1
    USER = 2

class Persona():
    def __init__(self, p_type: PersonaType):
        if p_type == PersonaType.CHATBOT:
            self.persona = self._define_chatbot()
        else:
            self.persona = self._define_user()

    def _define_chatbot(self):
        '''
        Generate persona for the chatbot
        '''
        pass
    
    def _define_user(self):
        '''
        Generate persona for the chatbot
        '''
        self.age = age  # Numerical
        self.gender = gender  # Categorical: Male, Female, Non-binary/Gender fluid, etc.
        self.cultural_background = cultural_background  # Categorical
        self.occupation = occupation  # Categorical
        self.education = education  # Categorical
        self.big_five_traits = big_five_traits  # Dictionary with keys: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
        self.emotional_intelligence = emotional_intelligence  # Numerical
        self.typical_mood = typical_mood  # Numerical
        self.emotional_range = emotional_range  # Numerical
        self.family_dynamics = family_dynamics  # Categorical
        self.relationship_status = relationship_status  # Categorical
        self.preferred_communication = preferred_communication  # List: Verbal, Non-verbal
        self.conflict_resolution_style = conflict_resolution_style  # List of styles
        self.stress_triggers = stress_triggers  # List of triggers
        self.coping_strategies = coping_strategies  # List of strategies
        self.significant_events = significant_events  # List of events
        self.current_circumstances = current_circumstances  # List of circumstances
        self.likes_dislikes = likes_dislikes  # List of likes/dislikes
        self.goals_aspirations = goals_aspirations  # List of goals/aspirations
        self.physical_health = physical_health  # Numerical
        self.mental_health = mental_health  # Numerical

        # Categorical elements as categories
        self.gender_categories = ['Male', 'Female', 'Non-binary/Gender fluid', 'Other']
        self.cultural_background_categories = ['North American', 'Latin American', 'European', 'African', 'Asian', 'Middle Eastern', 'Australian', 'Other']
        self.occupation_categories = ['Student', 'Healthcare', 'Technology', 'Education', 'Arts and Entertainment', 'Business', 'Manual Labor', 'Unemployed', 'Retired', 'Other']
        self.education_categories = ['No Formal Education', 'Primary School', 'Secondary School', 'Vocational Training', 'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'Doctorate', 'Other']
        self.family_dynamics_categories = ['Single Parent', 'Nuclear Family', 'Extended Family', 'Childless Couple', 'Single', 'Widowed', 'Divorced', 'Living with Friends', 'Other']
        self.relationship_status_categories = ['Single', 'In a Relationship', 'Engaged', 'Married', 'Divorced', 'Widowed', 'Separated', 'It\'s Complicated', 'Other']
        self.conflict_resolution_style_categories = ['Avoidant', 'Competitive', 'Collaborative', 'Compromising', 'Accommodating', 'Passive', 'Passive-Aggressive', 'Assertive', 'Other']
        self.stress_triggers_categories = ['Work', 'Finance', 'Family', 'Health', 'Relationships', 'Time Management', 'Personal Growth', 'Social Interactions', 'Other']
        self.coping_strategies_categories = ['Exercise', 'Meditation', 'Talking to Friends/Family', 'Hobbies', 'Professional Help', 'Substance Use', 'Avoidance', 'Problem-Solving', 'Other']
        self.significant_events_categories = ['Loss of a Loved One', 'Major Illness', 'Moving to a New Place', 'Career Change', 'Marriage', 'Divorce', 'Birth of a Child', 'Traumatic Event', 'Other']
        self.current_circumstances_categories = ['Studying', 'Working Full Time', 'Working Part Time', 'Seeking Employment', 'Raising Children', 'Retired', 'Travelling', 'Dealing with Illness', 'Other']
        self.likes_dislikes_categories = ['Sports', 'Arts', 'Technology', 'Nature', 'Reading', 'Music', 'Cooking', 'Travel', 'Other']
        self.goals_aspirations_categories = ['Career Development', 'Personal and Intellectual Growth', 'Health and Well-being', 'Relationships and Family', 'Financial Goals', 'Exploration and Adventure', 'Creative and Artistic Pursuits', 'Helping Others and Social Impact', 'Environmental Engagement', 'Personal Fulfillment', 'Other']
        pass
    
    def get_persona(self):
        '''
        Get persona for the chatbot
        '''
        pass
        return self.persona
    

        