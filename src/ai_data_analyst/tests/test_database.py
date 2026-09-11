from ai_data_analyst.database.connection import test_connection


def test_postgres_connection():
    version = test_connection()

    assert version is not None
    print(f"\nConnected to: {version}")