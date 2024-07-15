import s3fs
from utils.constants import AWS_ACCESS_KEY, AWS_SECRET_KEY


def connect_to_s3() -> s3fs.S3FileSystem:
    try:
        s3: s3fs.S3FileSystem = s3fs.S3FileSystem(
            key=AWS_ACCESS_KEY,
            secret=AWS_SECRET_KEY
        )
        return s3
    except Exception as e:
        print(e)


def create_bucket_if_not_exists(s3: s3fs.S3FileSystem, bucket: str):
    try:
        if not s3.exists(bucket):
            s3.mkdir(bucket)
            print("Bucket created!")
        else:
            print("Bucket already exists!")
    except Exception as e:
        print(e)


def upload_to_s3(s3: s3fs.S3FileSystem, file_path: str, bucket: str, s3_file_name: str):
    try:
        s3.put(file_path, bucket + "/raw/" + s3_file_name)
        print("File uploaded")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(e)
