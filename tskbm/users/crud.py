from tskbm.users.models import CreateUser


def create_user(user_in: CreateUser):
    user = user_in.model_dump()
    return {"operation": "success", "user": user}
