from experta import *


class Saber11(Fact):
    math = Field(int, mandatory=True)
    natural = Field(int, mandatory=True)
    social = Field(int, mandatory=True)


class Category(Fact):
    math = Field(str)
    natural = Field(str)
    social = Field(str)


class Preference(Fact):
    science = Field(bool)
    engineering = Field(bool)
    health = Field(bool)
    humanities = Field(bool)


class Recommend(Fact):
    science = Field(bool)
    engineering = Field(bool)
    health = Field(bool)
    humanities = Field(bool)


class Choice(Fact):
    science = Field(bool)
    engineering = Field(bool)
    health = Field(bool)
    humanities = Field(bool)


class CareerRecommend(KnowledgeEngine):

    msg_buffer = []

    # Saber 11 categories
    math_cat = ''
    natural_cat = ''
    social_cat = ''

    # Career choice
    humanities = 0
    engineering = 0
    science = 0
    health = 0

    # Getter categories results
    def get_math_cat(self):
        return self.math_cat

    def get_natural_cat(self):
        return self.natural_cat

    def get_social_cat(self):
        return self.social_cat

    # Getter recommendations and choices
    def get_humanities_choice(self):
        return self.humanities

    def get_engineering_choice(self):
        return self.engineering

    def get_science_choice(self):
        return self.science

    def get_health_choice(self):
        return self.health

    def reset_choice(self):
        self.engineering = 0
        self.science = 0
        self.health = 0
        self.humanities = 0

    # @DefFacts()
    # def _initial_action(self):
    #  pass

    """ MATH CATEGORIES """

    """ If the student got less than 40 in math, he belongs to category 'A' in math. """
    @Rule(Saber11(math=P(lambda x: x < 40)))
    def math_cat_a(self):
        self.math_cat = 'A'
        self.msg_buffer.append("Category 'A' in math.")
        self.declare(Category(math='A'))

    """ If the student scored between 41 and 60 in math, he belongs to category 'B' in math. """
    @Rule(Saber11(math=P(lambda x: x > 40) & P(lambda x: x <= 60)))
    def math_cat_b(self):
        self.math_cat = 'B'
        self.msg_buffer.append("Category 'B' in math.")
        self.declare(Category(math='B'))

    """ If the student scored between 61 and 80 in math, he belongs to category 'C' in math. """
    @Rule(Saber11(math=P(lambda x: x > 60) & P(lambda x: x <= 80)))
    def math_cat_c(self):
        self.math_cat = 'C'
        self.msg_buffer.append("Category 'C' in math.")
        self.declare(Category(math='C'))

    """ If the student got more than 80 in math, he belongs to category 'D' in math. """
    @Rule(Saber11(math=P(lambda x: x > 80)))
    def math_cat_d(self):
        self.math_cat = 'D'
        self.msg_buffer.append("Category 'D' in math.")
        self.declare(Category(math='D'))

    """ NATURAL SCIENCES CATEGORIES """

    """ If the student got less than 40 in Natural Sciences, he belongs to category 'A' in Natural Sciences. """
    @Rule(Saber11(natural=P(lambda x: x < 40)))
    def natural_cat_a(self):
        self.natural_cat = 'A'
        self.msg_buffer.append("Category 'A' in Natural Sciences.")
        self.declare(Category(natural='A'))

    """ If the student scored between 41 and 80 in Natural Sciences, he belongs to category 'B' in Natural Sciences. """
    @Rule(Saber11(natural=P(lambda x: x > 40) & P(lambda x: x <= 80)))
    def natural_cat_b(self):
        self.natural_cat = 'B'
        self.msg_buffer.append("Category 'B' in Natural Sciences.")
        self.declare(Category(natural='B'))

    """ If the student got more than 80 in Natural Sciences, he belongs to category 'C' in Natural Sciences """
    @Rule(Saber11(natural=P(lambda x: x > 80)))
    def natural_cat_c(self):
        self.natural_cat = 'C'
        self.msg_buffer.append("Category 'C' in Natural Sciences.")
        self.declare(Category(natural='C'))

    """ SOCIAL SCIENCES CATEGORIES """

    """ If the student got less than 61 in Social Sciences, he belongs to category 'A' in Social Sciences. """
    @Rule(Saber11(social=P(lambda x: x < 61)))
    def social_cat_a(self):
        self.social_cat = 'A'
        self.msg_buffer.append("Category 'A' in Social Sciences.")
        self.declare(Category(social='A'))

    """ If the student got more than 60 in Social Sciences, he belongs to category 'B' in Social Sciences. """
    @Rule(Saber11(social=P(lambda x: x > 60)))
    def social_cat_b(self):
        self.social_cat = 'B'
        self.msg_buffer.append("Category 'B' in Social Sciences.")
        self.declare(Category(social='B'))

    """ CAREER RECOMMENDATIONS BASED ON CATEGORIES RESULTS """

    """
    Only if the student belongs to category 'D' in mathematics, he should study engineering. 
    """
    @Rule(Category(math='D'))
    def recommend_engineering(self):
        self.msg_buffer.append("The student is recommended to choose Engineering.")
        self.declare(Recommend(engineering=True))
        if self.engineering == 0:
            self.engineering = 1

    """
    Only if the student belongs to category 'B' in social sciences, he should study humanities.
    """
    @Rule(Category(social='B'))
    def recommend_humanities(self):
        self.msg_buffer.append("The student is recommended to choose Humanities.")
        self.declare(Recommend(humanities=True))
        if self.humanities == 0:
            self.humanities = 1

    """ 
    If the student is category 'C' or 'D' in mathematics and 'B' or 'C' in natural sciences, the student should
    study science.
    """
    @Rule(
        AND(
            OR(Category(math='C'), Category(math='D')),
            OR(Category(natural='B'), Category(natural='C'))
        )
    )
    def recommend_science(self):
        self.msg_buffer.append("The student is recommended to choose Science.")
        self.declare(Recommend(science=True))
        if self.science == 0:
            self.science = 1

    """ 
    If the student is category 'B' or 'C' or 'D' in mathematics and 'C' in natural sciences, the student should
    study health.
    """
    @Rule(
        AND(
            OR(Category(math='B'), Category(math='C'), Category(math='D')),
            Category(natural='C')
        )
    )
    def recommend_health(self):
        self.msg_buffer.append("The student is recommended to choose Health.")
        self.declare(Recommend(health=True))
        if self.health == 0:
            self.health = 1

    """ CHOICES BASED ON PREFERENCES AND RECOMMENDATIONS """

    """ 
    If the student is recommended to study engineering and his preference is engineering, or if he's not recommended to
    study science but it's his preference, the student could choose engineering.
    """
    @Rule(
        OR(
            AND(Recommend(engineering=True), Preference(engineering=True)),
            AND(Recommend(engineering=True), NOT(Recommend(science=True)), Preference(science=True))
        )
    )
    def choice_engineering(self):
        self.msg_buffer.append("The student should choose Engineering.")
        self.declare(Choice(engineering=True))
        self.engineering = 2

    """ 
    If the student is recommended to study science and his preference is science, or if he's not recommended to
    study health but it's his preference, the student could choose science.
    """
    @Rule(
        OR(
            AND(Recommend(science=True), Preference(science=True)),
            AND(Recommend(science=True), NOT(Recommend(health=True)), Preference(health=True))
        )
    )
    def choice_science(self):
        self.msg_buffer.append("The student should choose Science.")
        self.declare(Choice(science=True))
        self.science = 2

    """ 
    If the student is recommended to study health and his preference is health, or if he's not recommended to
    study science but it's his preference, the student could choose health.
    """
    @Rule(
        OR(
            AND(Recommend(health=True), Preference(health=True)),
            AND(Recommend(health=True), NOT(Recommend(science=True)), Preference(science=True))
        )
    )
    def choice_health(self):
        self.msg_buffer.append("The student should choose Health.")
        self.declare(Choice(health=True))
        self.health = 2

    """ 
    If the student is recommended to study health and his preference is health, or if he's not recommended to
    study science but it's his preference, the student could choose health.
    """
    @Rule(
        AND(Recommend(humanities=True), Preference(humanities=True))
    )
    def choice_humanities(self):
        self.msg_buffer.append("The student should choose Humanities.")
        self.declare(Choice(humanities=True))
        self.humanities = 2


if __name__ == '__main__':
    engine = CareerRecommend()
    engine.reset()  # Prepare the engine for the execution.
    engine.declare(Saber11(math=15, natural=90, social=90))
    engine.declare(Preference(humanities=True))
    engine.run()  # Run it!
    for msg in engine.msg_buffer:
        print(msg)
