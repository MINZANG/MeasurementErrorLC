from manim import *
import numpy as np

class MeasurementErrorLC(Scene):
    def construct(self):
        
        # 標題文字
        title = Text("Impact of Measurement Errors on \nLC (Perpendicular Distance)", font_size=32).to_edge(UP)

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
        edge_line_ex = DashedLine(start, end, color=WHITE, dash_length=0.1)
        self.play(Create(edge_line_ex))

        self.wait(1)
        # 呼叫函式計算垂直線
        perp_line, foot_dot, Q = perpendicular_line_to_segment(edge_line_ex, circle_point)
        perp_line.set_color(WHITE)
        perp_line = make_arrow(perp_line, double=True, color=WHITE,dashed=False)
        foot_dot.set_color(WHITE)
        
        symbol = ImageMobject("pj_AxisEdge\symbols/vertical.png")
        symbol.scale(0.3)
        symbol.next_to(foot_dot, LEFT).shift(RIGHT*0.2)
        self.play(Create(perp_line), Create(foot_dot),FadeIn(symbol))
        self.wait(1)
        
        perp_line_text = Text("LC",font_size=18,color=WHITE).next_to(perp_line, UP).shift(DOWN*0.3)
        self.play(Write(perp_line_text))
        self.wait(1)
        
        edge_line2 = Line(LEFT*2 + UP*1, LEFT*2.2,color=WHITE)
        # 旋轉 15 度 (pi/2) ，以線段中心為中心點
        edje_text2 = Text("Measurement Value",font_size=18,color=YELLOW).next_to(edge_line2, UP)
        self.play(Rotate(edge_line2, angle=PI/12),Create(edje_text2))
        edge_line2.set_color(YELLOW)
        self.wait(1)
        
        start = edge_line2.get_start()
        direction = edge_line2.get_end() - edge_line2.get_start()
        end = start + direction * 5
        edge_line_ex2 = DashedLine(start, end, color=YELLOW, dash_length=0.1)
        self.play(Create(edge_line_ex2))
        self.wait(1)
        
        # 呼叫函式計算垂直線
        perp_line2, foot_dot2, Q = perpendicular_line_to_segment(edge_line_ex2, circle_point)
        perp_line2.set_color(YELLOW)
        perp_line2 = make_arrow(perp_line2, double=True, color=YELLOW,dashed=False)
        foot_dot2.set_color(YELLOW)
        symbol2 = ImageMobject("pj_AxisEdge\symbols/vertical.png")
        symbol2.scale(0.3)
        symbol2.next_to(foot_dot2, LEFT).shift(RIGHT*0.2)
        self.play(Create(perp_line2), Create(foot_dot2),FadeIn(symbol2))
        self.wait(1)
        
        perp_line_text2 = Text("LC",font_size=18,color=YELLOW).next_to(perp_line2, DOWN).shift(UP*0.2)
        self.play(Write(perp_line_text2))
        self.wait(2)
        
        target_line  = perp_line.copy().next_to(edje_text, RIGHT, buff=0.5)
        target_line2 = perp_line2.copy().next_to(edje_text2, RIGHT, buff=0.5)
        # 計算兩條線段最左端對齊的位移
        leftmost = min(target_line.get_left()[0], target_line2.get_left()[0])  # 取 x 座標最小
        target_line.shift(LEFT * (target_line.get_left()[0] - leftmost)).shift(RIGHT*1)
        target_line2.shift(LEFT * (target_line2.get_left()[0] - leftmost)).shift(RIGHT*1)
        
        self.play(perp_line.animate.move_to(target_line .get_center()).rotate(-perp_line.get_angle()))
        self.play(perp_line2.animate.move_to(target_line2.get_center()).rotate(-perp_line2.get_angle()))
        
        # 取得尾端 X 座標並建立連線
        x1, y1 = target_line.get_right()[:2]
        x2, y2 = target_line2.get_right()[:2]
        connecting_line = Line(start=[x1, y1, 0], end=[x2, y2, 0], color=GREEN)
        self.wait(1)

        # 計算中點
        mid_point = (connecting_line.get_start() + connecting_line.get_end()) / 2

        # 建立箭頭指向中點
        arrow = Arrow(start=mid_point + UP*1, end=mid_point, buff=0, color=RED).next_to(connecting_line,DOWN)
        
        # 翻轉 180 度
        arrow.rotate(PI)  # PI = 180度
        
        self.play(Create(arrow))
        self.wait(1)
        
        error_text = Text("Measurement Errors",font_size=18,color=RED).next_to(arrow, DOWN)
        self.play(Create(error_text))
        
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