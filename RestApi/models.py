from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, DateTime, Boolean

engine = create_engine('mysql+pymysql://root:Barca2381843@localhost/ReservAuditorium')
engine.connect()

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
BaseModel = declarative_base()


class User(BaseModel):
    """_summary_ 
    A class used to represent a User model.

    Args:
        id : int
          unique user number (primary_key)
        username : str
          unique username
        first_name : str
          first name of the user
        last_name : str
          family name of the user
        email : str
          electronic mail of the user
        password : str
          user's password
        phone : str
          user's phone
        user_status : bool
          determines whether the user is an admin or not

    Returns:
        __str__(): returns all user attributes.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(45), unique=True)
    first_name = Column(VARCHAR(45))
    last_name = Column(VARCHAR(45))
    email = Column(VARCHAR(45))
    password = Column(VARCHAR(45))
    phone = Column(VARCHAR(15))
    user_status = Column(Boolean)

    def __init__(self, username :str, first_name: str=None, last_name: str=None, email: str=None, password: str=None, phone: str=None, user_status: bool=False) -> None:
        """_summary_
        Constructs all the necessary attributes for the user object.

        Args:
            username (str): unique username.
            first_name (str, optional): first name of the user. Defaults to None.
            last_name (str, optional): family name of the user. Defaults to None.
            email (str, optional): electronic mail of the user. Defaults to None.
            password (str, optional): user's password. Defaults to None.
            phone (str, optional): user's phone. Defaults to None.
            user_status (bool, optional): determines whether the user is an admin or not. Defaults to False.
        """

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.user_status = user_status
    
    def __str__(self) -> str:
        """_summary_
        Returns all user attributes.

        Returns:
            str: displays all user information.
        """

        return f"id        : {self.id}\n" \
               f"username  : {self.username}\n" \
               f"firstName : {self.first_name}\n" \
               f"lastName  : {self.last_name}\n" \
               f"email     : {self.email}\n" \
               f"password  : {self.password}\n" \
               f"phone     : {self.phone}\n" \
               f"userStatus: {self.user_status}\n"


class Auditorium(BaseModel):
    """_summary_
    A class used to represent an Auditorium model.

    Args:
        id : int
          unique auditorium number (primary_key)
        number : int
          the auditorium number
        max_people : int
          the maximum number of people that can be in the auditorium
        is_free : bool
          check if auditorium is free

    Returns:
        __str__(): returns all auditorium attributes.
    """

    __tablename__ = "auditorium"

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    max_people = Column(Integer)
    is_free = Column(Boolean)

    def __init__(self, number: int=None, max_people: int=None, is_free: bool=False) -> None:
        """_summary_
        Constructs all the necessary attributes for the auditorium object.

        Args:
            number (int, optional): the auditorium number. Defaults to None.
            max_people (int, optional): the maximum number of people that can be in the auditorium. Defaults to None.
            is_free (bool, optional): check if auditorium is free. Defaults to False.
        """

        self.number = number
        self.max_people = max_people
        self.is_free = is_free
    
    def __str__(self) -> str:
        """_summary_
        Returns all auditorium attributes.

        Returns:
            str: displays all auditorium information.
        """

        return f"id         : {self.id}\n" \
               f"number     : {self.number}\n" \
               f"max_people : {self.max_people}\n" \
               f"is_free    : {self.is_free}\n"


class Access(BaseModel):
    """_summary_
    A class used to represent an Access model.

    Args:
        id : int
          unique access number (primary_key)
        auditorium_id : int
          an auditorium id which the reservation is linked (foreign_key)
        user_id : int
          a user id which the reservation is linked (foreign_key)
        start : datetime
          auditorium reservation start
        end : datetime
          end of auditorium reservation

    Returns:
        __str__(): returns all access attributes.
    """

    __tablename__ = "access"

    id = Column(Integer, primary_key=True)
    auditorium_id = Column(Integer, ForeignKey(Auditorium.id, onupdate="CASCADE", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"))
    start = Column(DateTime)
    end = Column(DateTime)

    def __init__(self, auditorium_id: int, user_id: int, start: datetime, end: datetime) -> None:
        """_summary_
        Constructs all the necessary attributes for the access object.

        Args:
            auditorium_id (int): an auditorium id which the reservation is linked (foreign_key).
            user_id (int): a user id which the reservation is linked (foreign_key).
            start (datetime): auditorium reservation start.
            end (datetime): end of auditorium reservation.
        """

        self.auditorium_id = auditorium_id
        self.user_id = user_id
        self.start = start
        self.end = end
    
    def __str__(self) -> str:
        """_summary_
        Returns all access attributes.

        Returns:
            str: displays all access information.
        """

        return f"id            : {self.id}\n" \
               f"auditorium_id : {self.auditorium_id}\n" \
               f"user_id       : {self.user_id}\n" \
               f"start_time    : {self.start}\n" \
               f"end_time      : {self.end}\n"


BaseModel.metadata.create_all(engine)