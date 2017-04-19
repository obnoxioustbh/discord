import random
import string

from bson.codec_options import CodecOptions
from pymongo.collation import Collation
from pymongo import MongoClient

client = MongoClient('mongodb://93.190.142.215', 27017)
db = client.get_database('admin', codec_options=CodecOptions(unicode_decode_error_handler='ignore'))
print('Signed in: {0}'.format(db.authenticate('admin', '.gpe7h+99W:P}gU}')))
data = db['discord']
codes = [{'code': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))} for i in range(100)]

print(codes)

data.insert_many(codes)