import os
import psycopg

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pgvector import Vector
from pgvector.psycopg import register_vector

#database cred
load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
USER_ID = os.environ["PAM_TEST_USER_ID"]

#load embed model 
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text):
    numbers = model.encode(
        text,
        normalize_embeddings=True
    )
    return Vector(numbers)

#connect SUPABASE
with psycopg.connect(
    DATABASE_URL,
    sslmode="require"
) as conn:
    register_vector(conn)

    with conn.cursor() as cursor:

        #get memories w/0 embeddings
        cursor.execute("""
            SELECT id, content
            FROM public.memories
            WHERE user_id = %s
            and embedding IS NULL
        """, (USER_ID,))
        memories = cursor.fetchall()

        for memory_id, content in memories:
            embedding = create_embedding(content)

            cursor.execute("""
                UPDATE public.memories
                SET embedding = %s
                WHERE id = %s AND user_id = %s
            """, (embedding, memory_id, USER_ID))

            print(f"Embedded Memory {memory_id}")

        conn.commit()
        print("Embedding saved!")

        #Ask databsase question
        question = input("\nAsk PAM a question:")

        query_embedding = create_embedding(question)

        #search with cosine distance
        cursor.execute("""
            SELECT id, content
            FROM public.memories
            WHERE user_id = %s
            ORDER BY embedding <=> %s
            LIMIT 3
        """, (USER_ID, query_embedding))

        results = cursor.fetchall()

        print("\nMost relevant memories:")

        for memory_id, content in results:
            print(f"M{memory_id}: {content}")
