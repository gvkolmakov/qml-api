# This software is distributed under MIT license, https://mit-license.org
# The newest verion can be downloaded at https://github.com/gvkolmakov/qml-api
# Please email G.Kolmakov with any questions at german@ngq.io

#version
VERSION = "20240813"
MINOR_VERSION = "D002" #updated Aug 28 2024

##########################################################
# Set talkativeness level: True or False
# DEBUG = True -> all messages
# DEBUG = False -> Some messages
DEBUG = False # True or False

# Do initial tests: True of False
DO_TEST = True #False for localhost, True for DO testing

if DO_TEST:
    my_host = "my-qml.org"; my_port = 443
else:
    my_host = "127.0.0.1"; my_port = 5000

### importing modules ##############
# initializing
import_error = False
import_error_message = []

try:
    import socket
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'socket\' module in your python3.")

try:
    import logging
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'logging\' module in your python3.")

try:
    import json
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'json\' module in your python3.")
    
try:
    import glob
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'glob\' module in your python3.")

try:
    import time
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'time\' module in your python3.")

try:
    import requests
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'requests\' module in your python3. ")
    import_error_message.append("One-liner to install from a terminal is:")
    import_error_message.append("python3 -m pip install requests")
    
try:
    import os
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'os\' module in your python3. ")

try:
    import sys
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'sys\' module in your python3. ")

try:
    import shutil
except ImportError as e:
    import_error = True
    import_error_message.append(e)
    import_error_message.append("Please install \'shutil\' module in your python3. ")

def log_import_errors():
    """Print module import errors"""
    with open("logfile.log", 'a') as f:
        print("Log started.", file=f)
        for i in range(len(import_error_message)):
            print("my_import_errors::", import_error_message[i], file=f)
            print(import_error_message[i])
        print("Session finished", file=f)
    exit()

if import_error:
    log_import_errors()
    #Session will end here because of the import error

# Setting up logger:
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='logfile.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Session started")
logger.info("[IMPORT] All modules imported")

# Checking internet
# basic connection:
def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logger.info("[NETWORK] Internet is working")
    except socket.error as ex:
        print(ex)
        print("[NETWORK] Please check your internet network\n")
        logger.error(ex)
        logger.error("[NETWORK] Please check your internet network")
        #logger.info("Session finished")

def check_server(host=my_host, port=my_port, timeout=3):
    """ Checking DO server """
    logger.info("[SERVER] Start checking DO server.")
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logger.info("[SERVER] Server is reacheable.")
    except socket.error as ex:
        print(ex)
        print("[SERVER] Cannot establish connection with the server.\n")
        logger.error(ex)
        logger.error("[SERVER] Cannot establish connection with the server.")
        logger.info("Session finished.")
        exit()

def check_server_version():
    """Check if the server and clinet versions match"""
    logger.info("Client major version = " + VERSION)
    logger.info("Client minor version = " + MINOR_VERSION)
    logger.info("[SERVER VERSION] Start checking server version.")
    if DO_TEST:
        url = 'https://my-qml.org/server_version'
    else:
        url = 'http://127.0.0.1:5000/server_version'
    version_dict = {'client_major_version': VERSION, 'client_minor_version': MINOR_VERSION}
    #response = requests.get(url=url)
    response = requests.post(url=url, json=version_dict)
    assert response.status_code == 200
    data = json.loads(response.content)
    SERVER_VERSION = data['server_version']
    SERVER_MINOR_VERION = data['server_minor_version']
    #checking if the versions match
    if VERSION == SERVER_VERSION:
        logger.info("[SERVER VERSION] Server and client major versions match")
        logger.warning("Server minor version = " + SERVER_MINOR_VERION)
        logger.warning("Client minor version = " + MINOR_VERSION)
    else:
        logger.warning("[SERVER VERSION] Server and client major versions NO NOT match")
        logger.warning("Server major version = " + SERVER_VERSION)
        logger.warning("Server minor version = " + SERVER_MINOR_VERSION)
        print("[WARNING] Server and client major versions NO NOT match.")
    
def get_dir_tree(starting_directory="."):
    """ Getting the dir tree """
    tree={}
    for root, directories, files in os.walk(starting_directory):
        dir_dict = {}
        dir_dict['dirs'] = directories
        dir_dict['files'] = files
        tree.update({root: dir_dict })
    return tree
    
