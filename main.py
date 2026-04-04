from fastapi import FastAPI
from contextlib import asynccontextmanager
import aiosqlite

DATABASE_NAME = 'test.db'

async def lifespan(app:FastAPI):
    
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("""
                CREATE TABLE IF NOT EXISTS tasks(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   task_name TEXT
                   );

""")
        await db.commit()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/get_tasks")
async def get_tasks():
    async with aiosqlite.connect(DATABASE_NAME) as db:
      
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM tasks")
        rows = await cursor.fetchall()
        tasks = [dict(row) for row in rows]
        
    return {"Tasks":tasks}

@app.post("/make_task")
async def make_task(task:str):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("INSERT INTO tasks (task_name) VALUES (?)",(task,))
        await db.commit()
        return {"message":f" task added succefully {task}"}

@app.put("/update_task/{task_id}")
async def update_task(task_id:int,update:str):
    async with aiosqlite.connect(DATABASE_NAME) as db :
        await db.execute("UPDATE tasks SET task_name = ? WHERE id = ? " ,(update,task_id))
        await db.commit()
        return {"message":f" task updated succefully {update}"}
    return {"message":"something went wrong"}
    
@app.post("get_task_by_id/{task_id}")
async def get_task(task_id:int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        cursor = await db.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
        row = await cursor.fetchall()
        
        return {"message":f"task: {row[1]}"}

@app.delete("/delte_task")
async def delete_task(task_id:int):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
        await db.commit()
        return {"message":"task deleted succefully"} 
    

# < ------------- NEXT TIME CREATE MORE ENDPOINTS TO PRACTICE SQL QUERIES --------------- >
# < ------------- NEXT TIME CREATE MORE ENDPOINTS TO PRACTICE SQL QUERIES --------------- >
# < ------------- NEXT TIME CREATE MORE ENDPOINTS TO PRACTICE SQL QUERIES --------------- >