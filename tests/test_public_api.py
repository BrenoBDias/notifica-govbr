import notifica_govbr


def test_version():
    assert notifica_govbr.__version__ == "0.1.1"


def test_public_api_exports():
    expected = {
        "FailedSend",
        "FakeNotificationAdapter",
        "HttpNotificationAdapter",
        "NotificaClient",
        "Notification",
        "NotificationPort",
        "Recipient",
        "SendResponse",
    }
    assert set(notifica_govbr.__all__) - {"__version__"} == expected


def test_public_api_names_are_importable():
    for name in notifica_govbr.__all__:
        assert hasattr(notifica_govbr, name), f"missing public name: {name}"


def test_readme_example_imports():
    """O exemplo do README precisa ser importável exatamente como está."""
    from notifica_govbr import (  # noqa: F401
        HttpNotificationAdapter,
        NotificaClient,
        Notification,
        Recipient,
    )
