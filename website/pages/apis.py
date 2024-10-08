import json
from datetime import datetime
from io import BytesIO

from flask import Blueprint, request, jsonify, send_file

import eb_cache
from bll.custom_form import CustomForm
from bll.custom_form_data import CustomFormData
from bll.file_upload import FileUpload
from eb_utils import http_helper
from eb_utils.configs import WebPaths
from bll.admin_menus import AdminMenus
from eb_utils.image_code import ImageCode
from entity.api_msg import ApiMsg

api_blue = Blueprint('apis', __name__, url_prefix=WebPaths.API_PATH)


@api_blue.route('getsubmenus', methods=['POST'])
def admin_stop_order():
    # data = json.loads(request.data)
    # data_id = data.get('pid', None)
    data_id = http_helper.get_prams('pid')
    data = []
    if data_id:
        menus_p = AdminMenus().get_by_pid(data_id)
        for ptree in menus_p:

            item_p = {"MenuTitle": ptree.menu_name, "img": ptree.image_url, "Items": []}

            menus_s = AdminMenus().get_by_pid(str(ptree._id))
            for stree in menus_s:
                item_s = {"ItemName": stree.menu_name, "url": stree.page_url, "img": stree.image_url}
                item_p["Items"].append(item_s)
            data.append(item_p)

    return jsonify({'code': 0, "data": data})


@api_blue.route('custom_form', methods=['POST'])
def custom_form():
    key = request.args.get('key')
    api_msg = ApiMsg('err')

    a_key = key.split('_')

    if len(a_key) == 2:
        form_id = a_key[1]
        bll_form = CustomForm()
        form_model = bll_form.find_one_by_id(form_id)
        if form_model:
            dict_prams = http_helper.get_prams_dict()
            is_safe = True
            if form_model.open_safe_code:
                image_code = dict_prams.get('safe_code')
                is_safe, api_msg.data = ImageCode().check_code(image_code)
            if is_safe:
                if dict_prams:
                    if 'safe_code' in dict_prams:
                        dict_prams.pop('safe_code')
                    is_safe, api_msg.data = CustomFormData().add(form_model, dict_prams)
                    api_msg.success = is_safe
            else:
                api_msg.data = '验证码不正确!'
        else:
            api_msg.data = f'can`t find form {form_id}'
    else:
        api_msg.data = 'bad for the form id'

    return jsonify(api_msg.__dict__)


@api_blue.route('upfile', methods=['POST'])
def up_file():
    request_type = request.args.get('t')  # t=ume
    data = {"state": 'unknown err'}
    file = None
    if request_type == 'ume':
        file = request.files['upfile']

    elif request_type in ['img', 'file']:
        file = request.files['file']

    if file:
        content = file.read()
        bll = FileUpload()
        model = bll.new_instance()
        model.original_name = file.filename
        model.content = content
        model.mimetype = file.mimetype
        data = bll.upload(model)

    return jsonify(data)


@api_blue.route('upfile/<filename>', methods=['GET'])
def get_up_file(filename):
    bll = FileUpload()
    model = bll.find_one_by_where({'url': filename})
    if model:
        file_obj = BytesIO(model.content)
        return send_file(file_obj, mimetype=model.mimetype)
    return 'Image not found.', 404

@api_blue.route('cacheset', methods=['GET'])
def cacheset():
    eb_cache.set_data(datetime.now(),60,"test_timeddd")
    return '成功写入'

@api_blue.route('cacheget', methods=['GET'])
def cacheget():
    data = eb_cache.get("test_timeddd")
    if data:
        return str(data)
    else:
        return "无数据"