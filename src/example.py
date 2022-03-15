from pipeline import ingestion_task

external_source_configuration = {
	"type": "snowflake",
	"account": "kva82352",
	"user": "kevinunkrich",
	"password": "kCUXmoKX.Ri@JfTuJZKVY_H3",
	"warehouse": "compute_wh",
	"database": "snowflake_sample_data",
	"schema": "tpch_sf1000",
}

internal_destination_configuration = {
	"type": "postgresql",
	"host": "localhost",
	"port": 5432,
	"user": "postgres",
	"password": "postgres",
	"database": "msi_dev",
}

mpipe = ingestion_task(
	source=external_source_configuration,
	destination=internal_destination_configuration
)
mpipe.run()