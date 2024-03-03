import environ

env = environ.Env(
    SECRET_KEY=(str, 'secret_key'),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(str, '*'),
)