# 🚀 Atelier Lambda Architecture avec Spark, Kafka et Hadoop

## 📋 Table des matières

- [Introduction](#introduction)
- [Architecture](#architecture)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [1. Batch Layer](#1-batch-layer)
  - [2. Speed Layer (Streaming)](#2-speed-layer-streaming)
  - [3. Serving Layer](#3-serving-layer)
- [Commandes utiles](#commandes-utiles)
- [Troubleshooting](#troubleshooting)

---

##  Introduction

Cet atelier implémente une **Lambda Architecture** complète avec :
- **Batch Layer** : Traitement de données historiques avec Spark et HDFS
- **Speed Layer** : Traitement temps réel avec Spark Streaming et Kafka
- **Serving Layer** : Fusion des vues Batch et Streaming

### Technologies utilisées

- **Apache Spark** : Traitement distribué (batch et streaming)
- **Apache Kafka** : Streaming de messages en temps réel
- **Apache Hadoop (HDFS)** : Stockage distribué
- **Docker** : Conteneurisation de l'infrastructure

---

##  Architecture

```
                    Lambda Architecture
                    
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Données Historiques          Données Temps Réel       │
│         ↓                              ↓                │
│   ┌──────────┐                  ┌──────────┐           │
│   │  HDFS    │                  │  Kafka   │           │
│   └────┬─────┘                  └────┬─────┘           │
│        ↓                              ↓                 │
│   ┌──────────┐                  ┌──────────┐           │
│   │  Batch   │                  │ Speed    │           │
│   │  Layer   │                  │ Layer    │           │
│   │  (Spark) │                  │ (Spark)  │           │
│   └────┬─────┘                  └────┬─────┘           │
│        ↓                              ↓                 │
│        └──────────┬───────────────────┘                │
│                   ↓                                     │
│            ┌──────────────┐                            │
│            │   Serving    │                            │
│            │    Layer     │                            │
│            └──────────────┘                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---



##  Structure du projet

```
atelier-lambda/
├── docker-compose.yml          # Configuration des conteneurs
├── config                      # Configuration Hadoop/YARN
├── README.md                   # Ce fichier
├── app/
│   ├── datasets/
│   │   └── transactions.json   # Dataset batch
│   ├── batch_job.py           # Job Spark batch
│   ├── streaming_job.py       # Job Spark streaming
│   └── serving_layer.py       # Fusion batch + streaming
└── volumes/
    └── namenode/              # Données HDFS (généré automatiquement)
```

---

##  Installation

### 1. Cloner ou créer le projet

```powershell
mkdir atelier-lambda
cd atelier-lambda
```

### 2. Créer la structure des dossiers

```powershell
mkdir app
mkdir app\datasets
mkdir volumes
```

### 3. Créer les fichiers nécessaires

#### `docker-compose.yml`

![img.png](images/img.png)

#### `config`
![img_1.png](images/img_1.png)



#### `app/datasets/transactions.json`
![img_2.png](images/img_2.png)


#### `app/batch_job.py`
![img_3.png](images/img_3.png)

#### `app/streaming_job.py`
![img_4.png](images/img_4.png)

#### `app/serving_layer.py`
![img_5.png](images/img_5.png)

### 4. Démarrer l'infrastructure

```powershell
docker-compose up -d
```
![img_6.png](images/img_6.png)

### 5. Vérifier que tous les conteneurs sont démarrés

```powershell
docker ps
```
![img_7.png](images/img_7.png)


##  Utilisation

### 1. Batch Layer

#### Exécuter le job batch

```powershell
docker exec -it spark-master /opt/spark/bin/spark-submit /app/batch_job.py
```
![img_8.png](images/img_8.png)

#### Résultat attendu
![img_9.png](images/img_9.png)


Les résultats sont sauvegardés dans `/app/batch_view`

#### Vérifier les fichiers générés

```powershell
docker exec -it spark-master ls -la /app/batch_view
```
![img_10.png](images/img_10.png)
---

### 2. Speed Layer (Streaming)

#### Étape 1 : Créer le topic Kafka

```powershell
docker exec broker /opt/kafka/bin/kafka-topics.sh --create --topic real-time-orders --bootstrap-server broker:9092 --partitions 3 --replication-factor 1
```
![img_11.png](images/img_11.png)

#### Étape 2 : Lancer le job Spark Streaming

```powershell
docker exec -it spark-master /opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 /app/streaming_job.py
```
![img_12.png](images/img_12.png)

#### Étape 3 : Dans un AUTRE terminal, lancer le producteur Kafka

```powershell
docker exec -it broker /opt/kafka/bin/kafka-console-producer.sh --topic real-time-orders --bootstrap-server broker:9092
```
![img_13.png](images/img_13.png)

#### Étape 4 : Envoyer des messages

Dans le producteur Kafka, tapez ces messages :
![img_14.png](images/img_14.png)


#### Résultat attendu

Dans le terminal du Spark Streaming, vous verrez les agrégations en temps réel :




---

### 3. Serving Layer

#### Fusionner les vues Batch et Streaming

```powershell
docker exec -it spark-master /opt/spark/bin/spark-submit /app/serving_layer.py
```
![img_15.png](images/img_15.png)

#### Résultat attendu
![img_16.png](images/img_16.png)
![img_17.png](images/img_17.png)



#### Vérifier le fichier JSON généré

```powershell
docker exec -it spark-master cat /app/serving_view.json
```
![img_18.png](images/img_18.png)
---





















