# SA_P_VJ
# Sistema de Compras en Línea - Microservicios con Docker y PostgreSQL

Este proyecto representa la migración de un sistema monolítico de compras en línea a una arquitectura basada en microservicios.

## Servicios implementados

- `gateway`: Punto de entrada al sistema
- `servicio_productos`: Gestión de productos
- `servicio_pedidos`: Gestión de pedidos
- `servicio_pagos`: Gestión de pagos
- Bases de datos PostgreSQL para cada microservicio

## Requisitos

- Docker
- Docker Compose

## Despliegue local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/online-shopping-system.git
cd online-shopping-system
```

## Configuración .env
DB_HOST=bd_servicio
DB_USER=postgres
DB_PASSWORD=admin
DB_NAME=ordenar

## construccion y levantamiento de los contenedores
docker-compose up --build

## prueba de servicios
```bash
## gateway
http://localhost:80 

http://localhost:3001/productos

http://localhost:3002/pedidos

http://localhost:3003/pagos
```


## Detener servicios 
docker-compose down
### eliminar volumenes 
docker-compose down -v

## reconstrucción servicios 
docker-compose build product_services
