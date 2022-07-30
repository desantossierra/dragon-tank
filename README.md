# dragon-tank

## installation

### static IP address 
I'm going to configure Ethernet as static IP address. This way Dragon can be wired to my laptop 

`sudo nano /etc/dhcpcd.conf`

```
interface eth0
static ip_address=10.42.0.10/24
static routers=10.42.0.1
static domain_name_servers=10.42.0.1 8.8.8.8 
```

### basic configuration 

#### avoid password for ssh connections
```
ssh-keygen
ssh-copy-id -i ~/.ssh/id_rsa.pub remote_host
```


icons
<a href="https://www.flaticon.es/iconos-gratis/robot" title="robot iconos">Robot iconos creados por Freepik - Flaticon</a>
<a href="https://www.flaticon.es/iconos-gratis/robot" title="robot iconos">Robot iconos creados por Flat Icons - Flaticon</a>
