from datetime import timedelta


JWT_SECRET_KEY = "dev_secret_change_later"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(hours=8)