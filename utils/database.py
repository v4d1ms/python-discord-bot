import psycopg2,os
from dotenv import load_dotenv
import psycopg2.pool
from utils.logs import success, info, error, warning


load_dotenv()

class Database():
    __instance = None

    # Singleton pattern
    # Making sure only one instance of the database is created && only one connection pool is created
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Database, cls).__new__(cls)

            try:
                # Creating once a connection pool 
                cls.__instance.pool = psycopg2.pool.ThreadedConnectionPool(
                    1,
                    50,
                    host=os.getenv("DB_HOST"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASS")
                )

            except (Exception, psycopg2.DatabaseError) as error:
                raise Exception("Database connection failed!")
            
        success("Database pool instance created!")
        return cls.__instance

    def execute_query(self, query : str, params : list =None):
        conn = None
        cursor = None

        try:
            conn = self.get_conn()
            cursor = conn.cursor()

            cursor.execute(query, params)

            if "SELECT" in query.upper():
                result = cursor.fetchall()
            else:
                result = cursor.rowcount

            conn.commit()

            return result
        
        except (Exception, psycopg2.DatabaseError) as error:

            if conn:
                conn.rollback()

            raise Exception(f"Failed to execute query!: \n {error}")
        
        finally:

            if cursor:
                info("Closing query cursor!")
                cursor.close()

            if conn:
                info("Returning database connection to the pool!")
                self.pool.putconn(conn)


    def get_conn(self):
        try: 
            __conn = self.pool.getconn()
            if not __conn:
                raise Exception("Failed to get connection from pool!")
            
            return __conn
        
        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(f"Database connection failed!: \n {error}")
        
    def close(self):
        if self.pool:
            self.pool.closeall()
            info("Database connection pool closed!")