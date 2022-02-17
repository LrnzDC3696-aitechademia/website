import os


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ["EMAIL_USER"]
    MAIL_PASSWORD = os.environ["EMAIL_PASS"]
    MAIN_ADMIN_EMAIL = os.environ["MAIN_ADMIN_EMAIL"]
    MAIN_ADMIN_PASSWORD = os.environ["MAIN_ADMIN_PASSWORD"]
    MAIN_ADMIN_USERNAME = os.environ["MAIN_ADMIN_USERNAME"]
