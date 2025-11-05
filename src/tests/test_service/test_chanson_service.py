import pytest

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from service.chanson_service import ChansonService


class TestChansonService:
    @pytest.fixture
    def service(self):
        """Fixture pour créer une instance du service."""
        return ChansonService()

    @pytest.fixture
    def titre(self):
        return "Imagine"

    @pytest.fixture
    def artiste(self):
        return "John Lennon"

    @pytest.fixture
    def chanson(self):
        titre = "Imagine"
        artiste = "John Lennon"
        return Chanson(titre, artiste)

    def test_instantiate_chanson(self, service, titre, artiste, chanson):
        """Teste l'instantiation d'une chanson, par défaut il n'y a pas d'année ni de paroles"""
        new_chanson = service.instantiate_chanson(titre, artiste)

        assert isinstance(new_chanson, Chanson)
        assert new_chanson == chanson
        assert new_chanson.annee is None
        assert new_chanson.paroles is None

    def test_add_chanson_paroles(self, service, titre, artiste):
        """Teste l'ajout des paroles et leur vectorisation"""
        chanson = service.instantiate_chanson(titre, artiste)
        service.add_chanson_paroles(chanson)

        assert isinstance(chanson, Chanson)
        assert chanson.paroles is not None
        assert isinstance(chanson.paroles, Paroles)
        assert isinstance(chanson.paroles.content, str)
        assert chanson.paroles.vecteur is not None
        assert isinstance(chanson.paroles.vecteur, list)
        assert isinstance(chanson.paroles.vecteur[0], float)
