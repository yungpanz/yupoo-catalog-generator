import urllib.request
import tempfile

class ImageDownloader:
    def __init__(self):
        pass

    def download(self, image_url, ref_url):
        # Create a request object with the image URL and the "Refer" header
        request = urllib.request.Request(image_url)
        request.add_header('referer', ref_url) # The "referer" header must be added in order to correctly download images from Yupoo
        
        # Open the image URL
        with urllib.request.urlopen(request) as response:
            # Create a temporary file to store the image
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')

            # Download the image in chunks to reduce memory usage
            chunk_size = 1024
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                temp_file.write(chunk)

        # Return the pathname of the temporary file
        return temp_file.name
