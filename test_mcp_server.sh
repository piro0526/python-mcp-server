#!/bin/bash

# MCPサーバーテストスクリプト
# このスクリプトはMCPサーバーの基本機能をテストします

set -e

echo "🚀 MCPサーバーのテストを開始します..."

# サーバーを起動して一時的なfifoを作成
SERVER_PID=""
TEMP_DIR=$(mktemp -d)
INPUT_FIFO="$TEMP_DIR/input"
OUTPUT_FILE="$TEMP_DIR/output"

# クリーンアップ関数
cleanup() {
    echo "🧹 クリーンアップ中..."
    if [ -n "$SERVER_PID" ]; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
    rm -rf "$TEMP_DIR"
}

# 終了時にクリーンアップを実行
trap cleanup EXIT

# fifoを作成
mkfifo "$INPUT_FIFO"

echo "📡 MCPサーバーを起動中..."
# サーバーを起動
python3 app.py < "$INPUT_FIFO" > "$OUTPUT_FILE" 2>&1 &
SERVER_PID=$!

# サーバーが起動するのを少し待つ
sleep 2

# サーバーが起動しているかチェック
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "❌ サーバーの起動に失敗しました"
    cat "$OUTPUT_FILE"
    exit 1
fi

echo "✅ サーバーが起動しました (PID: $SERVER_PID)"

# メッセージ送信関数
send_message() {
    local message="$1"
    local test_name="$2"
    
    echo "📤 テスト: $test_name"
    echo "送信: $message"
    
    # メッセージを送信
    echo "$message" > "$INPUT_FIFO"
    
    # レスポンスを待つ
    sleep 1
    
    # 出力を表示
    echo "📥 レスポンス:"
    tail -n 1 "$OUTPUT_FILE" | jq '.' 2>/dev/null || tail -n 1 "$OUTPUT_FILE"
    echo "---"
}

# テスト1: Initialize リクエスト
echo "🔧 テスト1: サーバー初期化"
INIT_MESSAGE='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"roots":{"listChanged":true},"sampling":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}}}'
send_message "$INIT_MESSAGE" "Initialize Request"

# テスト2: Initialized 通知
echo "🔧 テスト2: 初期化完了通知"
INITIALIZED_MESSAGE='{"jsonrpc":"2.0","method":"notifications/initialized"}'
send_message "$INITIALIZED_MESSAGE" "Initialized Notification"

# テスト3: Tools List リクエスト
echo "🔧 テスト3: ツールリスト取得"
TOOLS_LIST_MESSAGE='{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
send_message "$TOOLS_LIST_MESSAGE" "Tools List Request"

# テスト4: Tool Call リクエスト
echo "🔧 テスト4: ツール実行"
TOOL_CALL_MESSAGE='{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"exampleTool","arguments":{"input":"Hello, MCP!"}}}'
send_message "$TOOL_CALL_MESSAGE" "Tool Call Request"

# テスト5: 存在しないツールの呼び出し
echo "🔧 テスト5: 存在しないツールの呼び出し（エラーテスト）"
INVALID_TOOL_MESSAGE='{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"nonExistentTool","arguments":{}}}'
send_message "$INVALID_TOOL_MESSAGE" "Invalid Tool Call"

# テスト6: 不正なJSONメッセージ
echo "🔧 テスト6: 不正なJSONメッセージ（エラーテスト）"
INVALID_JSON='{"jsonrpc":"2.0","id":5,"method":"tools/call","params":'
send_message "$INVALID_JSON" "Invalid JSON Message"

# 最終的な出力を表示
echo "📄 全出力内容:"
echo "=============="
cat "$OUTPUT_FILE"
echo "=============="

echo "✅ テスト完了！"
echo "💡 ヒント: 各テストのレスポンスを確認して、期待される結果と比較してください。"
