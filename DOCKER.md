# Docker Guide for RealEstimate

This document provides detailed instructions for using Docker with the RealEstimate application.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system

## Quick Start

The simplest way to get started is with Docker Compose:

```bash
docker-compose up
```

This will:
1. Build the Docker image if it doesn't exist
2. Start the container
3. Map port 8000 from the container to your host
4. Mount your local directory to the container for live code changes

## Manual Docker Commands

### Building the Image

To build the Docker image:

```bash
docker build -t realestimate .
```

### Running the Container

To run the container:

```bash
docker run -p 8000:8000 realestimate
```

To run in CLI mode:

```bash
docker run realestimate python main.py --cli
```

### Development Mode

For development with hot reloading:

```bash
docker run -p 8000:8000 -v $(pwd):/app realestimate
```

## Configuration

You can customize the application by editing the `.env` file. Available options include:

- `HOST`: The host address to bind to (default: 0.0.0.0)
- `PORT`: The port to run the application on (default: 8000)

## Health Checks

The Docker container includes health checks that:

- Run every 30 seconds
- Check if the application is responding on port 8000
- Allow 5 seconds for initial startup
- Retry 3 times before considering the container unhealthy

## Troubleshooting

### Container Not Starting

If the container fails to start, check the logs:

```bash
docker-compose logs
```

### Application Not Accessible

If you can't access the application, ensure:

1. The container is running: `docker ps`
2. The port mapping is correct: `docker-compose ps`
3. No firewall is blocking port 8000

### Modifying the Container

To enter the running container:

```bash
docker exec -it $(docker ps -q -f name=realestimate) bash
```

## Best Practices

1. Always use the `.env` file for configuration
2. Use Docker Compose for development
3. Rebuild the image when dependencies change
4. Use separate volumes for persistent data when deploying to production