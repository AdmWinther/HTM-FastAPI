import os
from dotenv import load_dotenv

import databases
import aiosqlite
from sqlalchemy import result_tuple

load_dotenv()
databaseURL = str(os.getenv("DATABASE_URL"))
database = databases.Database("sqlite:///./test.db")

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
async def execute_query(query: str):
    async with aiosqlite.connect("test.db") as db:
        # Set the row factory to aiosqlite.Row
        db.row_factory = aiosqlite.Row
        async with db.execute(query) as cursor:
            data = await cursor.fetchall()
            results = []
            for row in data:
                results.append(dict(row))
            return results

async def insertIntoTable(query: str):
    async with aiosqlite.connect("test.db") as db:
        try:
            await db.execute(query)
            await db.commit()
            print ("Operation successful_Database")
            return True
        except Exception as e:
            print ("Operation failed_Database")
            print(e)
            return False

async def execute_transaction(queries):
    async with aiosqlite.connect("test.db") as db:
        try:
            async with db.execute("BEGIN"):
                for query in queries:
                    print(query)
                    await db.execute(query)
            await db.commit()
            print("All operations successful - Database")
            return True
        except aiosqlite.Error as e:
            await db.rollback()
            print("Operation failed - Database")
            print(e)
            return False