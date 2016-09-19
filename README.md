Welcome Page for Tech Department
===

This is a sign-up form for new comers. Users will be notified about relative events by email and SMS. Messaging service is provided by AliDayu.

###Prerequisite

This project runs on Python 3 with following components:

1. django (1.10.1 tested)
2. django-crispy-forms (1.6.0 tested)
3. django-simple-captcha (0.5.2 tested)
4. pillow (3.3.1 tested)

You can install these via `pip`.

###Development

1. `cp TechDepartment/secure_settings.sample.py TechDepartment/secure_settings.py`
2. Change the values in `secure_settings.py` as needed
3. Create a new database by `python3 manage.py migrate`
4. Change `DEBUG` to `False` in `settings.py` and set `ALLOWED_HOSTS` to server's host name (xxx.xxx.com)
5. `python3 manage.py collectstatic`
6. If there is nothing wrong in last step, overwrite static/ with staticfiles/
7. `python3 manage.py createsuperuser`
8. Deploy with uWSGI and nginx. Remember to use `--enable-threads` for uWSGI
9. Set up redirection on nginx: / -> /welcome
10. Log in at `/admin` and create groups

