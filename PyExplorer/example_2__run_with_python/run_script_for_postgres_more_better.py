import psycopg2
from local_settings import postgres_config


class PostgresManager:
    def __init__(self, config, is_autocommit=False):
        self.config = config
        self.is_autocommit = is_autocommit  # Флаг для включения/выключения автокоммита
        self.conn = None
        self.cur = None

    def __enter__(self):
        self.conn = psycopg2.connect(**self.config)
        self.conn.autocommit = self.is_autocommit  # Устанавливаем режим автокоммита для соединения
        self.cur = self.conn.cursor()
        return self.cur  # Возвращаем курсор для работы внутри with

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



# Пример использования
if __name__ == '__main__':
    with PostgresManager(postgres_config) as cur:
        cur.execute("SELECT * FROM training_json;")
        rows = cur.fetchall()
        for row in rows:
            print(row)
