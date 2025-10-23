from models import Base, get_engine
import os

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("✅ Database created/ready.")

if __name__ == "__main__":
    os.makedirs("instance", exist_ok=True)
    init_db()
