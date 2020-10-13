import click
import requests
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
@click.argument('joint_id')
def joint_info(joint_id, name='joint-info'):
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


@click.command()
@click.argument('joint_id')
@click.argument('rating')
def rate(joint_id, rating, name='rate'):
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
            request = requests.post(server_url + f"/joints/{joint_id}/rate",
                                    json=rating_json)



cli.add_command(show_joints)
cli.add_command(joint_info)
cli.add_command(rate)