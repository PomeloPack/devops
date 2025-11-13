kdyz se chce zapnout apliakce lokalne, vzdy ae musi zapnout kontejner z dockeru pro DB

docker run --name weather_local_db \
  -e POSTGRES_USER=pomelo \
  -e POSTGRES_PASSWORD=pomeloheslo \
  -e POSTGRES_DB=weather_app \
  -p 5432:5432 \
  -d postgres:16