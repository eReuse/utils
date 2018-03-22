import json
import json as json_lib

from boltons.urlutils import QueryParamDict, URL
from flask.testing import FlaskClient
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response

JSON = 'application/json'
ANY = '*/*'
AUTH = 'Authorization'
BASIC = 'Basic {}'


class Client(FlaskClient):
    """
    A client for the REST servers of DeviceHub and WorkbenchServer.

    - JSON first. By default it sends and expects receiving JSON files.
    - Assert regular status responses, like 200 for GET.
    - Auto-parses a nested dictionary of URL query params to the
      URL version with nested properties to JSON.
    - Meaningful headers format: a dictionary of name-values.
    """

    def open(self, uri: str, status: int or HTTPException = 200, accept=JSON, content_type=JSON,
             item=None, headers: dict = None, **kw) -> (dict or str, Response):
        """

        :param uri: The URI without basename and query.
        :param status: Assert the response for specified status. Set
                       None to avoid.
        :param accept: The Accept header. If 'application/json'
                       (default) then it will parse incoming JSON.
        :param item: The last part of the path. Useful to do something
                     like ``get('db/accounts', item='24')``. If you
                     use ``item``, you can't set a final backslash into
                     ``uri`` (or the parse will fail).
        :param headers: A dictionary of headers, where keys are header
                        names and values their values.
                        Ex: {'Accept', 'application/json'}.
        :param kw: Kwargs passed into parent ``open``.
        :return: A tuple with: 1. response data, as a string or JSON
                 depending of Accept, and 2. the Response object.
        """
        headers = headers or {}
        headers['Accept'] = accept
        headers['Content-Type'] = content_type
        headers = [(k, v) for k, v in headers.items()]
        if 'data' in kw and content_type == JSON:
            kw['data'] = json.dumps(kw['data'])
        if item:
            uri = URL(uri).navigate(item).to_text()
        response = super().open(uri, headers=headers, **kw)
        if status:
            _status = getattr(status, 'code', status)
            assert response.status_code == _status, \
                'Expected status code {} but got {}'.format(_status, response.status_code)
        data = response.get_data().decode()
        if accept == JSON:
            data = json_lib.loads(data) if data else {}
        return data, response

    def get(self, uri: str, query: dict = {}, item: str = None, status: int or HTTPException = 200,
            accept: str = JSON, headers: dict = None, **kw) -> (dict or str, Response):
        """
        Performs a GET.

        See the parameters in :meth:`ereuse_utils.test.Client.open`.
        Moreover:

        :param query: A dictionary of query params. If a parameter is a
                      dict or a list, it will be parsed to JSON, then
                      all params are encoded with ``urlencode``.
        :param kw: Kwargs passed into parent ``open``.
        """
        url = URL(uri)
        # Convert inner dicts and lists to json
        # We create a new dict to avoid mutating input
        url.query_params = QueryParamDict({
            k: json.dumps(v) if isinstance(v, (list, dict)) else v
            for k, v in query.items()
        })
        return super().get(url.to_text(), item=item, status=status, accept=accept, headers=headers,
                           **kw)

    def post(self, uri: str, data: str or dict, status: int or HTTPException = 201,
             content_type: str = JSON, accept: str = JSON, headers: dict = None, **kw) \
            -> (dict or str, Response):
        """
        Performs a POST.

        See the parameters in :meth:`ereuse_utils.test.Client.open`.
        """
        return super().post(uri, data=data, status=status, content_type=content_type,
                            accept=accept, headers=headers, **kw)

    def patch(self, uri: str, data: str or dict, status: int or HTTPException = 200,
              content_type: str = JSON, item: str = None, accept: str = JSON, headers: dict = None,
              **kw) -> (dict or str, Response):
        """
        Performs a PATCH.

        See the parameters in :meth:`ereuse_utils.test.Client.open`.
        """
        return super().patch(uri, item=item, data=data, status=status, content_type=content_type,
                             accept=accept, headers=headers, **kw)
