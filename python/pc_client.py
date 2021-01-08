import requests
import sys
from requests_toolbelt import MultipartEncoder

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(0)
    
    file_uri = sys.argv[1]
    print ("file uri: " + file_uri)

    file_name = file_uri.split('\\')[-1]

    print ("file name: " + file_name)
    data = {"file_name" : file_name}
    # files = {
    #     "file" : open(file_uri, "rb")
    # }

    m = MultipartEncoder(
        fields={
            'file_name': file_name,
            'file': ('file', open(file_uri, "rb"), 'text/plain')
        }
    )

    # r = requests.post("https://wx.ashliu.com/upload.php", data, files=files)
    r = requests.post("http://wx.ashliu.com/upload.php", data=m, headers={'Content-Type': m.content_type})
    print ("投递成功!")
    input("Enter to Exit.")