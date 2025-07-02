# MCP技術調査
## アーキテクチャ
### Host
- AI/LLM機能を内包したアプリ・ツール
- **複数のクライアント**を作成、管理（クライアントマネージャの実装）

### Client
- MCPホスト内に存在、MCPサーバと一対一に対応（ここについて様々な記事で記述があったが、Anthropicのドキュメントでは1つのホストに対してサーバの数だけクライアントが存在する構成が説明されていた）
- MCPのプロトコルに則ってサーバと通信を行う

### Server
- MCPクライアントと一対一に対応
- APIを叩く・データベース・ローカルファイルを参照などの機能を実装、結果をプロトコルに則ってクライアントに返す


## 通信
- Transport層：実際の通信を担当
- Protocol層：メッセージの形式に応じて適切に関数をハンドリング

### Transport層
#### 機能
- バイト列の送受信
- 受け取った文字列をメッセージオブジェクトにデコード

#### 実装
```python:transport.py
class transport:
    def __init__(self) -> None:
        self.onmessage: Optional[Callable] = None   # 応答処理のコールバック
        self.onerror: Optional[Callable] = None     # エラー処理のコールバック
        self.onclose: Optional[Callable] = None     # 終了処理のコールバック

    def start(self) -> None:
        # 通信を開始
        pass

    def send(self, message: dict) -> None:
        # 辞書形式でメッセージを受け取り文字列に変換して送信
        pass

    def close(self) -> None:
        # 通信を終了
        pass
```

### Protocol層
#### 機能
- 

#### JSON-RPCベースの通信
MCPで通信に使用されるメッセージは**JSON-RPC 2.0**形式に準じています。
MCPで利用されるメッセージの形式は以下の三種類です。
| 種類         | 説明           | パラメータ                         |
|--------------|----------------|------------------------------|
| Request      | 処理要求（応答必須） |  必須：jsonrpc, id, method  任意：params     |
| Response     | 応答（成功・エラー） |  必須：jsonrpc, id 任意：result, error（どちらかが含まれている必要あり）     |
| Notification | 通知（応答不要）     |  必須：jsonrpc, method  任意：params（idを含めることはできない）       |

#### 実装


## 通信フェーズ
### 初期化
### 通信中
### 終了