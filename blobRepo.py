import os, uuid
from azure.storage.blob import BlockBlobService, PublicAccess

class BlobRepo:

    def connect():
        try:
            block_blob_service = BlockBlobService(account_name='topicmodeling7885000326', account_key='XcdfPfvBQVgt0g+h3voFQ7ySystcnrJTsEQc73clWmsWuSzFFw6b5v89pO6idc7JyyUlefvC6bIV9QABluMBhA==')
            return block_blob_service.list_blobs(GetContainerName())

        except Exception as e:
            print(e)

    def GetContainerName():
        return 'exforge'

    if  __name__ == "__main__":
        connect()