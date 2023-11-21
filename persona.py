'''
Persona class for chatbot
Create persona for the chatbot from template
'''
from pathlib import Path

import enum
import random
import itertools

class PersonaType(enum.Enum):
    CHATBOT = 1
    USER = 2

class PersonaGenerator:
    def __init__(self):
        self.gender_categories = ['Male', 'Female', 'Non-binary/Gender fluid', 'Other']
        self.cultural_background_categories = ['North American', 'Latin American', 'European', 'African', 'Asian', 'Middle Eastern', 'Australian']
        self.occupation_categories = ['Student', 'Healthcare', 'Technology', 'Education', 'Arts and Entertainment', 'Business', 'Manual Labor', 'Unemployed', 'Retired']
        self.education_categories = ['No Formal Education', 'Primary School', 'Secondary School', 'Vocational Training', 'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'Doctorate']
        self.family_dynamics_categories = ['Single Parent', 'Nuclear Family', 'Extended Family', 'Childless Couple', 'Single', 'Widowed', 'Divorced', 'Living with Friends']
        self.relationship_status_categories = ['Single', 'In a Relationship', 'Engaged', 'Married', 'Divorced', 'Widowed', 'Separated', 'It\'s Complicated']
        self.attachment_styles = ['Secure', 'Anxious', 'Avoidant', 'Fearful']
        self.stress_triggers_categories = ['Work', 'Finance', 'Family', 'Health', 'Relationships', 'Time Management', 'Personal Growth', 'Social Interactions']
        self.coping_strategies_categories = ['Exercise', 'Meditation', 'Talking to Friends/Family', 'Hobbies', 'Professional Help', 'Substance Use', 'Avoidance', 'Problem-Solving']
        self.significant_past_events_categories = ['Loss of a Loved One', 'Major Illness', 'Moving to a New Place', 'Career Change', 'Marriage', 'Divorce', 'Birth of a Child', 'Traumatic Event']
        self.likes_dislikes_categories = ['Sports', 'Arts', 'Technology', 'Nature', 'Reading', 'Music', 'Cooking', 'Travel']
        self.goals_passions_aspirations_categories = ['Career Development', 'Personal and Intellectual Growth', 'Health and Well-being', 'Relationships and Family', 'Financial Goals', 'Exploration and Adventure', 'Creative and Artistic Pursuits', 'Helping Others and Social Impact', 'Environmental Engagement', 'Personal Fulfillment']
        self.mbti = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']

    def generate_gender(self):
        return random.choices(self.gender_categories, weights=[49.5, 49.5, 0.5, 0.5], k=1)[0]

    def generate_cultural_background(self):
        # Simplified weights based on estimated global population distribution
        weights = [15, 8, 10, 15, 30, 8, 4]
        return random.choices(self.cultural_background_categories, weights=weights, k=1)[0]

    def generate_mbti(self):
        # Simplified weights based on estimated global MBTI distribution
        weights = [11.6, 13.8, 1.5, 2.1, 5.4, 8.8, 4.4, 3.3, 4.3, 8.5, 8.1, 3.2, 8.7, 12.3, 2.5, 1.8]  # Percentages
        return random.choices(self.mbti, weights=weights, k=1)[0]

    def generate_attachment_style(self):
        # Estimated global distribution of attachment styles based on the book Attached by Amir Levine
        weights = [50, 20, 25, 5]  # Percentages for Secure, Anxious, Avoidant, Fearful
        return random.choices(self.attachment_styles, weights=weights, k=1)[0]

    def generate_occupation(self):
        # Rough estimate of global occupational distribution, World Employment and Social Outlook report by the International Labour Organization (ILO) 
        weights = [10, 8, 8, 8, 5, 15, 30, 10, 6]  # Percentages for Student, Healthcare, Technology, Education, Arts and Entertainment, Business and Finance, Manual Labor, Unemployed, Retired] #Based on BLS
        return random.choices(self.occupation_categories, weights=weights, k=1)[0]

    def generate_education(self):
        # Rough estimate of global education level distribution, 
        weights = [10, 20, 25, 5, 5, 20, 10, 5]  # Percentages for No Formal Education, Primary School, Secondary School, Vocational Training, Associate Degree, Bachelor's Degree, Master's Degree, Doctorate
        return random.choices(self.education_categories, weights=weights, k=1)[0]

    def generate_family_dynamics(self):
        # Rough estimate of global family dynamics
        weights = [10, 30, 20, 10, 10, 5, 10, 5]  # Percentages for Single Parent, Nuclear Family, Extended Family, Childless Couple, Single, Widowed, Divorced, Living with Friends
        return random.choices(self.family_dynamics_categories, weights=weights, k=1)[0]

    def generate_relationship_status(self):
        # Rough estimate of global relationship status
        weights = [30, 20, 5, 25, 5, 5, 5, 5]  # Percentages for Single, In a Relationship, Engaged, Married, Divorced, Widowed, Separated, It's Complicated
        return random.choices(self.relationship_status_categories, weights=weights, k=1)[0]

    def generate_persona(self):
        # Generate likes
        likes = random.sample(self.likes_dislikes_categories, k=2)
        # Filter out the likes to get remaining categories
        remaining_categories = [category for category in self.likes_dislikes_categories if category not in likes]
        # Generate dislikes from the remaining categories
        dislikes = random.sample(remaining_categories, k=2)

        persona = Persona(
            age=random.randint(2, 80), # when can babies start using computers to estimated age of not being able to use computers
            gender=self.generate_gender(), #based on global population
            cultural_background=self.generate_cultural_background(), #based on global population
            occupation=self.generate_occupation(),  # Based on rough estimate of global occupational distribution
            education=self.generate_education(),  # Based on rough estimate of global education level distribution
            family_dynamics=self.generate_family_dynamics(),  # Based on rough estimate of global family dynamics
            relationship_status=self.generate_relationship_status(),  # Based on rough estimate of global relationship status
            mbti=self.generate_mbti(), #based on global population
            attachment_style = self.generate_attachment_style(),

            emotional_intelligence=random.randint(1, 5),
            typical_mood=random.randint(1, 5),
            emotional_range=random.randint(1, 5),
            stress_triggers=random.sample(self.stress_triggers_categories, k=3),
            coping_strategies=random.sample(self.coping_strategies_categories, k=3),
            significant_events=random.sample(self.significant_past_events_categories, k=1),
            likes=likes,
            dislikes = dislikes,
            goals_aspirations=random.sample(self.goals_passions_aspirations_categories, k=3),
            physical_health=random.randint(1, 5),
            mental_health=random.randint(1, 5)
        )
        return persona

class Persona:
    def __init__(self, age, gender, cultural_background, occupation, education, family_dynamics, relationship_status, mbti, attachment_style, emotional_intelligence, typical_mood, emotional_range, stress_triggers, coping_strategies, significant_events, likes, dislikes, goals_aspirations, physical_health, mental_health):
        self.age = age
        self.gender = gender
        self.cultural_background = cultural_background
        self.occupation = occupation
        self.education = education
        self.family_dynamics = family_dynamics
        self.relationship_status = relationship_status
        self.mbti = mbti
        self.attachment_style = attachment_style
        self.emotional_intelligence = emotional_intelligence
        self.typical_mood = typical_mood
        self.emotional_range = emotional_range
        self.stress_triggers = stress_triggers
        self.coping_strategies = coping_strategies
        self.significant_events = significant_events
        self.likes = likes
        self.dislikes = dislikes
        self.goals_aspirations = goals_aspirations
        self.physical_health = physical_health
        self.mental_health = mental_health

    def __str__(self):
        # This method is for printing the persona's attributes in a readable format.
        return f"Persona(age={self.age}, gender='{self.gender}', cultural_background='{self.cultural_background}', occupation='{self.occupation}', education='{self.education}', family_dynamics='{self.family_dynamics}', relationship_status='{self.relationship_status}', mbti='{self.mbti}', attachment_style='{self.attachment_style}', emotional_intelligence={self.emotional_intelligence}, typical_mood={self.typical_mood}, emotional_range={self.emotional_range}, stress_triggers={self.stress_triggers}, coping_strategies={self.coping_strategies}, significant_events={self.significant_events}, likes={self.likes}, dislikes={self.dislikes}, goals_aspirations={self.goals_aspirations}, physical_health={self.physical_health}, mental_health={self.mental_health})"


        # if p_type == PersonaType.CHATBOT:
        #     self.persona = self._define_chatbot()
            # Store the attributes for a user persona
    def _define_chatbot(self):
        '''
        Generate persona for the chatbot
        '''

        pass
    
    def _define_user(self):
        '''
        Generate persona for the chatbot
        '''
        generator = PersonaGenerator()
        random_persona = generator.generate_persona()
        print(random_persona)
    
    def get_persona(self):
        '''
        Get persona for the chatbot
        '''
        pass
        return self.persona
    
    def generate_emotions_and_arousals():
        # Ekman's 6 emotions + neutral
        #neutral_emotions = ["Neural"]
        positive_emotions = ["Surprise", "Happy"]
        negative_emotions = ["Sad", "Fear", "Anger", "Disgust"]

        # Generate combinations: Positive to Negative
        positive_to_negative = [(pe, ne) for pe in positive_emotions for ne in negative_emotions]

        # Generate combinations: Negative to Positive
        negative_to_positive = [(ne, pe) for pe in positive_emotions for ne in negative_emotions]

        # Combine both lists
        drastic_changes = positive_to_negative + negative_to_positive

        # Assuming you have your drastic_changes list ready
        arousal_levels = ['weak', 'medium', 'strong']

        # Generate combinations of each emotion with an arousal level
        emotion_arousal_combinations = list(itertools.product(arousal_levels, repeat=2))

        # Now pair each emotion change with each arousal level combination
        all_combinations = list(itertools.product(drastic_changes, emotion_arousal_combinations))

        # for combo in all_combinations:
        #     emotion_pair, arousal_pair = combo
        #     print(f"Emotions: {emotion_pair}, Arousals: {arousal_pair}")

        return all_combinations
    

    # generator = PersonaGenerator()
    # random_persona = generator.generate_persona()
    # print(random_persona)