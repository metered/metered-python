# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_client.ipynb.

# %% auto 0
__all__ = ['GraphQLClient']

# %% ../nbs/01_client.ipynb 3
import os
import http.client
import json
from typing import Any, Dict, Callable

# %% ../nbs/01_client.ipynb 4
class GraphQLClient:
  def __init__(self,
    api: str = None,
    host: str = None,
    path: str = "/",
    query: str = None,
    variables: Dict[str, Any] = None,
  ) -> None:
    self.host = host if host else f"{api}.metered.app" if api else None
    self.path = path
    self.query = query
    self.variables = variables or {}

  def __call__(self,
    api: str = None,
    host: str = None,
    path: str = None,
    query: str = None,
    variables: Dict[str, Any] = {},
  ):
    if api or host or path or query or variables:
      return GraphQLClient(
        api=api or self.api,
        host=host or self.host,
        path=path or self.path,
        query=query or self.query,
        variables=variables or self.variables,
      )()

    payload = {
      "query": self.query,
      "variables": self.variables,
    }

    conn = http.client.HTTPSConnection(self.host)
    conn.request("POST", self.path, json.dumps(payload), {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + os.environ['METERED_API_KEY']
    })
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))

    if "errors" in json_data and json_data["errors"]:
      raise Exception(json.dumps(json_data["errors"]))
    
    return json_data
