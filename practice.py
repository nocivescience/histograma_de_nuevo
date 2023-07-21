from manim import *
class ResizeScene(Scene):
    def setup(self):
        questions=VGroup(
            Tex("¿","Qué ", "es ","$e^{t}$","?"),
            Tex('¿','Qué ', 'propiedades ', 'tiene ', '$e^{t}$','?'),
            Tex('¿','Qué ', 'propiedades ', 'definen ' , 'a ', '$e^{t}$','?'),
        )
        questions.scale(1.5)
        questions[0].next_to(questions[1], UP, buff=LARGE_BUFF)
        # questions[2][-1].next_to(questions[2][-2], UP, buff=LARGE_BUFF)
        questions.to_edge(UP)
        for i in range(len(questions)):
            questions[i][3+i].set_color(RED)
        top_cross = Cross().shift(questions[1].get_center())
        self.play(Write(questions[:2]))
        self.play(
            Create(top_cross),
        )
        self.wait()
        self.play(
            Transform(questions[1], questions[2]),
            FadeOut(questions[1]),
        )
        self.play(
            FadeOut(top_cross),
        )
        self.play(
            Write(questions[2]),
        )
        self.wait()
        derivate=self.get_deriv_and_ic('\\alpha')
        self.play(
            Write(derivate)
        )
        self.wait()
    def get_deriv_and_ic(self, const=None):
        if const is not None:
            const_str = '{'+str(const)+'}'
            mult_str = '\\cdot'
        else:
            const_str = '{}'
            mult_str = '{}'
        args = [
            '{\\frac{d}{dt}','e^{',const_str, '{t}}', '=', const_str, mult_str, 'e^{',const_str,'{t}}'
        ]
        derivate = MathTex(*args)
        self.ic= MathTex('e^{0}=1')
        self.ic.align_to(derivate, LEFT)
        group=VGroup(derivate, self.ic)
        group.arrange(DOWN, buff=LARGE_BUFF)
        group.scale(1.5)
        group.to_edge(DOWN, buff=LARGE_BUFF)
        return group
class ResizingScene(ResizeScene):
    configuration = {
        'x_range':[-4, 4, 1],
        'unit_size': 1,
        'include_numbers': True,
        'numbers_with_elongated_ticks': [0],
        'include_numbers': list(range(0,15)),
    }
    constants = {
        'alpha': 1,
        'const': 1,
    }
    def construct(self):
        self.setup_number_line(self.ic)
        self.setup_movers()
        self.show_formulas()
        self.pet_time_pass()
        self.wait()
    def setup_number_line(self,mob=None):
        self.number_line = NumberLine(**self.configuration)
        self.number_line.shift(2*DOWN)
        self.number_line.set_y(0)
        self.number_line.to_edge(DOWN, buff=LARGE_BUFF)
        if mob is not None:
            isinstance(mob, Mobject)
            self.play(ReplacementTransform(mob, self.number_line))
        else:
            raise Exception('this is not a mobject')
    def setup_movers(self):
        self.setup_value_trackers()
        self.setup_vector()
    def setup_value_trackers(self):
        input_tracker= ValueTracker(0)
        get_input = input_tracker.get_value
        def complex_number_to_point(z):
            zero=self.number_line.n2p(0)
            unit=self.number_line.n2p(1)-zero
            perp=rotate_vector(unit, TAU/4)
            z=complex(z)
            return zero + (z.real*unit) + (z.imag*perp)
        self.number_line.cn2p=complex_number_to_point
        def get_output():
            return np.exp(self.constants['const']* get_input())
        def get_out_point():
            return self.number_line.n2p(get_output())
        output_tracker=ValueTracker(1)
        output_tracker.add_updater(
            lambda m: m.set_value(get_output())
        )
        self.get_input=get_input
        self.get_output=get_output
        self.get_out_point=get_out_point
        self.input_tracker=input_tracker
        self.output_tracker=output_tracker
        self.add(input_tracker, output_tracker)
    def setup_vector(self):
        position_vect=Vector(color=RED)
        velocity_vect=Vector(color=BLUE)
        position_vect.add_updater(
            lambda m: m.put_start_and_end_on(
                self.number_line.cn2p(0),
                self.number_line.cn2p(self.get_output()),
            )
        )
        def get_velocity_vect(vect):
            vect.put_start_and_end_on(
                self.number_line.cn2p(0),
                self.number_line.cn2p(self.constants['const']*self.get_output()),
            )
            vect.shift(
                self.number_line.cn2p(self.get_input())-self.number_line.cn2p(0)
            )
            return vect
        velocity_vect.add_updater(get_velocity_vect)
        self.position_vect=position_vect
        self.velocity_vect=velocity_vect
    def show_formulas(self):
        self.play(Create(self.position_vect))
        self.play(
            Transform(self.position_vect, self.velocity_vect),
            path_arc=PI/2,
        )
    def pet_time_pass(self):
        rate = .25
        t_tracker = self.input_tracker
        t_tracker.add_updater(
            lambda m, dt: m.increment_value(dt*rate)
        )
        #here
        nl_copy = self.number_line.copy()
        nl_copy.submobjects = []
        nl_copy.stretch_to_fit_width(2*config['frame_width'], about_point=self.number_line.cn2p(-4))
        nl_copy.add(self.number_line)
        xs1=range(25, 100, 25)
        self.number_line.add(*[
            self.number_line.get_tick(x, size=1.5)
            for x in xs1
        ])
        self.number_line.add_numbers(
            xs1,
            num_decimal_places= 0,
            font_size= 150,
            buff=3,
        )
        self.play(
            self.number_line.animate.scale(.1, about_point=self.number_line.cn2p(-4)),
        )
        self.wait()
        xs2=range(200, 1000, 200)
        self.number_line.add(*[
            self.number_line.get_tick(x, size=3)
            for x in xs2
        ])
        self.number_line.add_numbers(
            xs2,
            num_decimal_places= 0,
            font_size=250,
            buff=4,
        )
        self.play(
            self.number_line.animate.scale(.1, about_point=self.number_line.cn2p(-4)),
        )
        self.wait()
        xs3=range(2000, 10000, 2000)
        self.number_line.add(*[
            self.number_line.get_tick(x, size=4)
            for x in xs3
        ])
        self.number_line.add_numbers(
            xs3,
            num_decimal_places= 0,
            font_size=300,
            buff=5,
        )
        self.play(
            self.number_line.animate.scale(.1, about_point=self.number_line.cn2p(-4)),
        )
        self.wait()