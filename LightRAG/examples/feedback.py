import psycopg2


# PostgreSQL connection setup
# def get_postgres_connection():
#     try:
#         connection = psycopg2.connect(
#            dbname="diesl_nexus_logs",
#         user="postgres",
#         password="passwojrd",
#         host="diesl-eus-psql-dev-02.postgres.database.azure.com",
#         port="5432"
#         )
#         print("Database connection successful!")  # Print message on successful connection
#         return connection
#     except Exception as e:
#         print(f"Failed to connect to the database: {e}")  # Print error message if connection fails
#         raise


def get_postgres_connection():
    try:
        connection = psycopg2.connect(
           dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
        )
        print("Database connection successful!")  # Print message on successful connection
        return connection
    except Exception as e:
        print(f"Failed to connect to the database: {e}")  # Print error message if connection fails
        raise



# Function to save feedback to PostgreSQL
def save_feedback_to_postgres(spec_text, submittal_text, final_report, feedback, comments):
    connection = get_postgres_connection()
    cursor = connection.cursor()
    
    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id SERIAL PRIMARY KEY,
            spec_text TEXT,
            submittal_text TEXT,
            final_report TEXT,
            feedback VARCHAR(100),
            comments TEXT
        )
    """)
    
#     # Insert feedback
    cursor.execute("""
        INSERT INTO user_feedback (spec_text, submittal_text, final_report, feedback, comments)
        VALUES (%s, %s, %s, %s, %s)
    """, (spec_text, submittal_text, final_report, feedback, comments))
    
    connection.commit()
    cursor.close()
    connection.close()
get_postgres_connection()