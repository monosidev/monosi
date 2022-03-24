from ingestion.transformers.base import Transformer

class AnomalyTransformer(Transformer):
    @classmethod
    def _transform(cls, zscores):
        sensitivity = 2.5

        anomalies = []
        for zscore in zscores:
            if abs(zscore['zscore']) > sensitivity:
                anomalies.append(zscore)

        return zscores

    @classmethod
    def _original_schema(cls):
        return {
            "type": "object",
            "properties": {
            },
            "secret": [ ],
        }

    @classmethod
    def _normalized_schema(cls):
        return {
            "type": "object",
            "properties": {
            },
            "secret": [ ],
        }

