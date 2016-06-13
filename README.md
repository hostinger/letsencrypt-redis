### Authenticate and install key/cert pair into Redis hosts (authentication reverse proxy):

```
certbot run -d example.com -a letsencrypt-redis:auth --letsencrypt-redis:auth-redis-hosts 192.168.1.1,192.168.1.2 -i letsencrypt-redis:installer --letsencrypt-redis:installer-redis-hosts 192.168.1.1,192.168.1.2 -n --force-renewal
```

### Install key/cert pair into local Redis

```
certbot run -d a.donatas.net -a standalone -i letsencrypt-redis:installer -n --force-renewal
```
