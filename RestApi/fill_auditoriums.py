from models import Session, Auditorium

def main():
    auditorium_1 = Auditorium(number=10, max_people=100, is_free=True)
    auditorium_2 = Auditorium(number=15, max_people=200, is_free=True)
    auditorium_3 = Auditorium(number=20, max_people=250, is_free=True)
    auditorium_4 = Auditorium(number=25, max_people=150, is_free=True)
    auditorium_5 = Auditorium(number=30, max_people=300, is_free=True)

    Session.add(auditorium_1)
    Session.add(auditorium_2)
    Session.add(auditorium_3)
    Session.add(auditorium_4)
    Session.add(auditorium_5)

    Session.commit()

    for i in range(5):
        print(Session.query(Auditorium).all()[i])

if __name__ == '__main__':
    main()