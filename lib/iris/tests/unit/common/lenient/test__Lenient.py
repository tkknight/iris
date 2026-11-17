# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for the :class:`iris.common.lenient._Lenient`."""

from collections.abc import Iterable

import pytest

from iris.common.lenient import (
    _LENIENT_ENABLE_DEFAULT,
    _LENIENT_PROTECTED,
    _Lenient,
    _qualname,
)


@pytest.fixture
def lenient():  # noqa: D103
    return _Lenient()


class Test___init__:
    """Test   init  ."""
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.expected = dict(active=None, enable=_LENIENT_ENABLE_DEFAULT)

    def test_default(self, lenient):  # noqa: D102
        assert lenient.__dict__ == self.expected

    def test_args_service_str(self):  # noqa: D102
        service = "service1"
        lenient = _Lenient(service)
        self.expected.update(dict(service1=True))
        assert lenient.__dict__ == self.expected

    def test_args_services_str(self):  # noqa: D102
        services = ("service1", "service2")
        lenient = _Lenient(*services)
        self.expected.update(dict(service1=True, service2=True))
        assert lenient.__dict__ == self.expected

    def test_args_services_callable(self):  # noqa: D102
        def service1():
            pass

        def service2():
            pass

        services = (service1, service2)
        lenient = _Lenient(*services)
        self.expected.update({_qualname(service1): True, _qualname(service2): True})
        assert lenient.__dict__ == self.expected

    def test_kwargs_client_str(self):  # noqa: D102
        client = dict(client1="service1")
        lenient = _Lenient(**client)
        self.expected.update(dict(client1=("service1",)))
        assert lenient.__dict__ == self.expected

    def test_kwargs_clients_str(self):  # noqa: D102
        clients = dict(client1="service1", client2="service2")
        lenient = _Lenient(**clients)
        self.expected.update(dict(client1=("service1",), client2=("service2",)))
        assert lenient.__dict__ == self.expected

    def test_kwargs_clients_callable(self):  # noqa: D102
        def client1():
            pass

        def client2():
            pass

        def service1():
            pass

        def service2():
            pass

        qualname_client1 = _qualname(client1)
        qualname_client2 = _qualname(client2)
        clients = {
            qualname_client1: service1,
            qualname_client2: (service1, service2),
        }
        lenient = _Lenient(**clients)
        self.expected.update(
            {
                _qualname(client1): (_qualname(service1),),
                _qualname(client2): (_qualname(service1), _qualname(service2)),
            }
        )
        assert lenient.__dict__ == self.expected


