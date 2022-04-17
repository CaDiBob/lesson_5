import requests
from environs import Env
from pprint import pprint


def remove_cart_item(access_token, cart_id, product_id):
    url = f'https://api.moltin.com/v2/carts/{cart_id}/items/{product_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    answer = response.json()
    return answer


def get_cart_products(access_token, cart_id):
    url = f'https://api.moltin.com/v2/carts/{cart_id}/items'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    answer = response.json()['data']
    return answer


def get_cart_info_products(products):
    products_info = str()
    for product in products:
        title = product['name']
        price = product['meta']['display_price']['with_tax']['unit']['formatted']
        quantity = product['quantity']
        amount = product['meta']['display_price']['with_tax']['value']['formatted']
        description = product['description']
        products_info += f'{title} \n'\
            f'{description}\n'\
            f'{price} за кг. \n'\
            f'{quantity} кг. {amount}\n\n'
    return products_info


def get_cart_sum(access_token, cart_id):
    url = f'https://api.moltin.com/v2/carts/{cart_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    answer = response.json()['data']
    total_price = answer['meta']['display_price']['with_tax']['formatted']
    return f'Общая сумма товаров: {total_price}'


def put_product_to_cart(access_token, cart_id, product_id, quantity):
    url = f'https://api.moltin.com/v2/carts/{cart_id}/items'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    json_data = {
        'data': {
            'id': product_id,
            'type': 'cart_item',
            'quantity': quantity,
        }
    }
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    answer = response.json()
    return answer


def create_cart(access_token, user_id):
    url = 'https://api.moltin.com/v2/carts'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    json_data = {
        'data': {
            'name': f'{user_id}`s cart',
        }
    }
    response = requests.post(url, headers=headers, json=json_data,)
    response.raise_for_status()
    answer = response.json()['data']['id']
    return answer


def get_moltin_access_token(client_id):
    url = 'https://api.moltin.com/oauth/access_token'
    data = {
        'client_id': client_id,
        'grant_type': 'implicit',
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    answer = response.json()
    return answer['access_token']


def get_products(access_token):
    url = 'https://api.moltin.com/v2/products'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    answer = response.json()
    return answer


def get_product_detail(access_token, product_id):
    url = f'https://api.moltin.com/v2/products/{product_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    answer = response.json()['data']
    return answer


def get_img(access_token, product_detail):
    image_id = product_detail['relationships']['main_image']['data']['id']
    url = f'https://api.moltin.com/v2/files/{image_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    answer = response.json()
    image_url = answer['data']['link']['href']
    return image_url


def get_product_info(product_detail):
    price = product_detail['meta']['display_price']['with_tax']['formatted']
    title = product_detail['name']
    description = product_detail['description']
    return f'{title} {price} за кг.\n\n'\
        f'{description}'


if __name__ == '__main__':
    env = Env()
    env.read_env()
    client_id = env('MOLTIN_CLIENT_ID')
    access_token = get_moltin_access_token(client_id)
    pprint(
        remove_cart_item(
            access_token,
            cart_id='e40bacb2-d8b1-44c2-89bd-2ae3ff78d0b8',
            product_id='f21a14f5-f796-4606-9d82-e50fcbd3bb45',
            )
    )
    # pprint(
    #     get_cart_products(
    #         access_token,
    #         cart_id='4c572813-70ce-43da-bfed-e6fb965130d0',
    #         )
    # )
    # pprint(put_product_to_cart(
    #     access_token,
    #     cart_id='4c572813-70ce-43da-bfed-e6fb965130d0',
    #     product_id='f21a14f5-f796-4606-9d82-e50fcbd3bb45',
    #     quantity=10)
    # )
    # pprint(get_cart_sum(
    #     access_token,
    #     cart_id='4c572813-70ce-43da-bfed-e6fb965130d0',
    # )
    # )
    # products = get_products(access_token)
    # pprint(products['data'][0])
    # for product in products['data']:
    #     product_id = product['id']
    #     print(get_product_info(get_product_detail(access_token, product_id)))
    exit()
