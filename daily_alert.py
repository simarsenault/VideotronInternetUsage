import json
import videotron


if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)

    videotron = videotron.Videotron(config['videotron_account'])
    current_month_usage = videotron.get_current_month_usage()
    print(current_month_usage)