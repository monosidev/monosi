from ingestion.transformers.base import Transformer

class AnomalyTransformer(Transformer):
    @classmethod
    def _transform(cls, zscores):
        return list(filter(lambda x: x['error'] == True, zscores))

    @classmethod
    def _original_schema(cls):
        return {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["error"]
          },
          "minItems": 1
        }

    @classmethod
    def _normalized_schema(cls):
        return {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
                "error": { 
                    "type": "boolean",
                    "const": True
                },
            },
            "required": ["error"]
          },
          "minItems": 1
        }
