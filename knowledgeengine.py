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
    math_cat = ''
    natural_cat = ''
    social_cat = ''

    def get_math_cat(self):
        return self.math_cat

    def get_natural_cat(self):
        return self.natural_cat

    def get_social_cat(self):
        return self.social_cat

    # @DefFacts()
    # def _initial_action(self):
    #  pass

    """ MATH CATEGORIES """

    """ If the student got less than 40 in math, he belongs to category 'A' in math. """
    @Rule(Saber11(math=P(lambda x: x < 40)))
    def math_catA(self):
        self.math_cat = 'A'
        print("Category 'A' in math.")
        self.declare(Category(math='A'))

    """ If the student scored between 41 and 60 in math, he belongs to category 'B' in math. """
    @Rule(Saber11(math=P(lambda x: x > 40) & P(lambda x: x <= 60)))
    def math_catB(self):
        self.math_cat = 'B'
        print("Category 'B' in math.")
        self.declare(Category(math='B'))

    """ If the student scored between 61 and 80 in math, he belongs to category 'C' in math. """
    @Rule(Saber11(math=P(lambda x: x > 60) & P(lambda x: x <= 80)))
    def math_catC(self):
        self.math_cat = 'C'
        print("Category 'C' in math.")
        self.declare(Category(math='C'))

    """ If the student got more than 80 in math, he belongs to category 'D' in math. """
    @Rule(Saber11(math=P(lambda x: x > 80)))
    def math_catD(self):
        self.math_cat = 'D'
        print("Category 'D' in math.")
        self.declare(Category(math='D'))

    """ NATURAL SCIENCES CATEGORIES """

    """ If the student got less than 40 in Natural Sciences, he belongs to category 'A' in Natural Sciences. """
    @Rule(Saber11(natural=P(lambda x: x < 40)))
    def natural_catA(self):
        self.natural_cat = 'A'
        print("Category 'A' in Natural Sciences.")
        self.declare(Category(natural='A'))

    """ If the student scored between 41 and 80 in Natural Sciences, he belongs to category 'B' in Natural Sciences. """
    @Rule(Saber11(natural=P(lambda x: x > 40) & P(lambda x: x <= 80)))
    def natural_catB(self):
        self.natural_cat = 'B'
        print("Category 'B' in Natural Sciences.")
        self.declare(Category(natural='B'))

    """ If the student got more than 80 in Natural Sciences, he belongs to category 'C' in Natural Sciences """
    @Rule(Saber11(natural=P(lambda x: x > 80)))
    def natural_catC(self):
        self.natural_cat = 'C'
        print("Category 'C' in Natural Sciences.")
        self.declare(Category(natural='C'))

    """ SOCIAL SCIENCES CATEGORIES """

    """ If the student got less than 61 in Social Sciences, he belongs to category 'A' in Social Sciences. """
    @Rule(Saber11(social=P(lambda x: x < 61)))
    def social_catA(self):
        self.social_cat = 'A'
        print("Category 'A' in Social Sciences.")
        self.declare(Category(social='A'))

    """ If the student got more than 60 in Social Sciences, he belongs to category 'B' in Social Sciences. """
    @Rule(Saber11(social=P(lambda x: x > 60)))
    def social_catB(self):
        self.social_cat = 'B'
        print("Category 'B' in Social Sciences.")
        self.declare(Category(social='B'))

    """ RULES TO RECOMMEND CAREER """

    """
    If the student belongs to category ‘C’ or ‘D’ in mathematics, and belongs to category C in natural sciences, he can 
    study whatever he wishes. 
    """
    @Rule(
        AND(
            OR(
                Category(math='C'),
                Category(math='D')),
            Category(natural='C')))
    def choose_whatever(self):
        print("The student can choose whatever he wishes.")
        self.declare(Recommend(science=True, engineering=True, health=True, humanities=True))

    """ If the student is category ‘A’ in mathematics, he cannot study science and engineering. """
    @Rule(Category(math='A'))
    def not_science_engineer(self):
        print("The student shouldn't study science or engineering.")
        self.declare(Recommend(science=False, engineering=False))

    """ 
    The student can only study health if he is in category ‘C’ in Natural Sciences and at least in category ‘C’ in 
    Mathematics. 
    """
    @Rule(
        NOT(AND(
            OR(
                Category(math='C'),
                Category(math='D')),
            Category(natural='C'))))
    def not_health(self):
        print("The student shouldn't choose health.")
        self.declare(Recommend(health=False))

    """
    If the student wants to study Engineering OR Science AND he is doing poorly in Mathematics, he can study Humanities 
    ***OR Health***<--(CONTRADICCIÓN) 
    """
    @Rule(
        AND(
            OR(
                Preference(engineering=True),
                Preference(science=True)
            ),
            OR(
                Category(math='A'),
                Category(math='B')
            )
        )
    )
    def choose_humanities(self):
        print("The student should choose humanities.")
        self.declare(Choice(humanities=True))

    """ If the student is doing poorly in Natural Sciences AND he wants to study Health, he can study Humanities. """

    @Rule(
        AND(
            Category(natural='A'),
            Preference(health=True)
        )
    )
    def choose_humanities(self):
        print("The student should choose humanities.")
        self.declare(Choice(humanities=True))


if __name__ == '__main__':
    engine = CareerRecommend()
    engine.reset()  # Prepare the engine for the execution.
    engine.declare(Saber11(math=15, natural=90, social=10))
    engine.declare(Preference(science=True))
    engine.run()  # Run it!
