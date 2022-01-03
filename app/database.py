from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQL_ALCHEMY_DATABASE_URL = "postgresql://<username>:<pass>@<ip address/hostname>/<database_name>"
SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost/fastapi"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
# in case of failure, I will loop till I find a connection
while True:
    try:
        # TODO: the connection need to be dinamic
        conn = psycopg2.connect(host="localhost",
                                database="fastapi",
                                user="postgres",
                                password="123456", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as err:
        print(f"Database failed! Error was {err}")
        time.sleep(2)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]




def find_post_by_id(id: int):
    for index, post in enumerate(my_posts):
        # print(post, f"id={id}", f"{post['id']}")
        if post['id'] == id:
            return post, index

"""
