import psycopg2

class Workdb:
    def __init__(self, passw, datab, user_n, host, port, id_user=None, name_user=None,
                 surname_user=None, email_user=None, telephone_user=None):
        self.password = passw
        self.database = datab
        self.user = user_n
        self.id = id_user
        self.name = name_user
        self.surname = surname_user
        self.email = email_user
        self.telephone = telephone_user
        self.host = host
        self.port = port

    """Создать базу"""

    def createbase(self):
        with psycopg2.connect(user=self.user, password=self.password,
                              host=self.host, port=self.port, database=self.database) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        CREATE TABLE IF NOT EXISTS clientdb(
                            ID_client INT PRIMARY KEY,
                            name VARCHAR(50) UNIQUE NOT NULL,
                            surname VARCHAR(100) UNIQUE NOT NULL,
                            email VARCHAR(100) UNIQUE NOT NULL;
                        """)
                cur.execute("""
                        CREATE TABLE IF NOT EXISTS telephone(
                            ID_telephone INT PRIMARY KEY,
                            number VARCHAR(20),
                            ID_client INT,
                            FOREIGN KEY (ID_client) REFERENCES clientdb(ID_client));
                        """)
            print('Успешное создание основы базы')
        conn.close()

    """добавить пользователя и залить телефоны."""

    def insertsql(self):
        with psycopg2.connect(user=self.user, password=self.password,
                              host=self.host, port=self.port, database=self.database) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        INSERT INTO clientdb(ID_client, name, surname, email) VALUES(
                                            %s, %s, %s, %s);
                            """, (self.id, self.name, self.surname, self.email))
                cur.execute("""SELECT MAX(ID_telephone) FROM telephone; """)
                result_num = cur.fetchone()[0]

                if result_num == None:
                    result_num = 1

                i = 0
                for number in self.telephone:
                    cur.execute(f"""
                        INSERT INTO telephone(ID_telephone, number, ID_client) VALUES(%s, %s, %s);
                                """, (int(result_num) + i, number, self.id))
                    i += 1

            print('Успешно создан: ', self.name)
        conn.close()

    """Добавить телефон существующему клиенту"""

    def inserttelephone(self):
        with psycopg2.connect(user=self.user, password=self.password,
                              host=self.host, port=self.port, database=self.database) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT id_client FROM clientdb WHERE id_client = %s;
                            """, (id_user,))
                result_id = cur.fetchone()[0]

                cur.execute("""SELECT MAX(ID_telephone) FROM telephone; """)
                result_num = cur.fetchone()[0]
                if result_num == None:
                    result_num = 0

                cur.execute("""INSERT INTO telephone(ID_telephone, number, ID_client) VALUES(%s, %s, %s);
                            """, (result_num + 1, telephone[0], int(result_id)))
            print('Успешно обработан: ', self.name)
        conn.close()

    def edituser(self):
        with psycopg2.connect(user=self.user, password=self.password,
                              host=self.host, port=self.port, database=self.database) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT id_client FROM clientdb WHERE id_client = %s;
                            """, (id_user,))
                cur.execute(f"""
                            UPDATE clientdb SET name = %s, surname = %s, email = %s
                            WHERE id_client = %s;
                            """, (self.name, self.surname, self.email, id_user))
                print('Успешно обновлено')
        conn.close()

    def delphone(self):
        with psycopg2.connect(user=self.user, password=self.password,
                              host=self.host, port=self.port, database=self.database) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                            DELETE FROM telephone
                            WHERE id_client = %s;
                            """, (id_user,))
                print('Успешно удалено')
        conn.close()

    def deluser(self):
        with psycopg2.connect(user=self.user, password=self.password,
                              host=self.host, port=self.port, database=self.database) as conn:
            with conn.cursor() as cur:
                cur.execute(f""" 
                                    DELETE FROM telephone 
                                    WHERE id_client = %s; 
                                    """, (id_user,))
                cur.execute(f""" 
                                    DELETE FROM clientdb 
                                    WHERE id_client = %s; 
                                    """, (id_user,))
            print('Пользователь успешно удалён')
        conn.close()

    def finduser(self):
        with psycopg2.connect(user=self.user, password=self.password,
                              host=self.host, port=self.port, database=self.database) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT * FROM clientdb 
                            JOIN telephone ON telephone.id_client = clientdb.id_client     
                            WHERE(%s IS NOT NULL AND name = %s) OR
                            (%s IS NOT NULL AND surname = %s) OR
                            (%s IS NOT NULL AND email = %s) OR
                            (%s IS NOT NULL AND number = %s);
                            """, (self.name, self.name, self.surname, self.surname, self.email, self.email,
                                  self.telephone[0], self.telephone[0]))
                print(*cur.fetchall())

        conn.close()


"""Получаем пароль из файла"""
with open("pass.txt", "r", encoding="utf8") as f:
    password = f.readline().strip()
if __name__ == "__main__":
    """СОЗДАНИЕ БАЗЫ"""
    database = "personaldb"
    user = "postgres"
    host = 'localhost'
    port = '5432'
    Workdb(password, database, user, host, port).createbase()  # Создание базы

    """Работа с базой"""
    id_user = '1'
    name = 'Стас'
    surname = 'Стасови'
    email = 'mail@mail1.ru'
    telephone = ['89252311']
    # telephone = ['111-1111', '222-2222', '333-3333']
    # telephone = ['']
    """Добавить юзера в базу"""
    # Workdb(password, database, user, host, port, id_user, name, surname, email, telephone).insertsql()

    """Добавить телефон из списка под индексом НОЛЬ поиск по id_user"""
    # Workdb(password, database, user, host, port, id_user, telephone).inserttelephone()

    """Корректировка user по id_user"""
    # Workdb(password, database, user, host, port, id_user, name, surname, email).edituser()

    """Удалить телефон"""
    # Workdb(password, database, user, host, port, id_user).delphone()

    """Удалить пользователя"""
    # Workdb(password, database, user, host, port, id_user).deluser()

    """Получить информацию из базы"""
    # Workdb(password, database, user, host, port, id_user, name, surname, email, telephone).finduser()
