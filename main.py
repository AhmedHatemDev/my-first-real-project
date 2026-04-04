from fastapi import FastAPI , HTTPException ,Depends
from typing import Annotated
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

async def get_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        db.row_factory = aiosqlite.Row
        yield db

DB = Annotated[aiosqlite.Connection,Depends(get_db)]

@app.get("/get_tasks")
async def get_tasks(db:DB):
    cursor = await db.execute("SELECT * FROM tasks")
    rows = await cursor.fetchall()
    tasks = [dict(row) for row in rows]
    return {"Tasks":tasks}

@app.post("/make_task")
async def make_task(task:str,db:DB):
    await db.execute("INSERT INTO tasks (task_name) VALUES (?)",(task,))
    await db.commit()
    return {"message":f" task added succefully {task}"}

@app.put("/update_task/{task_id}")
async def update_task(task_id:int,update:str,db:DB):
    cursor = await db.execute("UPDATE tasks SET task_name = ? WHERE id = ? " ,(update,task_id))
    await db.commit()
    if cursor.rowcount == 0 :
        raise HTTPException(status_code=404,detail="task not found")
    return {"message":f" task updated succefully {update}"}
    
@app.get("/get_task_by_id/{task_id}")
async def get_task(task_id:int,db:DB):
    cursor = await db.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
    row = await cursor.fetchone()
    if row:
        return {"task":row["task_name"]}
    raise HTTPException(status_code=404,detail="task not found")
        

@app.delete("/delete_task")
async def delete_task(task_id:int,db:DB):
    await db.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
    await db.commit()
    return {"message":"task deleted succefully"} 