class Test___call__:
    """Test   call  ."""
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.client = "myclient"
        self.lenient = _Lenient()

    def test_missing_service_str(self):  # noqa: D102
        assert not self.lenient("myservice")

    def test_missing_service_callable(self):  # noqa: D102
        def myservice():
            pass

        assert not self.lenient(myservice)

    def test_disabled_service_str(self):  # noqa: D102
        service = "myservice"
        self.lenient.__dict__[service] = False
        assert not self.lenient(service)

    def test_disable_service_callable(self):  # noqa: D102
        def myservice():
            pass

        qualname_service = _qualname(myservice)
        self.lenient.__dict__[qualname_service] = False
        assert not self.lenient(myservice)

    def test_service_str_with_no_active_client(self):  # noqa: D102
        service = "myservice"
        self.lenient.__dict__[service] = True
        assert not self.lenient(service)

    def test_service_callable_with_no_active_client(self):  # noqa: D102
        def myservice():
            pass

        qualname_service = _qualname(myservice)
        self.lenient.__dict__[qualname_service] = True
        assert not self.lenient(myservice)

    def test_service_str_with_active_client_with_no_registered_services(self):  # noqa: D102
        service = "myservice"
        self.lenient.__dict__[service] = True
        self.lenient.__dict__["active"] = self.client
        assert not self.lenient(service)

    def test_service_callable_with_active_client_with_no_registered_services(  # noqa: D102
        self,
    ):
        def myservice():
            pass

        def myclient():
            pass

        qualname_service = _qualname(myservice)
        self.lenient.__dict__[qualname_service] = True
        self.lenient.__dict__["active"] = _qualname(myclient)
        assert not self.lenient(myservice)

    def test_service_str_with_active_client_with_unmatched_registered_services(self):  # noqa: D102
        service = "myservice"
        self.lenient.__dict__[service] = True
        self.lenient.__dict__["active"] = self.client
        self.lenient.__dict__[self.client] = ("service1", "service2")
        assert not self.lenient(service)

    def test_service_callable_with_active_client_with_unmatched_registered_services(  # noqa: D102
        self,
    ):
        def myservice():
            pass

        def myclient():
            pass

        qualname_service = _qualname(myservice)
        qualname_client = _qualname(myclient)
        self.lenient.__dict__[qualname_service] = True
        self.lenient.__dict__["active"] = qualname_client
        self.lenient.__dict__[qualname_client] = ("service1", "service2")
        assert not self.lenient(myservice)

    def test_service_str_with_active_client_with_registered_services(self):  # noqa: D102
        service = "myservice"
        self.lenient.__dict__[service] = True
        self.lenient.__dict__["active"] = self.client
        self.lenient.__dict__[self.client] = ("service1", "service2", service)
        assert self.lenient(service)

    def test_service_callable_with_active_client_with_registered_services(self):  # noqa: D102
        def myservice():
            pass

        def myclient():
            pass

        qualname_service = _qualname(myservice)
        qualname_client = _qualname(myclient)
        self.lenient.__dict__[qualname_service] = True
        self.lenient.__dict__["active"] = qualname_client
        self.lenient.__dict__[qualname_client] = (
            "service1",
            "service2",
            qualname_service,
        )
        assert self.lenient(myservice)

    def test_service_str_with_active_client_with_unmatched_registered_service_str(  # noqa: D102
        self,
    ):
        service = "myservice"
        self.lenient.__dict__[service] = True
        self.lenient.__dict__["active"] = self.client
        self.lenient.__dict__[self.client] = "serviceXXX"
        assert not self.lenient(service)

    def test_service_callable_with_active_client_with_unmatched_registered_service_str(  # noqa: D102
        self,
    ):
        def myservice():
            pass

        def myclient():
            pass

        qualname_service = _qualname(myservice)
        qualname_client = _qualname(myclient)
        self.lenient.__dict__[qualname_service] = True
        self.lenient.__dict__["active"] = qualname_client
        self.lenient.__dict__[qualname_client] = f"{qualname_service}XXX"
        assert not self.lenient(myservice)

    def test_service_str_with_active_client_with_registered_service_str(self):  # noqa: D102
        service = "myservice"
        self.lenient.__dict__[service] = True
        self.lenient.__dict__["active"] = self.client
        self.lenient.__dict__[self.client] = service
        assert self.lenient(service)

    def test_service_callable_with_active_client_with_registered_service_str(  # noqa: D102
        self,
    ):
        def myservice():
            pass

        def myclient():
            pass

        qualname_service = _qualname(myservice)
        qualname_client = _qualname(myclient)
        self.lenient.__dict__[qualname_service] = True
        self.lenient.__dict__["active"] = qualname_client
        self.lenient.__dict__[qualname_client] = qualname_service
        assert self.lenient(myservice)

    def test_enable(self):  # noqa: D102
        service = "myservice"
        self.lenient.__dict__[service] = True
        self.lenient.__dict__["active"] = self.client
        self.lenient.__dict__[self.client] = service
        assert self.lenient(service)
        self.lenient.__dict__["enable"] = False
        assert not self.lenient(service)


class Test___contains__:
    """Test   contains  ."""
    def test_in(self, lenient):  # noqa: D102
        assert "active" in lenient

    def test_not_in(self, lenient):  # noqa: D102
        assert "ACTIVATE" not in lenient

    def test_in_qualname(self, lenient):  # noqa: D102
        def func():
            pass

        qualname_func = _qualname(func)
        lenient.__dict__[qualname_func] = None
        assert func in lenient
        assert qualname_func in lenient


