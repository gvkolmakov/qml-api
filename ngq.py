import json, requests, glob

# make _upload_data_files ( ...) an interface for _upload_data_files_chunk()
#
def _upload_data_files(endpoint = None, dataset_dir = None, user_id = None, data_id = None):
    """make chunks and sent via _upload_data_files_chunks"""
    
    chunk_size = 100
    file_list = glob.glob(dataset_dir + '*')
    chunks = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]
    print("number of chunks = ", len(chunks))
    
    for chunk in chunks:
        _upload_data_files_chunk(
                    endpoint = endpoint,
                    user_id = user_id,
                    data_id = data_id,
                    chunk = chunk)
    return 'OK'
    
def _upload_data_files_chunk(endpoint = None,
                    #dataset_dir = None,
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
    
    #url = 'http://24.199.84.84:5000/upload_data'
    url = endpoint
    #file_list = glob.glob(dataset_dir + '*')
    file_list = chunk
    files, ff = (), []      # tuple with files to upload to url, open files' descriptor list
    file_label = 'files'    # label should match request.files.getlist('files') on the server

    #adding files to tuple to send to the server
    for file in file_list:
        print(file)
        f1 = open(file, "rb")
        ff.append(f1)
        files = (*files, (file_label, f1)) #add file to tuple
        
    #adding query
    query_string = '?' + 'user_id=' + str(user_id)
    if data_id != None :
            query_string += '&data_id=' + str(data_id)
    api_url = url + query_string
    
    #print("ngq::_upload_data_files_chunk user_id =", user_id)
    #print("               query =", query_string)
    
    #sending files to server
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
    print("Response received from server:", json.loads(response.content))

    return json.loads(response.content)


def _upload_data_files_old(endpoint = None, dataset_dir = None, user_id = None, data_id = None):
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
        print(file)
        f1 = open(file, "rb")
        ff.append(f1)
        files = (*files, (file_label, f1)) #add file to tuple
        
    #adding query
    query_string = '?' + 'user_id=' + str(user_id)
    if data_id != None :
            query_string += '&data_id=' + str(data_id)
    api_url = url + query_string
    
    #sending files to server
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
    print("Response received from server:", json.loads(response.content))

    return json.loads(response.content)

def  _train_model_on_data(endpoint, user_id, data_id, model_name, num_classes):
    """Train model on server on specific dataset."""
    
    url = endpoint
    #query string
    query_string = '?'
    #api key - mandatory
    if user_id != None:
        query_string += 'user_id=' + str(user_id)
    else:
        return {'error': 'user_id missing', 'comment': 'Provide user_id to run the app correctly.'}
    #data id - mandatory
    if data_id != None:
        query_string += '&data_id=' + str(data_id)
    else:
        return {'error': 'data_id missing', 'comment': 'Provide data_id to run the app correctly.'}
    #model name - mandatory
    if model_name != None:
        query_string += '&model_name=' + str(model_name)
    else:
        return {'error': 'model_name missing', 'comment': 'Name your model somehow for the future reference, to run the app correctly.'}
    #num classes - optional
    if num_classes != None:
        query_string += '&num_classes=' + str(num_classes)
     
    api_url = url + query_string
    print('api_url =', api_url)
    
    #sending request to train model
    response = requests.post(url=api_url)
    assert response.status_code == 200
    
    #getting status and data_id
    response = requests.get(url=api_url)
    assert response.status_code == 200
    print("Response received from server:", json.loads(response.content))
    return json.loads(response.content)


def _get_labels(endpoint,user_id,dataset_dir,model_name):
    """ Get files labeled"""
    
    # Step 1. Upload files to the server to get labeled
    
    tmp_data_id = 'TMP_SET_TO_LABEL'
    
    # make endpoint for file transfer to server
    from urllib.parse import urlparse
    url = endpoint
    parse_object = urlparse(url)
    server_address = parse_object.netloc
    print('ngq::_get_labels:: server_address =', server_address)
    protocol = parse_object.scheme + '://'
    send_files_endpoint = protocol + server_address + '/upload_data'
    print('send_files_endpoint =', send_files_endpoint)
    
    # upload files to server
    _upload_data_files(endpoint=send_files_endpoint,
                       dataset_dir=dataset_dir,
                       user_id=user_id,
                       data_id = tmp_data_id)
    
    print("Data sent to server to TMP_SET_TO_LABEL dir")
    
    # Step 2. Run the model on those files
    url = endpoint
    
    # making query string
    query_string = '?'
    # api key - mandatory
    if user_id != None:
        query_string += 'user_id=' + str(user_id)
    else:
        return {'error': 'user_id missing', 'comment': 'Provide user_id to run the app correctly.'}
    
    # model name - mandatory
    if model_name != None:
        query_string += '&model_name=' + str(model_name)
    else:
        return {'error': 'model_name missing', 'comment': 'Name your model somehow for the future reference, to run the app correctly.'}
        
    # adding data_id = tmp_data_id
    query_string += '&data_id=' + tmp_data_id
    api_url = url + query_string
    print('ngq::_get_labels:: api_url =', api_url)
    
    response = requests.post(url=api_url)
    assert response.status_code == 200
    
    #getting status and labels dictionary
    response = requests.get(url=api_url)
    assert response.status_code == 200
    print("ngq:: _get_labels:: Response received from server:", json.loads(response.content))
    
    #return labels dictionary
    return json.loads(response.content)
    

##################### API WRAPPERS #####################

def upload_dataset_to_server_api(body):
    """ API wrapper.
    Take the api request and send a request to server to transfer files
    Calls  _upload_data_files(...) """
    
    #checking keys in body dict
    keys_list = body.keys()
    #print("ngq::upload_dataset_to_server_api keys_list =", keys_list)
    
    #checking endpoint
    default_endpoint = 'https://my-qml.org:8443/upload_data'
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
    default_endpoint = 'http://24.199.84.84:5000/train_model_on_data'
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
        
    #checking 'n_classes'
    if 'num_classes' in keys_list:
        num_classes = body['num_classes']
    else:
        num_classes = 'None'
    
    response = _train_model_on_data(endpoint = endpoint,
                                    user_id = user_id,
                                    data_id = data_id,
                                    model_name = model_name,
                                    num_classes = num_classes)
    return response
    

def get_labels_api(body):
    """ Get files labeled. API wrapper for _get_labels(...)"""
    
    #check keys in body dict
    keys_list = body.keys()
    
    #checking endpoint
    default_endpoint = 'http://24.199.84.84:5000/get_labels'
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
        
    response = _get_labels(endpoint = endpoint,
                           user_id = user_id,
                           dataset_dir = dataset_dir,
                           model_name = model_name)
    return response
    
