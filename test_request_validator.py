#!/usr/bin/env python3
"""
Request型チェッカーのテストコード
"""

from mcp_types import Request


def test_valid_requests():
    """有効なリクエストのテスト"""
    print("=== 有効なリクエストのテスト ===")

    # 基本的なリクエスト
    valid_data = {"jsonrpc": "2.0", "method": "test_method", "id": 1}

    print(f"テスト1: {valid_data}")
    is_valid = Request.is_valid_request(valid_data)
    print(f"結果: {is_valid}")

    if is_valid:
        req = Request(**valid_data)
        print(f"  - 通知か？: {req.is_notification()}")
        print(f"  - レスポンス必要？: {req.requires_response()}")

    # パラメータ付きリクエスト
    valid_data_with_params = {"jsonrpc": "2.0", "method": "test_method", "params": {"key": "value"}, "id": "test-id"}

    print(f"\nテスト2: {valid_data_with_params}")
    is_valid = Request.is_valid_request(valid_data_with_params)
    print(f"結果: {is_valid}")

    # 通知（idなし）
    notification_data = {"jsonrpc": "2.0", "method": "notification_method"}

    print(f"\nテスト3 (通知): {notification_data}")
    is_valid = Request.is_valid_request(notification_data)
    print(f"結果: {is_valid}")

    if is_valid:
        req = Request(**notification_data)
        print(f"  - 通知か？: {req.is_notification()}")
        print(f"  - レスポンス必要？: {req.requires_response()}")


def test_invalid_requests():
    """無効なリクエストのテスト"""
    print("\n=== 無効なリクエストのテスト ===")

    # 無効なjsonrpcバージョン
    invalid_jsonrpc = {"jsonrpc": "1.0", "method": "test_method", "id": 1}

    print(f"テスト1 (無効jsonrpc): {invalid_jsonrpc}")
    is_valid, error = Request.validate_request(invalid_jsonrpc)
    print(f"結果: {is_valid}, エラー: {error}")

    # メソッド名なし
    no_method = {"jsonrpc": "2.0", "id": 1}

    print(f"\nテスト2 (メソッド名なし): {no_method}")
    is_valid, error = Request.validate_request(no_method)
    print(f"結果: {is_valid}, エラー: {error}")

    # 空のメソッド名
    empty_method = {"jsonrpc": "2.0", "method": "", "id": 1}

    print(f"\nテスト3 (空メソッド名): {empty_method}")
    is_valid, error = Request.validate_request(empty_method)
    print(f"結果: {is_valid}, エラー: {error}")

    # 無効なID型
    invalid_id = {"jsonrpc": "2.0", "method": "test_method", "id": [1, 2, 3]}  # 配列は無効

    print(f"\nテスト4 (無効ID型): {invalid_id}")
    is_valid, error = Request.validate_request(invalid_id)
    print(f"結果: {is_valid}, エラー: {error}")


def test_edge_cases():
    """エッジケースのテスト"""
    print("\n=== エッジケースのテスト ===")

    # 最小限のリクエスト
    minimal = {"jsonrpc": "2.0", "method": "m"}

    print(f"テスト1 (最小限): {minimal}")
    is_valid = Request.is_valid_request(minimal)
    print(f"結果: {is_valid}")

    # パラメータが空辞書
    empty_params = {"jsonrpc": "2.0", "method": "test_method", "params": {}, "id": 0}

    print(f"\nテスト2 (空パラメータ): {empty_params}")
    is_valid = Request.is_valid_request(empty_params)
    print(f"結果: {is_valid}")

    # IDが0
    zero_id = {"jsonrpc": "2.0", "method": "test_method", "id": 0}

    print(f"\nテスト3 (ID=0): {zero_id}")
    is_valid = Request.is_valid_request(zero_id)
    print(f"結果: {is_valid}")


if __name__ == "__main__":
    test_valid_requests()
    test_invalid_requests()
    test_edge_cases()

    print("\n=== テスト完了 ===")