class Test___getattr__:
    """Test   getattr  ."""
    def test_in(self, lenient):  # noqa: D102
        assert lenient.active is None

    def test_not_in(self, lenient):  # noqa: D102
        emsg = "Invalid .* option, got 'wibble'."
        with pytest.raises(AttributeError, match=emsg):
            _ = lenient.wibble


class Test__getitem__:
    """Test  getitem  ."""
    def test_in(self, lenient):  # noqa: D102
        assert lenient["active"] is None

    def test_in_callable(self, lenient):  # noqa: D102
        def service():
            pass

        qualname_service = _qualname(service)
        lenient.__dict__[qualname_service] = True
        assert lenient[service]

    def test_not_in(self, lenient):  # noqa: D102
        emsg = "Invalid .* option, got 'wibble'."
        with pytest.raises(KeyError, match=emsg):
            _ = lenient["wibble"]

    def test_not_in_callable(self, lenient):  # noqa: D102
        def service():
            pass

        qualname_service = _qualname(service)
        emsg = f"Invalid .* option, got '{qualname_service}'."
        with pytest.raises(KeyError, match=emsg):
            _ = lenient[service]


class Test___setitem__:
    """Test   setitem  ."""
    def test_not_in(self, lenient):  # noqa: D102
        emsg = "Invalid .* option, got 'wibble'."
        with pytest.raises(KeyError, match=emsg):
            lenient["wibble"] = None

    def test_in_value_str(self, lenient):  # noqa: D102
        client = "client"
        service = "service"
        lenient.__dict__[client] = None
        lenient[client] = service
        assert lenient.__dict__[client] == (service,)

    def test_callable_in_value_str(self, lenient):  # noqa: D102
        def client():
            pass

        service = "service"
        qualname_client = _qualname(client)
        lenient.__dict__[qualname_client] = None
        lenient[client] = service
        assert lenient.__dict__[qualname_client] == (service,)

    def test_in_value_callable(self, lenient):  # noqa: D102
        def service():
            pass

        client = "client"
        qualname_service = _qualname(service)
        lenient.__dict__[client] = None
        lenient[client] = service
        assert lenient.__dict__[client] == (qualname_service,)

    def test_callable_in_value_callable(self, lenient):  # noqa: D102
        def client():
            pass

        def service():
            pass

        qualname_client = _qualname(client)
        qualname_service = _qualname(service)
        lenient.__dict__[qualname_client] = None
        lenient[client] = service
        assert lenient.__dict__[qualname_client] == (qualname_service,)

    def test_in_value_bool(self, lenient):  # noqa: D102
        client = "client"
        lenient.__dict__[client] = None
        lenient[client] = True
        assert lenient.__dict__[client]
        assert not isinstance(lenient.__dict__[client], Iterable)

    def test_callable_in_value_bool(self, lenient):  # noqa: D102
        def client():
            pass

        qualname_client = _qualname(client)
        lenient.__dict__[qualname_client] = None
        lenient[client] = True
        assert lenient.__dict__[qualname_client]
        assert not isinstance(lenient.__dict__[qualname_client], Iterable)

    def test_in_value_iterable(self, lenient):  # noqa: D102
        client = "client"
        services = ("service1", "service2")
        lenient.__dict__[client] = None
        lenient[client] = services
        assert lenient.__dict__[client] == services

    def test_callable_in_value_iterable(self, lenient):  # noqa: D102
        def client():
            pass

        qualname_client = _qualname(client)
        services = ("service1", "service2")
        lenient.__dict__[qualname_client] = None
        lenient[client] = services
        assert lenient.__dict__[qualname_client] == services

    def test_in_value_iterable_callable(self, lenient):  # noqa: D102
        def service1():
            pass

        def service2():
            pass

        client = "client"
        lenient.__dict__[client] = None
        qualname_services = (_qualname(service1), _qualname(service2))
        lenient[client] = (service1, service2)
        assert lenient.__dict__[client] == qualname_services

    def test_callable_in_value_iterable_callable(self, lenient):  # noqa: D102
        def client():
            pass

        def service1():
            pass

        def service2():
            pass

        qualname_client = _qualname(client)
        lenient.__dict__[qualname_client] = None
        qualname_services = (_qualname(service1), _qualname(service2))
        lenient[client] = (service1, service2)
        assert lenient.__dict__[qualname_client] == qualname_services

    def test_active_iterable(self, lenient):  # noqa: D102
        active = "active"
        assert lenient.__dict__[active] is None

        emsg = "Invalid .* option 'active'"
        with pytest.raises(ValueError, match=emsg):
            lenient[active] = (None,)

    def test_active_str(self, lenient):  # noqa: D102
        active = "active"
        client = "client1"
        assert lenient.__dict__[active] is None
        lenient[active] = client
        assert lenient.__dict__[active] == client

    def test_active_callable(self, lenient):  # noqa: D102
        def client():
            pass

        active = "active"
        qualname_client = _qualname(client)
        assert lenient.__dict__[active] is None
        lenient[active] = client
        assert lenient.__dict__[active] == qualname_client

    def test_enable(self, lenient):  # noqa: D102
        enable = "enable"
        assert lenient.__dict__[enable] == _LENIENT_ENABLE_DEFAULT
        lenient[enable] = True
        assert lenient.__dict__[enable]
        lenient[enable] = False
        assert not lenient.__dict__[enable]

    def test_enable_invalid(self, lenient):  # noqa: D102
        emsg = "Invalid .* option 'enable'"
        with pytest.raises(ValueError, match=emsg):
            lenient["enable"] = None


