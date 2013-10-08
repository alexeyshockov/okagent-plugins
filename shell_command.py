import string
import copy
import subprocess

""" Author: Alexey Shockov <alexey@shockov.com> """
class ShellCommand:
    plugin_name = 'shell_command'

    def __init__(self, config):
        self.labels = config.get('labels', {})

        self.command = config['command']

        self.column_delimiter = config.get('column_delimiter', "\t")
        self.value_column = int(config.get('value_column', "0"))

    def __call__(self):
        rows = subprocess.Popen(self.command, stdout=subprocess.PIPE, shell=True).stdout.read().split("\n")

        results = []

        for row in rows:
            cells = map(string.strip, row.split(self.column_delimiter))

            if len(cells) <= self.value_column or cells[self.value_column] == '':
                continue

            labels = copy.copy(self.labels)
            labels.update(dict((k, str(v)) for (k, v) in enumerate(cells) if k <> self.value_column))

            results.append({
                'labels': labels,
                'value': float(cells[self.value_column])
            })

        return results



if __name__ == "__main__":
    import sys
    import pprint
    import yaml

    config_filename = sys.argv[1]

    plugin_config = yaml.load(open(config_filename))
    plugin = ShellCommand(plugin_config.get('config', {}))

    print "Configuration:"
    print plugin_config['config']

    print "Metrics:"
    pprint.pprint(plugin())
