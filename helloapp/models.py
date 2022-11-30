
# Create your models here.
class GuessedNumber:
    guessed_number = int
    comparison = str

    def __str__(self):
        return str(self.guessed_number) + ' is' + self.comparison + ' than the secret number'
