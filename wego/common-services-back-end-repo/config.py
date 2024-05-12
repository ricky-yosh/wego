# common-services-back-end-repo

# mySQL: Password for the loginservice_user user in the userdb database
DATABASE_PASSWORD_MYSQL = "cabinetPortraitFaithSwitch"
# run migrations it defaults to mysql
# python manage.py migrate

# mongodb: Password for the fleet_admin use in the fleetdb database
DATABASE_PASSWORD_MONGO = "TreeKickDoorGreen"
# run migrations you have to specify mongodb since it is not the default
# python manage.py migrate --database=mongodb

# SECRET_KEY: Crucial for cryptographic signing, used in Django for security features like session management, CSRF protection, and password reset tokens.
SECRET_KEY = "django-insecure-ow$9=g3l^d(&#p$lmc$b&1ns**6=@ii9bop16_)pk9vc5lwotq"

# This will be turned off in the cloud
DEBUG = True