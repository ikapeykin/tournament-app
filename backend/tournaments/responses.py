from rest_framework.exceptions import APIException


class TournamentNotAvailable(APIException):
    status_code = 404
    default_detail = 'Tournament is not available.'
    default_code = 'tournament_unavailable'


class TournamentTaskNotAvailable(APIException):
    status_code = 404
    default_detail = 'Tournament task is not available.'
    default_code = 'tournament_unavailable'


class TournamentAlreadyJoined(APIException):
    status_code = 403
    default_detail = 'Already joined to the tournament.'
    default_code = 'tournament_unavailable'


class TournamentTeamDidNotJoin(APIException):
    status_code = 403
    default_detail = 'Team did not joined to the tournament.'
    default_code = 'tournament_unavailable'


class TournamentTaskAlreadySubmitted(APIException):
    status_code = 403
    default_detail = 'Tournament task already submitted.'
    default_code = 'tournament_unavailable'
