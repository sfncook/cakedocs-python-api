from google.cloud import storage

def upload_vdb(vdb_path, vdb_filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket('cake-docs-vector-dbs')
    blob_upload = bucket.blob(vdb_filename)
    print("Uploading to bucket...")
    blob_upload.upload_from_filename(vdb_path)
    print("Upload complete!")
