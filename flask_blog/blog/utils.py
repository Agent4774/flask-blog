import secrets
import os
from PIL import Image


def save_picture(current_user, form_picture):
	if form_picture != None:
		random_hex = secrets.token_hex(8)
		_, f_ext = form_picture.filename.rsplit('.')
		picture_filename = f'{random_hex}.{f_ext}'
		picture_path = os.path.join(
			app.root_path, 
			'static', 
			'pictures', 
			picture_filename
		)
		output_size = (125, 125)
		i = Image.open(form_picture)
		i.thumbnail(output_size)
		i.save(picture_path)
		return picture_filename
	return current_user.image_file