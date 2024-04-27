import sys; sys.path.append('./')
import ngq

#######################################################
# Also needs "requests" as a dependency.              #
# One-liner to install from a terminal is:            #
#      python3 -m pip install requests                #
# See for details: https://pypi.org/project/requests/ #
#######################################################

# This app is configured for a test user 'Test725'
# If you need persionalized settings or have any question, contact us at
# email: german@ngq.io

# 1. Upload files to the server:
body_upload = {
    'dataset_dir':  'my_datasets/MNIST_1024_imgs/',   # path to your dataset
    'data_id':      'MNIST_1024_imgs',                # give your dataset a name
    'endpoint':     'https://my-qml.org/upload_data', # server
    'user_id':      'Test725'                         # test user id
}
response = ngq.upload_dataset_to_server_api( body_upload )
print("\n==> File uploading response:\n", response)


# 2. Train model on data on the server:
body_train = {
    'data_id':      'MNIST_1024_imgs',  # name of your dataset
    'model_name':   'my_first_model',   # give your model a name
    'num_classes':  '10',               # how many classes in your data set
    'endpoint':     'https://my-qml.org/train_model_on_data',  # server
    'user_id':      'Test725'           # test user id
}
response = ngq.train_model_on_data_api( body_train )
print("\n==> Training response:\n", response)


# 3. Check if the training is complete and the model is ready to use.
body_check = {
    'model_name':   'my_first_model',           # name of your model
    'keep_trying':  'True',                     # If True, the code retries 20 times
    'endpoint':     'https://my-qml.org/check_model_ready', # server
    'user_id':      'Test725'                   # test user id
}
response = ngq.check_model_ready_api( body_check )
print("\n==> Check if model is already trained:\n", response)


# 4. Get labels for the files you placed in the directory in 'dataset_dir'
#    below. The path 'my_datasets/just_one_img/" is a github example.
body_get_labels = {
    'dataset_dir':  'my_datasets/just_one_img/', # path to files to get labeled
    'model_name':   'my_first_model',            # your trained model
    'endpoint':     'https://my-qml.org/get_labels',  # server
    'user_id':      'Test725'                   # test user id
}
response = ngq.get_labels_api( body_get_labels )
print("\n==> Hello, I received the following from the server:\n", response)
