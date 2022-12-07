#!/bin/bash

apt install ufw -y
ufw allow ssh
for i in `curl https://www.cloudflare.com/ips-v4`; do ufw allow from $i to any port http; done
for i in `curl https://www.cloudflare.com/ips-v4`; do ufw allow from $i to any port https; done
for i in `curl https://www.cloudflare.com/ips-v6`; do ufw allow from $i to any port http; done
for i in `curl https://www.cloudflare.com/ips-v6`; do ufw allow from $i to any port https; done