def client_post_log(tree):
    """Sending the log to the server"""
    if DO_TEST:
        url = 'https://my-qml.org/post_log'
    else:
        url = 'http://127.0.0.1:5000/post_log'
    files = [
    ('logfile', ('logfile.log', open('./logfile.log', 'rb'), 'application/octet')),
    ('tree', ('tree', json.dumps(tree), 'application/json'))]
    response = requests.post(url, files=files)
    assert response.status_code == 200
    return
    
def check_client_os():
    """ Check host system """
    sys_platform = sys.platform
    os_name = os.name
    logger.info("[OS] client sys platform = " + sys_platform)
    logger.info("[OS] client os name = " + os_name)
    return

def tests():
    """ Collect diagnostics data """
    check_internet()
    check_server()
    check_server_version()
    check_client_os()
    #tree = get_dir_tree()
    #client_post_log(tree)
   
tests()

#if DO_TEST:
#   tests()


# make _upload_data_files ( ...) an interface for _upload_data_files_chunk()
#
def _upload_data_files(endpoint = None, dataset_dir = None, user_id = None, data_id = None):
    """make chunks and sent via _upload_data_files_chunks"""
    
    chunk_size = 100
    file_list = glob.glob(dataset_dir + '*')
    chunks = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]
    if(DEBUG):
        logger.info("number of chunks = " + str(len(chunks)))
    
    for chunk in chunks:
        response =_upload_data_files_chunk(
                    endpoint = endpoint,
                    user_id = user_id,
                    data_id = data_id,
                    chunk = chunk)
        if response["error"] == "Error":
            return response
    response = {"error": "None", "message": "Your data files were uploaded to the server."}
    return response
    
def _upload_data_files_chunk(endpoint = None,
                    user_id = None,
                    data_id = None,
                    chunk = None):
    """Upload data files' chunk to server.
    The data_id chunk should be a list of files with full path like
    [my_datasets/MNIST_1024_imgs/img0001.png, my_datasets/MNIST_1024_imgs/img0002.png,
    ...].
    The length of the chunk list should be < 300.
    
    Usage:
    To upload files to the server:
        (my_data_id, status) = upload_data_files(local_file_dir)
    To add more files to the server to storage with data_id = my_data_id:
        (data_id, status) = upload_data_files(local_file_dir, data_id=my_data_id)
    """
    
    #url = 'http://24.199.84.84/upload_data'
    url = endpoint
    #file_list = glob.glob(dataset_dir + '*')
    file_list = chunk
    files, ff = (), []      # tuple with files to upload to url, open files' descriptor list
    file_label = 'files'    # label should match request.files.getlist('files') on the server

    #adding files to tuple to send to the server
    for file in file_list:
        if(DEBUG):
            logger.info(str(file))
        f1 = open(file, "rb")
        ff.append(f1)
        files = (*files, (file_label, f1)) #add file to tuple
        
    #adding query
    query_string = '?' + 'user_id=' + str(user_id)
    if data_id != "None" :
            query_string += '&data_id=' + str(data_id)
    api_url = url + query_string
    
    #print("ngq::_upload_data_files_chunk user_id =", user_id)
    #print("               query =", query_string)
    
    #sending files to server
    if(DEBUG):
        print("sending files:", files)
    response = requests.post( url=api_url, files=files )
    #print("status =", response.status_code)
    #closing all files in ff[]
    for f1 in ff:
        f1.close()
        #if f1.closed:
        #    print('file is closed')
    assert response.status_code == 200

    #getting status and data_id
    response = requests.get(url=api_url)
    assert response.status_code == 200
    if(DEBUG):
        print("Response received from server:", json.loads(response.content))

    return json.loads(response.content)


