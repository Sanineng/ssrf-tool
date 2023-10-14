# ssrf-tool

```bash
docker-compose up

docker exec -it ssrf-tool bash -i -c "LD_PRELOAD=/app/hook.so python3 app.py"
docker exec -it -w /develope/ssrf ssrf-tool bash -i -c "python3 app.py -f packet.out -p"

```
