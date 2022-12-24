from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

from apps import assignment_problem
from utils import abspath
from utils.logger_tools import get_general_logger
from configs.assignment_problem_web_config import HOST, PORT

logger = get_general_logger(name='Assignment_problem', path=abspath('logs'))


def main():
    app = assignment_problem.create_app()
    # app.run(debug=True, port=PORT)
    http_server = WSGIServer((HOST, PORT), app)
    logger.info('Connect_four Web Started.')
    logger.info(f'Host: {HOST} Port: {PORT} URL: http://{HOST}:{PORT}')
    http_server.serve_forever()


if __name__ == '__main__':
    main()
