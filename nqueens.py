from manimlib import *

class nQueens(Scene):
    N = 4
    result = 0
    crash = None
    def check(self, I, J):
        for i in range(self.N):
            if i != I and self.table[I][J] == self.table[i][J]:
                self.crash = (I,J), (i,J)
                return False
        for j in range(self.N):
            if j != J and self.table[I][J] == self.table[I][j]:
                self.crash = (I, J, I, j)
                return False
        if I > J:
            diff = I-J
            for k in range(self.N - diff):
                if k != J and self.table[I][J] == self.table[k+diff][k]:
                    self.crash = (I, J, k+diff, k)
                    return False
        else:
            diff = J-I
            for k in range(self.N - diff):
                if k != I and self.table[I][J] == self.table[k][k+diff]:
                    self.crash = (I, J, k, k+diff)
                    return False
        if I > self.N-1-J:
            diff = I-(self.N-1-J)
            for k in range(self.N - diff):
                if k != (self.N-1-J) and self.table[I][J] == self.table[k+diff][self.N-1-k]:
                    self.crash = (I, J, k+diff, self.N-1-k)
                    return False
        else:
            diff = (self.N-1-J)-I
            for k in range(self.N - diff):
                if k != I and self.table[I][J] == self.table[k][self.N-1-diff-k]:
                    self.crash = (I, J, k, self.N-1-diff-k)
                    return False
        return True

    def print(self):
        t = []
        f = 0
        for i in range(self.N):
            t_sub = []
            for j in range(self.N):
                t_m = self.animation_table[i][j].copy()
                if self.result == 0:
                    f = 1
                    t_m = t_m.shift(DOWN*2.5 + LEFT*4)
                else:
                    t_m = t_m.shift(DOWN*2.5 + RIGHT*4)
                t_sub.append(t_m)
            t.append(t_sub)
        if f == 1:
            self.result = 1
        yield AnimationGroup(
            *[TransformFromCopy(self.animation_table[i][j], t[i][j]) for i in range(self.N) for j in range(self.N)],
            lag_ratio=0
        )
        
        # for i in range(self.N):
        #     for j in range(self.N):
        #         t[i][j].generate_target()
        #         t[i][j].target.scale(.5)
        #         if self.result == 0:
        #             t[i][j].target.to_corner(LEFT+DOWN)
        #             self.result = 1
        #         else:
        #             t[i][j].target.to_corner(RIGHT+DOWN)
        # return t
    
    def find(self, j):
        for i in range(self.N):
            self.table[i][j] = 1
            yield self.animation_table[i][j].animate.set_fill(RED, opacity=1).set_stroke(RED, opacity=1, width=.1)
            if self.check(i, j):
                if j == self.N-1:
                    yield from self.print()
                else:
                    yield from self.find(j+1)
            else:
                i1, j1, i2, j2 = self.crash
                l = Line(self.animation_table[i1][j1], self.animation_table[i2][j2], color=RED)
                yield FadeIn(l)
                yield FadeOut(l)
                
            self.table[i][j] = 0
            yield self.animation_table[i][j].animate.set_fill(BLUE, opacity=1).set_stroke(BLUE, opacity=1, width=.1)

    def construct(self):
        def colorRed(square):
            self.play(square.animate.set_fill(RED, opacity=1).set_stroke(RED, opacity=1, width=.1))
        
        def colorBlue(square):
            self.play(square.animate.set_fill(BLUE, opacity=1).set_stroke(BLUE, opacity=1, width=.1))
        
        def blink(s1, s2):
            self.play(FadeOut(s1), FadeOut(s2))
            self.play(FadeIn(s1), FadeIn(s2))
        
        self.table = [[0 for i in range(self.N)] for j in range(self.N)]
        self.animation_table = VGroup(
            *[
                VGroup(
                    *[Square(1.0).set_fill(BLUE, opacity=1).set_stroke(BLUE, opacity=1, width=1).scale(.3).shift(UP*7)
                      for i in range(self.N)
                    ]
                ).arrange(RIGHT)
            for j in range(self.N)]
        ).arrange(DOWN)
        
        self.play(ShowCreation(self.animation_table))
        for t in self.find(0):
            self.play(t, run_time=.5)
        
        