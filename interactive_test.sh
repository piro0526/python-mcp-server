#!/bin/bash

# インタラクティブMCPクライアントテストスクリプト
# 手動でMCPサーバーとやり取りするためのツール

echo "🎯 インタラクティブMCPクライアント"
echo "======================================="
echo "このスクリプトはMCPサーバーと手動でやり取りできます。"
echo ""
echo "利用可能なテストコマンド:"
echo "  1) init    - サーバーを初期化"
echo "  2) tools   - ツールリストを取得"
echo "  3) call    - exampleToolを実行"
echo "  4) custom  - カスタムメッセージを送信"
echo "  5) quit    - 終了"
echo ""

# サーバーを起動
echo "📡 MCPサーバーを起動中..."
python3 app.py &
SERVER_PID=$!

# クリーンアップ関数
cleanup() {
    echo "🧹 サーバーを終了中..."
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
}

trap cleanup EXIT

sleep 2

# サーバーが起動しているかチェック
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "❌ サーバーの起動に失敗しました"
    exit 1
fi

echo "✅ サーバーが起動しました (PID: $SERVER_PID)"
echo ""

# メッセージ送信関数
send_to_server() {
    local message="$1"
    echo "📤 送信: $message"
    echo "$message"
    echo ""
}

# インタラクティブループ
while true; do
    echo -n "コマンドを選択してください (1-5): "
    read -r choice
    
    case $choice in
        1|init)
            echo "🔧 サーバーを初期化します..."
            send_to_server '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"roots":{"listChanged":true},"sampling":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
            ;;
        2|tools)
            echo "📋 ツールリストを取得します..."
            send_to_server '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
            ;;
        3|call)
            echo -n "exampleToolに送信するメッセージを入力してください: "
            read -r input_text
            echo "🔧 exampleToolを実行します..."
            send_to_server "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"exampleTool\",\"arguments\":{\"input\":\"$input_text\"}}}"
            ;;
        4|custom)
            echo "カスタムメッセージを入力してください:"
            read -r custom_message
            send_to_server "$custom_message"
            ;;
        5|quit)
            echo "👋 終了します..."
            break
            ;;
        *)
            echo "❌ 無効な選択です。1-5を入力してください。"
            ;;
    esac
    
    echo ""
done
