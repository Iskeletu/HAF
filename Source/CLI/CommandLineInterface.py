"""
Command Line Interface Module

TODO = Add command descriptions
"""

import argparse
import sys


class TicketCommand(object):
    """'Ticket' Command."""

    def __init__(self) -> None:
        """"""

        parser = argparse.ArgumentParser(
            description = 'Processes ticket based on the subcommand.',
            usage = '>>> ticket <subcommand> [<arguments>]'
        )
        
    def register(self) -> None:
        """"""

        Todo = True

    def open(self) -> None:
        """"""

        Todo = True


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')