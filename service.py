from connection import*


async def create_task(user_id, title, descp, due_date):
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO task(user_id, title, description, due_date) VALUES
            ($1, $2, $3, $4)        
                    """,user_id, title, descp, due_date)
        print("Create task successful")
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()



async def get_task(user_id):
    try:
        conn = await connection_db()
        tasks = await conn.fetch("""
            SELECT * FROM task
            where user_id = $1
        """, user_id)
        for task in tasks:
            print(f"""
Task id: {task["task_id"]}
Title: {task["title"]}
Description: {task["description"]}
Dueration: {task["due_date"]}
Status: {task["status"]}
Created at: {task["created_at"]}
""")
        return tasks
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()


async def update_task(id, title, desc, due_date, user_id):
    try:
        conn = connection_db()
        await conn.execute("""
            update task
            set title = $1,
            description = $2,
            due_date = $3
            where task_id = $4 and user_id = $4
                        """, title, desc, due_date, id, user_id)
        print("Update task successful")
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()


async def registration(username, password):
    try:
        conn = await connection_db()
        await conn.execute("""
            INSERT INTO users(username, password) VALUES
            ($1, $2)        
                    """, username, password)
        print("User has been created successfuly!")
        return True
    except asyncpg.exceptions.UniqueViolationError:
        print(f"\n===== ERROR! ====\nUser '{username}' already exists. Please choose another username or Login!")
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()


async def login(username, password):
    try:
        conn = await connection_db()
        user_id = await conn.fetch("""
            select user_id, username  from users
            where username = $1 and password = $2
        """, username, password)
        return user_id[0]["user_id"], user_id[0]["username"]
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()



async def delete_user():
    try:
        conn = connection_db()
        await conn.execute("""
            update users
            set is_active = False
            where user_id = $1
                        """, id)
        print("User has been deleted")
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()



async def get_user(username):
    try:
        conn = await connection_db()
        user = await conn.fetch("""
            SELECT username, created_at FROM users
            where username = $1 and is_active = True
        """, username)
        return user
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()


async def show_profile(user_id):
    try:
        conn = await connection_db()
        profile = await conn.fetch("""
            select u.username, u.created_at,( select COUNT(*) from task where task.user_id = u.user_id) as total_tasks,
            task.title as last_added_task, task.created_at as task_created_at from users as u
            left join task on task.user_id = u.user_id
            where u.user_id = $1
            order by task.created_at desc
            limit 1
    """, user_id)
        for user in profile:
            print(f"""
Usename: {user["username"]}
User created at: {user["created_at"]}
Total tasks created: {user["total_tasks"]}
Last added task title: {user["last_added_task"]}
Task added at: {user["task_created_at"]} 

""")
    except Exception as error:
        print(f"{type(error)}: {error}")
    finally:
        await conn.close()

