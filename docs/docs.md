# Docs

- Comando para rodar 
```
pdm dev
```

- Comando para rodar no IP
```bash
pdm dev "seu_ip:8000"
```

- Comando para rodar o celery
```bash
pdm run celery -A config.celery worker --loglevel=info
```

- Comando para ver status do rabbitmq
```bash
sudo systemctl status rabbitmq-server
```

- Comando para setar permissoes de algum usuario
```bash
sudo rabbitmqctl set_permissions -p anthony anthony ".*" ".*" ".*"
```

- Comando arrumar ssl
```bash
openssl s_client -connect localhost:5671
```

- Reiniciar rabbitmq
```bash
sudo systemctl restart rabbitmq-server
```
- Rota para atribuir driver e veiculo a um pedido

```bash
orders/<int:order_id>/assign/<int:vehicle_id>/<int:driver_id>/
```

- Rota para verificar se tem um pedido atribuido a um motorista:
```bash
 /orders/check-driver/int/
```

- Rota para mudar status do pedido: 
```
orders/<int:order_id>/status/<int:status_number>/
```

- Rota para finalizar um pedido:
```
order/<int:order_id>/unassign/
```