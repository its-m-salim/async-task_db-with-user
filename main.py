from connection import*
from service import *
import asyncio

is_login = None
dec = '=' * 10

async def main():
    global is_login
    await create_table()
    await create_user()
    while True:
        if is_login == None:
            print(f"\n{dec} AUTHENTICATION {dec}")
            try:
                n = int(input("\n1)Registration\n2)Login\n3)Search for user\n0)Exit\nChouse one: "))
            except ValueError:
                print("Please choose from options below!\n")
                continue
            match n:
                case 1:
                    name = input("Enter your name: ")
                    ps = input("Enter password: ")
                    await registration(name, ps)
                case 2:
                    name = input("Enter your name: ")
                    ps = input("Enter password: ")
                    if await login(name, ps):
                        is_login =  await login(name, ps)
                        print("success")
                    else:
                        print("Wrong password or username")
                        continue
                case 3:
                    name = input("Enter username to get info: ")
                    found = await get_user(name)
                    if found:
                        print(f"\n{dec} User Found! {dec}")
                        print(f"Useraname: {found[0]["username"]}\nCreated at: {found[0]["created_at"]}")
                    else:
                        print("User not found")
                case 0:
                    print("Good bye!")
                    break
        else:
            while True:
                print(f"{dec} LOGIN AS '{is_login[1]}' {dec}")
                n = int(input("1)Create task\n2)Get task\n3)Update task\n4)Show Profile\n0)Logout\nChoose one: "))
                match n:
                    case 1:
                        await create_task(is_login[0],input("Tile: "), input("Description: "), input("Dueration date:"))
                    case 2:
                        await get_task(is_login[0])
                    case 3:
                        try:
                            t_id = int(input("Enter task id: "))
                            t = input("Enter new title: ")
                            d = input("Enter new description: ")
                            dd = input("Enter new dueration date: ")
                            await update_task(t_id, t, d, dd, is_login[0])
                        except ValueError:
                            print("Id must be an integer!")
                            continue
                    case 4:
                        print(f"{dec} Your Profile {dec}")
                        await show_profile(is_login[0])
                        while True:
                            try:
                                st = int(input("1)Change password\n2)Delete user"))
                            except ValueError:
                                print("Please choose from options below")
                            match st:
                                case 1:
                                    # pss = input(f"Input current password for user '{is_login[1]}'")
                                    # if await check_user(pss) == None:
                                    #     print("No")
                                    # else:
                                    #     print("Yes")
                                    print("ON PROGGRESS")
                    case 0:
                        print(f"\n{dec} LOGOUT! {dec}\n")
                        is_login = None
                        break
                    case _:
                        print("Invalid input")

               




if __name__ == "__main__":
    asyncio.run(main())