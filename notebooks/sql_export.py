import config
import psycopg2 as ps
from psycopg2 import sql, errors

def create_database():
    
    DB_NAME = 'BLS_Data'

    # Create connection to PgAdmin 4 PostgreSQL Database
    try:

        conn = ps.connect(
            database='postgres',
            user = 'postgres',
            password = config.password,
            host = 'localhost',
            port = '5432'
        )

        conn.autocommit = True

        # Create cursor object to open connection to DB
        cursor = conn.cursor()

        # Create script to create the database
        cursor.execute("Select 1 from pg_database where datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
            print(f'Database {DB_NAME} created successfully.')
        else:
            print(f'Database {DB_NAME} already exists.')
    except (ps.OperationalError, ps.Error) as e:
            print(f'Database creation or connection error {e}')


    # Close the connection
    conn.close()
            


def write_to_DB():
    
    
    conn = ps.connect(database = "BLS_Data",
                            user = 'postgres',
                            password = config.password,
                            host = 'localhost',
                            port = '5432')

    
    conn.autocommit = True

    # Create cursor object to open connection to DB
    cursor = conn.cursor()

    # Create new table
    create_table_sql = '''
            CREATE TABLE IF NOT EXISTS SERIES_DETAILS(
                                SERIESID CHAR(20),\
                                YEAR SMALLINT,\
                                PERIOD CHAR(3),\
                                VALUE DECIMAL
                                );
            '''
    
    # Create BLS_Data table
    cursor.execute(create_table_sql)

    # Load data from data directory to database
    try:
         
        with open('../data/LaborForceParticipationRate.csv', 'r') as f:
            cursor.copy_expert("""
                                COPY SERIES_DETAILS(seriesID, year, period, value)
                                FROM STDIN
                                WITH CSV HEADER DELIMITER ','
                                """, f)
    except Exception as e:
        print(f'Error during data load {e}.')

    conn.commit()
    cursor.close()
    conn.close()




