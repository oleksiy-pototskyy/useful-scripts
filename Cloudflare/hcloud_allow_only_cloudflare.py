#!/usr/bin/python3
#
# This script allows to update Cloudflare IP addresses in Hetzner Firewalls
# It can help you to put your servers behind of Cloudflare and prevent any other traffic
#

import requests
import json

firewall_name = "web-restricted"        # Firewall rule which should be updated
hcloud_api_token = ""                   # Hetzner Cloud API Token

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + hcloud_api_token
}

# Identify firewall
firewall_id = 0
response = requests.get("https://api.hetzner.cloud/v1/firewalls", headers=headers)
if (response.status_code != 200):
    print("Can't obtain a list of firewall rules")
    quit()
json = response.json()
for item in json["firewalls"]:
    if item["name"] == firewall_name:
        firewall_id = item["id"]
if firewall_id == 0:
    print("Can't find firewall rule")
    quit()

# Create new version of firewall rules
cloudflare_ipv4_url = "https://www.cloudflare.com/ips-v4"
cloudflare_ipv6_url = "https://www.cloudflare.com/ips-v6"

cloudflare_ip_list = []

response = requests.get(cloudflare_ipv4_url)
if response.status_code != 200:
    print("Can't download of Cloudflare IPv4 list")
    quit()
for item in response.text.split("\n"):
    cloudflare_ip_list.append(item)

response = requests.get(cloudflare_ipv6_url)
if response.status_code != 200:
    print("Can't download of Cloudflare IPv6 list")
    quit()
for item in response.text.split("\n"):
    cloudflare_ip_list.append(item)

firewall_rules = {"rules": [
    {"direction": "in", "protocol": "tcp", "port": "443", "source_ips": cloudflare_ip_list, "destination_ips": [], "description": "Cloudflare"}
]}

# Apply new firewall rules
response = requests.post("https://api.hetzner.cloud/v1/firewalls/" + str(firewall_id) + "/actions/set_rules", headers=headers, json=firewall_rules)
print(response.status_code)
print(response.text)
