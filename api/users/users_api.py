from database.users import *
from fastapi import APIRouter
from pydantic import BaseModel

user_router = APIRouter(tags=["Управление пользователями"], prefix="/user")


class PostRequest(BaseModel):
    main_text: str
    user_id: int

@user_router.post("/post/{user_id}")
async def add_post(post: PostRequest):
    user = add_post_db(main_text=post.main_text, user_id=post.user_id)
    if user:
        return {"status": 0, "message": user}
    return {"status": 1, "message": "Ошибка, попробуйте заново!"}


class CommentRequest(BaseModel):
    user_id: int
    post_id: int
    main_text: str

@user_router.post("/comment/{user_id}")
async def add_comment(comment: CommentRequest):
    user = add_comment_db(user_id=comment.user_id, post_id=comment.post_id, main_text=comment.main_text)
    if user:
        return {"status": 0, "message": user}
    return {"status": 1, "message": "Ошибка, убедитесь, что вы правильно ввели все данные"}



class MessageRequest(BaseModel):
    user_id: int
    main_text: str
    name: str | None = "Аноним"

@user_router.post("/anon_message")
async def add_message(message: MessageRequest):
    user = add_message_db(user_id=message.user_id, main_text=message.main_text, name=message.name)
    if user:
        return {"status": 0, "message": user}
    return {"status": 1, "message": "Ошибка, убедитесь, что вы правильно ввели все данные"}


@user_router.delete("/post_delete/{post_id}")
async def remove_post(post_id: int):
    post = remove_post_db(post_id)
    if post:
        return {"status": 0, "message": "Пост успешно удален"}
    return {"status": 1, "message": "Пост не найден"}

@user_router.delete("/comment_delete/{comment_id}")
async def delete_comment(comment_id: int):
    comment = delete_comment_db(comment_id)
    if comment:
        return {"status": 0, "message": "Комментарий успешно удален"}
    return {"status": 1, "message": "Комментарий не найден"}


class PostChangeRequest(BaseModel):
    main_text: str

@user_router.put("/post_change/{post_id}")
async def change_post(post_id: int, post_data: PostChangeRequest):
    post = change_post_db(post_id, post_data.main_text)
    if post:
        return {"status": 0, "message": "Пост успешно изменен"}
    return {"status": 1, "message": "Пост не найден"}

class CommentChangeRequest(BaseModel):
    main_text: str

@user_router.put("/comment_change/{comment_id}")
async def change_comment(comment_id: int, comment_data: CommentChangeRequest):
    comment = change_comment_db(comment_id, comment_data.main_text) 
    if comment:
        return {"status": 0, "message": "Комментарий успешно изменен"}
    return {"status": 1, "message": "Комментарий не найден"}

