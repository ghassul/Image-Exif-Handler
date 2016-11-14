import piexif
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Image name including file extension")
    parser.add_argument("-t", "--title", help="Exif title data to add to image", default="")
    parser.add_argument("-s", "--subject", help="Exif subject data to add to image", default="")
    parser.add_argument("-g", "--tags", help="Exif tags data to add to image", default="")
    parser.add_argument("-c", "--comments", help="Exif comments data to add to image", default="")
    parser.add_argument("-a", "--authors", help="Exif authors data to add to image", default="")
    args = parser.parse_args()
    return {"image":    args.image, 
    			"title":    args.title,
    			"subject":  args.subject,
    			"tags":     args.tags,
    			"comments": args.comments,
    			"authors":  args.authors
    }

    
def to_int_tuple(s):
    """Takes a string input and returns a tuple of Int pairs in base 256"""
    unicode_string = s.decode('utf-8')
    converted_tuple = ()

    for x in unicode_string:
    	converted_tuple = converted_tuple + (ord(x) % 256, ord(x) / 256)

    return converted_tuple


def remove_empty_keys(input_dict):
	"""Returns dict with no keys with empty values"""
	return dict((k, v) for k, v in input_dict.iteritems() if v)


def build_exif_dict(title='', subject='', tags='', comments='', authors=''):
    """Takes in (title='', subject='', tags='', comments='', authors='')
    and returns a dictionary formatted for piexif"""
    base_dict = {
    	piexif.ImageIFD.XPTitle: to_int_tuple(title), 
    	piexif.ImageIFD.XPSubject: to_int_tuple(subject), 
    	piexif.ImageIFD.XPKeywords: to_int_tuple(tags), 
    	piexif.ImageIFD.XPComment: to_int_tuple(comments), 
    	piexif.ImageIFD.XPAuthor: to_int_tuple(authors)
    }
    exif_values = remove_empty_keys(base_dict)

    return exif_values


def add_exif_data(exif_data_dict, image_name='blank.jpg'):
    """Adds input dictionary onto given image name (exif_dict_data, image_name)"""
    exif_dict = {'0th': exif_data_dict}
    exif_bytes = piexif.dump(exif_dict)

    try:
    	piexif.insert(exif_bytes, image_name)
    	print "Exif data added onto: " + image_name
    except Exception, e:
    	print "Exif data not added:", e
    	raise


if __name__ == "__main__":
    user_args = parse_args()

    formatted_exif_data = build_exif_dict(user_args["title"], 
    										user_args["subject"], 
    										user_args["tags"], 
    										user_args["comments"],
    										user_args["authors"])

    add_exif_data(formatted_exif_data, user_args["image"])
