import pathlib
import aiosql

from todo.dependencies.database import _get_connection


ddl = aiosql.from_path(pathlib.Path(__file__).parent / "ddl", "aiosqlite")
queries = aiosql.from_path(pathlib.Path(__file__).parent / "dml", "aiosqlite")

