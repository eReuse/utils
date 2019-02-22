import pytest
import requests_mock.mocker

from ereuse_utils.session import DevicehubClient


@pytest.mark.xfail(reason='Make test')
def test_session():
    pass


def test_devicehub_client(requests_mock: requests_mock.mocker.Mocker):
    requests_mock.get('https://example.com/foo/bar/?foo=bar',
                      # request
                      request_headers={'Authorization': 'Basic tag'},
                      # response
                      json={'foo': 'bar'},
                      status_code=201)
    client = DevicehubClient('https://example.com', token='tag')
    data, response = client.get('foo/', uri='bar/', status=201, query=[('foo', 'bar')])
    assert data == {'foo': 'bar'}
    assert response.status_code == 201


def test_devicehub_client_inventories(requests_mock: requests_mock.mocker.Mocker):
    requests_mock.post('https://example.com/users/login/',
                       json={'token': 'fooToken', 'inventories': [{'id': 'db1'}]},
                       status_code=200)
    requests_mock.get('https://example.com/db1/foo/',
                      # request
                      request_headers={'Authorization': 'Basic fooToken'},
                      # response
                      json={'foo': 'bar'},
                      status_code=200)
    client = DevicehubClient('https://example.com', inventory=True)
    assert client.inventory is True
    client.login('foo@foo.com', 'bar')
    assert client.inventory == 'db1'
    data, response = client.get('foo/')
    assert data == {'foo': 'bar'}
    assert response.status_code == 200
