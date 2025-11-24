from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class VaderSentimentEngine:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def score(self, text: str):
        """
        Map VADER compound score (-1..1) to:
        - label: POSITIVE / NEUTRAL / NEGATIVE
        - score: 1..5
        """
        if not text:
            return "NEUTRAL", 3.0

        res = self.analyzer.polarity_scores(text)
        compound = res["compound"]  # -1 to 1

        # map compound to 1..5
        # e.g. -1 -> 1, 0 -> 3, 1 -> 5
        mapped = 3 + 2 * compound
        mapped = max(1, min(5, mapped))

        if mapped >= 4:
            label = "POSITIVE"
        elif mapped <= 2:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        return label, float(mapped)
