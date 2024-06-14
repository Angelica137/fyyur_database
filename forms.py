from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Optional
from enum import Enum


class GenreEnum(Enum):
    Alternative = "Alternative"
    Blues = "Blues"
    Classical = "Classical"
    Country = "Country"
    Electronic = "Electronic"
    Folk = "Folk"
    Funk = "Funk"
    HipHop = "Hip-Hop"
    HeavyMetal = "Heavy Metal"
    Instrumental = "Instrumental"
    Jazz = "Jazz"
    MusicalTheatre = "Musical Theatre"
    Pop = "Pop"
    Punk = "Punk"
    R_B = "R&B"
    Reggae = "Reggae"
    RocknRoll = "Rock n Roll"
    Soul = "Soul"
    Swing = "Swing"
    Other = "Other"


class StateEnum(Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'


class ShowForm(Form):
    artist_id = StringField('artist_id')
    venue_id = StringField('venue_id')
    start_time = DateTimeField(
        'start_time',
        validators=[
            DataRequired()],
        default=datetime.today())


class VenueForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=[(state.value, state.value) for state in StateEnum]
    )
    address = StringField('address', validators=[DataRequired()])
    phone = StringField(
        'phone',
        validators=[
            DataRequired(),
            Regexp(
                r'^\d{3}-\d{3}-\d{4}$',
                message="Phone number must be in the format xxx-xxx-xxxx")])
    image_link = StringField('image_link', validators=[Optional(), URL()])
    genres = SelectMultipleField(
        # TODO implement enum restriction - DONE
        'genres', validators=[DataRequired()],
        choices=[(genre.value, genre.value) for genre in GenreEnum])
    facebook_link = StringField(
        'facebook_link', validators=[
            Optional(), URL()])
    website = StringField('website', validators=[Optional(), URL()])
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description')


class ArtistForm(Form):
    name = StringField('name', validators=[DataRequired()])
    city = StringField('city', validators=[DataRequired()])
    state = SelectField(
        'state',
        validators=[DataRequired()],
        choices=[(state.value, state.value) for state in StateEnum]
    )
    phone = StringField(
        # TODO implement validation logic for phone - DONE
        'phone', validators=[DataRequired(), Regexp(r'^\d{3}-\d{3}-\d{4}$', message="Phone number must be in the format xxx-xxx-xxxx.")]
    )
    image_link = StringField('image_link', validators=[Optional(), URL()])
    genres = SelectMultipleField(
        # TODO implement enum restriction - DONE
        'genres', validators=[DataRequired()],
        choices=[(genre.value, genre.value) for genre in GenreEnum])
    facebook_link = StringField(
        # TODO implement enum restriction - is this supposed to be here. CANNOT
        # DO THIS
        'facebook_link', validators=[Optional(), URL()]
    )
    website = StringField('website', validators=[Optional(), URL()])
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description')


class CSRFForm(Form):
    pass


class SearchForm(Form):
    search_term = StringField("search-term", validators=[DataRequired()])
