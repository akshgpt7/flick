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
@click.argument('joint')
@click.argument('item')
@click.argument('size')
def order(joint, item, size, name='order'):

    try:

        order_details = []

        # If user choose to custom order their pizza
        if item == 0:

            click.echo('Create your own pizza! Enter your preferences below: ')

            # Ask for toppings etc.
            toppings = click.prompt('Choose toppings: ', type=str)
            sauce = click.prompt('Choose a sauce: ', type=str)
            crust = click.prompt('Choose a crust: ', type=str)

            order_details.append(
                {
                    'item_id': item,
                    'size': size,
                    'toppings': toppings,
                    'sauce': sauce,
                    'crust': crust
                }
            )

        click.echo('\nYou selected item ' + item + ' (' + size + ') from joint ' + joint)

        # Ask for user details
        click.echo('\nTell us a bit about yourself!')
        name = click.prompt('Name', type=str)
        address = click.prompt('Address', type=str)
        phone = click.prompt('Phone number', type=str)

        user_info = []
        user_info.append(
            {
                'name': name,
                'address': address,
                'phone': phone
            }
        )

        order_json = []
        order_json.append(
            {
                'joint_id': joint,
                'user_info': user_info,
                'order_details': order_details
            }
        )

        confirm = click.prompt("\nDo you want to place your order? Enter Y or N", type=str)
        if confirm == 'Y':
            response = requests.post(server_url + "/order", json.dumps(order_json))
            # TODO: Format response using returned JSON
            click.echo(response)
        else:
            click.echo("Order cancelled")

    except IndexError:
        click.echo(click.style('INVALID ORDER',
                               bg='red', fg='white')
                   )


cli.add_command(order)
cli.add_command(show_joints)
