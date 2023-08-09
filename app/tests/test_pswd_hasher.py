import pytest
from app.services.pswd_hasher import hash_password, verify_password


SAMPLE_HASH = "$2b$12$nSWCeNcCMWl14SwfjjbkIuH.ML3FGZ4bdy9.kTeRmgBmLVmxpzrAi"
SAMPLE_PSWD = "R@nd123"


@pytest.mark.asyncio
async def test_hash_password(pswd: str = SAMPLE_PSWD):
    h_password = hash_password(pswd)
    assert h_password


# TODO
# think about this test class, how make appropriate report where everything
# is green (right now test passes as expected but display is not good)


@pytest.mark.parametrize("pswd", ["r@nd123", "r@nd", "Rand123", "r@nD123",
                                  "R@nd123"])
class TestVerifyPassword:
    @pytest.mark.asyncio
    async def test_verify_password_ok(self, pswd: str):
        assert verify_password(pswd, SAMPLE_HASH)

    @pytest.mark.asyncio
    async def test_verify_password_wrong_password(self, pswd: str):
        assert not verify_password(pswd, SAMPLE_HASH)


@pytest.mark.asyncio
async def test_hash_password_wrong_argument_type(w_pswd: int = 1234):
    with pytest.raises(TypeError):
        h_password = hash_password(w_pswd)
