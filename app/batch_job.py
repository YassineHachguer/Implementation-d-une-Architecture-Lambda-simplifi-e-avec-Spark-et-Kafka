from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as sum_

spark = SparkSession.builder.appName("batch-job").getOrCreate()

df = spark.read.json("/app/datasets/transactions.json")

# Agrégation : somme par client
agg = df.groupBy("customer").agg(sum_("amount").alias("total_amount"))

agg.show()

# Sauvegarde comme "batch view"
agg.write.mode("overwrite").json("/app/batch_view")

spark.stop()