class Test_context:
    """Test context."""
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.lenient = _Lenient()
        self.default = dict(active=None, enable=_LENIENT_ENABLE_DEFAULT)

    def copy(self):  # noqa: D102
        return self.lenient.__dict__.copy()

    def test_nop(self):  # noqa: D102
        pre = self.copy()
        with self.lenient.context():
            context = self.copy()
        post = self.copy()
        assert pre == self.default
        assert context == self.default
        assert post == self.default

    def test_active_str(self):  # noqa: D102
        client = "client"
        pre = self.copy()
        with self.lenient.context(active=client):
            context = self.copy()
        post = self.copy()
        assert pre == self.default
        expected = self.default.copy()
        expected.update(dict(active=client))
        assert context == expected
        assert post == self.default

    def test_active_callable(self):  # noqa: D102
        def client():
            pass

        pre = self.copy()
        with self.lenient.context(active=client):
            context = self.copy()
        post = self.copy()
        qualname_client = _qualname(client)
        assert pre == self.default
        expected = self.default.copy()
        expected.update(dict(active=qualname_client))
        assert context == expected
        assert post == self.default

    def test_kwargs(self):  # noqa: D102
        client = "client"
        self.lenient.__dict__["service1"] = False
        self.lenient.__dict__["service2"] = False
        pre = self.copy()
        with self.lenient.context(active=client, service1=True, service2=True):
            context = self.copy()
        post = self.copy()
        self.default.update(dict(service1=False, service2=False))
        assert pre == self.default
        expected = self.default.copy()
        expected.update(dict(active=client, service1=True, service2=True))
        assert context == expected
        assert post == self.default

    def test_args_str(self):  # noqa: D102
        client = "client"
        services = ("service1", "service2")
        pre = self.copy()
        with self.lenient.context(*services, active=client):
            context = self.copy()
        post = self.copy()
        assert pre == self.default
        expected = self.default.copy()
        expected.update(dict(active=client, client=services))
        assert context["active"] == expected["active"]
        assert set(context["client"]) == set(expected["client"])
        assert post == self.default

    def test_args_callable(self):  # noqa: D102
        def service1():
            pass

        def service2():
            pass

        client = "client"
        services = (service1, service2)
        pre = self.copy()
        with self.lenient.context(*services, active=client):
            context = self.copy()
        post = self.copy()
        qualname_services = tuple([_qualname(service) for service in services])
        assert pre == self.default
        expected = self.default.copy()
        expected.update(dict(active=client, client=qualname_services))
        assert context["active"] == expected["active"]
        assert set(context["client"]) == set(expected["client"])
        assert post == self.default

    def test_context_runtime(self):  # noqa: D102
        services = ("service1", "service2")
        pre = self.copy()
        with self.lenient.context(*services):
            context = self.copy()
        post = self.copy()
        assert pre == self.default
        expected = self.default.copy()
        expected.update(dict(active="__context", __context=services))
        assert context == expected
        assert post == self.default


