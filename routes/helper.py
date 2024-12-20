import os
def allowed_file(filename):
    """Validate if the uploaded file is of an allowed type"""
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def secure_filename(filename):
    """Generate a safe version of the filename"""
    return filename.replace(" ", "_").replace("/", "_").lower()

def cleanup_files(file_paths):
    """Remove temporary files"""
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)