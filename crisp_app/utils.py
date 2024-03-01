def allowed_file(filename, allowed_extensions_list):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions_list

def create_new_col(raw_df, key, value):
    if not any(col in value for col in raw_df.columns):
        raw_df[key] = ''.join(map(str, value))
    
    else:
        raw_df[key] = raw_df[value].astype(str).apply('-'.join, axis=1)

    return raw_df





