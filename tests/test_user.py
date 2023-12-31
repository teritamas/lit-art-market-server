from fastapi.testclient import TestClient

from app.facades.database import user_store
from app.main import app
from app.master.user.models.domain import User

from app.facades.web3 import reversible_ft

client = TestClient(app)


def test_signup_not_exists(mocker):
    """ユーザが登録済みでない場合、新規登録ができること"""
    # give
    sample_user_id = "sample_user_id"
    mocker.patch(
        "app.master.user.services.entry_user_service.generate_id_str",
        return_value=sample_user_id,
    )
    user_store.delete_user(sample_user_id)  # 削除してから実行する

    # テスト用のウォレットアドレスの現在の残高を確認
    sample_user_wallet_address = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"
    current_deposit = reversible_ft.balance_of_address(sample_user_wallet_address)

    response = client.post(
        "/signup",
        json={
            "user_name": "test_user",
            "wallet_address": "0xb872960EF2cBDecFdC64115E1C77067c16f042FB",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": f"{sample_user_id}"}

    # テスト用のウォレットアドレスの残高が増えていることを確認
    # 本来は初期化ユーザは固定で50000ポイント振り込まれるが、テストユーザのポイントを償却する処理を入れていないので、実行前から比較して増えていればOKとする
    now_deposit = reversible_ft.balance_of_address(sample_user_wallet_address)
    assert now_deposit > current_deposit


def test_signup_exists(mocker):
    """ユーザが登録済みの場合、そのユーザのIDを返すこと"""
    test_signup_not_exists(mocker=mocker)
    # give
    sample_user_id = "sample_user_id"
    mocker.patch(
        "app.master.user.services.entry_user_service.generate_id_str",
        return_value=sample_user_id,
    )

    response = client.post(
        "/signup",
        json={
            "user_name": "test_user",
            "wallet_address": "0xb872960EF2cBDecFdC64115E1C77067c16f042FB",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"user_id": f"{sample_user_id}"}


def test_fetch_user(mocker):
    test_signup_not_exists(mocker)
    # give
    sample_user_id = "sample_user_id"

    response = client.get(
        f"/user/{sample_user_id}",
    )

    assert response.status_code == 200
    actual_user = User.parse_obj(response.json())
    assert actual_user.user_id == sample_user_id
    assert actual_user.user_name == "test_user"
    assert actual_user.deposit != -1
    assert actual_user.purchase_datasets == []


def test_login_wallet_address(mocker):
    # give
    sample_user_id = "sample_user_id"
    test_wallet_address = "0xb872960EF2cBDecFdC64115E1C77067c16f042FB"

    response = client.get(
        f"/login/wallet_address/{test_wallet_address}",
    )

    assert response.status_code == 200
    actual_user = User.parse_obj(response.json())
    assert actual_user.user_id == sample_user_id
    assert actual_user.user_name == "test_user"
    assert actual_user.deposit == -1
    assert actual_user.wallet_address == test_wallet_address
