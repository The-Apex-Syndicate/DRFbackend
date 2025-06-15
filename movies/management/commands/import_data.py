import pandas as pd
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre, ProductionCompany, ProductionCountry, SpokenLanguage, Actor, MovieActorMap
from django.db import transaction

def dump_movie_data():
    try:
        genres_df = pd.read_csv('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/genres.csv') 
        production_companies_df = pd.read_csv('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/production_companies.csv') 
        production_countries_df = pd.read_csv('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/production_countries.csv') 
        spoken_languages_df = pd.read_csv('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/spoken_languages.csv') 
        movies_df = pd.read_csv('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/movies_metadata.csv') 

        genre_mapping = {}  
        production_companies_mapping = {}
        production_countries_mapping = {}
        spoken_languages_mapping = {}
        movies_df = movies_df
        genres_df = genres_df
        production_companies_df = production_companies_df
        production_countries_df = production_countries_df
        spoken_languages_df = spoken_languages_df
        for _, row in genres_df.iterrows():
            with transaction.atomic():
                genre, created = Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name']}
                )
                genre_mapping[row['id']] = genre
                if created:
                    print(f"Created genre: {genre.name}")
        
        for _, row in production_companies_df.iterrows():
            with transaction.atomic():
                production_company, created = ProductionCompany.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name']}
                )
                production_companies_mapping[row['id']] = production_company
                if created:
                    print(f"Created production_company: {production_company.name}")

        for _, row in production_countries_df.iterrows():
            with transaction.atomic():
                production_country, created = ProductionCountry.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name']}
                )
                production_countries_mapping[row['id']] = production_country
                if created:
                    print(f"Created production_country: {production_country.name}")

        for _, row in spoken_languages_df.iterrows():
            with transaction.atomic():
                spoken_language, created = SpokenLanguage.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name']}
                )
                spoken_languages_mapping[row['id']] = spoken_language
                if created:
                    print(f"Created spoken_language: {spoken_language.name}")

        print("\nCreating movies ")
        
        for _, row in movies_df.iterrows():
            with transaction.atomic():
                try:
                    fields = {
                        'id': int(row['id']),
                        'adult': row['adult'],
                        'original_language': row['original_language'] if row['original_language']!='' else '',
                        'original_title': row['original_title'] if row['original_title']!='' else '',
                        'overview': row['overview'] if row['overview']!='' else '',
                        'popularity': row['popularity'],
                        'poster_path': row['poster_path'] if row['poster_path']!='' else '',
                        'revenue': row['revenue'],
                        'runtime': row['runtime'],
                        'status': row['status']  if row['status']!='' else '',
                        'tagline': row['tagline'] if row['tagline']!='' else '',
                        'title': row['title'] if row['title']!='' else '',
                        'video': row['video'],
                        'vote_average': row['vote_average'],
                        'vote_count': row['vote_count'],
                        'rating': row['rating'],
                    }
                    release_date = row['release_date']
                    if isinstance(release_date, str) and release_date.strip():
                        fields['release_date'] = release_date 

                    movie = Movie.objects.create(**fields)
                        
                except Exception as e:
                    # print("error here")
                    print(f"Error here processing movie {row['title']}: {str(e)}")
                try:
                    if isinstance(row['genres'], str):
                        genre_ids = row['genres'].split(',')

                    if isinstance(row['production_companies'], str):
                        production_company_ids =  row['production_companies'].split(',')

                    if isinstance(row['production_countries'], str):
                        production_country_ids = row['production_countries'].split(',')

                    if isinstance(row['spoken_languages'], str):
                        spoken_language_ids = row['spoken_languages'].split(',')

                    if genre_ids:
                        for genre_id in genre_ids:
                            if int(genre_id) in genre_mapping:
                                movie.genres.add(genre_mapping[int(genre_id)])

                    if production_company_ids:
                        for production_company_id in production_company_ids:
                            if int(production_company_id) in production_companies_mapping:
                                movie.production_companies.add(production_companies_mapping[int(production_company_id)])

                    if production_country_ids:
                        for production_country_id in production_country_ids:
                            if production_country_id in production_countries_mapping:
                                movie.production_countries.add(production_countries_mapping[production_country_id])

                    if spoken_language_ids:
                        for spoken_language_id in spoken_language_ids:
                            if spoken_language_id in spoken_languages_mapping:
                                movie.spoken_languages.add(spoken_languages_mapping[spoken_language_id])

                except Exception as e:
                    print(f"Error processing movie {row['title']}: {str(e)}")

            print(f"Created movie: {movie.title}")

                

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def dump_cast_data():
    try:
        movie_cast_df = pd.read_csv('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/movie_cast_map.csv') 
        actors_df = pd.read_csv('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/actors.csv') 

        actors_mapping = {}  
        movie_cast_df = movie_cast_df
        actors_df = actors_df
        for _, row in actors_df.iterrows():
            with transaction.atomic():
                actors, created = Actor.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name'], 
                              'gender': row['gender']
                              }
                )
                actors_mapping[row['id']] = actors
                if created:
                    print(f"Created actors: {actors.name}")

        for _, row in movie_cast_df.iterrows():
            with transaction.atomic():
                try:
                    actor_instance = None
                    movie_instance = None
                    try:
                        actor_instance = Actor.objects.get(id = row['actor_id'])
                    except Actor.DoesNotExist:
                        print("actor doesn't exists")
                    try:
                        movie_instance = Movie.objects.get(id=row['movie_id'])
                    except Movie.DoesNotExist:
                        print("movie doesn't exists")

                    if movie_instance and actor_instance:
                        movie_cast, created = MovieActorMap.objects.get_or_create(
                            actor = actor_instance,
                            movie = movie_instance,
                            defaults={
                                    'character_name': row['character_name'] if row['character_name']!='' else '',
                                    'profile_path' : row['profile_path'] if row['profile_path']!='' else ''
                                    }
                        )
                        if created:
                            print(f"Created MovieActorMap: {movie_cast.id}")
                except Exception as e:
                    print(f"Error processing movieActorMap : {str(e)}")


    except Exception as e:
        print(f"An error occurred: {str(e)}")


def update_video_url():
    df = pd.read_json('/Users/sathish/Desktop/MyCodes/Hackathon/DataProcessing/processed/trailer.json')
    df.dropna()
    for _, row in df.iterrows():
            with transaction.atomic():
                try: 
                    if isinstance(eval(row['movie_id']), int):
                        movie_instance = None
                        try:
                            movie_instance = Movie.objects.get(id=row['movie_id'])
                        except Movie.DoesNotExist:
                            print("movie doesn't exists")
                        if movie_instance:
                            movie_instance.video_url = row.get('trailer_url', '')
                            movie_instance.save()
                            print(f"Updated Movie: {movie_instance.title} {movie_instance.id}")   
                except:
                    print(row['movie_id'])     
class Command(BaseCommand):
    help = 'Import movies and genres from CSV files'

    def handle(self, *args, **kwargs):
        # dump_movie_data()
        # dump_cast_data()
        update_video_url()
