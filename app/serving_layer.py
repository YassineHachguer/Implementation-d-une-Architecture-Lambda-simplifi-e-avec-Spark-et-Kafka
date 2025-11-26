import json
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("serving-layer").getOrCreate()

# Lire batch
batch = spark.read.json("/app/batch_view")

print("=== Batch View ===")
batch.show()

# Simuler un résultat streaming
streaming_example = {
    "Ali": 80,
    "Sara": 40,
    "Mounir": 200
}

# Fusion Batch + Streaming
final_view = {}

for row in batch.collect():
    final_view[row["customer"]] = row["total_amount"]

for k, v in streaming_example.items():
    final_view[k] = final_view.get(k, 0) + v

print("\n=== Serving View ===")
print(final_view)

# Sauvegarde dans un fichier JSON
with open("/app/serving_view.json", "w") as f:
    json.dump(final_view, f, indent=4)

spark.stop()
