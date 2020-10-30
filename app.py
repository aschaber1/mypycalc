import json
import sys
from jaeger_client import Config
import logging

from flask import Flask, render_template, request

api = Flask('MyPyCalc')

@api.route('/', methods=['GET'])
def get_mypycalc():
    return render_template('form.html')

@api.route('/', methods=['POST'])
def post_mypycalc():
    with tracer.start_span('PostSpan') as span:
        a = int(request.form['a'])
        b = int(request.form['b'])
        result = a-b
        span.log_kv({'event': 'post', 'result': result})
        result_str = str(result)
        return render_template('form.html') + result_str, 201

if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='MyPyCalc',
        validate=True,
    )
    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()

    with tracer.start_span('TestSpan') as span:
        span.log_kv({'event': 'test message', 'life': 42})

        with tracer.start_span('ChildSpan', child_of=span) as child_span:
            child_span.log_kv({'event': 'down below'})

    api.run(host='0.0.0.0', port=8080)
