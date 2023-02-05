from loader import dp
from .admin import AdminMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(AdminMiddleware())

