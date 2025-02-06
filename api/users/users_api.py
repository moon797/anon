from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.users import *
from fastapi.responses import JSONResponse

user_router = APIRouter(tags=["Управление пользователями"], prefix="/user")


class PostRequest(BaseModel):
    main_text: str
    user_id: int


@user_router.post("/post")
async def add_post(post: PostRequest):
    result = add_post_db(main_text=post.main_text, user_id=post.user_id)
    if result:
        return {"status": 0, "message": result}
    raise HTTPException(status_code=400, detail="Ошибка, попробуйте заново!")


class CommentRequest(BaseModel):
    user_id: int
    post_id: int
    main_text: str


@user_router.post("/comment")
async def add_comment(comment: CommentRequest):
    result = add_comment_db(user_id=comment.user_id, post_id=comment.post_id, main_text=comment.main_text)
    if result:
        return {"status": 0, "message": result}
    raise HTTPException(status_code=400, detail="Ошибка, убедитесь, что вы правильно ввели все данные")


class MessageRequest(BaseModel):
    user_id: int
    main_text: str
    name: str | None = "Аноним"


@user_router.post("/anon_message")
async def add_message(message: MessageRequest):
    result = add_message_db(user_id=message.user_id, main_text=message.main_text, name=message.name)
    if result:
        return {"status": 0, "message": result}
    raise HTTPException(status_code=400, detail="Ошибка, убедитесь, что вы правильно ввели все данные")


@user_router.delete("/post_delete/{post_id}")
async def remove_post(post_id: int):
    result = remove_post_db(post_id)
    if result:
        return {"status": 0, "message": "Пост успешно удален"}
    raise HTTPException(status_code=404, detail="Пост не найден")


@user_router.delete("/comment_delete/{comment_id}")
async def delete_comment(comment_id: int):
    result = delete_comment_db(comment_id)
    if result:
        return {"status": 0, "message": "Комментарий успешно удален"}
    raise HTTPException(status_code=404, detail="Комментарий не найден")


class PostChangeRequest(BaseModel):
    main_text: str


@user_router.put("/post_change/{post_id}")
async def change_post(post_id: int, post_data: PostChangeRequest):
    result = change_post_db(post_id, post_data.main_text)
    if result:
        return {"status": 0, "message": "Пост успешно изменен"}
    raise HTTPException(status_code=404, detail="Пост не найден")


class CommentChangeRequest(BaseModel):
    main_text: str


@user_router.put("/comment_change/{comment_id}")
async def change_comment(comment_id: int, comment_data: CommentChangeRequest):
    result = change_comment_db(comment_id, comment_data.main_text)
    if result:
        return {"status": 0, "message": "Комментарий успешно изменен"}
    raise HTTPException(status_code=404, detail="Комментарий не найден")
