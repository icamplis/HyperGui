from GutGuiModules.utility import *
import logging

class RecColour:
    def __init__(self, recreated_color_frame, listener):
        self.root = recreated_color_frame

        # Listener
        self.listener = listener

        self.old_specs = ()
        self.specs = (True, False, False)
        self.spec_number = 7

        self.initial_data = []

        self.sto2_button = None
        self.sto2_checkbox = None
        self.sto2_checkbox_value = IntVar()

        self.nir_button = None
        self.nir_checkbox = None
        self.nir_checkbox_value = IntVar()

        self.thi_button = None
        self.thi_checkbox = None
        self.thi_checkbox_value = IntVar()

        self.twi_button = None
        self.twi_checkbox = None
        self.twi_checkbox_value = IntVar()

        self.save_label = None
        self.save_checkbox = None
        self.save_checkbox_value = IntVar()

        self.save_wo_scale_label = None
        self.save_wo_scale_checkbox = None
        self.save_wo_scale_checkbox_value = IntVar()

        self.upper_scale_text = None
        self.lower_scale_text = None
        self.upper_scale_input = None
        self.lower_scale_input = None
        self.upper_scale_value = None
        self.lower_scale_value = None

        self.norm_button = None
        self.og_button = None

        self.recreated_colour_image_graph = None
        self.recreated_colour_image = None
        self.recreated_colour_image_data = None
        self.image_array = None

        self.drop_down_var = StringVar()
        self.choices = ['1. Reflectance - Original', 
        '2. Reflectance - Original without Negative Values', 
        '3. Reflectance - Normalised',
        '4. Reflectance - Normalised without Negative Values', 
        '5. Absorbance - Original', 
        '6. Absorbance - Original without Negative Values', 
        '7. Absorbance - Normalised',
        '8. Absorbance - Normalised without Negative Values']

        self.info_label = None

        self._init_widget()

        self.displayed_image_mode = STO2  # STO2 by default
        self.sto2_button.config(foreground="red")

    def get_specs(self):
        return self.specs

    def get_spec_number(self):
        return self.spec_number

    def update_recreated_image(self, recreated_colour_image_data):
        if self.old_specs != self.specs:
            self.initial_data = recreated_colour_image_data
            self.old_specs = self.specs
        self.recreated_colour_image_data = recreated_colour_image_data
        self._scale()
        self._build_recreated_image()

    def get_current_data(self):
        return self.recreated_colour_image_data

    def get_displayed_image_mode(self):
        return self.displayed_image_mode

    def get_sto2_checkbox_value(self):
        return not bool(self.sto2_checkbox_value.get())

    def get_nir_checkbox_value(self):
        return not bool(self.nir_checkbox_value.get())

    def get_thi_checkbox_value(self):
        return not bool(self.thi_checkbox_value.get())

    def get_twi_checkbox_value(self):
        return not bool(self.twi_checkbox_value.get())

    def get_save_checkbox_value(self):
        return not bool(self.save_checkbox_value.get())

    def get_save_wo_scale_checkbox_value(self):
        return not bool(self.save_wo_scale_checkbox_value.get())

    def get_upper_scale_value(self):
        return self.upper_scale_input.get()

    # Helper
    def _init_widget(self):
        self._build_sto2()
        self._build_nir()
        self._build_thi()
        self._build_twi()
        self._build_save()
        self._build_save_wo_scale()
        self._build_upper_scale()
        self._build_lower_scale()
        self._build_info_label()
        self._build_drop_down()
        self._build_norm_og()
        self._build_recreated_image()

    def _build_sto2(self):
        self.sto2_button = make_button(self.root, text='St02', width=4, command=self.__update_to_sto2, row=1, column=0, inner_pady=5, 
            outer_padx=(15, 10)) 
        self.sto2_checkbox = make_checkbox(self.root, "", row=1, column=0, var=self.sto2_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 2))
        self.sto2_checkbox.deselect()
        self.sto2_checkbox.bind('<Button-1>', self.__update_sto2_check_status)

    def _build_nir(self):
        self.nir_button = make_button(self.root, text='NIR', width=4, command=self.__update_to_nir, row=1, column=1, inner_pady=5, outer_padx=(0, 10))
        self.nir_checkbox = make_checkbox(self.root, "", row=1, column=1, var=self.nir_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.nir_checkbox.deselect()
        self.nir_checkbox.bind('<Button-1>', self.__update_nir_check_status)

    def _build_thi(self):
        self.thi_button = make_button(self.root, text="THI", row=1, column=2, command=self.__update_to_thi, inner_padx=0, inner_pady=5, width=6, outer_padx=(0, 10))
        self.thi_checkbox = make_checkbox(self.root, "", row=1, column=2, var=self.thi_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 5))
        self.thi_checkbox.deselect()
        self.thi_checkbox.bind('<Button-1>', self.__update_thi_check_status)

    def _build_twi(self):
        self.twi_button = make_button(self.root, text="TWI", width=6, row=1, column=3, command=self.__update_to_twi, inner_padx=0, inner_pady=5, outer_padx=(0, 15))
        self.twi_checkbox = make_checkbox(self.root, "", row=1, column=3, var=self.twi_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_padx=(0, 10))
        self.twi_checkbox.deselect()
        self.twi_checkbox.bind('<Button-1>', self.__update_twi_check_status)

    def _build_save(self):
        self.save_label = make_label(self.root, "Save", row=8, column=0, columnspan=2, outer_padx=(0,30), outer_pady=(10, 0), inner_padx=10, inner_pady=5)
        self.save_checkbox = make_checkbox(self.root, text="", row=8, column=1,var=self.save_checkbox_value, sticky=NW, inner_padx=0, inner_pady=0, outer_pady=(10, 15), outer_padx=(0, 60))
        self.save_checkbox.deselect()
        self.save_checkbox.bind('<Button-1>', self.__update_save_with_scale_check_status)

    def _build_save_wo_scale(self):
        self.save_wo_scale_label = make_label(self.root, "Save W/O Scale", row=8, column=1, columnspan=3, outer_padx=0, outer_pady=(10, 0), inner_padx=10, inner_pady=5)
        self.save_wo_scale_checkbox = make_checkbox(self.root, text="", row=8, column=3, var=self.save_wo_scale_checkbox_value, sticky=NE, inner_padx=0, inner_pady=0, outer_pady=(10, 15), outer_padx=(0, 35))
        self.save_wo_scale_checkbox.deselect()
        self.save_wo_scale_checkbox.bind('<Button-1>', self.__update_save_wo_scale_check_status)

    def _build_lower_scale(self):
        self.lower_scale_text = make_text(self.root, content="Lower:", row=6, column=0, columnspan=2, width=6, bg=tkcolour_from_rgb(BACKGROUND), pady=5, padx=(0, 60))
        self.lower_scale_input = make_entry(self.root, row=6, column=1, width=12, pady=5, padx=(0, 15), columnspan=2)
        self.lower_scale_input.bind('<Return>', self.__update_upper_lower)
        if self.lower_scale_value != None:
            self.lower_scale_input.insert(END, str(round(self.lower_scale_value, 5)))

    def _build_upper_scale(self):
        self.upper_scale_text = make_text(self.root, content="Upper: ", row=7, column=0, columnspan=2, width=6, bg=tkcolour_from_rgb(BACKGROUND), pady=(5, 0), padx=(0, 60))
        self.upper_scale_input = make_entry(self.root, row=7, column=1, width=12, pady=(5,0), padx=(0, 15), columnspan=2)
        self.upper_scale_input.bind('<Return>', self.__update_upper_lower)
        if self.upper_scale_value != None:
            self.upper_scale_input.insert(END, str(round(self.upper_scale_value, 5)))

    def _build_info_label(self):
        self.info_label = make_label_button(self.root, text='Recreated Image', command=self.__info, width=14)
        self.info_label.grid(columnspan=3, padx=(0, 50))

    def _build_drop_down(self):
        self.drop_down_var.set(self.choices[6])
        self.drop_down_menu = OptionMenu(self.root, self.drop_down_var, *self.choices, command=self.__update_data)
        self.drop_down_menu.configure(highlightthickness=0, width=6, 
            anchor='w', padx=15)
        self.drop_down_menu.grid(column=2, row=0, columnspan=2, padx=(0, 15))

    def _build_norm_og(self):
        self.norm_button = make_button(self.root, text="NORM", row=6, column=3, columnspan=1, command=self.__norm, inner_padx=3, inner_pady=0, outer_padx=(0, 15), outer_pady=5, width=5)
        self.og_button = make_button(self.root, text="OG", row=7, column=3, columnspan=1, command=self.__og, inner_padx=3, inner_pady=0, outer_padx=(0, 15), outer_pady=(5, 0), width=5)

    def _build_recreated_image(self):
        if self.recreated_colour_image_data is None:
            # Placeholder
            self.recreated_colour_image = make_label(self.root, "recreated_colour image placeholder", row=2, column=0, rowspan=4, columnspan=4, inner_pady=50, inner_padx=50, outer_padx=0, outer_pady=(15, 10))
        else:
            logging.debug("BUILDING RECREATED COLOUR IMAGE...")
            (self.recreated_colour_image_graph, self.recreated_colour_image, self.image_array) = make_image(self.root, self.recreated_colour_image_data, row=2, column=0, columnspan=4, rowspan=4, lower_scale_value=self.lower_scale_value, upper_scale_value=self.upper_scale_value, color_rgb=BACKGROUND)
            self.recreated_colour_image.get_tk_widget().bind('<Button-2>', self.__pop_up_image)

    def _scale(self):
        self.upper_scale_value = float(np.ma.max(self.recreated_colour_image_data))
        self.lower_scale_value = float(np.ma.min(self.recreated_colour_image_data))
        self._build_lower_scale()
        self._build_upper_scale()


    # Commands (Callbacks)

    def __norm(self):
        self.update_recreated_image(self.initial_data/np.ma.max(self.initial_data))

    def __og(self):
        self.update_recreated_image(self.initial_data)

    def __info(self):
        info = self.listener.get_recreated_info()
        title = "Recreated Image Information"
        make_info(title=title, info=info)

    def __update_to_sto2(self):
        self.sto2_button.config(foreground="red")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = STO2
        self.listener.render_new_recreated_image_data()

    def __update_to_nir(self):
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="red")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = NIR
        self.listener.render_new_recreated_image_data()

    def __update_to_thi(self):
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="red")
        self.twi_button.config(foreground="black")
        self.displayed_image_mode = THI
        self.listener.render_new_recreated_image_data()

    def __update_to_twi(self):
        self.sto2_button.config(foreground="black")
        self.nir_button.config(foreground="black")
        self.thi_button.config(foreground="black")
        self.twi_button.config(foreground="red")
        self.displayed_image_mode = TWI
        self.listener.render_new_recreated_image_data()

    def __update_data(self, event):
        choice = self.drop_down_var.get()[:2]
        if choice == '1.':
            self.specs = (False, True, False)
        elif choice == '2.':
            self.specs = (False, True, True)
        elif choice == '3.':
            self.specs = (False, False, False)
        elif choice == '4.':
            self.specs = (False, False, True)
        elif choice == '5.':
            self.specs = (True, True, False)
        elif choice == '6.':
            self.specs = (True, True, True)
        elif choice == '7.':
            self.specs = (True, False, False)
        elif choice == '8.':
            self.specs = (True, False, True)
        self.spec_number = choice[0]
        self.listener._update_recreated_specs(self.specs)

    def __update_sto2_check_status(self, event):
        value = self.get_sto2_checkbox_value()
        self.listener.update_saved(STO2_DATA, value)

    def __update_nir_check_status(self, event):
        value = self.get_nir_checkbox_value()
        self.listener.update_saved(NIR_DATA, value)

    def __update_twi_check_status(self, event):
        value = self.get_twi_checkbox_value()
        self.listener.update_saved(TWI_DATA, value)

    def __update_thi_check_status(self, event):
        value = self.get_thi_checkbox_value()
        self.listener.update_saved(THI_DATA, value)

    def __update_save_with_scale_check_status(self, event):
        value = self.get_save_checkbox_value()
        self.listener.update_saved(REC_IMAGE, value)

    def __update_save_wo_scale_check_status(self, event):
        value = self.get_save_wo_scale_checkbox_value()
        self.listener.update_saved(REC_IMAGE_WO_SCALE, value)

    def __update_upper_lower(self, event):
        self.upper_scale_value = float(self.upper_scale_input.get())
        self.lower_scale_value = float(self.lower_scale_input.get())
        self._build_recreated_image()

    def __pop_up_image(self, event):
        make_popup_image(self.recreated_colour_image_graph)
