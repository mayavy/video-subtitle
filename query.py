
from datetime import datetime, timezone
import boto3
import botocore
from boto3.dynamodb.conditions import Key

from project.settings import dynamodb, DB_TABLE_NAME


class Db_Handler:
    """
    DataBase handler class for handling the aws-dynamodb.
    Performs only query and put operations
    """

    def __init__(self):
        self.dyn_resource = dynamodb
        self.table = dynamodb.Table(DB_TABLE_NAME)

    def query_words(self, words: list):
        """ 
        Query word(s) from the database.
        words: List of words
        yield :: generator object iterating all word(s) 
        """
        try:
            def q(word):
                return self.table.query(KeyConditionExpression=Key('word').eq(word))['Items']
            for word in words:
                yield q(word)
        except Exception as e:
            pass

    def put_entry(self, video):
        """ 
        Put single item in the database.
        video: Video class object
        return: None 
        """
        try:
            for word, ranges in video.word_dict.items():
                if word != '':
                    self.table.put_item(
                        Item={
                            'word': word,
                            'uploaded_by': datetime.now(timezone.utc).strftime(r"%d/%m/%Y, %H:%M:%S"),
                            'video_id': video.id,
                            'ranges': ranges})
        except Exception as e:
            pass
