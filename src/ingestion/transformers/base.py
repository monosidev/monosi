import logging
from jsonschema import validate
import abc
import json
import pyjq

class Transformer:
    @classmethod
    def match(cls, input, schema):
        try:
            validate(instance=input, schema=schema)
            return True
        except Exception as e:
            logging.info(e)
            return False

    @abc.abstractclassmethod
    def _original_schema(cls):
        # Schema to match against on input
        raise NotImplementedError("Transformer: Original Schema")

    @abc.abstractclassmethod
    def _normalized_schema(cls):
        # Schema to match against on output
        raise NotImplementedError("Transformer: Nomralized Schema")

    @abc.abstractclassmethod
    def _transform(cls, input):
        # Actual transform logic
        raise NotImplementedError

    @classmethod
    def _after_transform(cls, input):
        return input

    @classmethod
    def transform(cls, incoming_json):
        if cls.match(incoming_json, cls._original_schema()) == False:
            raise Exception("Error: Can't transform, incoming JSON doesn't match schema.\n\nSchema: {}\n\nInput: {}", cls._original_schema(), incoming_json)

        outgoing_json = cls._transform(incoming_json)
        outgoing_json = cls._after_transform(outgoing_json)

        # TODO: Check transform worked properly
        # if cls.match(outgoing_json, cls._normalized_schema()) == False:
        #     raise Exception("Error: Can't transform, outgoing JSON doesn't match schema.\n\nSchema: {}\n\nOutgoing: {}", cls._normalized_schema(), outgoing_json)

        return outgoing_json

class JSONTransformer(Transformer):
    @abc.abstractclassmethod
    def _mapped_schema(cls):
        raise NotImplementedError

    @classmethod
    def _transform(cls, input):
        json_input = json.loads(json.dumps(input, indent=4, sort_keys=True, default=str))
        transformed_results = pyjq.all(
            cls._mapped_schema(),
            json_input,
        )
        return transformed_results

