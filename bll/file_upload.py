from bson import ObjectId

from bll.bll_base import BllBase
from entity.file_model import FileModel

ALLOWED_EXTENSIONS = {'.gif', '.png', '.jpg', '.jpeg', '.bmp', '.rar','.zip','.txt','.pdf','.doc','.docx','.XLS','.XLSX','.PPT','.PPTX','.CSV','.MP3','.MP4','.AVI','.MOV','.WMV'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(f_type):
    return f_type.lower() in ALLOWED_EXTENSIONS


class FileUpload(BllBase[FileModel]):

    def new_instance(self) -> FileModel:
        model = FileModel()
        model._id = ObjectId()
        return model

    def upload(self, model: FileModel):

        data = {"originalName": '', "name": '', "url": '', "size": 0, "state": 'unknown err', "type": ''}
        file_extension = model.original_name.rsplit('.', 1)[1].lower()
        model.type = f'.{file_extension}'
        if not allowed_file(model.type):
            data["state"] = f"Not allowed file type:{model.type}"
            return data

        model.size = len(model.content)

        if model.size > MAX_FILE_SIZE:
            data["state"] = 'File size exceeds the limit of 5MB.'
            return data

        model.url = f"{model._id}{model.type}"  # /api/upload/
        self.add(model)
        data["originalName"] = model.original_name
        data["name"] = model.original_name
        data["url"] = f'/api/upfile/{model.url}'
        data["size"] = model.size
        data["state"] = "SUCCESS"
        data["type"] = model.type

        return data
