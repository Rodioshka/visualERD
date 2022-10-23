from core.database import Database


def get_information_db() -> list:
    qs = """
            select json_agg(json_build_object('table_name',key,'columns', values))
from (select first_table                                       as key,
             json_agg(json_build_object('column_name', column_name, 'type', data_type, 'col_with_foreign',
                                        col_with_foreing, 'second_table_name', second_table_name, 'second_column_name'
                                        , second_column_name)) as values
      from (select first_table,
                   column_name,
                   data_type,
                   case when col_with_foreing is not null then col_with_foreing else '-' end   as col_with_foreing,
                   case when col_with_foreing is not null then second_table_name else '-' end  as second_table_name,
                   case when col_with_foreing is not null then second_column_name else '-' end as second_column_name
            from (SELECT col.table_name  as first_table,
                         col.column_name,
                         col.data_type,
                         kcu.column_name as col_with_foreing,
                         ccu.table_name  AS second_table_name,
                         ccu.column_name AS second_column_name
                  FROM information_schema.columns as col

                           left join information_schema.table_constraints AS tc on col.table_name = tc.table_name
                           left JOIN information_schema.key_column_usage AS kcu
                                     ON tc.constraint_name = kcu.constraint_name
                                         AND tc.table_schema = kcu.table_schema
                                         and col.column_name = kcu.column_name
                           left JOIN information_schema.constraint_column_usage AS ccu
                                     ON ccu.constraint_name = tc.constraint_name
                                         AND ccu.table_schema = tc.table_schema

                  WHERE tc.constraint_type = 'FOREIGN KEY'
                  order by first_table, column_name) a
           ) b
      group by first_table) as c;     
        """
    return Database().query(sql=qs)


def main():
    tables = get_information_db()
    for table in tables[0][0]:
        print(table['table_name'])
        print(table['columns'])
        break


if __name__ == '__main__':
    get_information_db()