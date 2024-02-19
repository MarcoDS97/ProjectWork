from database import execute_query


class Show:
    def __init__(self, show_id, show_title):
        self.show_id = show_id
        self.show_title = show_title

    @staticmethod
    def get_all():
        # Implementa il codice per recuperare tutti gli shows dal database
        query = "SELECT * FROM shows"
        items = execute_query(query)
        shows = [Show(item['show_id'], item['title']) for item in items]
        return shows

    def to_dict(self):
        return {
            'show_id': self.show_id,
            'show_title': self.show_title
        }
