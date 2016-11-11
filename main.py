import piexif

image_name = 'blank.jpg'

def convert_to_byteform(s):
	unicode_string = s.decode('utf-8')
	converted_tuple = ()

	for x in unicode_string:
		converted_tuple = converted_tuple + (ord(x) % 256, ord(x) / 256)


	return converted_tuple


def build_exif_dict(title=None, subject=None, tags=None, comments=None, authors=None):

	base_dict = {
		piexif.ImageIFD.XPTitle: convert_to_byteform(title), 
		piexif.ImageIFD.XPSubject: convert_to_byteform(subject), 
		piexif.ImageIFD.XPKeywords: convert_to_byteform(tags), 
		piexif.ImageIFD.XPComment: convert_to_byteform(comments), 
		piexif.ImageIFD.XPAuthor: convert_to_byteform(authors)
	}

	return dict((k, v) for k, v in base_dict.iteritems() if v) #Removes keys with None value


def add_exif_data(exif_data_dict):
	exif_dict = {'0th':exif_data_dict}
	exif_bytes = piexif.dump(exif_dict)
	piexif.insert(exif_bytes, image_name)