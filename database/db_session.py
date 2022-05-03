import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__Session = None


def create_session():
    global __Session
    global_init()
    return __Session()


def global_init():
    global __Session

    if __Session:
        return

    conn_str = f'sqlite:///sqlite.db'

    engine = sa.create_engine(conn_str, echo=True, future=True)
    __Session = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)
