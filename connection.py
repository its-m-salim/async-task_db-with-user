from dotenv import load_dotenv
import asyncpg
import os


load_dotenv()

passw = os.getenv("DB_PASSWORD")

async def connection_db():
    try:
        conn = await asyncpg.connect(
            port=5432,
            host = 'localhost',
            user="salim",
            database="task_db",
            password=passw
        )
        print("Connection successful!")
        return conn
    except Exception as error:
        print(f"{type(error)}: {error}")


async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS task(
            user_id int references users(user_id) on delete cascade,
            task_id serial primary key,
            title varchar(200),
            description text,
            due_date varchar(50),
            status bool default false,
            created_at timestamp default now(),
            is_active bool default true    
            )
        """)
        print("Task table created successful!")
        return True
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()



async def create_user():
    try:
        conn = await connection_db()
        await conn.execute("""
        create table if not exists users(
            user_id serial primary key,
            username varchar(100) unique,
            password varchar(100),
            created_at timestamp default now(),
            is_active bool default true
        )
        """)
        print("User table created successful!")
        return True
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()