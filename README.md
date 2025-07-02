# python-mcp-server

Python製のMCP（Model Context Protocol）サーバーです。

## 特長

- Pythonで実装されたシンプルなMCPサーバー
- 学習やプロトタイピングに最適
- 拡張・カスタマイズが容易
- stdio transport対応
- 非同期処理によるスケーラブルな設計

## 必要要件

- Python 3.8以上
- pydantic

## インストール

```bash
git clone https://github.com/your-username/python-mcp-server.git
cd python-mcp-server
```

## MCP Inspector での使用

MCP Inspectorは、MCPサーバーの開発とデバッグに便利なツールです。


## Claude Desktop での設定

Claude DesktopでこのMCPサーバーを使用するには、設定ファイルを編集します。

### 設定例

`claude_desktop_config.json` ファイルに以下の設定を追加してください：

```json
{
  "mcpServers": {
    "python-mcp-server": {
      "command": "python",
      "args": ["/path/to/your/python-mcp-server/app.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/python-mcp-server"
      }
    }
  }
}
```

### 設定手順

1. **サーバーパスの確認**
   ```bash
   pwd  # 現在のディレクトリパスをコピー
   ```

2. **設定ファイルの編集**
   - 上記のパスを実際のサーバーディレクトリに置き換え
   - Python実行ファイルのパスが正しいことを確認

3. **Claude Desktop の再起動**
   - 設定変更後、Claude Desktopを完全に終了して再起動

4. **接続確認**
   - Claude Desktopでチャットを開始
   - MCPサーバーのツールが利用可能になっているか確認

## 機能

### 実装済み機能

- ✅ **Basic MCP Protocol**: JSON-RPC 2.0ベースの通信
- ✅ **Tool Management**: ツールの登録・実行・一覧取得
- ✅ **Async Support**: 非同期処理による効率的な通信
- ✅ **Error Handling**: 適切なエラーレスポンス
- ✅ **Stdio Transport**: 標準入出力による通信

### 提供されるツール

- **add_number**: 数値計算ツール
  - 2つの整数を受け取り、その合計を返す
  - **入力パラメータ**:
    - `a` (int32): 第1の数値
    - `b` (int32): 第2の数値
  - **出力**: `{"output": 合計値}`
  - **使用例**: `a=5, b=3` → `{"output": 8}`
  - JSON Schema による入力検証対応

#### ツールの詳細仕様

```json
{
  "name": "add_number",
  "description": "Adds two numbers.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "a": {"type": "int32"},
      "b": {"type": "int32"}
    }
  }
}
```

### アーキテクチャ

```
app.py          # メインアプリケーション
├── mcp.py      # MCPサーバーコア
├── server.py   # プロトコルサーバー
├── protocol.py # JSON-RPC プロトコル処理
├── transport.py # 通信レイヤー（stdio）
└── mcp_types.py # 型定義
```

## ライセンス

MIT License

## 貢献

IssueやPull Requestは歓迎します。

## 関連リンク

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
- [Claude Desktop](https://claude.ai/desktop)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 開発者向け情報

### プロジェクト構造

```
python-mcp-server/
├── app.py                 # メインアプリケーション
├── mcp.py                # MCPサーバーコア
├── server.py             # プロトコルサーバー
├── protocol.py           # JSON-RPC処理
├── transport.py          # stdio通信
├── mcp_types.py          # 型定義
├── test_mcp_server.sh    # 自動テスト
├── test_client.py        # Pythonテストクライアント
├── interactive_test.sh   # インタラクティブテスト
├── TEST_README.md        # テスト説明書
└── README.md             # このファイル
```

### カスタムツールの追加

```python
from mcp_types import Tool

# カスタムツールの定義
def my_custom_function(input_text: str) -> dict:
    return {"result": f"Processed: {input_text}"}

custom_tool = Tool(
    name="myCustomTool",
    title="My Custom Tool", 
    description="カスタム処理を行うツール",
    inputSchema={
        "type": "object",
        "properties": {
            "input_text": {"type": "string"}
        },
        "required": ["input_text"]
    },
    outputSchema={
        "type": "object", 
        "properties": {
            "result": {"type": "string"}
        }
    },
    callback=my_custom_function
)

# ツールの登録
mcp_server.register_tool(custom_tool)
```