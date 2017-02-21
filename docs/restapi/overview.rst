REST API Overview
=================

Endpoints
---------

https://api.graygram.com


Image Request
-------------

**Endpoint**: https://www.graygram.com

.. http:get:: /photos/(photo_id)/(int:width)x(int:height)

   Get the binary of resized image. The value of (`width`) and (`height`) must be equal.


Error Response
--------------

The error response contains a json object named ``error``. This object contains optional ``message`` and optional ``field``.

**Example response**:

.. sourcecode:: http

   HTTP/1.1 400 Bad Request
   Content-Type: application/json

   {
     "error": {
       "message": "Missing parameter",
       "field": "username"
     }
   }
