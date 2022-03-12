from .base import Destination, DestinationConfiguration

class S3DestinationConfiguration(DestinationConfiguration):
	@classmethod
	def validate(cls, configuration):
        return {
            "type": "object",
            "properties": {
                "bucket": { "type": "string" },
                "region": { "type": "string" },
                "aws_access_key": { "type": "string" },
                "aws_secret_key": { "type": "string" },
            },
            "secret": [ "aws_secret_key" ],
        }

    def connection_string(self) -> str:
    	raise NotImplementedError

	@property
	def type(self):
		raise "s3"

class S3Destination(Destination):
	def _push(self):
		raise NotImplementedError
