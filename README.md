# Pyxel-Physics

[日本語](#japanese) | [English](#english)

<a name="japanese"></a>

## 日本語

### 概要

レトロゲームエンジン**![Pyxel](https://github.com/kitao/pyxel/blob/main/docs/README.ja.md)**上で動作する軽量で、プログラミング初心者向けの2D物理演算フレームワークです.

## 特徴

- **知識がなくても使いやすい**
  - 直感的な仕組み。`App`,`World` を作って `add` するだけで、すぐにゲームが作ることができます！
  - 豊富なデモと日本語によるドキュメント (予定)

## インストール方法 & チュートリアル

```txt
pip install pyxel-physics-engine
```

```python
import pyxphys 
import pyxel

class Ball(pyxphys.GameObject):
    color : int = 6 # ボールの色
    radius : int = 10 # ボールの半径

    def __init__(self):
        super().__init__(x=100, y=20)
        self.name = "ball"
        self.vx = 0
        self.vy = -4
        self.add_collider(pyxphys.CircleCollider(self.radius))
    
    def update(self):
        if self.y > 190:
            self.vy *= -0.9
            self.y = 190

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

# 初期設定
app = pyxphys.App(200,200) # アプリ本体
world = pyxphys.World(gravity = 0.9) # アプリの中における世界
app.add_world(world) # ゲーム本体に、世界を追加

world.add_object(Ball()) # "world"という世界にBallオブジェクトを追加

app.run() # アプリを実行
```

<a name="english"></a>

## English

This framework enables you to use a physic object with a retro game-engine **Pyxel**.
