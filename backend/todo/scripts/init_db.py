from todo.database import engine
from todo.models import Base


def main():
    Base.metadata.create_all(bind=engine)
    print("Postgres db initialized!")


if __name__ == "__main__":
    main()
