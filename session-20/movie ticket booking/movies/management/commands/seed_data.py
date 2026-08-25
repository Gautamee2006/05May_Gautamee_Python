from django.core.management.base import BaseCommand
from movies.models import Movie, Show
import datetime
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds initial movies and shows for testing.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding movies and show data...")

        movies_data = [
            {
                "title": "Avengers: Endgame",
                "description": "After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions.",
                "genre": "Action",
                "language": "English",
                "duration": 181,
                "release_date": datetime.date(2019, 4, 26),
                "poster": "https://images.unsplash.com/photo-1568832359672-e36cf5d74f54?w=600&auto=format&fit=crop&q=80",
                "rating": 4.8
            },
            {
                "title": "The Dark Knight",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "genre": "Action",
                "language": "English",
                "duration": 152,
                "release_date": datetime.date(2008, 7, 18),
                "poster": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80",
                "rating": 4.9
            },
            {
                "title": "Inception",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "genre": "Sci-Fi",
                "language": "English",
                "duration": 148,
                "release_date": datetime.date(2010, 7, 16),
                "poster": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
                "rating": 4.7
            },
            {
                "title": "KGF Chapter 2",
                "description": "In the blood-soaked Kolar Gold Fields, Rocky's name strikes fear into his foes. While his allies look up to him, the government sees him as a threat to law and order.",
                "genre": "Action",
                "language": "Hindi",
                "duration": 168,
                "release_date": datetime.date(2022, 4, 14),
                "poster": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=600&auto=format&fit=crop&q=80",
                "rating": 4.5
            },
            {
                "title": "Interstellar",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "genre": "Sci-Fi",
                "language": "English",
                "duration": 169,
                "release_date": datetime.date(2014, 11, 7),
                "poster": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&auto=format&fit=crop&q=80",
                "rating": 4.6
            }
        ]

        created_count = 0
        today = timezone.now().date()

        for m_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=m_data['title'],
                defaults=m_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created movie: {movie.title}")

            # Create sample shows for today and tomorrow
            times = [
                (datetime.time(10, 30), "Audi 1", 200.00),
                (datetime.time(14, 15), "Audi 2", 250.00),
                (datetime.time(18, 0), "IMAX Screen", 350.00),
                (datetime.time(21, 30), "Audi 1", 280.00),
            ]

            for days_offset in range(3):
                show_date = today + datetime.timedelta(days=days_offset)
                for t, screen, price in times:
                    Show.objects.get_or_create(
                        movie=movie,
                        date=show_date,
                        time=t,
                        screen_name=screen,
                        defaults={"ticket_price": price}
                    )

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded database with movies and shows!"))
