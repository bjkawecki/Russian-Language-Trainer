class UserMessageTopicsMixin:
    def get_topics(self):
        return {
            1: "Ich möchte einen Fehler melden.",
            2: "Ich möchte einen Verbesserungsvorschlag machen.",
            3: "Etwas anderes.",
        }
