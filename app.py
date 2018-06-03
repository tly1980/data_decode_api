import json
import base64
import io

from bottle import request
import bottle
import fastavro

# app is for campability for gunicorn
app = bottle.default_app()
# application is for compability for uwsgi
application = app

class AvroEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, bytes):
      try:
        return obj.decode('utf8')
      except:
        return obj.decode('base64')
    return json.JSONEncoder.default(self, obj)

app.install(
    bottle.JSONPlugin(json_dumps=lambda s: json.dumps(s, cls=AvroEncoder))
)

@app.post('/avro/decode')
def decode_evh_capture():
  #import pdb;pdb.set_trace()
  reader = fastavro.reader(request.body)
  ret = []
  for l in reader:
    ret.append(l)
  return {'content': ret}


if __name__ == "__main__":
  app.run(host='localhost', port=8080, reloader=True)
