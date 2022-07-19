import hmac
import hashlib
import base64
import json

SECRET_KEY = 'toron_pass_word_hash'

important_message = 'pebjj!21$'


m = hmac.new(SECRET_KEY.encode('utf-8'), important_message.encode('utf-8'), hashlib.sha256)

print(m)

print(m.hexdigest())

private_key = 'toron_pass_word_hash'
checkout_request = 'pebjj!21$'
hexdigest = hmac.new(private_key.encode(), msg=checkout_request.encode(), digestmod=hashlib.sha256,).hexdigest()
digest = hmac.new(private_key.encode(), msg=checkout_request.encode(), digestmod=hashlib.sha256,).digest()
signature = base64.b64encode((hexdigest + "|" + checkout_request).encode()).decode()
print(hexdigest)
print(signature)
print(hexdigest.encode())
print(base64.b64encode(hexdigest.encode()).decode())
print( digest)
print( base64.b64encode(digest))
print( str(base64.b64encode(digest), 'utf-8'))
