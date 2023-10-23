import re

from fastapi import HTTPException
from starlette import status


def get_integrity_violation_key_name(orig_arg: str) -> str:
    """
    function which extracts name of the table key which caused
    IntegrityError; as an input receives exception arg
    :param orig_arg: exception's arg
    :return: str; value
    """
    print("ERRRORRR")
    print(orig_arg.capitalize())
    detail = orig_arg.split("Key")
    key = re.split(r"[()=]", detail[1])[1]
    return key


def data_caused_integrity_error(ex_arg: str) -> HTTPException:
    """
    function which generates HTTPException instance for cases when db
    IntegrityError exception is raised
    :param ex_arg: exception's detail message
    :return: instance of HTTPException
    """
    column_name = get_integrity_violation_key_name(ex_arg)
    return HTTPException(
        status.HTTP_409_CONFLICT,
        detail=f"{column_name} is not free, try another"
    )


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

data_exception = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="check data"
)

failed_login = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="check login or password"
)
expired_jwt = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="jwt expired, login to receive new one"
)

authorization_not_completed = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="authorization for operation wasn't completed, check login of "
           "requester for correctness"
)

user_not_found = HTTPException(
    status.HTTP_404_NOT_FOUND,
    detail="certain user wasn't found"
)