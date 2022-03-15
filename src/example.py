from pipeline import ingestion_task

external_source_configuration = {
	"type": "",
	"account": "",
	"user": "",
	"password": "",
	"warehouse": "",
	"database": "",
	"schema": "",
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