class Test_enable:
    """Test enable."""
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.lenient = _Lenient()

    def test_getter(self):  # noqa: D102
        assert self.lenient.enable == _LENIENT_ENABLE_DEFAULT

    def test_setter_invalid(self):  # noqa: D102
        emsg = "Invalid .* option 'enable'"
        with pytest.raises(ValueError, match=emsg):
            self.lenient.enable = 0

    def test_setter(self):  # noqa: D102
        assert self.lenient.enable == _LENIENT_ENABLE_DEFAULT
        self.lenient.enable = False
        assert not self.lenient.enable


class Test_register_client:
    """Test register client."""
    def test_not_protected(self, lenient):  # noqa: D102
        emsg = "Cannot register .* client"
        for protected in _LENIENT_PROTECTED:
            with pytest.raises(ValueError, match=emsg):
                lenient.register_client(protected, "service")

    def test_str_service_str(self, lenient):  # noqa: D102
        client = "client"
        services = "service"
        lenient.register_client(client, services)
        assert client in lenient.__dict__
        assert lenient.__dict__[client] == (services,)

    def test_str_services_str(self, lenient):  # noqa: D102
        client = "client"
        services = ("service1", "service2")
        lenient.register_client(client, services)
        assert client in lenient.__dict__
        assert lenient.__dict__[client] == services

    def test_callable_service_callable(self, lenient):  # noqa: D102
        def client():
            pass

        def service():
            pass

        qualname_client = _qualname(client)
        qualname_service = _qualname(service)
        lenient.register_client(client, service)
        assert qualname_client in lenient.__dict__
        assert lenient.__dict__[qualname_client] == (qualname_service,)

    def test_callable_services_callable(self, lenient):  # noqa: D102
        def client():
            pass

        def service1():
            pass

        def service2():
            pass

        qualname_client = _qualname(client)
        qualname_services = (_qualname(service1), _qualname(service2))
        lenient.register_client(client, (service1, service2))
        assert qualname_client in lenient.__dict__
        assert lenient.__dict__[qualname_client] == qualname_services

    def test_services_empty(self, lenient):  # noqa: D102
        emsg = "Require at least one .* client service."
        with pytest.raises(ValueError, match=emsg):
            lenient.register_client("client", ())

    def test_services_overwrite(self, lenient):  # noqa: D102
        client = "client"
        services = ("service1", "service2")
        lenient.__dict__[client] = services
        assert lenient[client] == services
        new_services = ("service3", "service4")
        lenient.register_client(client, services=new_services)
        assert lenient[client] == new_services

    def test_services_append(self, lenient):  # noqa: D102
        client = "client"
        services = ("service1", "service2")
        lenient.__dict__[client] = services
        assert lenient[client] == services
        new_services = ("service3", "service4")
        lenient.register_client(client, services=new_services, append=True)
        expected = set(services + new_services)
        assert set(lenient[client]) == expected


