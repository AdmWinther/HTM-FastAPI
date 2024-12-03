import os
from tabnanny import verbose

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
        verbose: bool = os.getenv("VERBOSE") == "True"
        try:
            await db.execute(query)
            await db.commit()
            if verbose: print ("Operation successful_Database")
            return True
        except Exception as e:
            if verbose: print ("Operation failed_Database")
            print(e)
            return False

async def execute_transaction(queries):
    async with aiosqlite.connect("test.db") as db:
        verbose: bool = os.getenv("VERBOSE") == "True"
        try:
            async with db.execute("BEGIN"):
                for query in queries:
                    if verbose: print(query)
                    await db.execute(query)
            await db.commit()
            if verbose: print("All operations successful - Database")
            return True
        except aiosqlite.Error as e:
            await db.rollback()
            if verbose:print("Operation failed - Database")
            print(e)
            return False

async def getData(query: str):
    async with aiosqlite.connect("test.db") as db:
        async with db.execute(query) as cursor:
            data = await cursor.fetchall()
            return data