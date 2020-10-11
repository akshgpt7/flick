# Driver file for the front end


import click


@click.command()
@click.option('--catalog', help='List all the pizza places available')
@click.option('--store_cc', help='Store Credit Card to make checkout process faster')


def main(count, name):
    """Order a Pizza through the command line!"""
    for x in range(count):
        click.echo('Hello %s!' % name)


if __name__ == '__main__':
    main()
