from rest_framework.decorators import api_view
from rest_framework.response import Response

# ==============================================================================
# Comparison between JSON and XML:
#
# JSON (JavaScript Object Notation):
# - Uses key-value pairs and data structures like objects and arrays.
# - Lightweight, human-readable, and easy to parse in web applications.
#
# XML (eXtensible Markup Language):
# - Uses nested opening and closing tags.
# - Verbose payload structure with strict tag parsing.
#
# Sample Flipkart Product Response:
#
# JSON Example:
# {
#     "name": "Wireless Headphones",
#     "price": 1999
# }
#
# XML Example:
# <product>
#     <name>Wireless Headphones</name>
#     <price>1999</price>
# </product>
# ==============================================================================


@api_view(['GET'])
def hello_spotify(request):
    return Response({"message": "Hello, Spotify Fans!"})
