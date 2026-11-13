"""Paquet installable de classification de sentiment."""

from importlib.metadata import version

__version__ = version("sentiment-app")

from sentiment_app.predict import predict

__all__ = ["__version__", "predict"]
