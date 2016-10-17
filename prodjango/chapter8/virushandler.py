import pyclamd
from django.core.files import uploadhandler
from django.conf import settings

# Set up pyclamd to access running instance of clamavd, according to settings
host = getattr(settings, 'CLAMAV_HOST', 'localhost')
port = getattr(settings, 'CLAMAV_PORT', 3310)
pyclamd.init_network_socket(host, port)

class VirusScan(uploadhandler.FileUploadHandler):
    def receive_data_chunk(self, raw_data, start):
        if self.virus_found:
            # If a virus was already found, there's no need to
            # run it through the virus scanner a second time.
            return None
        try:
            if pyclamd.scan_stream(raw_data):
                # A virus was found, so the file should
                # be removed from the input stream.
                raise uploadhandler.SkipFile()
        except pylamd.ScanError:
            # Clam AV couldn't be contacted, so the file wasn't scanned.
            # Since we can't guarantee the safety of any files,
            # no other files should be processed either.
            raise uploadhander.StopUpload()
        # If everything went fine, pass the data along
        return raw_data

    def file_complete(self, file_size):
        # This doesn't store the file anywhere, so it should
        # rely on other handlers to provide a File instance.
        return None
