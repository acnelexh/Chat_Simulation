'''
Persona class for chatbot
Create persona for the chatbot from template
'''
from pathlib import Path

import enum
import random

class PersonaType(enum.Enum):
    CHATBOT = 1
    USER = 2

class PersonaGenerator:
    def __init__(self):
        self.gender_categories = ['Male', 'Female', 'Non-binary/Gender fluid', 'Other']
        self.cultural_background_categories = ['North American', 'Latin American', 'European', 'African', 'Asian', 'Middle Eastern', 'Australian', 'Other']
        self.occupation_categories = ['Student', 'Healthcare', 'Technology', 'Education', 'Arts and Entertainment', 'Business', 'Manual Labor', 'Unemployed', 'Retired', 'Other']
        self.education_categories = ['No Formal Education', 'Primary School', 'Secondary School', 'Vocational Training', 'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'Doctorate', 'Other']
        self.family_dynamics_categories = ['Single Parent', 'Nuclear Family', 'Extended Family', 'Childless Couple', 'Single', 'Widowed', 'Divorced', 'Living with Friends', 'Other']
        self.relationship_status_categories = ['Single', 'In a Relationship', 'Engaged', 'Married', 'Divorced', 'Widowed', 'Separated', 'It\'s Complicated', 'Other']
        self.attachment_styles = ['Secure', 'Anxious', 'Avoidant', 'Fearful']
        self.stress_triggers_categories = ['Work', 'Finance', 'Family', 'Health', 'Relationships', 'Time Management', 'Personal Growth', 'Social Interactions', 'Other']
        self.coping_strategies_categories = ['Exercise', 'Meditation', 'Talking to Friends/Family', 'Hobbies', 'Professional Help', 'Substance Use', 'Avoidance', 'Problem-Solving', 'Other']
        self.significant_past_events_categories = ['Loss of a Loved One', 'Major Illness', 'Moving to a New Place', 'Career Change', 'Marriage', 'Divorce', 'Birth of a Child', 'Traumatic Event', 'Other']
        self.likes_dislikes_categories = ['Sports', 'Arts', 'Technology', 'Nature', 'Reading', 'Music', 'Cooking', 'Travel', 'Other']
        self.goals_passions_aspirations_categories = ['Career Development', 'Personal and Intellectual Growth', 'Health and Well-being', 'Relationships and Family', 'Financial Goals', 'Exploration and Adventure', 'Creative and Artistic Pursuits', 'Helping Others and Social Impact', 'Environmental Engagement', 'Personal Fulfillment', 'Other']
        self.mbti = ['ISTJ', 'ISFJ', 'INFJ', 'INTJ', 'ISTP', 'ISFP', 'INFP', 'INTP', 'ESTP', 'ESFP', 'ENFP', 'ENTP', 'ESTJ', 'ESFJ', 'ENFJ', 'ENTJ']

    def generate_gender(self):
        return random.choices(self.gender_categories, weights=[49.5, 49.5, 0.5, 0.5], k=1)[0]

    def generate_cultural_background(self):
        # Simplified weights based on estimated global population distribution
        weights = [15, 8, 10, 15, 30, 8, 4, 10]
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
        weights = [15, 10, 15, 10, 5, 10, 15, 5, 5, 10]  # Percentages for Student, Healthcare, Technology, Education, Arts and Entertainment, Business, Manual Labor, Unemployed, Retired, Other
        return random.choices(self.occupation_categories, weights=weights, k=1)[0]

    def generate_education(self):
        # Rough estimate of global education level distribution, 
        weights = [10, 20, 25, 5, 5, 15, 10, 5, 5]  # Percentages for No Formal Education, Primary School, Secondary School, Vocational Training, Associate Degree, Bachelor's Degree, Master's Degree, Doctorate, Other
        return random.choices(self.education_categories, weights=weights, k=1)[0]

    def generate_family_dynamics(self):
        # Rough estimate of global family dynamics
        weights = [10, 25, 20, 10, 10, 5, 10, 5, 5]  # Percentages for Single Parent, Nuclear Family, Extended Family, Childless Couple, Single, Widowed, Divorced, Living with Friends, Other
        return random.choices(self.family_dynamics_categories, weights=weights, k=1)[0]

    def generate_relationship_status(self):
        # Rough estimate of global relationship status
        weights = [25, 20, 5, 25, 5, 5, 5, 5, 5]  # Percentages for Single, In a Relationship, Engaged, Married, Divorced, Widowed, Separated, It's Complicated, Other
        return random.choices(self.relationship_status_categories, weights=weights, k=1)[0]

    def generate_persona(self):
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
            stress_triggers=random.sample(self.stress_triggers_categories, k=1),
            coping_strategies=random.sample(self.coping_strategies_categories, k=1),
            significant_events=random.sample(self.significant_past_events_categories, k=1),
            likes_dislikes=random.sample(self.likes_dislikes_categories, k=1),
            goals_aspirations=random.sample(self.goals_passions_aspirations_categories, k=1),
            physical_health=random.randint(1, 5),
            mental_health=random.randint(1, 5)
        )
        return persona

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
        generator = PersonaGenerator()
        random_persona = generator.generate_persona()
        print(random_persona)
    
    def get_persona(self):
        '''
        Get persona for the chatbot
        '''
        pass
        return self.persona
    
user_persona = Persona(PersonaType.USER)

# Step 2: Invoke the get_persona method to get the generated persona
generated_persona = user_persona.get_persona()

# Step 3: Output the generated persona
print(generated_persona)

        