def _upload_data_files_old(endpoint = "None", dataset_dir = "None", user_id = "None", data_id = "None"):
    """
    Old version, send all files at once.
    Cannot process more than 300 files because of the limit in open files' number.
    
    Upload data files to server, get the data_id
    Usage:
    To upload files to the server:
        (my_data_id, status) = upload_data_files(local_file_dir)
    To add more files to the server to storage with data_id = my_data_id:
        (data_id, status) = upload_data_files(local_file_dir, data_id=my_data_id)
    """
    
    #url = 'http://24.199.84.84:5000/upload_data'
    url = endpoint
    file_list = glob.glob(dataset_dir + '*')
    files, ff = (), []      # tuple with files to upload to url, open files' descriptor list
    file_label = 'files'    # label should match request.files.getlist('files') on the server

    #adding files to tuple to send to the server
    for file in file_list:
        if(DEBUG):
            print(file)
        f1 = open(file, "rb")
        ff.append(f1)
        files = (*files, (file_label, f1)) #add file to tuple
        
    #adding query
    query_string = '?' + 'user_id=' + str(user_id)
    if data_id != "None" :
            query_string += '&data_id=' + str(data_id)
    api_url = url + query_string
    
    #sending files to server
    if(DEBUG):
        print("sending files:", files)
    response = requests.post( url=api_url, files=files )
    #print("status =", response.status_code)
    #closing all files in ff[]
    for f1 in ff:
        f1.close()
        #if f1.closed:
        #    print('file is closed')
    assert response.status_code == 200

    #getting status and data_id
    response = requests.get(url=api_url)
    assert response.status_code == 200
    if(DEBUG):
        print("Response received from server:", json.loads(response.content))

    return json.loads(response.content)

def  _train_model_on_data(endpoint, user_id, data_id, model_name, num_classes):
    """Train model on server on specific dataset."""
    
    url = endpoint
    #query string
    query_string = '?'
    #api key - mandatory
    if user_id != "None":
        query_string += 'user_id=' + str(user_id)
    else:
        return {'error': 'Error', 'message': 'user_id missing. Provide user_id to run the app correctly.'}
    #data id - mandatory
    if data_id != "None":
        query_string += '&data_id=' + str(data_id)
    else:
        return {'error': 'Error', 'message': 'data_id missing. Provide data_id to run the app correctly.'}
    #model name - mandatory
    if model_name != "None":
        query_string += '&model_name=' + str(model_name)
    else:
        return {'error': 'Error', 'message': 'model_name missing. Name your model somehow for the future reference, to run the app correctly.'}
    #num classes - optional
    if num_classes != "None":
        query_string += '&num_classes=' + str(num_classes)
     
    api_url = url + query_string
    if(DEBUG):
        print('api_url =', api_url)
    
    #sending request to train model
    response = requests.post(url=api_url)
    assert response.status_code == 200
    if(DEBUG):
        print("Response received from server:", json.loads(response.content))
    return json.loads(response.content)
    
    #getting status and data_id
    #response = requests.get(url=api_url)
    #assert response.status_code == 200
    #print("Response received from server:", json.loads(response.content))
    #return json.loads(response.content)


def _get_labels(endpoint,user_id,dataset_dir,model_name):
    """ Get files labeled"""
    
    # Step 1. Upload files to the server to get labeled
    
    tmp_data_id = 'TMP_SET_TO_LABEL'
    
    # make endpoint for file transfer to server
    from urllib.parse import urlparse
    url = endpoint
    parse_object = urlparse(url)
    server_address = parse_object.netloc
    if(DEBUG):
        print('ngq::_get_labels:: server_address =', server_address)
    protocol = parse_object.scheme + '://'
    send_files_endpoint = protocol + server_address + '/upload_data'
    if(DEBUG):
        print('send_files_endpoint =', send_files_endpoint)
    
    # upload files to server
    _upload_data_files(endpoint=send_files_endpoint,
                       dataset_dir=dataset_dir,
                       user_id=user_id,
                       data_id = tmp_data_id)
    
    logger.info("Data sent to server to TMP_SET_TO_LABEL dir")
    
    # Step 2. Run the model on those files
    url = endpoint
    
    # making query string
    query_string = '?'
    # api key - mandatory
    if user_id != "None":
        query_string += 'user_id=' + str(user_id)
    else:
        return {'error': 'Error', 'message': 'user_id missing. Provide user_id to run the app correctly.'}
    
    # model name - mandatory
    if model_name != "None":
        query_string += '&model_name=' + str(model_name)
    else:
        return {'error': 'Error', 'message': 'model_name missing. Name your model somehow for the future reference, to run the app correctly.'}
        
    # adding data_id = tmp_data_id
    query_string += '&data_id=' + tmp_data_id
    api_url = url + query_string
    if(DEBUG):
        print('ngq::_get_labels:: api_url =', api_url)
    
    response = requests.post(url=api_url)
    assert response.status_code == 200
    
    #getting status and labels dictionary
    response = requests.get(url=api_url)
    assert response.status_code == 200
    if(DEBUG):
        print("ngq:: _get_labels:: Response received from server:", json.loads(response.content))
    
    #return labels dictionary
    return json.loads(response.content)
    
    
    
