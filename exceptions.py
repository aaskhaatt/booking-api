class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class RoomNotFoundError(Exception):
    pass


class BookingNotFoundError(Exception):
    pass


class BookingConflictError(Exception):
    pass


class BookingAccessDeniedError(Exception):
    pass

class InvalidBookingTimeError(Exception):
    pass