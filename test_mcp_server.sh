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
# サーバーを起動（標準出力と標準エラー出力の両方をキャプチャ、unbuffered）
python3 -u app.py < "$INPUT_FIFO" > "$OUTPUT_FILE" 2>&1 &
SERVER_PID=$!

# サーバーが起動するのを少し待つ
sleep 2

# サーバーが起動しているかチェック
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "❌ サーバーの起動に失敗しました"
    echo "📄 エラー出力:"
    cat "$OUTPUT_FILE"
    exit 1
fi

echo "✅ サーバーが起動しました (PID: $SERVER_PID)"
echo "📊 初期出力の確認:"
sleep 1  # 初期化メッセージを待つ
if [ -s "$OUTPUT_FILE" ]; then
    echo "出力ファイルにデータがあります："
    head -n 5 "$OUTPUT_FILE"
else
    echo "まだ出力がありません（正常 - サーバーが入力待機中）"
fi

# プロセスの状態を確認
echo "🔍 プロセス状態: $(ps -p $SERVER_PID -o state= 2>/dev/null || echo 'Unknown')"
echo ""

# FIFOを持続的に開く（バックグラウンドで）
exec 3>"$INPUT_FIFO"

# メッセージ送信関数
send_message() {
    local message="$1"
    local test_name="$2"
    
    echo "📤 テスト: $test_name"
    echo "送信: $message"
    
    # 送信前の出力行数を記録
    local lines_before=$(wc -l < "$OUTPUT_FILE" 2>/dev/null || echo "0")
    
    # メッセージを送信（ファイルディスクリプタ3を使用）
    echo "$message" >&3
    
    # レスポンスを待つ（標準出力の処理時間を考慮）
    sleep 3
    
    # 送信後の出力行数を確認
    local lines_after=$(wc -l < "$OUTPUT_FILE" 2>/dev/null || echo "0")
    
    # 新しい出力があるかチェック
    if [ "$lines_after" -gt "$lines_before" ]; then
        echo "📥 レスポンス (新しい出力: $((lines_after - lines_before)) 行):"
        # 新しい行のみを表示
        tail -n $((lines_after - lines_before)) "$OUTPUT_FILE" | while read -r line; do
            if [ -n "$line" ]; then
                echo "$line" | jq '.' 2>/dev/null || echo "$line"
            fi
        done
    else
        echo "📥 レスポンス: (新しい出力なし)"
        echo "現在の出力状況を確認..."
        if [ -s "$OUTPUT_FILE" ]; then
            echo "最新の出力:"
            tail -n 3 "$OUTPUT_FILE"
        else
            echo "出力ファイルが空です"
        fi
    fi
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

# テスト実行中の出力をリアルタイムで表示
echo "📊 現在の出力状況:"
echo "出力ファイルサイズ: $(wc -l < "$OUTPUT_FILE") 行"
echo ""

# 最終的な出力を表示
echo "📄 全出力内容:"
echo "=============="
cat "$OUTPUT_FILE"
echo "=============="

echo "✅ テスト完了！"
echo "💡 ヒント: 各テストのレスポンスを確認して、期待される結果と比較してください。"

# FIFOを閉じる
exec 3>&-
