from unittest.mock import MagicMock, patch

import pytest

from business_object.chanson import Chanson
from business_object.paroles import Paroles
from dao.dao import DAO
from dao.dao_chanson import DAO_chanson


@pytest.fixture
def reset_db():
    dao = DAO()
    dao._drop_table()


@pytest.fixture
def fake_paroles():
    return Paroles(content="Paroles de test", vecteur=[0.1, 0.2, 0.3])


@pytest.fixture
def fake_chanson(fake_paroles):
    return Chanson(titre="TestSong", artiste="TestArtist", annee=2024, paroles=fake_paroles)


def test_add_chanson_ok(fake_chanson):
    reset_db
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1  # simule un INSERT INTO réussi

    # with DBConnection().connection as connection:
        # with connection.cursor() as cursor:
    with patch("dao_chanson.DBConnection") as mock_connection:
        mock_connection.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao.add_chanson(fake_chanson)

    mock_cursor.execute.assert_called_once()
    assert res is True


def test_add_chanson_duplicate(fake_chanson):
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 0  # déjà existante

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao.add_chanson(fake_chanson)

    assert res is False


# === TEST get_chansons ===
def test_get_chansons_returns_list(fake_paroles):
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {
            "titre": "A",
            "artiste": "B",
            "annee": 2020,
            "embed_paroles": [0.1, 0.2],
            "str_paroles": "blabla",
        }
    ]

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        result = dao.get_chansons()

    assert len(result) == 1
    assert result[0].titre == "A"


def test_get_chansons_none_when_empty():
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = None

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao.get_chansons()

    assert res is None


# === TEST get_chanson_from_embed_paroles ===
def test_get_chanson_from_embed_paroles_found(fake_paroles):
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "titre": "T",
        "artiste": "A",
        "annee": 2021,
        "embed_paroles": fake_paroles.vecteur,
        "str_paroles": fake_paroles.content,
    }

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        result = dao.get_chanson_from_embed_paroles(fake_paroles.vecteur)

    assert result.titre == "T"
    assert result.artiste == "A"


def test_get_chanson_from_embed_paroles_none(fake_paroles):
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao.get_chanson_from_embed_paroles(fake_paroles.vecteur)

    assert res is None


# === TEST get_chanson_from_titre_artiste ===
def test_get_chanson_from_titre_artiste_found(fake_paroles):
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {
        "titre": "T",
        "artiste": "A",
        "annee": 2020,
        "embed_paroles": fake_paroles.vecteur,
        "str_paroles": fake_paroles.content,
    }

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao.get_chanson_from_titre_artiste("T", "A")

    assert res.titre == "T"
    assert res.artiste == "A"


def test_get_chanson_from_titre_artiste_none():
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao.get_chanson_from_titre_artiste("T", "A")

    assert res is None


# === TEST _del_chanson_via_titre_artiste ===
def test_del_chanson_via_titre_artiste_success():
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 1

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao._del_chanson_via_titre_artiste("T", "A")

    assert res is True


def test_del_chanson_via_titre_artiste_not_found():
    dao = DAO_chanson()
    mock_cursor = MagicMock()
    mock_cursor.rowcount = 0

    with patch("dao_chanson.DBConnection") as mock_conn:
        mock_conn.return_value.connection.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        res = dao._del_chanson_via_titre_artiste("T", "A")

    assert res is False
