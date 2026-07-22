import datetime
import uuid


def get_test_data(count=50):
    return [
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genres': ['Action', 'Sci-Fi'],
            'title': 'The StarStar',
            'description': 'New World',
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [{'id': str(uuid.uuid4()), 'name': 'Stan'}],
            'actors': [
                {'id': str(uuid.uuid4()), 'name': 'Ann'},
                {'id': str(uuid.uuid4()), 'name': 'Bob'},
            ],
            'writers': [
                {'id': str(uuid.uuid4()), 'name': 'Ben'},
                {'id': str(uuid.uuid4()), 'name': 'Howard'},
            ],
        }
        for _ in range(count)
    ]


def get_test_data_film():
    return [
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genres': ['Action', 'Sci-Fi'],
            'title': '',
            'description': 'New World',
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [{'id': str(uuid.uuid4()), 'name': 'Stan'}],
            'actors': [
                {'id': str(uuid.uuid4()), 'name': 'Ann'},
                {'id': str(uuid.uuid4()), 'name': 'Bob'},
            ],
            'writers': [
                {'id': str(uuid.uuid4()), 'name': 'Ben'},
                {'id': str(uuid.uuid4()), 'name': 'Howard'},
            ],
        },
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 8.5,
            'genres': ['Action', 'Sci-Fi'],
            'title': 'My5669',
            'description': 'New World',
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [{'id': str(uuid.uuid4()), 'name': 'Stan'}],
            'actors': [
                {'id': str(uuid.uuid4()), 'name': 'Ann'},
                {'id': str(uuid.uuid4()), 'name': 'Bob'},
            ],
            'writers': [
                {'id': str(uuid.uuid4()), 'name': 'Ben'},
                {'id': str(uuid.uuid4()), 'name': 'Howard'},
            ],
        },
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': -1,
            'genres': ['Drama', 'Sci-Fi'],
            'title': 'My uncle',
            'description': 'New World',
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [{'id': str(uuid.uuid4()), 'name': 'Stan'}],
            'actors': [
                {'id': str(uuid.uuid4()), 'name': 'Ann'},
                {'id': str(uuid.uuid4()), 'name': 'Bob'},
            ],
            'writers': [
                {'id': str(uuid.uuid4()), 'name': 'Ben'},
                {'id': str(uuid.uuid4()), 'name': 'Howard'},
            ],
        },
        {
            'id': str(uuid.uuid4()),
            'imdb_rating': 10,
            'genres': ['Drama', 'Sci-Fi'],
            'title': 'Summer',
            'description': 'New World',
            'actors_names': ['Ann', 'Bob'],
            'writers_names': ['Ben', 'Howard'],
            'directors': [{'id': str(uuid.uuid4()), 'name': 'Stan'}],
            'actors': [
                {'id': str(uuid.uuid4()), 'name': 'Ann'},
                {'id': str(uuid.uuid4()), 'name': 'Bob'},
            ],
            'writers': [
                {'id': str(uuid.uuid4()), 'name': 'Ben'},
                {'id': str(uuid.uuid4()), 'name': 'Howard'},
            ],
        },
    ]
