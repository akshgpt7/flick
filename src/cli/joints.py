import click
import requests
import json
from texttable import Texttable


server_url = "http://127.0.0.1:5000"

@click.group()
def cli():
    pass


@click.command()
@click.option('-l', '--location', type=str)
@click.option('-r', '--min-rating', type=float)
def show_joints(location, min_rating, name='show-joints'):
    table = Texttable()
    items = []
    headings = [['Joint', 'id']]

    response = requests.get(server_url + "/joints")
    response_json = response.json()

    try:

        for detail in response_json:
            items.append([detail['name'], str(detail['joint_id'])])

        if location:
            items = []
            for detail in response_json:
                if detail['location'].lower() == location.lower():
                    items.append([detail['name'], str(detail['joint_id'])])
        
        if min_rating:
            allowed_ids = []
            ratings_response = requests.get(server_url + "/joints/ratings")
            ratings_json = ratings_response.json()

            for r in ratings_json:
                if r['rating'] >= min_rating:
                    allowed_ids.append(r['joint_id'])

            if len(items) != 0:
                for i in range(len(items)):
                    if int(items[i][1]) not in allowed_ids:
                        items.pop(i)
            else:
                for detail in response_json:
                    if detail['joint_id'] in allowed_ids:
                        items.append([detail['name'], str(detail['joint_id'])])

        if len(items) > 0:
            table.add_rows(headings + items)
            click.echo(click.style('AVAILABLE JOINTS', bg='black', fg='white'))
            click.echo('\n' + table.draw())
            click.echo('\nUse command: `joint-info [id]` for info on a joint.')
        else:
            click.echo(click.style('NO AVAILABLE JOINTS FOR YOUR SEARCH',
                                bg='red', fg='white')
                    )


    except IndexError:
        click.echo(click.style('NO AVAILABLE JOINTS FOR YOUR SEARCH',
                               bg='red', fg='white')
                   )


@click.command()
@click.argument('joint', type=int)
@click.argument('item', type=int)
def order(joint, item, name='order'):

    try:

        pizza_name = ''
        joint_name = ''
        price = ''

        size = click.prompt("What size do you want? Enter S, M or L", type=str)
        while not (size == 'S') and not (size == 'M') and not (size == 'L'):
            size = click.prompt("Invalid selection! Enter S, M or L", type=str)

        joints_response = requests.get(server_url + "/joints")
        joints_json = joints_response.json()
        for j in joints_json:
            if int(j['joint_id']) == joint:
                joint_name = j['name']

        menu = requests.get(server_url + "/joints/" + str(joint) + "/menu")
        menu_json = menu.json()
        for i in menu_json:
            if int(i['pizza_id']) == item:
                pizza_name = i['name']
                for p in i['prices']:
                    price = p[size]

        if pizza_name and joint_name and price:
            click.echo('\nYou selected ' + pizza_name + ' (size ' + size + ' for $' + str(price) + ') from ' + joint_name)

        order_details = {
            'item_id': item,
            'size': size,
        }

        # If user chooses to custom order their pizza
        if item == 0:

            click.echo('Create your own pizza! Enter your preferences below: ')

            # Ask for toppings etc.
            toppings = click.prompt('Choose your toppings: ', type=str)
            sauce = click.prompt('Choose your sauce', type=str)
            crust = click.prompt('Choose your crust (thin/thick)', type=str)

            order_details['custom'] = {
                'toppings': toppings,
                'sauce': sauce,
                'crust': crust
            }

        # Ask for user details
        click.echo('\nTell us a bit about yourself!')
        name = click.prompt('Name', type=str)
        address = click.prompt('Address', type=str)
        phone = click.prompt('Phone number', type=str)

        user_info = {
            'name': name,
            'address': address,
            'phone': phone
        }

        order_json = {}
        order_json['joint_id'] = joint
        order_json['details'] = {'user_info': user_info, 'order_details': order_details}

        confirm = click.prompt("\nDo you want to place your order? Enter Y or N", type=str)

        if confirm == 'Y':
            response = requests.post(server_url + "/order", json.dumps(order_json))
            if response.ok:
                click.echo('Thank you for your order!')
            else:
                click.echo('Uh-oh, something went wrong! Please try again.')
        else:
            click.echo("Order cancelled")

    except IndexError:
        click.echo(click.style('INVALID ORDER',
                               bg='red', fg='white')
                   )


cli.add_command(order)
cli.add_command(show_joints)