def _check_model_ready(endpoint,user_id,model_name):
    """ Check if model is ready"""
        
    # adding user_ad - mandatory
    if user_id != "None":
        query_string = '?user_id=' + str(user_id)
    else:
        return {"error": "Error", "message": 'Your user_id missing. Provide user_id to run the app correctly.'}
        
    # adding model_name- mandatory
    if model_name != "None":
        query_string += '&model_name=' + str(model_name)
    else:
        return {"error": "Error", "message": 'Your model_name missing. Provide model_name to run the app correctly.'}
    
    import time
    time.sleep(0.2)
    #making POST request
    api_url = endpoint + query_string
    if(DEBUG):
        print('ngq::_check_model_ready:: api_url =', api_url)
    response = requests.post(url=api_url)
    assert response.status_code == 200
    loads = json.loads(response.content)
    return loads

def  _train_MNIST_model(endpoint, user_id, model_type, model_name, training_size, batch_size, epochs, image_resolution):
    """Train MNIST model on server."""
    
    #user_id - mandatory
    if user_id != "None":
        query_string = '?user_id=' + str(user_id)
    else:
        return {'error': 'Error', 'message': 'user_id missing. Provide user_id to run the app correctly.'}
       
    #model type - mandatory
    if model_type != "None":
        query_string += '&model_type=' + str(model_type)
    else:
        return {'error': 'Error', 'message': 'model_type missing. Use either \"simple\" or \"complex\" or \"lenet\".'}
    
    #model name - optional
    if model_name != "None":
        query_string += '&model_name=' + str(model_name)
    else:
        return {'error': 'Warning', 'message': 'model_name missing. '}
    
    #model params
    query_string += '&training_size=' + str(training_size)
    query_string += '&batch_size=' + str(batch_size)
    query_string += '&epochs=' + str(epochs)
    query_string += '&image_resolution=' + str(image_resolution)
    
    # full api url request
    api_url = endpoint + query_string
    if(DEBUG):
        print('ngq:: _train_MNIST_model:: api_url =', api_url)
    
    #sending request to train model
    response = requests.post(url=api_url)
    assert response.status_code == 200
    if(DEBUG):
        print("Response received from server:", json.loads(response.content))
    return json.loads(response.content)
    
    
#########

def  _download_MNIST_results(endpoint, user_id, model_name):
    """Download MNISt traiuning results from the server."""
    
    #user_id - mandatory
    if user_id != "None":
        query_string = '?user_id=' + str(user_id)
    else:
        return {'error': 'Error', 'message': 'user_id missing. Provide user_id to run the app correctly.'}
       
    #model name - mandatory
    if model_name != "None":
        query_string += '&model_name=' + str(model_name)
    else:
        return {'error': 'Warning', 'message': 'model_name missing. '}
        
    # full api url request
    api_url = endpoint + query_string
    if(DEBUG):
        print('ngq:: _download_MNIST_results:: api_url =', api_url)
    
    #sending request to the server
    response = requests.post(url=api_url)
    assert response.status_code == 200
    
    #getting the filename to save the downloaded results
    def get_filename():
        """ Get filename to save the data
            usage: filename = pick_filename()
        """
        import os.path
        # filename parts setup
        basename = 'results'
        extension = '.txt.backup'
        
        def next_filename():
            """ Returning results-1.txt.backup etc.
            Assuming that results.txt.backup already exists."""
            imax = 10000
            for i in range(1,imax+1):
                fname = basename + "-" + str(i) + extension
                if not os.path.isfile(fname):
                    return fname
            print("*** Error: ngq.py:: _download_MNIST_results:: get_filename:: next_filename:: Cannot generate new filename, reaches the limit. Increase imax in the code. Now imax =", imax)
            return False
            
        # returning the file name
        fullname = basename + extension
        if not os.path.isfile(fullname):
            return fullname
        else:
            return next_filename()
     
    results_filename = 'results.txt'
    
    #backup current results file if it exists
    if os.path.isfile(results_filename):
        backup_filename = get_filename()
        print("backup filename = ", backup_filename)
        shutil.copy(results_filename, backup_filename)
    
    with open(results_filename, "ab") as f:
        f.write(response.content)
        #print("File downloaded successfully!")
    
    return {"error": "None", "message": "The file " + results_filename + " was downloaded."}
    
##################### API WRAPPERS #####################

