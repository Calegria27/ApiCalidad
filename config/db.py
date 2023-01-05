from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'server' and 'database' with the name of your SQL Server instance and the name of your database
engine = create_engine('mssql+pymssql://UsuSistratos:15678.usu@192.168.1.31:1433/SistratosWeb', pool_pre_ping=True)
conn= engine.connect()