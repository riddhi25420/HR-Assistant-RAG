import oracledb
from backend.config import Config
def get_connection():
    return oracledb.connect(user=Config.ORACLE_USER,password=Config.ORACLE_PASSWORD,host=Config.ORACLE_HOST,port=Config.ORACLE_PORT,service_name=Config.ORACLE_SERVICE)