def upload_dataset_to_server_api(body):
    """ API wrapper.
    Take the api request and send a request to server to transfer files
    Calls  _upload_data_files(...) """
    
    #checking keys in body dict
    keys_list = body.keys()
    #print("ngq::upload_dataset_to_server_api keys_list =", keys_list)
    
    #checking endpoint
    default_endpoint = 'https://my-qml.org/upload_data'
    if 'endpoint' in keys_list:
        endpoint = body['endpoint']
    else:
        endpoint = default_endpoint

    #checking user_id
    if 'user_id' in keys_list:
        user_id = body['user_id']
    else:
        user_id = 'None'
        
    #checking 'dataset_dir'
    if 'dataset_dir' in keys_list:
        dataset_dir = body['dataset_dir']
    else:
        dataset_dir = 'None'
    
    #checking 'data_id'
    if 'data_id' in keys_list:
        data_id = body['data_id']
    else:
        data_id = 'None'
    
    response = _upload_data_files(endpoint = endpoint,
                                  dataset_dir = dataset_dir,
                                  user_id = user_id,
                                  data_id = data_id)
    return response
    

def train_model_on_data_api(body):
    """API wrapper for _train_model_on_data(...)"""
    
    #check keys in body dict
    keys_list = body.keys()
    
    #checking endpoint
    default_endpoint = 'https://24.199.84.84/train_model_on_data'
    if 'endpoint' in keys_list:
        endpoint = body['endpoint']
    else:
        endpoint = default_endpoint
        
    #checking user_id
    if 'user_id' in keys_list:
        user_id = body['user_id']
    else:
        user_id = 'None'
    
    #checking 'data_id'
    if 'data_id' in keys_list:
        data_id = body['data_id']
    else:
        data_id = 'None'
        
    #checking 'model_name'
    if 'model_name' in keys_list:
        model_name = body['model_name']
    else:
        model_name = 'None'
        
    #checking 'num_classes'
    if 'num_classes' in keys_list:
        num_classes = body['num_classes']
    else:
        num_classes = 'None'
    
    response = _train_model_on_data(endpoint = endpoint,
                                    user_id = user_id,
                                    data_id = data_id,
                                    model_name = model_name,
                                    num_classes = num_classes)
    import time
    time.sleep(1.0)
    
    return response
    

def get_labels_api(body):
    """ Get files labeled. API wrapper for _get_labels(...)"""
    
    #check keys in body dict
    keys_list = body.keys()
    
    #checking endpoint
    default_endpoint = 'https://24.199.84.84/get_labels'
    if 'endpoint' in keys_list:
        endpoint = body['endpoint']
    else:
        endpoint = default_endpoint
        
    #checking user_id
    if 'user_id' in keys_list:
        user_id = body['user_id']
    else:
        user_id = 'None'
    
    #checking 'dataset_dir'
    if 'dataset_dir' in keys_list:
        dataset_dir = body['dataset_dir']
    else:
        dataset_dir = 'None'
        
    #checking 'model_name'
    if 'model_name' in keys_list:
        model_name = body['model_name']
    else:
        model_name = 'None'
    
    #check if model exists and ready
    def change_endpoint(endpoint, new_route):
        """Change endpoint. Example:
        new_endpoint = change_endpoint(
                            endpoint=endpoint,
                            new_route='/check_model_ready')
        changes the route in endpoint to /check_model_ready.
        """
        from urllib.parse import urlparse
        url = endpoint
        parse_object = urlparse(url)
        server_address = parse_object.netloc
        if(DEBUG):
            print('ngq::get_labels_api:: server_address =', server_address)
        protocol = parse_object.scheme + '://'
        new_endpoint = protocol + server_address + new_route
        if(DEBUG):
            print('new endpoint =', new_endpoint)
        return new_endpoint
        
    #make a new endpoint, to check if model is ready
    check_model_ready_endpoint = change_endpoint(
                                    endpoint=endpoint,
                                    new_route='/check_model_ready')
    #now checking if model is ready
    response = _check_model_ready(
                    endpoint=check_model_ready_endpoint,
                    user_id=user_id,
                    model_name=model_name)
    if response["error"] != "None":
        if(DEBUG):
            print("Model is not ready")
        return response
    
    #get labels from server
    response = _get_labels(endpoint = endpoint,
                           user_id = user_id,
                           dataset_dir = dataset_dir,
                           model_name = model_name)
    return response
    
