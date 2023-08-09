import json

from flask import Blueprint, request, jsonify

from bll.custom_form_data import CustomFormData
from eb_utils import http_helper
from eb_utils.configs import WebPaths
from bll.admin_menus import AdminMenus
from entity.api_msg import ApiMsg

api_blue = Blueprint('apis', __name__, url_prefix=WebPaths.API_PATH)


@api_blue.route(f'getsubmenus', methods=['POST'])
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


@api_blue.route(f'custom_form', methods=['POST'])
def custom_form():
    key_id = http_helper.get_prams('key')
    dict_prams = http_helper.get_prams_dict()
    api_msg = ApiMsg('err')
    if dict_prams:
        CustomFormData(key_id).add(dict_prams)
        api_msg.success = True
        api_msg.data = 'ok'

    return jsonify(api_msg.__dict__)
