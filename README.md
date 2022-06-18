# Levantar contenedores

docker-compose up -d

# Reiniciar contenedores

docker-compose restart

# Acceder a la shell de rasa

docker-compose exec nlu rasa shell

# Ver url de ngrok

docker-compose exec ngrok curl http://ngrok:4040/api/tunnels  

Hay que mirar el campo public_url
