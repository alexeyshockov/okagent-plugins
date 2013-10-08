import string
import copy
import subprocess

""" Author: Alexey Shockov <alexey@shockov.com> """
class ShellCommand:
    plugin_name = "shell_command"

    def __init__(self, config):
        self.labels = config.get("labels", {})

        self.command = config["command"]

        self.header = config.get("header", ("value"))
        self.column_delimiter = config.get("column_delimiter", "\t")

    def __call__(self):
        rows = map(string.strip, subprocess.Popen(self.command, shell = True, stdout = subprocess.PIPE).stdout.read().split("\n"))
        rows = filter((lambda row: row <> ''), rows)

        results = []

        for row in rows:
            cells = map(string.strip, row.split(self.column_delimiter))

            row = dict(zip(self.header, cells))

            labels = copy.copy(self.labels)
            labels.update(dict((k, str(v)) for (k, v) in zip(self.header, cells) if k <> "value"))

            results.append({
                'labels': labels,
                'value': float(row["value"])
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
