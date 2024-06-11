from app import app, db, Artist, Show, Venue
from datetime import datetime


def seed_data():
    with app.app_context():
        # Create sample venues
        venues_data = [
            {
                "name": "The Musical Hop",
                "city": "San Francisco",
                "state": "CA",
                "address": "1015 Folsom Street",
                "phone": "123-123-1234",
                "image_link": "https://example.com/image1.jpg",
                "facebook_link": "https://facebook.com/venue1",
                "website": "https://www.themusicalhop.com",
                "seeking_talent": True,
                "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
                "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"]
            },
            {
                "name": "Park Square Live Music & Coffee",
                "city": "San Francisco",
                "state": "CA",
                "address": "34 Whiskey Moore Ave",
                "phone": "123-123-1234",
                "image_link": "https://example.com/image2.jpg",
                "facebook_link": "https://facebook.com/venue2",
                "website": "https://www.parksquarelivemusicandcoffee.com",
                "seeking_talent": False,
                "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"]
            },
            {
                "name": "The Dueling Pianos Bar",
                "city": "New York",
                "state": "NY",
                "address": "335 Delancey Street",
                "phone": "914-003-1132",
                "image_link": "https://example.com/image3.jpg",
                "facebook_link": "https://facebook.com/venue3",
                "website": "https://www.theduelingpianos.com",
                "seeking_talent": False,
                "genres": ["Classical", "R&B", "Hip-Hop"]
            }
        ]

        venue_objs = []
        for venue_data in venues_data:
            venue = Venue(
                name=venue_data["name"],
                city=venue_data["city"],
                state=venue_data["state"],
                address=venue_data["address"],
                phone=venue_data["phone"],
                image_link=venue_data["image_link"],
                facebook_link=venue_data["facebook_link"],
                website=venue_data["website"],
                seeking_talent=venue_data["seeking_talent"],
                seeking_description=venue_data.get("seeking_description"),
                genres=venue_data["genres"]
            )
            db.session.add(venue)
            venue_objs.append(venue)

        db.session.commit()  # Commit venues to generate their IDs

        # Create sample artists
        artists_data = [
            {
                "name": "Guns N Petals",
                "genres": ["Rock n Roll"],
                "city": "San Francisco",
                "state": "CA",
                "phone": "326-123-5000",
                "website": "https://www.gunsnpetalsband.com",
                "facebook_link": "https://www.facebook.com/GunsNPetals",
                "seeking_venue": True,
                "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
                "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
            },
            {
                "name": "Matt Quevedo",
                "genres": ["Jazz"],
                "city": "New York",
                "state": "NY",
                "phone": "300-400-5000",
                "facebook_link": "https://www.facebook.com/mattquevedo923251523",
                "seeking_venue": False,
                "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
            },
            {
                "name": "The Wild Sax Band",
                "genres": ["Jazz", "Classical"],
                "city": "San Francisco",
                "state": "CA",
                "phone": "432-325-5432",
                "seeking_venue": False,
                "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
            }
        ]

        artist_objs = []
        for artist_data in artists_data:
            artist = Artist(
                name=artist_data["name"],
                city=artist_data["city"],
                state=artist_data["state"],
                phone=artist_data["phone"],
                image_link=artist_data["image_link"],
                facebook_link=artist_data.get("facebook_link"),
                website=artist_data.get("website"),
                seeking_venue=artist_data["seeking_venue"],
                seeking_description=artist_data.get("seeking_description"),
                genres=artist_data["genres"]
            )
            db.session.add(artist)
            artist_objs.append(artist)

        db.session.commit()  # Commit artists to generate their IDs

        # Create sample shows
        shows_data = [
            {
                "artist_id": artist_objs[0].id,
                "venue_id": venue_objs[0].id,
                "start_time": datetime(2019, 5, 21, 21, 30)
            },
            {
                "artist_id": artist_objs[1].id,
                "venue_id": venue_objs[1].id,
                "start_time": datetime(2019, 6, 15, 23, 0)
            },
            {
                "artist_id": artist_objs[2].id,
                "venue_id": venue_objs[2].id,
                "start_time": datetime(2035, 4, 1, 20, 0)
            },
            {
                "artist_id": artist_objs[2].id,
                "venue_id": venue_objs[2].id,
                "start_time": datetime(2035, 4, 8, 20, 0)
            },
            {
                "artist_id": artist_objs[2].id,
                "venue_id": venue_objs[2].id,
                "start_time": datetime(2035, 4, 15, 20, 0)
            }
        ]

        for show_data in shows_data:
            show = Show(
                artist_id=show_data["artist_id"],
                venue_id=show_data["venue_id"],
                start_time=show_data["start_time"]
            )
            db.session.add(show)

        db.session.commit()  # Commit shows

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
