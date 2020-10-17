sudo docker kill $(sudo docker ps -q)
sudo docker run -d -p 80:5000 -e SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:@@{DB_PASSWORD}@@@@@{Postgres.address}@@:5432/@@{DB_NAME}@@" hexadtech/demo-app:uat
