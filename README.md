# Iris


### Docker run

```
docker run \
--name iris \
-p 10000:10000 \
-e host= \
-e username= \
-e password= \
-e db_name= \
-e fluentd_host= \
-e redis_host= \
cooomma/iris:2.0
```