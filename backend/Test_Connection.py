
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL is missing from .env")

with psycopg.connect(
    database_url,
    sslmode="require"
) as conn:

    print("Successfully connected to Supabase!")

    
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, content, person_name, location
            FROM public.memories;
        """)

        memories = cursor.fetchall()

        for memory in memories:
            print(memory)
