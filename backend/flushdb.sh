

echo yes | python3 manage.py reset_db --router=default
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python3 manage.py makemigrations && python3 manage.py migrate