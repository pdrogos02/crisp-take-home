import os

def test_index_get(client):
    response = client.get('/')

    assert b"Welcome to the Crisp Transformation App" in response.data

def test_file_upload_get(client):
    response = client.get('/file/upload')

    assert b"Upload Input Files" in response.data

def test_file_upload(client):
    files={'input_data_file': open(os.path.join(client.__dict__['application'].config['ROOT_PATH'], 'data/bad_lines_dummy_file_crisp.csv'), 'rb'),
            'crisp_config_yaml_file': open(os.path.join(client.__dict__['application'].config['ROOT_PATH'], 'data/crisp_config.yml'), 'rb')}

    response = client.post('/file/upload', data=files)
    
    assert b"Input File Upload Success" in response.data