
import boto3
# import os
# import sys
import uuid
import PIL.Image

s3_client = boto3.client('s3')


def handler(event, context):

    # どんな event を受け取るのだ？
    for record in event['Records']:
        # バケット名、オブジェクト名、ダウンロードパス、アップロードパスを生成
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        upload_path = '/tmp/resized-{}'.format(key)

        # バケットの、key 名ファイルを、このパスにダウンロード
        s3_client.download_file(bucket, key, download_path)
        # ダウンロードしたファイルを、処理して、アップロード待ちパスに格納
        resize_image(download_path, upload_path)
        # アップロード待ちファイルを、このバケットに、このファイル名で格納
        s3_client.upload_file(upload_path, '{}resized'.format(bucket), key)


def resize_image(download_path, upload_path):
    # PIL.Image を使って画像を開き、サムネイルを作成し、保存
    with Image.open(download_path) as image:
        # 画像の(width, height)を それぞれ 1/2 にして、thumbnail の引数に渡す
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(upload_path)
