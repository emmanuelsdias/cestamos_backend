import uvicorn
from fastapi import FastAPI
from app.controllers import user, recipe, invitation, friendship, shop_list, item, user_list

import alembic.config

app = FastAPI()

app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(recipe.router, prefix="/recipe", tags=["Recipe"])
app.include_router(invitation.router, prefix="/invitation", tags=["Invitation"])
app.include_router(friendship.router, prefix="/friendship", tags=["Friendship"])
app.include_router(shop_list.router, prefix="/shop_list", tags=["Shop List"])
app.include_router(item.router, prefix="/item", tags=["Item"])
app.include_router(user_list.router, prefix="/user_list", tags=["User List"])


alembic_args = ["--raiseerr", "-c", "app/alembic.ini", "upgrade", "head"]

if __name__ == "__main__":
    alembic.config.main(argv=alembic_args)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)