import os

def test_data_transform_get(client):
    files={'input_data_file': open(os.path.join(client.__dict__['application'].config['ROOT_PATH'], 'data/bad_lines_dummy_file_crisp.csv'), 'rb'),
            'crisp_config_yaml_file': open(os.path.join(client.__dict__['application'].config['ROOT_PATH'], 'data/crisp_config.yml'), 'rb')}

    upload_response = client.post('/file/upload', data=files)

    response = client.get('/data/transform')

    assert b"Confirm Uploaded Input Files and Transform" in response.data

def test_data_transform(client):
    files={'input_data_file': open(os.path.join(client.__dict__['application'].config['ROOT_PATH'], 'data/bad_lines_dummy_file_crisp.csv'), 'rb'),
            'crisp_config_yaml_file': open(os.path.join(client.__dict__['application'].config['ROOT_PATH'], 'data/crisp_config.yml'), 'rb')}


    upload_response = client.post('/file/upload', data=files)

    response = client.post('/data/transform')
    
    assert b"Transformed Output - Crisp App" in response.data