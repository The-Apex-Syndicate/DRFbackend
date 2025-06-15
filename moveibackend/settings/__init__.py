import os
env = os.getenv("DJANGO_ENV", "local")

if env == "prod":
    from .prod import *
else:
    from .local import *