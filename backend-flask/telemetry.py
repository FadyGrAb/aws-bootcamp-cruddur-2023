import os

# Honeycomb imports
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# AWS X-Ray imports
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# CloudWatch logs imports
import watchtower
import logging
from time import strftime

# Rollbar imports
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

class Telemetry:
    def __init__(self, app, honeycomb_active=True, cloudwatch_active=True, xray_active=True,
                    rollbar_active=True, rollbar_payload_handler=None, disable=False):
        """
        A class to organize app telemetry.
        You can select indevidual telemetry flags or ignore the flags and
        disable the telemetry alltogether by setting "disable" to True.
        """
        if not disable:
            if honeycomb_active:
                # Initialize Honeycomb
                provider = TracerProvider()
                processor = BatchSpanProcessor(OTLPSpanExporter())
                provider.add_span_processor(processor)
                trace.set_tracer_provider(provider)
                

                FlaskInstrumentor().instrument_app(app)
                RequestsInstrumentor().instrument()

                self._honeycomb_trace = trace
            else:
                self._honeycomb_trace = None

            if cloudwatch_active:
                # Configuring Logger to Use CloudWatch
                LOGGER = logging.getLogger(__name__)
                LOGGER.setLevel(logging.DEBUG)
                console_handler = logging.StreamHandler()
                cw_handler = watchtower.CloudWatchLogHandler('cruddur')
                LOGGER.addHandler(console_handler)
                LOGGER.addHandler(cw_handler)
                self._cloudwatch_logger = LOGGER
            else:
                self._cloudwatch_logger = None

            if xray_active:
                # Initialize X-ray
                xray_url = os.getenv("AWS_XRAY_URL")
                xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
                XRayMiddleware(app, xray_recorder)

                self._xray_recorder = xray_recorder
            else:
                self._xray_recorder = None

            if rollbar_active:
                # Init Rollbar
                rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
                """init rollbar module"""
                rollbar.init(
                    # access token
                    rollbar_access_token,
                    # environment name
                    'production',
                    # server root directory, makes tracebacks prettier
                    root=os.path.dirname(os.path.realpath(__file__)),
                    # flask already sets up logging
                    allow_logging_basic_config=False)

                if rollbar_payload_handler:
                    rollbar.events.add_payload_handler(rollbar_payload_handler)

                # send exceptions from `app` to rollbar, using flask's signal system.
                got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

                self._rollbar_logger = rollbar
            else:
                self._rollbar_logger = None

        else:
            self._honeycomb_trace = self._cloudwatch_logger = self._xray_recorder = self._rollbar_logger = None

    def rollbar_report_message(self, message, message_type):
        if self._rollbar_logger:
            self._rollbar_logger.report_message(message, message_type)

    def cloudwatch_log_error(self, message):
        if self._cloudwatch_logger:
            self._cloudwatch_logger.error(message)

    def honeycomb_get_tracer(self, tracer_name):
        if self._honeycomb_trace:
            return self._honeycomb_trace.get_tracer(tracer_name)


    @property
    def honeycomb_trace(self):
        if self._honeycomb_trace:
            return self._honeycomb_trace
        else:
            print("Honeycomb is disabled")

    @property
    def cloudwatch_logger(self):
        if self._cloudwatch_logger:
            return self._cloudwatch_logger
        else:
            print("Honeycomb is disabled")

    @property
    def xray_recorder(self):
        if self._xray_recorder:
            return self._xray_recorder
        else:
            print("Honeycomb is disabled")

    # @property
    # def rollbar_logger(self):
    #     if self._rollbar_logger:
    #         return self._rollbar_logger
    #     else:
    #         print("Honeycomb is disabled")