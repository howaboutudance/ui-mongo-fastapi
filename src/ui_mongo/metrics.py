from enum import Enum
import functools
import prometheus_client
from ui_mongo import config


class EntryTransactionType(Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    update = "UPDATE"
    delete = "DELETE"


UI_ENTRY_CREATED = prometheus_client.Counter(
    f"{config.settings.app_name}_entry_transactions",
    "number of transaction on entries",
    labelnames=["app_name", "transaction_type", "function_name"]
)


def inc_entry_transaction(transaction_type: EntryTransactionType,
                          app: str = config.settings.app_name,
                          function_name: str = "unkown"):
    UI_ENTRY_CREATED.labels(app, str(transaction_type), function_name).inc()


# decorator for routes
def transaction_metric(transaction_type: EntryTransactionType):
    def metric_decorator(func):
        inc_entry_transaction(
            transaction_type,
            config.settings.app_name,
            str(func.__name__))

        @functools.wraps(func)
        def wrap_transaction_function(*args, **kwargs):
            return func(*args, **kwargs)
        return wrap_transaction_function
    return metric_decorator
