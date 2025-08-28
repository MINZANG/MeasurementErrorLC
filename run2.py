from manim import *
import numpy as np

class MeasurementDx(Scene):
    def construct(self):
        
        # 標題文字
        title = Text("DX Distance Using Correct \n Point-to-Point Method", font_size=32).to_edge(UP)

        # 顯示動畫
        self.play(FadeIn(title))
        self.wait(1)
        
        edge_line = Line(LEFT*2 + UP*1, LEFT*2.2,color=WHITE)
        circle = circle = Circle(radius=0.4,color=WHITE).move_to([0, -2, 0])
        circle_point = Dot(color=WHITE).move_to([0, -2, 0])
        edje_text = Text("True Value",font_size=18,color=WHITE).next_to(edge_line, UP).shift(UP*0.3)

        self.play(Create(edge_line),Create(circle),Create(circle_point),Create(edje_text))
        self.wait(1)
        
        # 用 edge_line 的起點 + (方向向量 * 6) 來生成虛線
        start = edge_line.get_start()
        direction = edge_line.get_end() - edge_line.get_start()
        end = start + direction * 5

        self.wait(1)
        
        edge_line2 = Line(LEFT*2 + UP*1, LEFT*2.2,color=WHITE)
        # 旋轉 15 度 (pi/2) ，以線段中心為中心點
        edje_text2 = Text("Measurement Value",font_size=18,color=YELLOW).next_to(edge_line2, UP)
        self.play(Rotate(edge_line2, angle=PI/12),Create(edje_text2))
        edge_line2.set_color(YELLOW)
        self.wait(1)
        
        # 垂直方向向量
        unit_dir = UP  # [0,1,0]，向上

        # 原本線段長度
        line_length = np.linalg.norm(edge_line.get_end() - edge_line.get_start())

        # 計算虛線起點與終點，使其穿過 circle_point
        new_start = circle_point.get_center() - unit_dir * (line_length / 2)
        new_end   = circle_point.get_center() + unit_dir * (line_length / 2)

        # 建立虛線
        dashed_line = DashedLine(start=new_start, end=new_end, color=YELLOW)
        
        # 方向向量（單位向量）
        direction = dashed_line.get_unit_vector()
        extend_length = 2  # 延長距離
        new_end = dashed_line.get_end() + direction * extend_length
        dashed_line.put_start_and_end_on(dashed_line.get_start(), new_end)
        
        self.play(Create(dashed_line))
        self.wait(1)
        
        # 取得線段中點
        mid_point = edge_line.get_center()  # 或 line.get_midpoint()
        mid_dot = Dot(point=mid_point, color=RED)
        
        perp_line, foot_dot, Q = perpendicular_line_to_segment(dashed_line,mid_dot,line_color=RED,dot_color=RED)
        perp_line_text = Text("DX",font_size=18,color=RED).next_to(perp_line, UP)
        self.play(Create(perp_line),Create(foot_dot),Create(perp_line_text),Create(mid_dot))
        self.wait(1)
        
        
        self.wait(3)


def perpendicular_line_to_segment(line: Line, dot: Dot, line_color=BLUE, dot_color=GREEN):
    """
    建立從 dot 到 line (線段) 的垂直距離線
    參數:
        line : Manim Line (線段)
        dot  : Manim Dot  (點)
    回傳:
        (perp_line, foot_dot, Q)
        perp_line : 垂直距離線 (Line)
        foot_dot  : 垂直點 (Dot)
        Q         : 垂足座標 (numpy array)
    """
    A = line.get_start()
    B = line.get_end()
    P = dot.get_center()

    AB = B - A
    AP = P - A
    t = np.dot(AP, AB) / np.dot(AB, AB)   # 投影比例
    Q = A + t * AB                        # 垂直座標

    perp_line = Line(P, Q, color=line_color)
    foot_dot = Dot(Q, color=dot_color)
    return perp_line, foot_dot, Q


def make_arrow(line: Line, double: bool = True, color=WHITE, dashed=False, dash_length=0.1):
    """
    將現有 Line 或 DashedLine 轉換成箭頭線段
    參數:
        line        : Line 物件 (Manim)
        double      : 是否雙端箭頭
        color       : 顏色
        dashed      : 是否虛線
        dash_length : 虛線長度
    回傳:
        Arrow / DoubleArrow / DashedLine 物件
    """
    start = line.get_start()
    end = line.get_end()

    if dashed:
        arrow_line = DashedLine(start, end, color=color, dash_length=dash_length, width=0.2)
    elif double:
        arrow_line = DoubleArrow(start, end, color=color, buff=0, tip_length=0.2)
    else:
        arrow_line = Arrow(start, end, color=color, buff=0, tip_length=0.2)

    return arrow_line