def check_model_ready_api(body):
    """ Check if model is trained."""
    
    #check keys in body dict
    keys_list = body.keys()
    
    #checking endpoint
    default_endpoint = 'https://24.199.84.84/check_model_ready'
    if 'endpoint' in keys_list:
        endpoint = body['endpoint']
    else:
        endpoint = default_endpoint
        
    #checking user_id
    if 'user_id' in keys_list:
        user_id = body['user_id']
    else:
        user_id = 'None'
    
    #checking 'model_name'
    if 'model_name' in keys_list:
        model_name = body['model_name']
    else:
        model_name = 'None'
        
    #checking 'keep_trying'
    MAX_TRIES = 20 #max number of tries
    TIME_OUT  = 4.0  #in seconds
    num_tries = 1
    if 'persistent' in keys_list:
        if body['persistent'] == 'True':
            num_tries = MAX_TRIES
    
    #trying num_tries times
    if num_tries == 1:
        response = _check_model_ready(endpoint = endpoint,
                           user_id = user_id,
                           model_name = model_name)
        return response
    else:
        for i in range(num_tries):
            response = _check_model_ready(endpoint = endpoint,
                               user_id = user_id,
                               model_name = model_name)
            if response["error"] == "Warning":
                print("    ** Training in progress. Will authomatically retry in", TIME_OUT, "seconds.")
                time.sleep(TIME_OUT)
            else:
                return response
    return response
        


def train_MNIST_model_api(body):
    """ Train MNIST model on the server, Berk version"""
    
    #check keys in body dict
    keys_list = body.keys()
    
    #checking endpoint - mandatory
    default_endpoint = 'https://24.199.84.84/check_model_ready'
    if 'endpoint' in keys_list:
        endpoint = body['endpoint']
    else:
        endpoint = default_endpoint
        
    #checking user_id - mandatory
    if 'user_id' in keys_list:
        user_id = body['user_id']
    else:
        user_id = 'None'
    
    #checking 'model_type' - mandatory
    types = ['simple', 'complex', 'lenet'] #supported types
    if 'model_type' in keys_list:
        type = body['model_type']
        if type in types:
            model_type = type
        else:
            return {"error": "Error", "message": "Model type \'" +  type + "\' is not supported. The supported model types are: \'simple\', \'complex\', \'lenet\'. Please check your input for typos."}
    else:
        return {"error": "Error", "message": "Model type is a mandatory parameters. Please provide it. The supported model types are: \'simple\', \'complex\', \'lenet\'."}
    
    #checking 'model_name' - optional
    if 'model_name' in keys_list:
        model_name = body['model_name']
    else:
        model_name = 'my_mnist_model' # name by default
        
    #training set size - optional
    if 'training_set_size' in keys_list:
        training_size = body['training_set_size']
    else:
        training_size = [10, 20, 100, 500, 1000, 2000, 5000] #default value
        
    #batch size - optional
    if 'batch_size' in keys_list:
        batch_size = body['batch_size']
    else:
        batch_size = [32] #default value

    #number of epochs - optional
    if 'epochs' in keys_list:
        epochs = body['epochs']
    else:
        epochs = [50] #default value

    #image resolution set size - optional
    if 'image_resolution' in keys_list:
        image_resolution = body['image_resolution']
    else:
        image_resolution = [4, 7, 14, 28] #default value
      
    response = _train_MNIST_model(endpoint = endpoint,
                            user_id = user_id,
                            model_type = model_type,
                            model_name = model_name,
                            training_size = training_size,
                            batch_size = batch_size,
                            epochs = epochs,
                            image_resolution = image_resolution)
    
    return response
    
 
#######
def download_MNIST_results_api(body):
    """ Train MNIST model on the server, Berk version"""
    
    #check keys in body dict
    keys_list = body.keys()
    
    #checking endpoint - mandatory
    default_endpoint = 'https://24.199.84.84/download_mnist_results'
    if 'endpoint' in keys_list:
        endpoint = body['endpoint']
    else:
        endpoint = default_endpoint
        
    #checking user_id - mandatory
    if 'user_id' in keys_list:
        user_id = body['user_id']
    else:
        return{"error": "Error", "message": "Please provide user_id."}
    
    #checking 'model_type' - mandatory
    if 'model_name' in keys_list:
        model_name = body['model_name']
    else:
        return{"error": "Error", "message": "Please provide model_name."}
    
    response = _download_MNIST_results(endpoint = endpoint,
                            user_id = user_id,
                            model_name = model_name)
    
    return response
  
