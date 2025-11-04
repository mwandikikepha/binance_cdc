**Binance CDC Data Pipeline with Monitoring**
A real-time Change Data Capture (CDC) pipeline for streaming Binance cryptocurrency market data using Debezium, Apache Kafka, PostgreSQL, and Grafana for monitoring and visualization.

**Architecture Overview**
text
Binance REST API → PostgreSQL (Source) → Debezium CDC → Kafka → JDBC Sink → PostgreSQL (Sink) → Grafana
Complete Data Flow
Data Ingestion: Binance market data collected via REST API and stored in source PostgreSQL

CDC Capture: Debezium monitors PostgreSQL changes and streams to Kafka

Event Streaming: Kafka topics store change events

Data Sinking: JDBC connector writes events to sink PostgreSQL for analytics

Monitoring & Visualization: Grafana dashboards for real-time monitoring

 Features
Real-time Data Streaming: Continuous capture of Binance market data changes

Change Data Capture: Debezium-based CDC from PostgreSQL to Kafka

Event-Driven Architecture: Kafka as the central event bus

Data Durability: Persistent storage in PostgreSQL sink

Real-time Monitoring: Grafana dashboards for pipeline metrics

Dockerized Environment: Complete containerized setup

Scalable Design: Ready for horizontal scaling

 Tech Stack
Data Processing: Python, Binance API

CDC: Debezium, Kafka Connect

Message Broker: Apache Kafka

Databases: PostgreSQL (Aiven + Local Sink)

Monitoring: Grafana, Prometheus (optional)

Containerization: Docker, Docker Compose

Orchestration: Kafka Connect REST API

 Project Structure
text
binance_project/
├── docker-compose.yml              
├── extract_load_binance.py         
├── postgres_connector_temp.json    
├── postgres_sink_connector_temp.json 
├── grafana/
│   ├── dashboards/                
│            
├── .gitignore                     
└            
 Prerequisites
Docker & Docker Compose

Python 3.8+

Aiven PostgreSQL account (for source database)

Binance API access

 Quick Start
1. Clone and Setup
bash
git clone https://github.com/mwandikikepha/binance_cdc.git
cd binance_cdc

# Create environment file from template
cp env.template .env
2. Configure Environment
Edit .env with your credentials:

env
# Source PostgreSQL (Aiven)
POSTGRES_HOST=your-aiven-host.g.aivencloud.com
POSTGRES_PORT=22644
POSTGRES_USER=avnadmin
POSTGRES_PASSWORD=your-aiven-password
POSTGRES_DB=defaultdb

# Sink PostgreSQL (Local)
SINK_POSTGRES_HOST=postgres_sink
SINK_POSTGRES_PORT=5432
SINK_POSTGRES_USER=sink_user
SINK_POSTGRES_PASSWORD=sink_pass
SINK_POSTGRES_DB=sink_db

# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_CONNECT_URL=http://localhost:8083

# Grafana
GF_SECURITY_ADMIN_PASSWORD=admin
GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
3. Start the Infrastructure
bash
# Start all services (Kafka, Connect, PostgreSQL Sink, Grafana)
docker-compose up -d
4. Deploy CDC Connectors
bash
# Deploy source and sink connectors
python deploy_connectors.py
5. Access Monitoring Dashboards
Grafana: http://localhost:3000 (admin/admin)

Kafka Connect UI: http://localhost:8083

Sink PostgreSQL: docker exec -it binance_project-postgres_sink-1 psql -U sink_user -d sink_db



Setting up Grafana Data Sources:
PostgreSQL Data Source:

Name: PostgreSQL Sink

Host: postgres_sink:5432

Database: sink_db

User: sink_user

Password: sink_pass

 Docker Compose Services
yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    # ... zookeeper config

  kafka:
    image: confluentinc/cp-kafka:latest
    # ... kafka config
    ports:
      - "9092:9092"

  kafka-connect:
    image: confluentinc/cp-kafka-connect:latest
    # ... connect config
    ports:
      - "8083:8083"

  postgres_sink:
    image: postgres:13
    # ... postgres config
    ports:
      - "5432:5432"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - ./grafana/provisioning:/etc/grafana/provisioning
      - ./grafana/dashboards:/var/lib/grafana/dashboards
    depends_on:
      - postgres_sink


Example Grafana Queries:
sql
-- Recent price changes
SELECT symbol, price, event_time 
FROM binance_schema.binance_prices 
ORDER BY event_time DESC 
LIMIT 15;



Operations
Connector Management:
bash
# Check connector status
curl http://localhost:8083/connectors/binance_postgres_connector/status

# Restart connector
curl -X POST http://localhost:8083/connectors/binance_postgres_connector/restart

# View connector config
curl http://localhost:8083/connectors/binance_postgres_connector/config

Database Maintenance:
sql
-- Monitor replication slots
SELECT * FROM pg_replication_slots;

-- Check publication status
SELECT * FROM pg_publication;

-- Monitor sink database size
SELECT pg_size_pretty(pg_database_size('sink_db'));

Troubleshooting
Common Issues:
Connector FAILED State:

Check PostgreSQL replication settings

Verify network connectivity to Aiven

Check slot and publication existence

High Kafka Lag:

Scale sink connector tasks

Optimize PostgreSQL sink performance

Check network bandwidth

Grafana Connection Issues:

Verify PostgreSQL sink is accessible

Check data source configuration

Validate user permissions

Logs Inspection:
bash
# Kafka Connect logs
docker logs binance_project-kafka-connect-1

# PostgreSQL sink logs
docker logs binance_project-postgres_sink-1

# Grafana logs
docker logs binance_project-grafana-1

 
