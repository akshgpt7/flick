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
@click.option('--reviews', is_flag=True)
@click.argument('joint_id')
def joint_info(joint_id, reviews, name='joint-info'):
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


@click.command()
@click.option('--veggie', is_flag=True, help='Order a vegetarian pizza')
@click.argument('joint_id', type=int)
def show_menu(joint_id, veggie):
    response = requests.get(server_url + f"/joints/{joint_id}/menu")

    # Will be true when the user passes a pizza joint ID that doesn't exist
    if response.status_code == 404:
        print("The pizza joint id that you passed doesn't exist")
        exit(1)

    response_list = response.json()
    for res in response_list:
        if veggie:
            if res['vegetarian']:
                print(res)
        else:
            print(res)



cli.add_command(show_joints)
cli.add_command(joint_info)
cli.add_command(rate)
cli.add_command(show_menu)
