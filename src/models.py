from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
Base = declarative_base()



people_films = Table(
    'people_films',
    Base.metadata,
    Column('people_id', Integer, ForeignKey('people.id'), primary_key=True),
    Column('film_id', Integer, ForeignKey('film.id'), primary_key=True)
)

people_vehicles = Table(
    'people_vehicles',
    Base.metadata,
    Column('people_id', Integer, ForeignKey('people.id'), primary_key=True),
    Column('vehicle_id', Integer, ForeignKey('vehicle.id'), primary_key=True)
)

people_starships = Table(
    'people_starships',
    Base.metadata,
    Column('people_id', Integer, ForeignKey('people.id'), primary_key=True),
    Column('starship_id', Integer, ForeignKey('starship.id'), primary_key=True)
)

class User(db.Model):
    __tablename__: 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[list["Favorite"]] = db.relationship(
        "Favorite",
        back_populates='favorite'
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    element_id: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(default="")


class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    height: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(20), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    planet: Mapped["Planet"] = db.relationship(back_populates="people")

    films: Mapped[list["Film"]] = db.relationship(
        "Film",
        secondary=people_films,
        back_populates='people'
    )

    vehicles: Mapped[list["Vehicle"]] = db.relationship(
        "Vehicle",
        secondary=people_vehicles,
        back_populates='people'
    )

    starships: Mapped[list["Starship"]] = db.relationship(
        "Starship",
        secondary=people_starships,
        back_populates='people'
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.planet.name,
            "films": self.films,
            "vehicles": self.vehicles,
            "starships": self.starships
        }

class Film(db.Model):
    __tablename__ = 'film'
    id: Mapped[int] = mapped_column(primary_key=True)
    episode_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    director: Mapped[str] = mapped_column(String(50), nullable=False)
    producer: Mapped[str] = mapped_column(String(50), nullable=False)
    release_date: Mapped[str] = mapped_column(String(20), nullable=False)

    people: Mapped[list["People"]] = db.relationship(
        "People",
        secondary=people_films,
        back_populates='films'
    )

    def serialize(self):
        return {
            "id": self.id,
            "episode_id": self.episode_id,
            "title": self.title,
            "director": self.director,
            "producer": self.producer,
            "release_date": self.release_date,
            "people": self.people
        }
    


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(50), nullable=False)
    cost_in_credits: Mapped[str] = mapped_column(String(50), nullable=False)
    vehicle_class: Mapped[str] = mapped_column(String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "vehicle_class": self.vehicle_class
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    population: Mapped[str] = mapped_column(String(50), nullable=False)
    terrain: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(50), nullable=False)

    people: Mapped[list["People"]] = db.relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            "people": self.people
        }

class Starship(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(50), nullable=False)
    cost_in_credits: Mapped[str] = mapped_column(String(50), nullable=False)
    passengers: Mapped[str] = mapped_column(String(50), nullable=False)

    people: Mapped[list["People"]] = db.relationship(
        "People",
        secondary=people_starships,
        back_populates='starships'
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "passengers": self.passengers,
            "people": self.people
        }
