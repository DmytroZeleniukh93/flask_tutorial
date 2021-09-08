import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_menu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def add_post(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с таким url уже существует")
                return False
            
            self.__cur.execute('INSERT INTO posts VALUES(NULL, ?, ?, ?)', (title, text, url))
            self.__db.commit()
        except sqlite3.Error as error:
            print(f'Error {error}')
            return False
        return True

    def get_post(self, post_id):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {post_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))
        return (False, False)

    def get_posts_anonce(self):
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))
        return []

