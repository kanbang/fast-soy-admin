'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2024-07-01 20:32:45
LastEditors: zhai
LastEditTime: 2024-07-01 21:45:18
'''
import aiosqlite


async def copy_table_data(tb: str):
    async with aiosqlite.connect("db_system2.sqlite3") as source_db:
        async with source_db.execute(f"SELECT * FROM {tb};") as cursor:
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]

    async with aiosqlite.connect("db_system.sqlite3") as target_db:
        await target_db.execute(
            f"DELETE FROM {tb};"
        )  # Ensure target table is empty
        if rows:
            # Quote column names to avoid conflicts with reserved keywords
            quoted_columns = [f'"{col}"' for col in columns]
            placeholders = ", ".join(["?"] * len(columns))
            insert_sql = f"INSERT INTO {tb} ({', '.join(quoted_columns)}) VALUES ({placeholders})"
            await target_db.executemany(insert_sql, rows)
        await target_db.commit()

async def main():
    await copy_table_data("menus")
    await copy_table_data("roles")
    await copy_table_data("users_roles")
    await copy_table_data("roles_menus")
    await copy_table_data("mfst")
    await copy_table_data("mfs")
    await copy_table_data("equipment")

import asyncio

asyncio.run(main())
