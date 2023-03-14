from psycopg_pool import ConnectionPool
import os
import re
import sys
from flask import current_app as app
from colorama import Fore, Back, Style
import pathlib

class Db:
  def __init__(self):
    self.pool = ConnectionPool(os.getenv("CONNECTION_URL"))

  def get_template(self,*args):
    app_root_directory = pathlib.Path(app.root_path)
    template_inner_directory = pathlib.Path.joinpath(args[:-1])
    template_file = args[-1] + ".sql"

    template_directory = (app_root_directory / "db") / "sql" / template_inner_directory
    template_path = template_directory / template_file
    
    print("\n")
    print(Back.GREEN + Fore.WHITE + f"Load SQL Template: {template_path}" + Style.RESET_ALL)

    with template_path.open(mode="r") as f:
      template_content = f.read()
      lines = f.readlines()
      # Prints line numbers :)
      for i in range(len(lines)):
        print(str(i + 1).rjust(2), lines[i])

    return template_content

  def print_params(self, params):
    """we want to commit data such as an insert
      be sure to check for RETURNING in all uppercases

    Args:
        params (_type_): _description_
    """
    # blue = '\033[94m'
    # no_color = '\033[0m'
    print(Back.BLUE + Fore.WHITE + "SQL Params:" + Style.RESET_ALL)
    for key, value in params.items():
      print(key, ":", value)

  def print_sql(self,title,sql):
    # cyan = '\033[96m'
    # no_color = '\033[0m'
    print(Back.CYAN + Fore.WHITE + f"SQL STATEMENT-[{title}]------" + Style.RESET_ALL)
    print(sql)

  def print_sql_err(self,err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print (Fore.RED + f"\npsycopg ERROR: {err} on line number: {line_num}")
    print (f"psycopg traceback: {traceback} -- type: {err_type}")

    # print the pgcode and pgerror exceptions
    print (f"pgerror: {err.pgerror}")
    print (f"pgcode: {err.pgcode} \n" + Style.RESET_ALL)

  def query_commit(self, sql, params={}):
    self.print_sql('commit with returning',sql)

    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)

    try:
      with self.pool.connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit()
        # if is_returning_id:
        #   return returning_id
    except Exception as err:
      self.print_sql_err(err)

    return returning_id if is_returning_id else None

  def query_array_json(self, sql, params={}):
    """when we want to return a json object

    Args:
        sql (str): the query
        params (dict, optional): extra parameters. Defaults to {}.

    Returns:
        dict: json sql query result
    """
    self.print_sql('array', sql)
    wrapped_sql = self.query_wrap_array(sql)

    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        json = cur.fetchone()

    return json[0]
      
  def query_object_json(self,sql,params={}):
    """When we want to return an array of json objects

    Args:
        sql (str): the query
        params (dict, optional): extra parameters. Defaults to {}.

    Returns:
        list: the list of query result and a list of dicts.
    """

    self.print_sql('json',sql)
    self.print_params(params)

    wrapped_sql = self.query_wrap_object(sql)

    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        json = cur.fetchone()

    if json == None:
      "{}"
    else:
      return json[0]
    
  def query_wrap_object(self,template):
    sql = f"""
            (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) 
            FROM ({template}) object_row);
          """
    return sql
  
  def query_wrap_array(self,template):
    sql = f"""
            (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json)
            FROM ({template}) array_row);
          """
    return sql

db = Db()