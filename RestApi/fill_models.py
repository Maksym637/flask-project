from models import Session, User, Auditorium, Access

def main():
    """_summary_
    In this module, I add and commit some attributes to my database (ReservAuditorium).
    After that, all added attributes are output to the console.
    """

    user_1 = User(username="MO", first_name="Maksym", last_name="Oliinyk", email="Maks@gmail.com", password="1111", phone="2381843", user_status=True)
    user_2 = User(username="TP", first_name="Tetiana", last_name="Piuryk", email="Tet@gmail.com", password="2222", phone="5556677", user_status=True)
    auditorium_1 = Auditorium(number=15, max_people=200, is_free=True)
    auditorium_2 = Auditorium(number=30, max_people=250, is_free=True)
    access = Access(auditorium_id=1, user_id=1, start="2022-04-28 11:15:00", end="2022-04-28 13:00:00")
    
    Session.add(user_1)
    Session.add(user_2)
    Session.add(auditorium_1)
    Session.add(auditorium_2)
    Session.commit()

    Session.add(access)
    Session.commit()
    
    print(" --- USERS --- ")
    print(Session.query(User).all()[0])
    print(Session.query(User).all()[1])
    print(" --- AUDITORIUMS --- ")
    print(Session.query(Auditorium).all()[0])
    print(Session.query(Auditorium).all()[1])
    print(" --- ACCESS --- ")
    print(Session.query(Access).all()[0])
    
    Session.close()

if __name__ == "__main__":
    main()