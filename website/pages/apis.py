import json

from flask import Blueprint, request, jsonify

from eb_utils.configs import WebPaths
from entity.admin_menus import AdminMenus

api_blue = Blueprint('apis', __name__, url_prefix=WebPaths.API_PATH)


@api_blue.route(f'getsubmenus', methods=['POST'])
def admin_stop_order():
    data = json.loads(request.data)
    data_id = data.get('pid', None)
    data = []
    if data_id:
        menus_p = AdminMenus().get_by_pid(data_id)
        for ptree in menus_p:
            # print(ptree)
            item_p = {"MenuTitle": ptree['menu_name'], "img": ptree['image_url'], "Items": []}

            menus_s = AdminMenus().get_by_pid(str(ptree['_id']))
            for stree in menus_s:
                item_s = {"ItemName": stree['menu_name'], "url": stree['page_url'], "img": stree['image_url']}
                item_p["Items"].append(item_s)
            data.append(item_p)

    return jsonify({'code': 0, "data": data})
