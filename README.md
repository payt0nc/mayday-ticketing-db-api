# Iris

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2d03ec192d2f48a89ab68e144d28a6e8)](https://www.codacy.com/app/payton/mayday-ticketing-db-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Cooomma/mayday-ticketing-db-api&amp;utm_campaign=Badge_Grade)


## Docker

### docker cli

```bash
$> docker build . -t "iris"
$> docker run -d -e stage=PRODUCTION --env-file=env.list -p 8081:10000 --name iris iris
```

### docker-compose

```bash
$> docker-compose up
```