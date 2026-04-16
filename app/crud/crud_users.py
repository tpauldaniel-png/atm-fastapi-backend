from app import models, utils
from fastapi import HTTPException, status, Response


def create_user(user_data,db):
    try:
        user_dict = user_data.model_dump()
        user_dict["password"] = utils.hash_password(user_data.password)


        new_user = models.User(**user_dict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    except Exception:
        db.rollback()
        raise 
    
    


def get_all_users(db):
    try:

        users = db.query(models.User).all()

        return users

    except Exception:
        raise 



def get_user(user_id, db):
    
    user = db.query(models.User).filter(models.User.user_id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    return user
    




def update_user(user_id, user, db):

    try:

        user_query = db.query(models.User).filter(models.User.user_id == user_id)

        user_to_update = user_query.first()


        if user_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with {user_id} does not exist")
        

        user_dict = user.model_dump()
        user_dict["password"] = utils.hash_password(user.password)

        user_query.update(user_dict, synchronize_session=False)


        db.commit()

        return user_query.first()
    
    except Exception:
        db.rollback()
        raise







def delete_user(user_id, db):

    try:

        query = db.query(models.User).filter(models.User.user_id == user_id)

        if query.first() == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {user_id} does not exist")
        
        query.delete(synchronize_session=False)

        db.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except Exception:
        db.rollback()
        raise




