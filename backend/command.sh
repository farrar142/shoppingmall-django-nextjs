
rm -rf static
echo yes | python3 manage.py collectstatic
uvicorn base.asgi:application --reload --host 0.0.0.0 --port $1
# python3 manage.py runserver 0.0.0.0:$1 
# python3 manage.py runserver 0.0.0.0:$1