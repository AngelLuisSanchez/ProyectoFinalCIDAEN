class WordCloud():
    def __init__(self, text, weight, color):
        self.text = text
        self.weight = weight
        self.color = color

    def serialize(self):
        return {
            'text': self.text,
            'weight': self.weight,
            'color': self.color
        }
