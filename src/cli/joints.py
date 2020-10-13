import random
import click
import requests
import json
from texttable import Texttable

server_url = "http://127.0.0.1:5000"


@click.group()
def cli():
    pass


@click.command()
@click.option('-l', '--location', type=str, help='Filter pizza joints by location')
@click.option('-r', '--min-rating', type=float, help='Filter pizza joints by minimum rating')
def show_joints(location, min_rating, name='show-joints'):
    """View all available pizza joints"""

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
    """Place your order for pizza :)"""

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

            
@click.command()
@click.option('--reviews', is_flag=True, help='Display reviews')
@click.argument('joint_id')
def joint_info(joint_id, reviews, name='joint-info'):
    """View information about a specific pizza joint"""

    response = requests.get(server_url + f"/joints/{joint_id}")
    if response.status_code == 404:
        click.echo(click.style(f'JOINT ID {joint_id} DOES NOT EXIST',
                               bg='red', fg='white')
                   )
    else:
        response_json = response.json()

        info = f"""
        {response_json['name']} (id: {joint_id})
        {response_json['description']}
        Location: {response_json['location']}
        Rating: {round(response_json['rating'], 1)}
        """

        click.echo(info)

        if reviews:
            click.echo("\t3 Random Reviews:")
            response = requests.get(
                server_url + f"/joints/{joint_id}/reviews")
            review_list = response.json()

            try:
                review_numbers = random.sample(range(0, len(review_list)), 3)
            except ValueError:
                click.echo(f"\tOnly {len(review_list)} reviews for this joint.")
                review_numbers = [n for n in range(len(review_list))]

            for i in review_numbers:
                click.echo("\t~  " + review_list[i])


@click.command()
@click.option('--review', type=str)
@click.argument('joint_id')
@click.argument('rating')
def rate(joint_id, rating, review, name='rate'):
    """Send a review for a pizza joint!"""
    response = requests.get(server_url + f"/joints/{joint_id}")
    if response.status_code == 404:
        click.echo(click.style(f'JOINT ID {joint_id} DOES NOT EXIST',
                               bg='red', fg='white')
                   )
    else:
        if int(rating) < 0 or int(rating) > 5:
            click.echo(click.style(
                f'Invalid Rating. Please choose a number between 0-5.',
                fg='red')
            )
        else:
            rating_json = {'joint_id': joint_id, 'rating': rating}
            if review:
                rating_json['review'] = review
            else:
                rating_json['review'] = None
            request = requests.post(server_url + f"/joints/{joint_id}/rate",
                                    json=rating_json)
            if request.ok:
                click.echo('Review submitted - Thanks for your feedback!')
            else:
                click.echo('Uh-oh! Something went wrong, please try again.')


@click.command()
@click.option('--veggie', is_flag=True, help='Filter for vegetarian options')
@click.argument('joint_id', type=int)
def show_menu(joint_id, veggie, name='show-menu'):
    """Show menu items for joint specified"""
    response = requests.get(server_url + f"/joints/{joint_id}/menu")
    table = Texttable()
    headings = [['Name', 'Toppings']]

    # Will be true when the user passes a pizza joint ID that doesn't exist
    if response.status_code == 404:
        print("The pizza joint id that you passed doesn't exist")
        exit(1)

    response_list = response.json()
    table_rows = []
    for res in response_list:
        if veggie:
            if res['vegetarian']:
                table_rows.append([res['name'], res['toppings']])
        else:
            table_rows.append([res['name'], res['toppings']])

    table.add_rows(headings + table_rows)
    click.echo('\n' + table.draw())
                                    

cli.add_command(order)
cli.add_command(show_joints)
cli.add_command(joint_info)
cli.add_command(rate)
cli.add_command(show_menu)
