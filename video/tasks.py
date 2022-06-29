"""
Contains Celery task definition(s) and other required Class and variable 
defiantions for handling Video-File(s) which must available locally.
 """

import subprocess
import re
import uuid
from itertools import chain

from project.celery import app

from django.core.files.storage import  FileSystemStorage, default_storage

from project.settings import BASE_DIR,  temporary_storage
from project.aws_conf import AWS_MEDIA_DIR, s3_client
from query import Db_Handler


class Video:
    """Class containing meta data about the video-file stored locally 
    which was sent by the user.
    """
    def __init__(self, filename:str, originalname:str):
        """
        filename: Name of the video-file saved locally.
        originalname: Name of the video-file object recieved.

        self.loc: absolute path of locally stored video-file.
        self.id: generated id for database as primary key.
        word_dict: word or pharses (as key) found in subtitles 
        for each time-segment whernever they occured wrapped
        inside a list.(as value).
        time-segement :: (start, end) formatted as hh:mm:ss,ms.
        """
        self.loc = f'{BASE_DIR}{temporary_storage.url(filename)}'
        self.id = f'{uuid.uuid4()}_|_{originalname}'
        self.word_dict = {} # word or phrase dict

    def upload_s3(self, ):
        """Uploads locally stored video-file to AWS-S3 bucket
        return :: BOOL
        """
        try:
            s3_client.upload_file(self.loc,'v-assignment', f'{AWS_MEDIA_DIR}{self.id}')
            return True
        except Exception as e:
            print(e)
            return False

    def extract(self, binary_path:str): 
        """
        Extract word or phrases from video-file stored.
        binary_path: absolute path for video-file procssing binary(or executable)
        return :: None
        """

        loc = self.loc
        print(loc)

        args = (binary_path, loc, "-stdout", "--no_progress_bar")
        popen = subprocess.Popen(args,stderr=subprocess.DEVNULL,  stdout=subprocess.PIPE)
        popen.wait()
        output = popen.stdout.read().decode('utf-8')
    
        p1 = r'\d+\r\n(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)\r\n'
        p2 = r'(.*?(?=\r\n\r\n\d+|$))'
        pattern = p1+p2
        # detected subtitle segment for each time-segment
        sub_segment = ((step.group(1), step.group(2), step.group(3))  for step in re.finditer(pattern, output , flags=re.DOTALL ) )


        for segment in sub_segment:
            string  = segment[2].lower()
            word_iter = self.gen_word_iter(string)
            
            for word in word_iter : # proper words or phrases

                if word not in self.word_dict.keys():
                    self.word_dict[word] = [(segment[0], segment[1])]
                elif (segment[0], segment[1]) not in self.word_dict[word]: # same word after first time
                    self.word_dict[word] += [(segment[0], segment[1])]

    

    def enter_db(self):
        """Places entry into the database
        return :: None
        """
        Db_Handler().put_entry(self)

    def delete_temp_file(self):
        """Deletes locally stored video-file
        return :: None
        """
        temporary_storage.delete(self.loc)

    def handle_all(self, binary_path:str ):
        """Calls all other instance-methods of this class automatically. 
        binary_path: absolute path for video-file procssing binary(or executable)
        return :: Video::object.id
        """
        try:
            self.extract(binary_path)
            if self.upload_s3():
                self.enter_db()
            
        except Exception as e:
            print(f'{e} : occured')
        finally:
            self.delete_temp_file()
 
        return self.id

    @staticmethod
    def gen_word_iter(string:str):
        str_clean_gen = (char for char in string if char.isalnum() or char in [' ','-', '\'', "\"", "\n"])
            
        word_iter = chain( (word.group() for word in re.finditer(r'\b[a-zA-Z]+\b', string)) ,  # proper words 
                        (phrase.strip() for phrase in ''.join(str_clean_gen).strip().split('\n')) ) # phrases

        return word_iter

@app.task
def video_task(filename:str, originalname:str, binary_path:str): #celery task
    """
    Celery task for processing of video-file stored locally.
    filename: Name of the video-file saved locally.
    originalname: Name of the video-file object recieved.
    binary_path: absolute path for video-file procssing binary(or executable)
    return :: str
    """
    id = Video(filename, originalname).handle_all(  binary_path)
    return f'\nvideo with id: {id} processed'

