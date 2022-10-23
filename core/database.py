import psycopg2
from psycopg2.extras import RealDictCursor
from .config import DB


def get_queryset(query: str) -> RealDictCursor:
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=DB['USER'],
                                      password=DB['PASSWORD'],
                                      host=DB['HOST'],
                                      port=DB['PORT'],
                                      database=DB['DB_NAME'])
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query=query)
        qs = cursor.fetchall()
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
        return qs
    except Exception as error:
        print("Ошибка при работе с PostgreSQL", error)


def get_table_with_foreign_keys():
    qs = """
                SELECT
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name
        FROM
            information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY';
    """
    return get_queryset(query=qs)


def get_table_with_columns():
    qs = """
            select t.table_name, col.column_name, col.data_type, col.is_nullable
        from information_schema.columns as col
                 join information_schema.tables t on col.table_name = t.table_name and t.table_schema = 'public'
        order by t.table_name, col.column_name;
    """
    return get_queryset(query=qs)


if __name__ == '__main__':
    print(get_table_with_foreign_keys())
