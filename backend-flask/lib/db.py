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
    template_inner_directory = pathlib.Path(*args[:-1])
    template_file = args[-1] + ".sql"

    template_directory = (app_root_directory / "db") / "sql" / template_inner_directory
    template_path = template_directory / template_file
    
    print("\n")
    print(Back.GREEN + Fore.WHITE + f"Load SQL Template: {template_path}" + Style.RESET_ALL)

    with template_path.open(mode="r") as f:
      template_content = f.read()
      lines = template_content.split("\n")
      # Prints line numbers :)
      for idx, line in enumerate(lines):
        line_number = str(idx + 1).rjust(2)
        print(f"{line_number} {line}")
      
    return template_content

  def print_params(self, params):
    """ we want to commit data such as an insert
        be sure to check for RETURNING in all uppercases
    """
    print(Back.BLUE + Fore.WHITE + "SQL Params:" + Style.RESET_ALL)
    for key, value in params.items():
      print(key, ":", value)

  def print_sql(self, title, sql):
    print("\n" + Back.CYAN + Fore.WHITE + f"SQL STATEMENT-[{title}]------" + Style.RESET_ALL)
    lines = sql.split("\n")
    for idx, line in enumerate(lines):
      line_number = str(idx + 1).rjust(2)
      print(f"{line_number} {line}")

  def print_sql_err(self,err):
    # get details about the exception 
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print (Fore.RED + f"\npsycopg ERROR: {err} on line number: {line_num}")
    print (f"psycopg traceback: {traceback} -- type: {err_type}")

    # # print the pgcode and pgerror exceptions
    # print (f"pgerror: {err.pgerror}")
    # print (f"pgcode: {err.pgcode} \n" + Style.RESET_ALL)

  def query_commit(self, sql, params={}):
    self.print_sql('Commit with returning', sql)
    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)
    returning_id = None

    try:
      with self.pool.connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        conn.commit()
    except Exception as err:
      self.print_sql_err(err)

    return returning_id if returning_id is not None else None

  def query_array_json(self, sql, params={}):
    """when we want to return a json object"""

    self.print_sql('array', sql)
    wrapped_sql = self.query_wrap_array(sql)

    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql,params)
        json = cur.fetchone()

    return json[0]
      
  def query_object_json(self,sql,params={}):
    """When we want to return an array of json objects"""

    self.print_sql('json',sql)
    self.print_params(params)
    wrapped_sql = self.query_wrap_object(sql)

    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(wrapped_sql, params)
        json = cur.fetchone()
    if json is not None:
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