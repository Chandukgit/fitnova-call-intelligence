from sqlalchemy import text

from app.database.session import SessionLocal


def test_connection():
    db = SessionLocal()

    try:
        result = db.execute(text("SELECT 1"))

        print("✅ Database Connected Successfully!")

        print(result.scalar())

    except Exception as e:

        print("❌ Database Connection Failed")

        print(e)

    finally:

        db.close()


if __name__ == "__main__":
    test_connection()