class Test_register_service:
    """Test register service."""
    def test_str(self, lenient):  # noqa: D102
        service = "service"
        assert service not in lenient.__dict__
        lenient.register_service(service)
        assert service in lenient.__dict__
        assert not isinstance(lenient.__dict__[service], Iterable)
        assert lenient.__dict__[service]

    def test_callable(self, lenient):  # noqa: D102
        def service():
            pass

        qualname_service = _qualname(service)
        assert qualname_service not in lenient.__dict__
        lenient.register_service(service)
        assert qualname_service in lenient.__dict__
        assert not isinstance(lenient.__dict__[qualname_service], Iterable)
        assert lenient.__dict__[qualname_service]

    def test_not_protected(self, lenient):  # noqa: D102
        emsg = "Cannot register .* service"
        for protected in _LENIENT_PROTECTED:
            lenient.__dict__[protected] = None
            with pytest.raises(ValueError, match=emsg):
                lenient.register_service("active")


class Test_unregister_client:
    """Test unregister client."""
    def test_not_protected(self, lenient):  # noqa: D102
        emsg = "Cannot unregister .* client, as .* is a protected .* option."
        for protected in _LENIENT_PROTECTED:
            lenient.__dict__[protected] = None
            with pytest.raises(ValueError, match=emsg):
                lenient.unregister_client(protected)

    def test_not_in(self, lenient):  # noqa: D102
        emsg = "Cannot unregister unknown .* client"
        with pytest.raises(ValueError, match=emsg):
            lenient.unregister_client("client")

    def test_not_client(self, lenient):  # noqa: D102
        client = "client"
        lenient.__dict__[client] = True
        emsg = "Cannot unregister .* client, as .* is not a valid .* client."
        with pytest.raises(ValueError, match=emsg):
            lenient.unregister_client(client)

    def test_not_client_callable(self, lenient):  # noqa: D102
        def client():
            pass

        qualname_client = _qualname(client)
        lenient.__dict__[qualname_client] = True
        emsg = "Cannot unregister .* client, as .* is not a valid .* client."
        with pytest.raises(ValueError, match=emsg):
            lenient.unregister_client(client)

    def test_str(self, lenient):  # noqa: D102
        client = "client"
        lenient.__dict__[client] = (None,)
        lenient.unregister_client(client)
        assert client not in lenient.__dict__

    def test_callable(self, lenient):  # noqa: D102
        def client():
            pass

        qualname_client = _qualname(client)
        lenient.__dict__[qualname_client] = (None,)
        lenient.unregister_client(client)
        assert qualname_client not in lenient.__dict__


class Test_unregister_service:
    """Test unregister service."""
    def test_not_protected(self, lenient):  # noqa: D102
        emsg = "Cannot unregister .* service, as .* is a protected .* option."
        for protected in _LENIENT_PROTECTED:
            lenient.__dict__[protected] = None
            with pytest.raises(ValueError, match=emsg):
                lenient.unregister_service(protected)

    def test_not_in(self, lenient):  # noqa: D102
        emsg = "Cannot unregister unknown .* service"
        with pytest.raises(ValueError, match=emsg):
            lenient.unregister_service("service")

    def test_not_service(self, lenient):  # noqa: D102
        service = "service"
        lenient.__dict__[service] = (None,)
        emsg = "Cannot unregister .* service, as .* is not a valid .* service."
        with pytest.raises(ValueError, match=emsg):
            lenient.unregister_service(service)

    def test_not_service_callable(self, lenient):  # noqa: D102
        def service():
            pass

        qualname_service = _qualname(service)
        lenient.__dict__[qualname_service] = (None,)
        emsg = "Cannot unregister .* service, as .* is not a valid .* service."
        with pytest.raises(ValueError, match=emsg):
            lenient.unregister_service(service)

    def test_str(self, lenient):  # noqa: D102
        service = "service"
        lenient.__dict__[service] = True
        lenient.unregister_service(service)
        assert service not in lenient.__dict__

    def test_callable(self, lenient):  # noqa: D102
        def service():
            pass

        qualname_service = _qualname(service)
        lenient.__dict__[qualname_service] = True
        lenient.unregister_service(service)
        assert qualname_service not in lenient.__dict__
