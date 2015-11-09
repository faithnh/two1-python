import click

from two1.lib.util.decorators import json_output


@click.command("send")
@click.argument('address', type=click.STRING)
@click.argument('satoshis', type=click.INT)
@json_output
def send(config, address, satoshis):
    """Send the specified address some satoshis.

\b
Usage
-----
Mine bitcoin at 21.co, flush it to the Blockchain, and then send 5000
to the Apache Foundation.
$ 21 mine
$ 21 flush
# Wait ~10-20 minutes for flush to complete and block to mine
$ 21 send 1BtjAzWGLyAavUkbw3QsyzzNDKdtPXk95D 1000
"""
    w = config.wallet.w
    FEES = 0  # Ideal: get this from wallet
    balance = w.confirmed_balance()
    if balance > satoshis + FEES:
        txids = w.send_to(address=address,
                          amount=satoshis)
        if len(txids) > 0:
            assert len(txids) == 1, "Unexpected: more than one transaction"
            txid = txids[0]["txid"]
            tx = txids[0]["tx"]
            click.echo("Successfully sent %s satoshis to %s.\n"
                       "txid: %s\n"
                       "tx: %s\n"
                       "To see in the blockchain: "
                       "https://blockexplorer.com/address/%s\n"
                       % (satoshis, address, txid, tx, address))
    else:
        click.echo("Insufficient Blockchain balance of %s satoshis.\n"
                   "Cannot send %s satoshis to %s.\n"
                   "Do %s, then %s to increase your Blockchain balance." %
                   (balance, satoshis, address,
                    click.style("21 mine", bold=True),
                    click.style("21 flush", bold=True)))
        txids = []
    return txids
