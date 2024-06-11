from app import app, db, Artist, Show, Venue
from datetime import datetime


def seed_data():
    with app.app_context():
        venue1 = Venue(
            name="The Musical Hop",
            city="San Francisco",
            state="CA",
            address="1015 Folson Street",
            phone="123-123-1234",
            image_link="https://example.com/image1.jpg", 
            facebook_link="https://facebook.com/venue1"
				)
        venue2 = Venue(
            name="Park Square Live Music & Coffee", 
            city="San Francisco", 
            state="CA", 
            address="34 Whiskey Moore Ave", 
            phone="123-123-1234", 
            image_link="https://example.com/image2.jpg", 
            facebook_link="https://facebook.com/venue2"
        )
        venue3 = Venue(
            name="The Dueling Pianos Bar", 
            city="New York", 
            state="NY", 
            address="335 Delancey Street", 
            phone="123-123-1234", 
            image_link="https://example.com/image3.jpg", 
            facebook_link="https://facebook.com/venue3"
        )
        
        db.session.add_all([venue1, venue2, venue3])
        
        artist1 = Artist(
            name="Guns N Petals", 
            city="San Francisco", 
            state="CA", 
            phone="326-123-5000", 
            genres="Rock n Roll", 
            image_link="https://example.com/artist1.jpg", 
            facebook_link="https://facebook.com/artist1", 
            needs_talent=False, 
            needs_venue=True
        )
        artist2 = Artist(
            name="Matt Quevedo", 
            city="New York", 
            state="NY", 
            phone="300-400-5000", 
            genres="Jazz", 
            image_link="https://example.com/artist2.jpg", 
            facebook_link="https://facebook.com/artist2", 
            needs_talent=True, 
            needs_venue=False
        )
        artist3 = Artist(
            name="The Wild Sax Band", 
            city="San Francisco", 
            state="CA", 
            phone="432-325-5432", 
            genres="Jazz, Classical", 
            image_link="https://example.com/artist3.jpg", 
            facebook_link="https://facebook.com/artist3", 
            needs_talent=True, 
            needs_venue=True
        )
        
        db.session.add_all([artist1, artist2, artist3])
        
        show1 = Show(
            artist_id=1, 
            venue_id=1, 
            start_time=datetime(2023, 7, 21, 21, 30)
        )
        show2 = Show(
            artist_id=2, 
            venue_id=2, 
            start_time=datetime(2023, 8, 22, 20, 00)
        )
        show3 = Show(
            artist_id=3, 
            venue_id=3, 
            start_time=datetime(2023, 9, 23, 19, 00)
        )
        
        db.session.add_all((show1, show2, show3))
        
        db.session.commit()
        print("Database seeded successflly!")


if __name__ == "__main__":
    seed_data()