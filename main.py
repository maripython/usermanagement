from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from pymongo.errors import PyMongoError
from datetime import datetime
from database import Users
from models import UserSchema, UserUpdate

app = FastAPI()


@app.get("/")
async def check_server():
    return {'status': 'success'}


@app.post("/users", status_code=201)
async def create_user(user: UserSchema):
    try:
        existing_user = Users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="User with this email already exists")

        user_dict = user.dict()
        user_dict["dob"] = user.dob.isoformat()
        result = Users.insert_one(user_dict)
        return {"id": str(result.inserted_id), "message": "User created successfully"}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")


@app.get("/users/{user_id}", status_code=200)
async def get_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        user = Users.find_one({"_id": ObjectId(user_id)})
        user['_id'] = str(user['_id'])
        del user['added_on']
        del user['updated_on']
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {'status': 'success', 'data': user}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")


@app.put("/users/{user_id}", status_code=200)
async def update_user(user_id: str, payload: UserUpdate):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        user = Users.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = payload.dict(exclude_unset=True)
        if "dob" in update_data:
            update_data["dob"] = update_data["dob"].isoformat()
            update_data["updated_on"] = datetime.now()

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        Users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        return {"status": "success", "message": "User updated successfully"}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")


@app.delete("/users/{user_id}", status_code=200)
async def delete_user(user_id: str):
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        deleted_user = Users.find_one_and_delete({"_id": ObjectId(user_id)})
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
