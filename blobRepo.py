import os, uuid
from azure.storage.blob import BlockBlobService, PublicAccess

from config import Configuration

class BlobRepo:

    def GetBlobs(self):
        try:
            block_blob_service = BlockBlobService(account_name=Configuration.GetAzureBlobAccountName(), account_key=Configuration.GetAzureBlobKey())
            blobs = block_blob_service.list_blobs(Configuration.GetBlobContainerName())

            for b in blobs:
                print(b.name)
                bt = block_blob_service.get_blob_to_text(Configuration.GetBlobContainerName(), b.name)
                yield bt.content

        except Exception as e:
            print(e)
