from posixpath import abspath
from flask import (
    Blueprint, request
)
from pprint import pprint
from utils import abspath
from utils.response_tools import ArgumentExceptionResponse, SuccessDataResponse
from utils.logger_tools import get_general_logger
import json

logger = get_general_logger(name='general', path=abspath('blueprints', 'assignment_problem', 'logs'))
bp = Blueprint('assignment_problem', __name__, url_prefix='/api/assignment_problem')


@bp.route('solution', methods=['GET', 'POST'])
def get_solution():
    pass




