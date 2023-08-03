import pytest
from app.services.pswd_hasher import hash_password, verify_password


SAMPLE_HASH = "$2b$12$nSWCeNcCMWl14SwfjjbkIuH.ML3FGZ4bdy9.kTeRmgBmLVmxpzrAi"
SAMPLE_PSWD = "R@nd123"


@pytest.mark.asyncio
async def test_hash_password(pswd: str = SAMPLE_PSWD):
    h_password = hash_password(pswd)
    assert h_password


@pytest.mark.asyncio
async def test_verify_password_ok():
    assert verify_password(SAMPLE_PSWD, SAMPLE_HASH)


@pytest.mark.asyncio
async def test_verify_password_wrong_password(w_pswd: str = "r@nd123"):
    assert not verify_password(w_pswd, SAMPLE_HASH)


@pytest.mark.asyncio
async def test_hash_password_wrong_argument_type(w_pswd: int = 1234):
    with pytest.raises(TypeError):
        h_password = hash_password(w_pswd)
