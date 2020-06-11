# Hachi

ネットワークの通信負荷&スループット測定 GUI ツール

## 概要

`Hachi`は TCP/UDP パケットによるネットワークのトラフィック負荷テストや、スループット計測に利用できます。
スループット計測する場合はクライアント側とサーバ側両方の端末で動作させてください。
類似ツール[`Nana`](https://www.vector.co.jp/soft/winnt/net/se168678.html)と互換を持たせてあるため、Nana<=>Hachi の組み合わせでもスループット計測は可能です。

## イメージ

![画面キャプチャ](capture.png)

## `Nana`との対比

### サーバ機能

|                      | Nana                                                   | Hachi                                                  |
| :------------------- | :----------------------------------------------------- | :----------------------------------------------------- |
| TCP パケット受信     | ○                                                      | ○                                                      |
| UDP パケット受信     | ○                                                      | ○                                                      |
| 待受 IP アドレス指定 | ○                                                      | ○                                                      |
| 待受ポート指定       | ○                                                      | ○                                                      |
| スループット計測     | 受信パケット数/秒<br>１パケットあたりのデータ長<br>bps | 受信パケット数/秒<br>１パケットあたりのデータ長<br>bps |
| Multicast 受信       | ○                                                      | ×                                                      |
| IPv6 対応            | ○                                                      | ○                                                      |

### クライアント機能

<table>
  <thead>
		<tr>
			<th colspan="3"></th>
			<th>Nana</th>
			<th>Hachi</th>
		</tr>
  </thead>
	<tbody>
		<tr>
			<td rowspan="5">TCPパケット送信</td>
			<td rowspan="2">送信元設定</td>
			<td>IPアドレス</td>
			<td>△(Originalパケット生成で可能)</td>
			<td>ルーティング情報より決定</td>
		</tr>
		<tr>
			<td>ポート番号</td>
			<td>△(Originalパケット生成で可能)</td>
			<td>一つのみ指定可能</td>
		</tr>
		<tr>
			<td rowspan="2">送信先設定</td>
			<td>IPアドレス</td>
			<td>一つのみ指定可能</td>
			<td>一つのみ指定可能</td>
		</tr>
		<tr>
			<td>ポート番号</td>
			<td>一つのみ指定可能</td>
			<td>一つのみ指定可能</td>
		</tr>
		<tr>
			<td colspan="2">IPv6対応</td>
			<td>○</td>
			<td>○</td>
		</tr>
		<tr>
			<td rowspan="5">UDPパケット送信</td>
			<td rowspan="2">送信元設定</td>
			<td>IPアドレス</td>
			<td>△(Originalパケット生成で可能)</td>
			<td>ルーティング情報より決定</td>
		</tr>
		<tr>
			<td>ポート番号</td>
			<td>△(Originalパケット生成で可能)</td>
			<td>複数指定、範囲指定可能</td>
		</tr>
		<tr>
			<td rowspan="2">送信先設定</td>
			<td>IPアドレス</td>
			<td>一つのみ指定可能</td>
			<td>複数指定可能</td>
		</tr>
		<tr>
			<td>ポート番号</td>
			<td>一つのみ指定可能</td>
			<td>複数指定、範囲指定可能</td>
		</tr>
		<tr>
			<td colspan="2">IPv6対応</td>
			<td>○</td>
			<td>○</td>
		</tr>
		<tr>
			<td rowspan="3">ICMPパケット送信</td>
			<td>送信元設定</td>
			<td>IPアドレス</td>
			<td rowspan="3">×</td>
			<td>ルーティング情報より決定</td>
		</tr>
		<tr>
			<td>送信先設定</td>
			<td>IPアドレス</td>
			<td>複数指定可能</td>
		</tr>
		<tr>
			<td colspan="2">IPv6対応</td>
			<td>○</td>
		</tr>
		<tr>
			<td rowspan="3">共通設定</td>
			<td colspan="2">パケットデータ長</td>
			<td>1,500 byteまで</td>
			<td>9,999 byteまで</td>
		</tr>
		<tr>
			<td colspan="2">パケット数/秒</td>
			<td>○</td>
			<td>○</td>
		</tr>
		<tr>
			<td colspan="2">最高速パケット送信</td>
			<td>○</td>
			<td>○</td>
		</tr>
		<tr>
			<td colspan="3">スループット計測</td>
			<td>送信パケット数/秒</br>１パケットあたりのデータ長</br>bps</td>
			<td>送信パケット数/秒</br>１パケットあたりのデータ長</br>bps</td>
		</tr>
	</tbody>
</table>

### オプション機能

|                                    | Nana | Hachi |
| :--------------------------------- | :--- | :---- |
| ログの保存                         | ○    | ○     |
| タスク優先度指定                   | ○    | ○     |
| TypeOfService 設定                 | ○    | ×     |
| TimeToLive 設定                    | ○    | ×     |
| 送信パケットデータ長のランダム変化 | ○    | ×     |
| 送信パケット数/秒のランダム変化    | ○    | ×     |

## インストール

適当なディレクトリに`hachi.exe`を置いて実行してください。
アンインストールは配置した`hachi.exe`を削除して下さい。

### 動作確認環境

- Windows 7(32bit/64bit)
- Windows 10(64bit)

## Change Log

- v1.4.0(2020/06/11)
  - ICMP クライアント機能を追加
  - 64bit 版作成
  - 32bit 版の PyInstaller オプションから`--noconsole`を削除（マルウェア検知回避対策）
- v1.3.0(2019/04/10)
  - UDP 送信の送信元、送信先ポートの範囲指定を追加
- v1.2.0(2018/05/23)
  - 最大ジャンボフレーム拡張(9,000byte -> 9,999bye)
  - パケット送信元設定指定
  - パケット送信先の複数 IP アドレス、ポート指定追加
  - タスク優先度設定追加
- v1.1.0(2018/05/15)
  - 送信先ポートの範囲選択機能追加
- v1.0.0(2018/04/27)
  - 初回リリース

## Future

- 受信インタフェース マルチ対応
- スループットのグラフ表示

## ソースビルド

本ソフトウェアは Python プログラムを`PyInstaller`で実行可能ファイルにパッケージングしています。

### ビルド環境

- v1.4.0 以降

  - Windows 10 64bit
  - Python 3.7.7(32bit/64bit)

- v1.3.0

  - Windows 10 64bit
  - Python 3.6.5(32-bit)

- v1.2.0 まで
  - Windows 7 64bit
  - Python 3.6.5(32-bit)

### 依存パッケージ

- PyInstaller
- netifaces

### 実行ファイルビルドコマンド

```
builder.bat
```

## ライセンス情報

[MIT](https://github.com/kinformation/hachi/blob/master/LICENSE.txt)

## 作者

[kinformation](https://github.com/kinformation)
