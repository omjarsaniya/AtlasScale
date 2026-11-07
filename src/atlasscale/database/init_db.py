from atlasscale.database.connection import Base, engine
from atlasscale.database.models import JobModel


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()