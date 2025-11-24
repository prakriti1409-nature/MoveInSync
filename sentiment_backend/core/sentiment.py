class SentimentEngine:
    def __init__(self, keyword_dict=None):
        # Very simple dictionary; you can extend easily
        self.keyword_dict = keyword_dict or {
            "good": 1,
            "great": 2,
            "excellent": 2,
            "polite": 1,
            "on time": 1,
            "late": -1,
            "rude": -2,
            "bad": -1,
            "unsafe": -2,
            "reckless": -2,
            "slow": -1,
        }

    def score(self, text: str):
        """
        Returns (label, score_1_to_5)
        """
        if not text:
            return "NEUTRAL", 3.0

        text_lower = text.lower()
        raw_score = 0

        for word, val in self.keyword_dict.items():
            if word in text_lower:
                raw_score += val

        # Base 3 (neutral), adjust by raw_score
        mapped_score = 3 + raw_score

        # Clamp to [1, 5]
        mapped_score = max(1, min(5, mapped_score))

        if mapped_score >= 4:
            label = "POSITIVE"
        elif mapped_score <= 2:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"

        return label, float(mapped_score)
