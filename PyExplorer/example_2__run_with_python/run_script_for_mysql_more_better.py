import mysql.connector

from local_settings import mysql_config


class MySQLManager:
    def __init__(self, config, is_autocommit=False):
        self.config = config
        self.is_autocommit = is_autocommit  # Флаг для включения/выключения автокоммита
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.config)
        self.conn.autocommit = self.is_autocommit  # Устанавливаем режим автокоммита для соединения
        self.cur = self.conn.cursor()
        return self  # Возвращаем курсор для работы внутри with

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cur:
            self.cur.close()
        if self.conn:
            if not self.is_autocommit:  # Выполняем commit/rollback только при выключенном автокоммите
                if exc_type is None:
                    self.conn.commit()  # Фиксируем изменения, если ошибок не было
                else:
                    self.conn.rollback()  # Откатываем при ошибке
            self.conn.close()

    def show_databases(self):
        try:
            self.cur.execute("SHOW DATABASES;")
            rows = self.cur.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(e)

    def get_countries(self):
        try:
            self.cur.execute("SELECT * FROM employees.countries;")
            rows = self.cur.fetchall()
            for row in rows:
                print(row)
        except Exception as e:
            print(e)

    def delete_by_id(self, id):
        try:
            # self.cur.execute("""DELETE FROM images WHERE id = %s;""", (id,))
            self.cur.execute("""DELETE FROM employees.countries WHERE country_id = %s;""", (id,))
            print(f"Запись с id {id} успешно удалена!")

        except Exception as e:
            print(e)

    def add_file(self, f):
        try:
            source_file = os.path.join('/app/images_source', f)
            target_dir = "/app/images"

            filename = self.random_filename(f)  # создаём случайное имя файла
            target_file = os.path.join(target_dir, filename)

            shutil.copy(source_file, target_file)

            original_name = f
            size = round(os.stat(source_file).st_size / 1000, 1)
            file_type = f.split('.')[-1]
            self.cur.execute(
                """
            INSERT INTO images (filename, original_name, size, file_type)
            VALUES (%s, %s, %s, %s);""",
                (filename, original_name, size, file_type)
            )
            print(f"Файл {f} добавлен")
        except Exception as e:
            print(e)

    def show_table(self, is_print=True):
        self.cur.execute("""SELECT * FROM images;""")
        rows = self.cur.fetchall()
        if not is_print:
            return rows
        for row in rows:
            print(row)
        return None

    def get_page_by_page_num(self, page_num, is_print=True):
        # page_num -> 1 - 100000
        offset = (page_num - 1) * 10
        self.cur.execute("""SELECT * FROM images OFFSET %s LIMIT 10;""", (offset,))
        rows = self.cur.fetchall()
        if not is_print:
            return rows
        for row in rows:
            print(row)
        return None


# Пример использования
if __name__ == '__main__':
    with MySQLManager(mysql_config) as curr:
        curr.delete_by_id("ZW")

