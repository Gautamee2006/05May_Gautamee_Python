from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from role_app.models import Product, Movie, Review, Playlist, Order


class Command(BaseCommand):
    help = 'Setup default groups and permissions for role_app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Setting up Django Groups and Permissions...'))

        # Get Content Types
        product_ct = ContentType.objects.get_for_model(Product)
        movie_ct = ContentType.objects.get_for_model(Movie)
        review_ct = ContentType.objects.get_for_model(Review)
        playlist_ct = ContentType.objects.get_for_model(Playlist)
        order_ct = ContentType.objects.get_for_model(Order)

        # Role to Permissions mapping
        role_permissions = {
            'Seller': [
                Permission.objects.get(codename='add_product', content_type=product_ct),
                Permission.objects.get(codename='change_product', content_type=product_ct),
                Permission.objects.get(codename='view_product', content_type=product_ct),
                Permission.objects.get(codename='view_order', content_type=order_ct),
            ],
            'Buyer': [
                Permission.objects.get(codename='view_product', content_type=product_ct),
                Permission.objects.get(codename='add_order', content_type=order_ct),
                Permission.objects.get(codename='view_order', content_type=order_ct),
            ],
            'MovieCritic': [
                Permission.objects.get(codename='view_movie', content_type=movie_ct),
                Permission.objects.get(codename='add_review', content_type=review_ct),
                Permission.objects.get(codename='change_review', content_type=review_ct),
                Permission.objects.get(codename='view_review', content_type=review_ct),
            ],
            'MovieFan': [
                Permission.objects.get(codename='view_movie', content_type=movie_ct),
                Permission.objects.get(codename='view_review', content_type=review_ct),
            ],
            'Admin': [
                Permission.objects.get(codename='add_playlist', content_type=playlist_ct),
                Permission.objects.get(codename='change_playlist', content_type=playlist_ct),
                Permission.objects.get(codename='view_playlist', content_type=playlist_ct),
                Permission.objects.get(codename='delete_playlist', content_type=playlist_ct),
            ]
        }

        for role_name, perms in role_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)
            group.permissions.set(perms)
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'Group "{role_name}" {status} with {len(perms)} permissions.'))

        self.stdout.write(self.style.SUCCESS('Successfully configured all groups and permissions!'))
