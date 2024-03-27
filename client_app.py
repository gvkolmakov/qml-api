import sys; sys.path.append('./')
import ngq


# Upload files to the server:
body_upload = {
    'endpoint':     'http://24.199.84.84:5000/upload_data',  # DO server
    'api_key':      'Test725',                    # get it from the registration
    'dataset_dir':  'my_datasets/MNIST_1024_imgs/',  # from where to upload
    'data_id':      'MNIST_1024_imgs'                # name your dataset for the reference
}
response = ngq.upload_dataset_to_server_api( body_upload )



# Train model on data on the server:
body_train = {
    'endpoint':     'http://24.199.84.84:5000/train_model_on_data',  # DO server
    'api_key':      'Test725',        # get it from the registration
    'data_id':      'MNIST_1024_imgs',   # name of the training dataset
    'model_name':   'my_first_model',   # name your model for the future reference
    'num_classes':  '10'                # how many classes in data set
}
response = ngq.train_model_on_data_api( body_train )



body_get_labels = {
    'endpoint':     'http://24.199.84.84:5000/get_labels',  # DO server
    'api_key':      'Test725',                    # get it from the registration
    'dataset_dir':  'my_datasets/just_one_img/',
    'model_name':   'my_first_model',               # your trained model
}
labels = ngq.get_labels_api( body_get_labels )

print("\nHello, I received the labels from the server:")
print(labels)



    
    
    
    
    
    
    

    



