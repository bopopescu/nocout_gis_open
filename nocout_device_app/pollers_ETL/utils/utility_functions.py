import socket
import re
import mysql.connector
import os
from datetime import datetime,timedelta
import time
def get_from_socket(site_name, query):
    """
    Function_name : get_from_socket (collect the query data from the socket)

    Args: site_name (poller on which monitoring data is to be collected)

    Kwargs: query (query for which data to be collectes from nagios.)

    Return : None

    raise 
         Exception: SyntaxError,socket error 
    """
    socket_path = "/omd/sites/%s/tmp/run/live" % site_name
    try:
    	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    	s.connect(socket_path)
    except Exception e:
        raise e
    s.settimeout(60.0)
    s.send(query)
    s.shutdown(socket.SHUT_WR)
    output = ''
    while True:
        try:
                out = s.recv(100000000)
        except socket.timeout,e:
                print 'socket timeout'
                err=e.args[0]
                if err == 'timed out':
                        sys.exit(1)
        out.strip()
        if not len(out):
            break
        output += out
    return output



def pivot_timestamp_fwd(timestamp):
    """
    Function_name : pivot_timestamp (function for pivoting the time to 5 minutes interval)

    Args: timestamp

    Kwargs: None
    return:
           t_stmp (pivoted time stamp)
    Exception:
           None
    """
    t_stmp = timestamp + timedelta(minutes=-(timestamp.minute % 5))
    #if (timestamp.minute %5) != 0:
    t_stmp = t_stmp + timedelta(minutes=5)


    return t_stmp


def get_threshold(perf_data):
    """
    Function_name : get_threshold (function for parsing the performance data and storing in the datastructure)

    Args: perf_data performance_data extracted from rrdtool

    Kwargs: None
    return:
           threshold_values (data strucutre containing the performance_data for all data sources)
    Exception:
           None
    """

    threshold_values = {}

    #if len(perf_data) == 1:
    #   return threshold_values
    for param in perf_data.split(" "):
        param = param.strip("['\n', ' ']")
    	if param.partition('=')[2]:
            	if ';' in param.split("=")[1]:
                    	threshold_values[param.split("=")[0]] = {
                    	"war": re.sub('ms', '', param.split("=")[1].split(";")[1]),
                    	"cric": re.sub('ms', '', param.split("=")[1].split(";")[2]),
                    	"cur": re.sub('ms', '', param.split("=")[1].split(";")[0])
                    	}
            	else:
                    	threshold_values[param.split("=")[0]] = {
                    	"war": None,
                    	"cric": None,
                    	"cur": re.sub('ms', '', param.split("=")[1].strip("\n"))
                    	}
    	else:
        	threshold_values[param.split("=")[0]] = {
            "war": None,
            "cric": None,
            "cur": None
                        }

    return threshold_values


def db_port(site_name=None):
    """
    Function_name : db_port (function for extracting the port value for mongodb for particular poller,As different poller will 
            have different)

    Args: site_name (poller on which monitoring is performed)

    Kwargs: None
    return:
           port (mongodb port)
    Exception:
           IOError
    """
    port = None
    if site_name:
        site = site_name
    else:
        file_path = os.path.dirname(os.path.abspath(__file__))
        path = [path for path in file_path.split('/')]

        if len(path) <= 4 or 'sites' not in path:
            raise Exception, "Place the file in appropriate omd site"
        else:
            site = path[path.index('sites') + 1]
    
    port_conf_file = '/omd/sites/%s/etc/mongodb/mongod.d/port.conf' % site
    try:
        with open(port_conf_file, 'r') as portfile:
            port = portfile.readline().split('=')[1].strip()
    except IOError, e:
        raise IOError, e

    return port


def get_nocout_site_name(site=None):
	file_path = os.path.dirname(os.path.abspath(__file__))
	path = [p for p in file_path.split('/')]
	
	if len(path) <= 4 or 'sites' not in path:
		raise Exception, 'Place the ETL scripts in appropriate omd site location'
	else:
		site = path[path.index('sites') + 1]


	return site


def mysql_conn(db=None, **kwargs):
    """
    Function to create connection to mysql database

    Args:
        db (dict): Mysqldb connection object

    Kwargs:
        kwargs (dict): Dict to store mysql connection variables
    """
    try:
        db = mysql.connector.connect(
                user=kwargs.get('configs').get('user'),
                passwd=kwargs.get('configs').get('sql_passwd'),
                host=kwargs.get('configs').get('ip'),
                db=kwargs.get('configs').get('sql_db'),
		port=kwargs.get('configs').get('sql_port'),
		buffered=True
        )
    except mysql.connector.Error as err:
        raise mysql.connector.Error, err

    return db

def get_machine_name(machine_name=None):
    """
    Function to get fully qualified domain name of the machine
    where Python interpreter is currently executing
    """
    try:
        machine_name = socket.gethostname()
    except Exception, e:
        raise Exception(e)

    return machine_name

def get_epoch_time(datetime_obj):
    """
    Function to convert python datetime object into
    unix epoch time

    Args:
        datetime_obj (datetime): Python datetime object

    Output:
        Unix epoch time in intteger format
    """
    # Get the time in IST (GMT+5:30)
    #utc_time = datetime(1970, 1,1, 5, 30)
    if isinstance(datetime_obj, datetime):
        start_epoch = datetime_obj
        epoch_time = int(time.mktime(start_epoch.timetuple()))

        return epoch_time
    else:
        return datetime_obj

def insert_data(table, data_values, **kwargs):
    """
    Function to insert data into mysql tables

    Args:
        table (str): Table name into which data to be inserted
        data_values: Values in the form of list of tuples

    Kwargs:
        kwargs (dict): Python dict to store connection variables
    """
    db = mysql_conn(configs=kwargs.get('configs')
    query = "INSERT INTO `%s` " % table
    query += """
            (device_name, service_name, machine_name, 
            site_name, data_source, current_value, min_value, 
            max_value, avg_value, warning_threshold, 
            critical_threshold, sys_timestamp, check_timestamp,ip_address,severity,age) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s,%s,%s)
            """
    cursor = db.cursor()
    try:
        cursor.executemany(query, data_values)
    except mysql.connector.Error as err:
        raise mysql.connector.Error, err
    db.commit()
    cursor.close()

