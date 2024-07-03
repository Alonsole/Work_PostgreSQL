import psycopg2

class Workdb:
    def __init__(self, passw, datab, user_n, id_user=None, name_user=None,
                 surname_user=None, email_user=None, telephone_user=None):
        self.password = passw
        self.database = datab
        self.user = user_n
        self.id = id_user
        self.name = name_user
        self.surname = surname_user
        self.email = email_user
        self.telephone = telephone_user
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)

    def createbase(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS clientdb(
                        ID_client INT PRIMARY KEY,
                        name VARCHAR(50) UNIQUE NOT NULL,
                        surname VARCHAR(100) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL
                    );
                    """)
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS telephone(
                        ID_telephone INT PRIMARY KEY,
                        number VARCHAR(20),
                        ID_client INT,
                        FOREIGN KEY (ID_client) REFERENCES clientdb(ID_client)
                    );
                    """)
            self.conn.commit()  # фиксируем в БД
        print('Успешное создание основы базы')
        self.conn.close()

    """добавить пользователя и залить телефоны."""
    def insertsql(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                    INSERT INTO clientdb(ID_client, name, surname, email) VALUES(
                                        {self.id},'{self.name}', '{self.surname}', '{self.email}');
                        """)
            cur.execute("""SELECT MAX(ID_telephone) FROM telephone; """)
            result_num = cur.fetchone()[0]

            if result_num == None:
                result_num = 1

            i = 0
            for number in self.telephone:
                cur.execute(f"""
                    INSERT INTO telephone(ID_telephone, number, ID_client) VALUES(
                                        {int(result_num) + i}, '{number}', {self.id});
                            """)
                i += 1
                self.conn.commit()
        print('Успешно создан: ', self.name)
        self.conn.close()

    """Добавить телефон существующему клиенту"""
    def inserttelephone(self):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT id_client FROM clientdb WHERE id_client = %s;
                        """, (id_user,))
            result_id = cur.fetchone()[0]

            cur.execute("""SELECT MAX(ID_telephone) FROM telephone; """)
            result_num = cur.fetchone()[0]
            if result_num == None:
                result_num = 0

            cur.execute(f"""
                    INSERT INTO telephone(ID_telephone, number, ID_client) VALUES(
                                        {result_num + 1}, '{telephone[0]}', {int(result_id)});
                        """)
            self.conn.commit()
        print('Успешно обработан: ', self.name)
        self.conn.close()

    def edituser(self):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT id_client FROM clientdb WHERE id_client = %s;
                        """, (id_user,))
            result_id = cur.fetchone()[0]
            cur.execute(f"""
                        UPDATE clientdb SET name = '{self.name}', surname = '{self.surname}', email = '{self.email}'
                        WHERE id_client = %s;
                        """, (id_user,))
            self.conn.commit()
            print('Успешно обновлено')
        self.conn.close()

    def delphone(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                        DELETE FROM telephone
                        WHERE id_client = %s;
                        """, (id_user,))
            self.conn.commit()
            print('Успешно удалено')
        self.conn.close()

    def deluser(self):
        conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)
        with conn.cursor() as cur:
            cur.execute(f"""
                        DELETE FROM clientdb
                        WHERE id_client = %s;
                        """, (id_user,))
            conn.commit()
            print('Пользователь успешно удалён')
        conn.close()

    def finduser(self):
        with self.conn.cursor() as cur:
            cur.execute(f"""
                SELECT * FROM clientdb
                JOIN telephone ON telephone.id_client = clientdb.id_client 
                WHERE name = %s OR surname = %s OR email = %s OR number = %s;
                """, (self.name, self.surname, self.email, self.telephone[0]))
            print(*cur.fetchall())

        self.conn.close()

"""Получаем пароль из файла"""
with open("pass.txt", "r", encoding="utf8") as f:
    password = f.readline().strip()

"""СОЗДАНИЕ БАЗЫ"""
database = "personaldb"
user = "postgres"
# Workdb(password,database,user).createbase() # Создание базы

"""Работа с базой"""
id_user = '1'
name = 'Стас'
surname = 'Стасов'
email = '1@mail'
# telephone = ['899191991']
# telephone = ['111-1111', '222-2222', '333-3333']
telephone = ['']
"""Добавить юзера в базу"""
Workdb(password, database, user, id_user, name, surname, email, telephone).insertsql()

"""Добавить телефон из списка под индексом НОЛЬ поиск по id_user"""
# Workdb(password, database, user, id_user, telephone).inserttelephone()

"""Корректировка user по id_user"""
# Workdb(password, database, user, id_user, name, surname, email).edituser()

"""Удалить телефон"""
# Workdb(password, database, user, id_user).delphone()

"""Удалить пользователя"""
# Workdb(password, database, user, id_user).deluser()

"""Получить информацию из базы"""
# Workdb(password, database, user, id_user, name, surname, email, telephone).finduser()